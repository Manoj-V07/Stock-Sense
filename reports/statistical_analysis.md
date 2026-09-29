# StockSense Phase 2 Statistical Analysis

All tests use alpha = 0.05. Statistical significance is distinct from practical business significance.

### Promotion and demand
- **H0:** Promotion does not change demand distributions
- **H1:** Promotion changes demand distributions
- **Test:** Mann-Whitney U; statistic=156,705,659.0000, p-value=0; effect size=0.6875
- **Decision:** Reject.
- **Assumptions/sample:** Independent observations; ordinal/rank test; distributions need not be normal; All observed rows with valid demand.
- **Interpretation/limitation:** Association is statistically assessed; confounding by product, store, timing remains.
### Mean demand across store types
- **H0:** Demand distributions are equal across store types
- **H1:** At least one store type differs
- **Test:** Kruskal-Wallis; statistic=2.6102, p-value=0.2711; effect size=NA
- **Decision:** Do not reject.
- **Assumptions/sample:** Independent groups; rank-based test; similar distribution shape is desirable; All observed rows grouped by store_type.
- **Interpretation/limitation:** A significant result identifies a difference, not its cause.
### Promotion status and stock-out frequency
- **H0:** Promotion and stock-out status are independent
- **H1:** They are associated
- **Test:** Chi-square independence; statistic=0.9849, p-value=0.321; effect size=NA
- **Decision:** Do not reject.
- **Assumptions/sample:** Expected cell counts should be adequate; rows independent; Rows with observed closing inventory.
- **Interpretation/limitation:** Stock-out observations may be affected by assortment and missing inventory coverage.

## Supporting relationship analysis
Spearman relationships for demand and stock-out status are saved in `data/processed/eda_summary_tables/external_numeric_relationships.csv`. Correlation is descriptive association, not causation; nonlinear effects and confounding remain possible.
