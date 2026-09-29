# StockSense Phase 2 Business Insights

## Executive Summary
- **Revenue:** Beverages has the highest observed revenue contribution (17.1%); S02 has the highest observed store revenue.
- **Demand:** Demand is observed at 29,079 date-store-product rows. The highest-volume category is Beverages.
- **Stores:** S03 has the highest observed stock-out rate among stores with inventory observations; this is descriptive, not an arbitrary composite rank.
- **Promotion:** Promoted and normal observations are compared by rank test; the result is association, not causal uplift.
- **Weekend:** Weekend effects are stored by category and store in `weekend_category.csv` and `weekend_store.csv`; the short August window limits generalisation.
- **Volatility:** Store-product volatility is retained as signal; the highest-CV combinations are in `store_product_volatility.csv`.
- **Inventory/shelf-life:** Coverage and shelf-life exposure are only interpretable where closing inventory and positive demand are available. `shelf_life_exposure_ratio > 1` means projected coverage exceeds shelf life, not that expiry occurred.
- **Momentum:** 422 combinations are classified as accelerating under the exploratory 7-day ratio thresholds; this is a hypothesis for Phase 3, not a production feature.
- **Lead time:** `lead_time_stockout.csv` compares lead days, coverage, demand, and stock-outs without causal claims.
- **Financial exposure:** Potential lost revenue is a descriptive stock-out proxy based on observed demand and price; it is not model-based expected loss.
- **Cross-store:** `store_product_cross_store.csv` is the candidate input for rebalancing review; no transfer recommendation is made in Phase 2.
- **Supplier:** `supplier_exposure.csv` describes operational exposure by supplier, not supplier fault.
- **Reconciliation:** `reconciliation_summary.csv` preserves the Phase 1 conclusion that POS demand and inventory sold are different operational signals.
- **External factors:** Spearman associations are in `external_numeric_relationships.csv`; limited history means weak relationships should not be promoted automatically to features.

## KPI Baseline
| KPI | Value | Definition |
|---|---:|---|
| Revenue | 49,067,973.0000 | Sum of aggregated transaction revenue |
| Units sold | 288,761.0000 | Sum of transaction_demand |
| Stock-out rate | 0.0015 | Observed closing <= 0 / rows with closing inventory |
| Inventory turnover | 7,683.4577 | COGS using inventory_sold x cost / mean closing inventory value; inventory rows only |
| Days of inventory | 130.1740 | Closing stock / same-row transaction demand; positive-demand rows only |
| Promotion lift | 2.4261 | Mean row demand promoted vs normal minus 1; association, not causation |
| Estimated lost sales | 39,456.8810 | Observed stock-out rows x transaction demand x average selling price; descriptive proxy |

## Limitations
- The master covers observed combinations rather than a complete calendar; absent rows cannot be treated as zero demand.
- Inventory coverage is incomplete for transaction-only observations, so stock-out and inventory KPIs use valid closing-inventory rows.
- The main history is roughly one month, making momentum, seasonality, and regime evidence provisional.
- Transaction demand and `inventory_sold` are not interchangeable.
- No causal claims, expiry claims, or model-based lost-sales claims are made.
