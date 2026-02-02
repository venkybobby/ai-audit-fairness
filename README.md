# AI Fairness Audit – Hiring Bias

A **fairness audit** script that checks an ML model for gender bias (income >50K prediction), applies the **4/5ths rule**, and builds a **fairer model** using [Fairlearn](https://fairlearn.org/).

## What it does

1. **Loads** the Adult (Census) dataset and predicts income >50K.
2. **Trains** a baseline model (scaled features + logistic regression).
3. **Audits** selection rate by gender and computes the **disparity ratio** (4/5ths rule).
4. **Mitigates** using Fairlearn’s **ExponentiatedGradient** with **demographic parity**.
5. **Re-audits** the mitigated model and prints an **OFFICIAL AUDIT REPORT** (pass/fail, EU AI Act note).

## Quick start

```bash
# Clone the repo (after you create it on GitHub)
git clone https://github.com/YOUR_USERNAME/ai-audit-fairness.git
cd ai-audit-fairness

# Create a virtual environment (optional)
python -m venv venv
venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Run the audit
python ai_audit.py
```

## Requirements

- Python 3.8+
- See `requirements.txt`: `pandas`, `scikit-learn`, `fairlearn`

## Key concepts

| Concept | Meaning |
|--------|--------|
| **Selection rate** | Fraction of each group that gets the positive prediction (>50K). |
| **4/5ths rule** | Disadvantaged group’s selection rate must be ≥ 80% of the highest group’s. |
| **Demographic parity** | Equal selection rate across groups. |
| **ExponentiatedGradient** | Fairlearn method that reweights samples and retrains to satisfy the fairness constraint. |

## Project structure

```
ai-audit-fairness/
├── README.md              # This file
├── ai_audit.py            # Main audit script
├── ai_audit_EXPLAINED.md  # Step-by-step explanation & interview guide
├── requirements.txt
└── .gitignore
```

## Output

- Selection rates per group (e.g. Male / Female).
- **Disparity ratio** and **PASS** or **FAIL** (4/5ths rule).
- **NEW Disparity Ratio** after mitigation.
- Optional note on EU AI Act high-risk when the baseline fails.

## License

MIT (or your choice).
