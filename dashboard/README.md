# StockSense · Enterprise Inventory Intelligence Dashboard

StockSense is an AI-powered retail inventory intelligence platform providing dual-model demand forecasting, stock-out risk prevention, promo elasticity analytics, and automated reorder decision intelligence.

---

## 🚀 How to Run the Dashboard

### Option 1: Direct Browser Launch (Zero Dependencies)
Simply open the file in your preferred browser:
- Double-click [`dashboard/index.html`](file:///d:/DS/DS%20Hackathon/DAY%202/dashboard/index.html) in your file explorer, or
- Right-click and choose **Open with > Google Chrome / Microsoft Edge / Firefox**.

---

### Option 2: Local HTTP Server (Recommended)
Run a lightweight local server from the project directory:

```bash
# Using Python
python -m http.server 5173 --bind 127.0.0.1 --directory dashboard
```

Then visit in your browser:
👉 **[http://127.0.0.1:5173](http://127.0.0.1:5173)**

---

## 💎 Features & Capabilities

1. **Executive Dashboard (`sec-overview`)**:
   - Real-time KPIs: **$49.07M Total Revenue**, **94.8% Inventory Coverage**, **6.2% Stock-out Incident Rate**, **250 Active SKUs**.
   - Interactive Doughnut breakdown of 8 Product Categories.
   - Store revenue ranking with unit volume comparison.
   - Aggregate daily demand trend line (2022–2024).

2. **AI Pipeline Architecture (`sec-pipeline`)**:
   - Interactive step-by-step visual pipeline: Data Cleaning & Imputation → Feature Engineering (Lags, Rolling Volatility, Promo) → Dual Machine Learning Models → SHAP Explainability → Prescriptive Optimization.

3. **Demand Intelligence (`sec-eda`)**:
   - Category Pareto curve highlighting top revenue drivers (Beverages, Fruits & Vegetables, Snacks drive 48.6% of GMV).
   - Dynamic store time-series explorer with live store dropdown.
   - SKU demand volatility segmentation (High, Moderate, Stable).

4. **Stock-out Risk Analysis (`sec-stockout`)**:
   - Stock-out incident distribution across stores.
   - Reconciliation breakdown: Observed Zero-Sales vs Latent Unmet Demand vs Actual Out-of-Stock events.
   - High-risk store identification.

5. **Promotion Lift & Price Elasticity (`sec-promotions`)**:
   - Uplift breakdown across all 8 product departments.
   - Beverages (+31.8%) and Snacks (+24.6%) demonstrated the highest elasticity.
   - Statistical significance indicators.

6. **Model Benchmark & Feature Ablation (`sec-models`)**:
   - **Demand Forecasting Model Comparison**: CatBoost Regressor (Champion: WAPE 12.2%, RMSE 14.12) vs LightGBM vs XGBoost vs Random Forest vs Ridge vs Baseline.
   - **Stock-out Risk Classification**: LightGBM Classifier (Champion: PR-AUC 0.884, ROC-AUC 0.923) vs XGBoost vs CatBoost.
   - **Feature Ablation Impact**: Shows performance delta when dropping lag demand, rolling volatility, promo flags, and store clusters.

7. **Hypothesis Testing Suite (`sec-stats`)**:
   - Rigorous non-parametric tests:
     - Kruskal-Wallis Test across stores ($H=142.3, p < 0.001$).
     - Mann-Whitney U Test on promotion sales lift ($p < 0.0001$).
     - Wilcoxon Signed-Rank Test on inventory turnover pressure.
     - Kolmogorov-Smirnov Test for non-normality validation.

8. **Decision Intelligence & Reorder Engine (`sec-decisions`, `sec-inventory`)**:
   - Four-pillar prescriptive optimization logic.
   - Live High-Risk SKU Reorder prioritization table with recommended reorder units, safety stock sizing, and 7-day forecast.
   - Store reorder pressure volume distribution.
