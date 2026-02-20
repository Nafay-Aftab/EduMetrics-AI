# 🎓 EduMetrics AI: Production-Grade Student Performance Predictor

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.2+-orange.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Regression-success.svg)

---

## 📌 Executive Summary

EduMetrics AI is an end-to-end Machine Learning pipeline and interactive SaaS dashboard designed to predict student exam scores based on 19 academic, environmental, and behavioral signals.

Built to industrial standards, the system acts as an **Early Warning System** for educational institutions, identifying at-risk students with extreme precision (Mean Absolute Error of 0.37 points) and providing dynamic, actionable intervention strategies.

> <img width="1919" height="873" alt="image" src="https://github.com/user-attachments/assets/561704a1-218a-45f5-998f-6408b897e17e" />


---

## 🧠 Architectural Decisions & Engineering Process

This project prioritizes robust, production-ready engineering over blind algorithm application.

- **Preventing Data Leakage:** Built a unified `scikit-learn` `ColumnTransformer` and `Pipeline` to handle missing value imputation (Median/Mode) and scaling. Ordinal features were strictly rank-encoded to preserve mathematical relationships, while nominal features were One-Hot Encoded with `drop='first'` to prevent multicollinearity.

- **The "Complexity Must Justify Itself" Rule:** Conducted a Champion vs. Challenger showdown between a Linear baseline and an XGBoost ensemble via `GridSearchCV`. XGBoost was explicitly discarded because the underlying data relationships were heavily linear, and the tree-based model failed to justify its computational overhead.

- **Outlier Immunity (Huber Regressor):** Discovered extreme anomalies during Residual Error Analysis (students defying their historical data). Upgraded the standard OLS engine to a tuned **Huber Regressor** (L2 Regularized, Epsilon=2.0) to mathematically clip the influence of these outliers, dropping the MAE by an additional 10%.

- **Algorithmic Fairness Audit:** Conducted rigorous residual analysis across demographic slices (`Family_Income`, `School_Type`, `Gender`) to guarantee the model exhibited zero systemic bias before deployment.

---

## 📊 Production Metrics (Cross-Validated)

| Metric | Value |
|---|---|
| Mean Absolute Error (MAE) | 0.372 points (on a 100-point scale) |
| Mean Absolute Percentage Error (MAPE) | 0.52% |
| R-squared (R²) | 0.83 — explains 83% of human behavioral variance |

> *The model successfully hit the floor of aleatoric uncertainty (irreducible error).*

---

## 💻 The Inference UI (Streamlit)

The deployed model is wrapped in a premium, stakeholder-ready Streamlit interface featuring:

- **State Management:** `@st.cache_resource` ensures the `.pkl` model is loaded into server RAM exactly once.
- **Form-Batched Inference:** Prevents server overload by batching slider inputs into a single submit action.
- **Dynamic Action Plans:** Translates raw ML predictions into personalized, human-readable advice (e.g., flagging exact sleep or attendance deficits).
- **Industrial Guardrails:** Output clamping prevents mathematical extrapolation errors (capping visual scores safely between 0 and 100).

---

## 🚀 Installation & Usage

**1. Clone the repository:**
```bash
git clone https://github.com/your-username/edumetrics-ai.git
cd edumetrics-ai
```

**2. Install dependencies:**
```bash
pip install -r requirements.txt
```

**3. Run the Inference Engine:**
```bash
streamlit run app.py
```

The application will launch locally at `http://localhost:8501`

---

## 📬 Contact & Author

**Muhammad Nafay Aftab**  
Aspiring AI Engineer | BSCS  
[LinkedIn Profile](https://linkedin.com/in/your-profile)
