# StockSense — Feature Dictionary
**Phase 3: Feature Engineering & Demand Intelligence** | 2026-09-29

---

## 1. Prediction Contract
- **Prediction Unit (Grain):** `Date × Store × Product`
- **Prediction Time:** End of the current observation date $t$ (closing of business).
- **Demand Target:** `next_7_day_demand` (sum of demand over calendar days $[t+1, t+7]$).
- **Stock-Out Target:** `stockout_flag` (operational closing <= 0 on date $t$; forward risk: `next_7_day_stockout`).
- **Leakage Golden Rule:** Any feature used to predict future performance contains *only* information available at or before date $t$.

---

## 2. Feature Registry Summary
- **Total Registry Entries:** 86
- **Required (Mandatory Challenge):** 24
- **Candidate Unique Intelligence:** 31
- **Needs Ablation Testing (Phase 4):** 22
- **Rejected Candidates (Documented Rationale):** 9

---

## 3. Detailed Feature Dictionary by Group

### GROUP A — TIME

| Feature | Status | Definition | Source Columns | Calculation | Leakage Risk & Guard | Business Meaning |
|---|---|---|---|---|---|---|
| `day_of_week` | **REQUIRED** | Day of week integer (1=Monday, 7=Sunday) | Master dataset / Calendar | Point-in-time formula | None (known from calendar) | EDA confirmed strong day-of-week demand variation |
| `weekend_flag` | **REQUIRED** | Binary flag for Saturday and Sunday | Master dataset / Calendar | Point-in-time formula | None (known from calendar) | EDA weekend vs weekday tests showed significant volume shift |
| `month` | **REQUIRED** | Calendar month (8 for August) | Master dataset / Calendar | Point-in-time formula | None (known from calendar) | Challenge required specification |
| `week_no` | **REQUIRED** | ISO calendar week number (31 to 35) | Master dataset / Calendar | Point-in-time formula | None (known from calendar) | Captures intra-month weekly progression |
| `festival_flag` | **REQUIRED** | Binary flag indicating local or public festival | Master dataset / Calendar | Point-in-time formula | None (pre-scheduled holiday) | Positive demand association observed during festival events |
| `day_of_month` | **CANDIDATE** | Calendar day of month (1 to 31) | Master dataset / Calendar | Point-in-time formula | None (known from calendar) | Captures payday and monthly consumption cycles |
| `is_month_end` | **CANDIDATE** | Binary flag for month-end period (day >= 28) | Master dataset / Calendar | Point-in-time formula | None (known from calendar) | End of month salary and grocery restocking cycle |

### GROUP B — DEMAND LAGS

| Feature | Status | Definition | Source Columns | Calculation | Leakage Risk & Guard | Business Meaning |
|---|---|---|---|---|---|---|
| `lag_1` | **REQUIRED** | Transaction demand 1 calendar day earlier (t-1) | Master dataset / Calendar | Point-in-time formula | None (strictly t-1) | Direct demand persistence signal |
| `lag_7` | **REQUIRED** | Transaction demand 7 calendar days earlier (t-7) | Master dataset / Calendar | Point-in-time formula | None (strictly t-7) | Captures same-day-of-week demand seasonality |
| `lag_14` | **REQUIRED** | Transaction demand 14 calendar days earlier (t-14) | Master dataset / Calendar | Point-in-time formula | None (strictly t-14) | Fortnightly cyclical demand signal |

### GROUP C — ROLLING DEMAND

| Feature | Status | Definition | Source Columns | Calculation | Leakage Risk & Guard | Business Meaning |
|---|---|---|---|---|---|---|
| `rolling_mean_7` | **REQUIRED** | Mean daily demand over trailing 7 calendar days [t-7, t-1] | Master dataset / Calendar | Point-in-time formula | None (strictly shifted) | Core short-term level indicator for demand forecasting |
| `rolling_mean_14` | **REQUIRED** | Mean daily demand over trailing 14 calendar days [t-14, t-1] | Master dataset / Calendar | Point-in-time formula | None (strictly shifted) | Medium-term baseline level indicator |
| `rolling_std_7` | **REQUIRED** | Standard deviation of demand over trailing 7 calendar days [t-7, t-1] | Master dataset / Calendar | Point-in-time formula | None (strictly shifted) | Captures recent demand dispersion and uncertainty |

### GROUP D — INVENTORY

| Feature | Status | Definition | Source Columns | Calculation | Leakage Risk & Guard | Business Meaning |
|---|---|---|---|---|---|---|
| `days_of_inventory` | **REQUIRED** | Closing stock / trailing daily demand (capped at 365) | Master dataset / Calendar | Point-in-time formula | None (point-in-time closing & past demand) | Core inventory sufficiency metric |
| `inventory_to_demand_ratio` | **REQUIRED** | Closing stock / trailing 7-day demand volume | Master dataset / Calendar | Point-in-time formula | None (point-in-time closing & past demand) | Weekly coverage multiple for inventory planning |
| `reorder_gap` | **REQUIRED** | Closing stock minus reorder level | Master dataset / Calendar | Point-in-time formula | None (point-in-time closing & reorder level) | Direct trigger for replenishment orders when negative |
| `low_stock_flag` | **CANDIDATE** | Binary flag indicating closing <= reorder_lvl | Master dataset / Calendar | Point-in-time formula | None (point-in-time closing & reorder level) | Operational reorder breach indicator |
| `stockout_observed` | **CANDIDATE** | Binary flag indicating closing <= 0 at observation date t | Master dataset / Calendar | Point-in-time formula | None (point-in-time closing) | Identifies historical stock-out events for diagnostic review |
| `no_observed_demand_flag` | **CANDIDATE** | Flag indicating closing > 0 but trailing demand is zero | Master dataset / Calendar | Point-in-time formula | None (point-in-time closing & past demand) | Identifies dormant or slow-moving stock |
| `days_to_stockout` | **NEEDS ABLATION TEST** | Expected days until depletion based on trailing demand rate | Master dataset / Calendar | Point-in-time formula | None (point-in-time closing & past demand) | Critical operational runway metric |
| `lead_time_gap` | **NEEDS ABLATION TEST** | days_to_stockout minus supplier lead_days | Master dataset / Calendar | Point-in-time formula | None (point-in-time runway & supplier lead time) | Direct replenishment safety buffer (negative = stockout risk) |

### GROUP E — PRICE / PROMOTION

| Feature | Status | Definition | Source Columns | Calculation | Leakage Risk & Guard | Business Meaning |
|---|---|---|---|---|---|---|
| `discount_pct` | **REQUIRED** | Average percentage discount on date t | Master dataset / Calendar | Point-in-time formula | None (point-in-time transaction attribute) | Direct price elasticity driver |
| `promotion_flag` | **REQUIRED** | Binary promotion active flag on date t | Master dataset / Calendar | Point-in-time formula | None (point-in-time promotion state) | Mann-Whitney test confirmed significant demand uplift |
| `price_change` | **REQUIRED** | Selling price minus catalogue MRP | Master dataset / Calendar | Point-in-time formula | None (point-in-time price vs catalog MRP) | Monetary price deviation from standard list price |
| `price_change_pct` | **CANDIDATE** | Percentage price discount relative to catalog MRP | Master dataset / Calendar | Point-in-time formula | None (point-in-time price vs catalog MRP) | Standardized price realization percentage |

### GROUP F — STORE

| Feature | Status | Definition | Source Columns | Calculation | Leakage Risk & Guard | Business Meaning |
|---|---|---|---|---|---|---|
| `store_type` | **REQUIRED** | Format of retail store (Supermarket, Hypermarket, etc.) | Master dataset / Calendar | Point-in-time formula | None (static metadata) | Structural store format segmentation |
| `city` | **REQUIRED** | Store location city | Master dataset / Calendar | Point-in-time formula | None (static metadata) | Geographic clustering of demand |
| `region` | **REQUIRED** | Geographic region (North, South, etc.) | Master dataset / Calendar | Point-in-time formula | None (static metadata) | Macro regional purchasing power |
| `floor_area_sqft` | **CANDIDATE** | Store floor area in square feet | Master dataset / Calendar | Point-in-time formula | None (static metadata) | Store capacity and physical customer footprint |
| `avg_daily_customers` | **CANDIDATE** | Historical average daily footfall benchmark | Master dataset / Calendar | Point-in-time formula | None (static master attribute) | Proxy for store traffic baseline |

### GROUP G — PRODUCT

| Feature | Status | Definition | Source Columns | Calculation | Leakage Risk & Guard | Business Meaning |
|---|---|---|---|---|---|---|
| `category` | **REQUIRED** | Standardised product category (Beverages, Dairy, etc.) | Master dataset / Calendar | Point-in-time formula | None (static catalog attribute) | EDA revealed massive category-level revenue and velocity differences |
| `sub_category` | **CANDIDATE** | Granular product sub-classification | Master dataset / Calendar | Point-in-time formula | None (static catalog attribute) | Fine-grained demand clustering |
| `brand` | **REQUIRED** | Product brand identifier | Master dataset / Calendar | Point-in-time formula | None (static catalog attribute) | Brand loyalty and pricing power |
| `mrp` | **CANDIDATE** | Maximum Retail Price (catalog list price) | Master dataset / Calendar | Point-in-time formula | None (static catalog attribute) | Baseline price anchor |
| `cost_price` | **CANDIDATE** | Wholesale procurement unit cost | Master dataset / Calendar | Point-in-time formula | None (static catalog attribute) | Determines unit margins and inventory carrying valuation |
| `shelf_life_days` | **REQUIRED** | Rated shelf life of product in days | Master dataset / Calendar | Point-in-time formula | None (static catalog attribute) | Perishability constraint for Dairy and Fresh items |
| `lead_days` | **REQUIRED** | Supplier replenishment lead time in days | Master dataset / Calendar | Point-in-time formula | None (static contract parameter) | Replenishment latency parameter |

### GROUP H — EXTERNAL

| Feature | Status | Definition | Source Columns | Calculation | Leakage Risk & Guard | Business Meaning |
|---|---|---|---|---|---|---|
| `temp_c` | **CANDIDATE** | Daily average ambient temperature in Celsius | Master dataset / Calendar | Point-in-time formula | None (point-in-time weather observation) | Spearman correlation with Beverage category demand |
| `rain_mm` | **CANDIDATE** | Daily precipitation in millimeters | Master dataset / Calendar | Point-in-time formula | None (point-in-time weather observation) | Footfall impact during monsoon showers |
| `local_event` | **CANDIDATE** | Binary flag for local sporting or cultural events | Master dataset / Calendar | Point-in-time formula | None (scheduled event) | Localized demand spikes |

### GROUP I — DEMAND MOMENTUM

| Feature | Status | Definition | Source Columns | Calculation | Leakage Risk & Guard | Business Meaning |
|---|---|---|---|---|---|---|
| `recent_7_day_demand` | **NEEDS ABLATION TEST** | Sum of demand over trailing calendar window [t-7, t-1] | Master dataset / Calendar | Point-in-time formula | None (strictly shifted trailing window) | Direct recent volume level |
| `previous_7_day_demand` | **NEEDS ABLATION TEST** | Sum of demand over prior calendar window [t-14, t-8] | Master dataset / Calendar | Point-in-time formula | None (strictly shifted prior window) | Prior baseline volume level |
| `demand_momentum_ratio` | **NEEDS ABLATION TEST** | recent_7_day_demand / previous_7_day_demand | Master dataset / Calendar | Point-in-time formula | None (strictly historical ratio) | Quantifies trend direction (acceleration vs decline) |
| `demand_change_pct` | **NEEDS ABLATION TEST** | Percentage change in demand across consecutive 7-day windows | Master dataset / Calendar | Point-in-time formula | None (strictly historical ratio) | Scale-independent growth velocity metric |
| `momentum_class` | **NEEDS ABLATION TEST** | Categorical velocity segment (Accelerating, Stable, Declining) | Master dataset / Calendar | Point-in-time formula | None (strictly historical thresholds) | 422 combinations identified as accelerating in Phase 2 |

### GROUP J — DEMAND VOLATILITY

| Feature | Status | Definition | Source Columns | Calculation | Leakage Risk & Guard | Business Meaning |
|---|---|---|---|---|---|---|
| `demand_cv_7` | **NEEDS ABLATION TEST** | Coefficient of variation of demand over trailing [t-7, t-1] | Master dataset / Calendar | Point-in-time formula | None (strictly shifted trailing window) | Differentiates erratic items from steady staples |
| `zero_demand_ratio_7` | **NEEDS ABLATION TEST** | Proportion of zero-demand days in trailing [t-7, t-1] | Master dataset / Calendar | Point-in-time formula | None (strictly shifted trailing window) | Quantifies demand intermittency frequency |
| `demand_range_7` | **NEEDS ABLATION TEST** | Max minus min daily demand in trailing [t-7, t-1] | Master dataset / Calendar | Point-in-time formula | None (strictly shifted trailing window) | Dispersion spread indicator |
| `intermittent_demand_flag` | **NEEDS ABLATION TEST** | Flag indicating >=50% zero demand days in trailing window | Master dataset / Calendar | Point-in-time formula | None (strictly shifted trailing window) | Signals intermittent demand profile requiring Croston-type modeling |

### GROUP K — DEMAND REGIME

| Feature | Status | Definition | Source Columns | Calculation | Leakage Risk & Guard | Business Meaning |
|---|---|---|---|---|---|---|
| `demand_regime` | **NEEDS ABLATION TEST** | Behavioral classification (Stable, Accelerating, Declining, Volatile, Intermittent) | Master dataset / Calendar | Point-in-time formula | None (strictly historical rules) | Phase 2 behavioral segmentation hypothesis |

### GROUP L — RECONCILIATION / DATA QUALITY

| Feature | Status | Definition | Source Columns | Calculation | Leakage Risk & Guard | Business Meaning |
|---|---|---|---|---|---|---|
| `inventory_balance_gap` | **CANDIDATE** | closing - (opening + received - sold) | Master dataset / Calendar | Point-in-time formula | None (point-in-time ledger audit) | Phase 1 reconciliation found 2 arithmetic mismatches |
| `inventory_demand_gap` | **CANDIDATE** | inventory_sold minus transaction_demand | Master dataset / Calendar | Point-in-time formula | None (point-in-time POS vs WMS comparison) | Phase 1 established POS and WMS measure distinct flows |
| `inventory_consistency_flag` | **CANDIDATE** | Binary flag indicating reconciliation_status == 'CONSISTENT' | Master dataset / Calendar | Point-in-time formula | None (point-in-time ledger audit) | 99.97% consistent records identified in Phase 1 |
| `inventory_data_quality_score` | **CANDIDATE** | Continuous composite score in [0, 1] penalizing data anomalies | Master dataset / Calendar | Point-in-time formula | None (point-in-time quality audit) | Prevents noisy records from corrupting model training |

### GROUP M — FINANCIAL

| Feature | Status | Definition | Source Columns | Calculation | Leakage Risk & Guard | Business Meaning |
|---|---|---|---|---|---|---|
| `unit_margin` | **CANDIDATE** | avg_selling_price - cost_price | Master dataset / Calendar | Point-in-time formula | None (point-in-time prices) | Direct measure of profit generated per unit sold |
| `margin_pct` | **CANDIDATE** | unit_margin / avg_selling_price | Master dataset / Calendar | Point-in-time formula | None (point-in-time prices) | Normalized profit margin percentage |
| `inventory_value` | **CANDIDATE** | closing * cost_price | Master dataset / Calendar | Point-in-time formula | None (point-in-time closing & cost price) | Working capital tied up in inventory |
| `daily_revenue` | **CANDIDATE** | transaction_demand * avg_selling_price | Master dataset / Calendar | Point-in-time formula | None (point-in-time daily sales value) | Observed top-line sales throughput |
| `potential_revenue_exposure` | **CANDIDATE** | closing * avg_selling_price | Master dataset / Calendar | Point-in-time formula | None (point-in-time inventory at selling price) | Upper bound of realizable revenue in stock |
| `potential_margin_exposure` | **CANDIDATE** | closing * unit_margin | Master dataset / Calendar | Point-in-time formula | None (point-in-time inventory at unit margin) | Upper bound of realizable profit margin in stock |
| `stockout_exposure_value` | **CANDIDATE** | Reorder level deficit valued at selling price | Master dataset / Calendar | Point-in-time formula | None (point-in-time reorder deficit) | Monetary deficit required to restore safety buffer |

### GROUP N — SUPPLIER

| Feature | Status | Definition | Source Columns | Calculation | Leakage Risk & Guard | Business Meaning |
|---|---|---|---|---|---|---|
| `supplier_product_count` | **CANDIDATE** | Total unique products sourced from this supplier | Master dataset / Calendar | Point-in-time formula | None (static catalog master) | Supplier operational portfolio size |
| `supplier_avg_lead_time` | **CANDIDATE** | Mean lead time for supplier product portfolio | Master dataset / Calendar | Point-in-time formula | None (static catalog master) | Supplier responsiveness benchmark |
| `supplier_lead_time_std` | **CANDIDATE** | Standard deviation of lead times across supplier portfolio | Master dataset / Calendar | Point-in-time formula | None (static catalog master) | Supplier lead-time unpredictability |
| `supplier_dependency` | **CANDIDATE** | Proportion of category products sourced from this supplier | Master dataset / Calendar | Point-in-time formula | None (static catalog master) | Single-supplier concentration vulnerability |

### GROUP O — CROSS-STORE INTELLIGENCE

| Feature | Status | Definition | Source Columns | Calculation | Leakage Risk & Guard | Business Meaning |
|---|---|---|---|---|---|---|
| `network_product_mean_inventory` | **NEEDS ABLATION TEST** | Average closing inventory across all stores for this product on date t | Master dataset / Calendar | Point-in-time formula | None (contemporaneous date t cross-section) | Network-wide stock availability baseline |
| `store_relative_inventory_ratio` | **NEEDS ABLATION TEST** | Store closing stock relative to network mean for this product | Master dataset / Calendar | Point-in-time formula | None (contemporaneous date t cross-section) | Detects localized maldistribution of inventory |
| `network_product_mean_demand` | **NEEDS ABLATION TEST** | Average trailing demand across all stores for this product | Master dataset / Calendar | Point-in-time formula | None (contemporaneous trailing demand) | Network velocity benchmark |
| `store_relative_demand_ratio` | **NEEDS ABLATION TEST** | Store trailing demand relative to network mean for this product | Master dataset / Calendar | Point-in-time formula | None (contemporaneous trailing demand) | Detects high-velocity stores needing stock transfer |
| `excess_inventory_flag` | **NEEDS ABLATION TEST** | Flag indicating store has >1.5x network stock and >20 days coverage | Master dataset / Calendar | Point-in-time formula | None (contemporaneous rebalancing rule) | Identifies donor stores for lateral inventory transfer |
| `shortage_risk_flag` | **NEEDS ABLATION TEST** | Flag indicating store has <0.6x network stock and negative lead-time gap | Master dataset / Calendar | Point-in-time formula | None (contemporaneous rebalancing rule) | Identifies recipient stores urgently requiring rebalancing |

### GROUP P — SHELF-LIFE

| Feature | Status | Definition | Source Columns | Calculation | Leakage Risk & Guard | Business Meaning |
|---|---|---|---|---|---|---|
| `shelf_life_exposure_ratio` | **NEEDS ABLATION TEST** | days_to_stockout / shelf_life_days | Master dataset / Calendar | Point-in-time formula | None (point-in-time runway vs rated shelf life) | Identifies inventory holding duration exceeding rated shelf life |
| `high_shelf_life_exposure_flag` | **NEEDS ABLATION TEST** | Binary flag indicating shelf_life_exposure_ratio > 1.0 | Master dataset / Calendar | Point-in-time formula | None (point-in-time runway vs rated shelf life) | Flags holding risk for Dairy/perishable items without claiming expiry |

### GROUP Q — INTERACTIONS

| Feature | Status | Definition | Source Columns | Calculation | Leakage Risk & Guard | Business Meaning |
|---|---|---|---|---|---|---|
| `promo_x_weekend` | **CANDIDATE** | promotion_flag * weekend_flag | Master dataset / Calendar | Point-in-time formula | None (point-in-time product of valid features) | Promotions on weekends generate amplified footfall and sales |
| `discount_x_promo` | **CANDIDATE** | discount_pct * promotion_flag | Master dataset / Calendar | Point-in-time formula | None (point-in-time product of valid features) | Measures promotion depth intensity |
| `lead_time_x_volatility` | **NEEDS ABLATION TEST** | lead_days * demand_cv_7 | Master dataset / Calendar | Point-in-time formula | None (historical cv & supplier lead time) | Safety stock buffering formula component |
| `reorder_gap_x_lead_time` | **NEEDS ABLATION TEST** | reorder_gap / lead_days | Master dataset / Calendar | Point-in-time formula | None (point-in-time gap & lead time) | Rate of inventory depletion per lead day |

### REJECTED CANDIDATES

| Feature | Status | Definition | Source Columns | Calculation | Leakage Risk & Guard | Business Meaning |
|---|---|---|---|---|---|---|
| `overall_product_mean_demand` | **REJECTED** | Mean product demand calculated across full dataset history | Master dataset / Calendar | Point-in-time formula | CRITICAL LEAKAGE: uses future August observations | Would contaminate early August predictions with end-of-August demand |
| `store_id_as_continuous` | **REJECTED** | Treating store codes S01..S10 as continuous floating point numbers | Master dataset / Calendar | Point-in-time formula | Spurious correlation (no geometric ordering) | Store IDs are nominal categorical labels, not linear distances |
| `product_id_as_continuous` | **REJECTED** | Treating product IDs P101..P220 as numeric continuum | Master dataset / Calendar | Point-in-time formula | Arbitrary ordering distortion | Product IDs are nominal keys; treating as numbers invalidates distance metrics |
| `expected_closing` | **REJECTED** | Formulaic expected closing inventory from ledger arithmetic | Master dataset / Calendar | Point-in-time formula | Collinearity and masks true inventory discrepancy | Phase 1 Leakage Classification explicitly marked as DO_NOT_USE_AS_FEATURE |
| `expiry_date_prediction` | **REJECTED** | Predicting exact spoilage/expiry date of items on shelf | Master dataset / Calendar | Point-in-time formula | Fabricated signal (no batch-age metadata in data) | Dataset lacks batch manufacturing dates; replaced with Shelf-Life Exposure |
| `model_expected_lost_revenue` | **REJECTED** | Stockout probability multiplied by forecasted revenue loss | Master dataset / Calendar | Point-in-time formula | Premature circular dependency on ML models not yet trained | Belongs strictly to Phase 4 inference and Phase 5 decision engine |
| `unbounded_inventory_ratios` | **REJECTED** | Raw closing / demand ratios producing division-by-zero inf | Master dataset / Calendar | Point-in-time formula | Numerical instability crashing ML tree algorithms | Replaced with safe-division logic and operational caps (365 days) |
| `arbitrary_transfer_decision` | **REJECTED** | Hardcoded lateral transfer commands between stores | Master dataset / Calendar | Point-in-time formula | Out of scope for feature engineering | Transfer recommendation logic belongs to Phase 5 optimization |
| `weather_interaction_explosion` | **REJECTED** | Exhaustive cross-products of weather, city, category, and hour | Master dataset / Calendar | Point-in-time formula | Overfitting and curse of dimensionality | Phase 2 EDA showed modest weather correlations; feature explosion rejected |

---

## 4. Rejection Register Rationale
The StockSense architecture deliberately rejects features that sound appealing but violate statistical integrity or introduce future target leakage:
1. **`overall_product_mean_demand`**: Computing a product's mean across the entire dataset uses late August sales to predict early August. Replaced with shifted rolling averages (`rolling_mean_7`, `rolling_mean_14`).
2. **Store & Product IDs as Continuous**: Store S01 vs S05 does not imply a distance of 4 units. Categorical encoding must preserve nominal structure.
3. **`expected_closing`**: Phase 1 marked this as a mathematical ledger tautology that obscures genuine inventory discrepancies.
4. **Expiry Date Prediction**: Dataset provides rated shelf life, not individual carton batch ages. Renamed to `shelf_life_exposure_ratio`.
5. **Model-Expected Lost Revenue**: Calculating expected financial loss requires future stockout probability from models not yet trained.
6. **Unbounded Inventory Ratios**: Division by zero produces infinities that destabilize gradient boosted trees. Safe-division guards and operational caps (365 days) are enforced.
