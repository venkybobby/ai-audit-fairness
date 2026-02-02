# AI Audit Script – What It Does & How to Explain It (Interviews)

## 1. What This File Does (One Sentence)

**It audits a hiring-style ML model for gender bias (income >50K prediction on the Adult dataset), measures whether it violates the 4/5ths rule, then builds a "fair" version using Fairlearn and re-audits it.**

---

## 2. Step-by-Step Flow

| Step | What Happens | Why It Matters |
|------|--------------|----------------|
| **Load data** | Uses Fairlearn's Adult (Census) dataset: predict income >50K from features (age, education, sex, etc.). | Classic benchmark for fairness; simulates "who gets the positive outcome." |
| **Sensitive feature** | Takes `sex`, strips whitespace (e.g. `" Male"` → `"Male"`). | Ensures group names are consistent for metrics. |
| **Preprocess** | `get_dummies` on X, train/test split (70/30), same split for X, y, and sensitive attribute A. | Model gets numeric features; we keep A aligned for per-group metrics. |
| **Baseline model** | Pipeline: `StandardScaler` → `LogisticRegression(max_iter=1000)`. Fit on train, predict on test. | Scaling helps convergence; pipeline keeps preprocessing and model together. |
| **First audit** | `MetricFrame` with `selection_rate` by group (Male/Female). Computes **disparity ratio** = min(rate) / max(rate). | Measures if one group is selected (predicted >50K) much less often than the other. |
| **4/5ths rule** | If ratio < 0.8 → FAIL (violation). Else PASS. Optional note: high-risk under EU AI Act. | Legal/HR standard: selection rate of protected group must be at least 4/5 of the highest rate. |
| **Mitigation** | `ExponentiatedGradient` + `DemographicParity`: refits a classifier with constraints so selection rates across groups are closer. Uses **scaled** X and plain `LogisticRegression` (no Pipeline inside mitigator). | Reduces disparity; Demographic Parity = "equal selection rate across groups." |
| **Second audit** | Same `MetricFrame` on mitigated predictions. Reports "NEW Disparity Ratio." | Shows whether the fair model actually improved the metric. |

---

## 3. Concepts You Should Be Able to Explain

- **Selection rate (per group)**  
  Among people in that group, what fraction got the positive prediction (e.g. predicted income >50K)?  
  **Interview:** "We measure selection rate for each protected group and compare them."

- **Disparity ratio (4/5ths rule)**  
  Ratio = (smaller selection rate) / (larger selection rate). If this is below 0.8, it's considered a disparity.  
  **Interview:** "We use the 4/5ths rule: the disadvantaged group's selection rate must be at least 80% of the advantaged group's."

- **Demographic parity**  
  Equal selection rate across groups (e.g. Male vs Female get "positive" at the same rate).  
  **Interview:** "We enforced demographic parity so that the rate of positive predictions is similar across groups."

- **ExponentiatedGradient (Fairlearn)**  
  A reduction method: it reweights samples and retrains the model multiple times so that the chosen fairness constraint (e.g. demographic parity) is satisfied.  
  **Interview:** "We used Fairlearn's ExponentiatedGradient to train a classifier under a demographic parity constraint, so the model is optimized for accuracy while meeting the fairness constraint."

- **MetricFrame**  
  Fairlearn utility to compute a metric (e.g. selection rate) **overall** and **per group**.  
  **Interview:** "We used MetricFrame to get selection rate broken down by sensitive attribute so we could compute the disparity ratio."

---

## 4. Changes Made (And Why) – For "What did you do?" Questions

These are the fixes/improvements that were added; you can describe them as design and robustness choices.

| Change | Purpose |
|--------|--------|
| **`sensitive_feature = X['sex'].str.strip()`** | Dataset has values like `" Male"` / `" Female"`. Stripping avoids duplicate groups and KeyErrors when looking up by group name. |
| **Pipeline: StandardScaler + LogisticRegression** | Scaling stabilizes optimization and avoids convergence warnings; pipeline keeps preprocessing and model in one place. |
| **`max_iter=1000` (baseline) / `5000` (mitigator)** | Enough iterations so logistic regression converges; mitigator runs many inner fits so it needs a higher limit. |
| **No hardcoded `'Male'` / `'Female'`** | Group names can vary (e.g. with/without space). Code uses `mf.by_group.index.tolist()` and uses the first two groups for ratio. Avoids KeyError and works across datasets. |
| **Disparity ratio = min(rate) / max(rate)** | Single number for 4/5ths: ratio < 0.8 means one group is disadvantaged. Works regardless of which group is which. |
| **Scaled data + plain LogisticRegression inside ExponentiatedGradient** | ExponentiatedGradient calls `fit(X, y, sample_weight=...)`. Sklearn's Pipeline doesn't accept top-level `sample_weight`. So we scale X once (StandardScaler), then pass scaled X to a plain LogisticRegression that does accept `sample_weight`. |
| **EU AI Act note on FAIL** | Connects the result to regulation: systems with significant disparity could be considered high-risk. |

---

## 5. How to Explain This in an Interview

### Short version (30 seconds)

"This script is a **fairness audit** for a binary classifier on the Adult dataset—predicting high income. We measure **selection rate** by gender and check the **4/5ths rule** (disparity ratio). If the baseline fails, we use Fairlearn's **ExponentiatedGradient** with **demographic parity** to train a fairer model, then re-audit. The report says pass/fail and we can compare disparity before and after mitigation."

### Medium version (2 minutes)

"The goal is to **audit an ML system for hiring-style bias**—here we use income prediction as a proxy.

- We load the Adult dataset, define **sex** as the sensitive attribute, and train a **baseline** (scaled features + logistic regression).
- We use Fairlearn's **MetricFrame** to get **selection rate** per group—what fraction of men vs women get the positive prediction. The **disparity ratio** is the smaller rate over the larger; if it's below **0.8**, we say it **fails the 4/5ths rule**.
- We then build a **mitigated model** with **ExponentiatedGradient** and a **demographic parity** constraint, so selection rates across groups are pushed closer. We **re-audit** the mitigated model and report the new disparity ratio.

Along the way we had to **scale the data** for convergence, avoid **hardcoding group names** so the code works with different label formats, and use **plain LogisticRegression** inside the mitigator because it passes **sample_weight** and Pipeline doesn't. The script is set up so we can clearly explain what we measured and how we improved it."

### If they ask "Why Fairlearn?"

"Fairlearn gives us **MetricFrame** for per-group metrics and **reductions** like ExponentiatedGradient for constraint-based fairness. We use the same library for measuring and mitigating, and it's designed for real-world fairness workflows and documentation."

### If they ask "What would you do next?"

- Try other constraints (e.g. equalized odds) or other mitigators.
- Add more metrics (e.g. false positive rate by group).
- Use a different sensitive attribute or multiple attributes (with care for intersectionality).
- Integrate this into a CI or review process so every model is audited before deployment.

---

## 6. File Structure (Quick Reference)

```
Imports (pandas, sklearn, fairlearn)
    ↓
Load Adult data, set y = (>50K), sensitive_feature = sex (stripped)
    ↓
get_dummies, train/test split (X, y, A)
    ↓
Baseline: Pipeline(StandardScaler, LogisticRegression) → fit → predict
    ↓
MetricFrame(baseline predictions) → disparity ratio → 4/5ths pass/fail
    ↓
Scale X_train, X_test; ExponentiatedGradient(LogisticRegression, DemographicParity)
    ↓
mitigator.fit(X_train_s, y_train, sensitive_features=A_train)
    ↓
MetricFrame(mitigated predictions) → NEW disparity ratio
    ↓
Print OFFICIAL AUDIT REPORT (baseline rates, ratio, pass/fail, EU AI Act note)
```

You can use this document to rehearse: explain the flow, the fairness concepts, and the main design choices (scaling, no hardcoded groups, sample_weight with the mitigator).
