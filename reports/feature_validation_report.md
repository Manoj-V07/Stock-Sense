# StockSense — Feature Validation Report
**Phase 3: Automated Quality & Integrity Verification** | 2026-09-29

---

## 1. Executive Summary
- **Original Master Dataset Shape:** 29,079 rows × 53 columns
- **Engineered Master Feature Dataset Shape:** 29,079 rows × 116 columns
- **New Engineered Features & Targets:** 63 columns
- **Automated Verification Status:** **ALL 14 CHECKS PASSED**

---

## 2. Detailed Audit of the 14 Required Checks (Step 31)

| Check # | Verification Requirement | Status | Observed Value / Finding |
|---|---|---|---|
| 1 | Master grain remains unique (`date × store_id × product_id`) | **PASS** | 29,079 unique rows; 0 duplicate grains |
| 2 | No duplicate Date × Store × Product rows | **PASS** | `df.duplicated(['date', 'store_id', 'product_id']).sum() == 0` |
| 3 | Lag values are mathematically correct | **PASS** | Verified on sample Store S01, P101: `lag_1(t) == demand(t-1)` |
| 4 | Rolling windows exclude current day demand | **PASS** | `rolling_mean_7` on Aug 08 exactly matches Aug 01..07 mean (excludes Aug 08) |
| 5 | Future information is not present in features | **PASS** | Zero forward-looking columns in feature set; targets quarantined |
| 6 | No infinite values exist in dataset | **PASS** | Numerical columns verified: 0 instances of `inf` or `-inf` |
| 7 | Missing value and zero handling documented | **PASS** | Unobserved inventory preserved as NaN (not zero); dormant stock flagged |
| 8 | Sparse histories correctly flagged | **PASS** | 71 sparse Store x Product combinations flagged via `sparse_history_flag` |
| 9 | Target creation correct and complete | **PASS** | `next_7_day_demand` (23,468 valid rows), `stockout_flag` (21,009 valid rows) |
| 10 | Chronological Train/Val/Test boundaries preserved | **PASS** | Strict time splits (Aug 01-16, Aug 17-20, Aug 21-24) defined |
| 11 | Static categorical attributes correctly encoded | **PASS** | `store_type`, `category`, `brand` preserved as clean categoricals |
| 12 | Feature definitions match dictionary | **PASS** | All features in pipeline mapped 1:1 to `feature_dictionary.md` |
| 13 | Documented justification for every unique feature | **PASS** | Justifications grounded in Phase 1 reconciliation & Phase 2 statistical tests |
| 14 | Ablation groups prepared for Phase 4 | **PASS** | Tiers defined: Baseline, Demand Intel, Inventory Intel, Business Intel, Full |

---

## 3. Feature Group Distribution

| Feature Group | Count | Description & Key Members |
|---|---:|---|
| **GROUP A — TIME** | 7 | `day_of_week`, `weekend_flag`, `month`, `week_no`, `festival_flag`, `day_of_month`, `is_month_end` |
| **GROUP B — DEMAND LAGS** | 3 | `lag_1`, `lag_7`, `lag_14` (true calendar shifts) |
| **GROUP C — ROLLING DEMAND** | 3 | `rolling_mean_7`, `rolling_mean_14`, `rolling_std_7` (strictly shifted trailing windows) |
| **GROUP D — INVENTORY** | 8 | `days_of_inventory`, `inventory_to_demand_ratio`, `reorder_gap`, `low_stock_flag`, `stockout_observed`, `days_to_stockout`, `lead_time_gap`, `no_observed_demand_flag` |
| **GROUP E — PRICE / PROMOTION** | 4 | `discount_pct`, `promotion_flag`, `price_change`, `price_change_pct` |
| **GROUP F — STORE** | 5 | `store_type`, `city`, `region`, `floor_area_sqft`, `avg_daily_customers` |
| **GROUP G — PRODUCT** | 7 | `category`, `sub_category`, `brand`, `mrp`, `cost_price`, `shelf_life_days`, `lead_days` |
| **GROUP H — EXTERNAL** | 5 | `temp_c`, `rain_mm`, `holiday`, `festival`, `local_event` |
| **GROUP I — DEMAND MOMENTUM** | 5 | `recent_7_day_demand`, `previous_7_day_demand`, `demand_momentum_ratio`, `demand_change_pct`, `momentum_class` |
| **GROUP J — DEMAND VOLATILITY** | 4 | `demand_cv_7`, `zero_demand_ratio_7`, `demand_range_7`, `intermittent_demand_flag` |
| **GROUP K — DEMAND REGIME** | 1 | `demand_regime` (Stable, Accelerating, Declining, Volatile, Intermittent) |
| **GROUP L — RECONCILIATION / DATA QUALITY** | 4 | `inventory_balance_gap`, `inventory_demand_gap`, `inventory_consistency_flag`, `inventory_data_quality_score` |
| **GROUP M — FINANCIAL** | 7 | `unit_margin`, `margin_pct`, `inventory_value`, `daily_revenue`, `potential_revenue_exposure`, `potential_margin_exposure`, `stockout_exposure_value` |
| **GROUP N — SUPPLIER** | 4 | `supplier_product_count`, `supplier_avg_lead_time`, `supplier_lead_time_std`, `supplier_dependency` |
| **GROUP O — CROSS-STORE INTELLIGENCE** | 6 | `network_product_mean_inventory`, `store_relative_inventory_ratio`, `network_product_mean_demand`, `store_relative_demand_ratio`, `excess_inventory_flag`, `shortage_risk_flag` |
| **GROUP P — SHELF-LIFE** | 2 | `shelf_life_exposure_ratio`, `high_shelf_life_exposure_flag` |
| **GROUP Q — INTERACTIONS** | 4 | `promo_x_weekend`, `discount_x_promo`, `lead_time_x_volatility`, `reorder_gap_x_lead_time` |
| **TARGETS (LABELS)** | 3 | `next_7_day_demand` (Demand regression), `stockout_flag` (Operational classification), `next_7_day_stockout` (Forward classification) |

---

## 4. Phase 4 Ablation Testing Architecture
To satisfy the critical rule (*'Do not assume unique features are useful simply because they sound intelligent'*), Phase 4 will evaluate incremental predictive gain across 5 progressive tiers:

```
TIER 1: BASELINE (Mandatory Challenge Features)
├── Time: day_of_week, weekend_flag, month, week_no, festival_flag
├── Lags: lag_1, lag_7, lag_14
├── Rolling: rolling_mean_7, rolling_mean_14, rolling_std_7
├── Inventory: days_of_inventory, inventory_to_demand_ratio, reorder_gap
├── Price/Promo: discount_pct, price_change, promotion_flag
└── Store/Product: store_type, category, brand, shelf_life_days, lead_days

TIER 2: BASELINE + DEMAND INTELLIGENCE
└── Add: momentum_ratio, demand_cv_7, zero_demand_ratio_7, demand_regime

TIER 3: BASELINE + INVENTORY INTELLIGENCE
└── Add: days_to_stockout, lead_time_gap, shelf_life_exposure_ratio, reconciliation_score

TIER 4: BASELINE + BUSINESS INTELLIGENCE
└── Add: unit_margin, inventory_value, supplier_avg_lead_time, cross_store_ratios

TIER 5: FULL MODEL
└── All validated features and curated interactions
```
