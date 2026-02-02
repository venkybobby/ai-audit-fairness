import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from fairlearn.metrics import MetricFrame, selection_rate, demographic_parity_difference
from fairlearn.datasets import fetch_adult
from fairlearn.preprocessing import CorrelationRemover

# Calculate weights to balance the groups
# (In a real audit, you'd use a mitigator like ExponentiatedGradient)
from fairlearn.reductions import ExponentiatedGradient, DemographicParity

print("--- 🔍 STARTING PROFESSIONAL AI AUDIT v2.0 ---")

# 1. LOAD DATA
data = fetch_adult(as_frame=True)
X = data.data
y = (data.target == '>50K').astype(int)

# FIX: The Adult dataset often has leading spaces (e.g., " Male" instead of "Male")
sensitive_feature = X['sex'].str.strip() 

# 2. PRE-PROCESS & PIPELINE (Fixes the Convergence Warning)
X_clean = pd.get_dummies(X)
X_train, X_test, y_train, y_test, A_train, A_test = train_test_split(
    X_clean, y, sensitive_feature, test_size=0.3, random_state=42
)

# 1. CREATE A PIPELINE: This scales the data AND runs the model in one go
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model', LogisticRegression(max_iter=1000))  # 1000 is now plenty!
])

# 2. TRAIN: The pipeline automatically scales the X_train before fitting
pipeline.fit(X_train, y_train)

# 3. PREDICT: The pipeline also scales X_test automatically before predicting
y_pred = pipeline.predict(X_test)

# 3. AUDIT
metrics = {'selection_rate': selection_rate}
mf = MetricFrame(metrics=metrics, y_true=y_test, y_pred=y_pred, sensitive_features=A_test)

# This 'Mitigator' wraps your model and forces it to be fair
# ExponentiatedGradient passes sample_weight to fit(), which Pipeline doesn't accept.
# So we scale the data first and use plain LogisticRegression (which accepts sample_weight).
scaler_mit = StandardScaler()
X_train_s = scaler_mit.fit_transform(X_train)
X_test_s = scaler_mit.transform(X_test)

mitigator = ExponentiatedGradient(
    LogisticRegression(max_iter=5000, random_state=42),
    constraints=DemographicParity()
)

# Train the "Fair" model (on scaled data)
mitigator.fit(X_train_s, y_train, sensitive_features=A_train)
y_pred_mitigated = mitigator.predict(X_test_s)

# Audit the NEW results
mf_fair = MetricFrame(metrics=metrics, y_true=y_test, y_pred=y_pred_mitigated, sensitive_features=A_test)
fair_groups = mf_fair.by_group.index.tolist()
if len(fair_groups) == 2:
    r_f0 = mf_fair.by_group.loc[fair_groups[0], 'selection_rate']
    r_f1 = mf_fair.by_group.loc[fair_groups[1], 'selection_rate']
    new_ratio = min(r_f0, r_f1) / max(r_f0, r_f1) if max(r_f0, r_f1) > 0 else 0
    print(f"NEW Disparity Ratio: {new_ratio:.2f}")

# 4. PROFESSIONAL REPORTING
print("\n--- OFFICIAL AUDIT REPORT ---")
# Use actual group names from the metric frame (dataset may use "Male"/"Female" or " Male"/" Female")
groups = mf.by_group.index.tolist()
if len(groups) != 2:
    print(f"Unexpected number of groups: {groups}")
else:
    r0, r1 = mf.by_group.loc[groups[0], 'selection_rate'], mf.by_group.loc[groups[1], 'selection_rate']
    print(f"Selection Rate ({groups[0]}):   {r0:.2%}")
    print(f"Selection Rate ({groups[1]}): {r1:.2%}")
    # 4/5ths rule: ratio of smaller to larger selection rate
    lower, higher = min(r0, r1), max(r0, r1)
    ratio = lower / higher if higher > 0 else 0
    print(f"Disparity Ratio: {ratio:.2f}")

    if ratio < 0.8:
        print("RESULT: ❌ FAIL (Violation of the 4/5ths Rule)")
        print("GOVERNANCE NOTE: This system would be flagged as 'High-Risk' under the EU AI Act.")
    else:
        print("RESULT: ✅ PASS")
print("----------------------------")
