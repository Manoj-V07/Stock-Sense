# StockSense -- Data Quality Report
**Phase 1** | 2026-09-29 10:50:38

---

## 1. Dataset Overview

| Dataset | Rows | Columns | Dup Rows | Missing |
|---------|------|---------|----------|---------|
| transactions | 151,928 | 11 | 25 | 9 |
| products | 120 | 8 | 0 | 0 |
| stores | 10 | 6 | 0 | 0 |
| inventory | 26,907 | 9 | 0 | 2 |
| external_factors | 310 | 8 | 0 | 7 |

## 2. Data Quality Issues

| Dataset | Column | Issue | Count | % | Action | Justification |
|---------|--------|-------|-------|---|--------|---------------|
| products | category | Case/spelling inconsistency | 6 | 5.00% | Standardised to canonical Title-case name | 6 variants (beverage,BEVERAGES,DAIRY,SNACKS,household,Staples[space]) mapped. |
| products | cost_price/mrp | cost_price > mrp | 0 | 0.00% | No action | PASS -- no violations |
| products | supplier_id | Invalid supplier ID (SUP999) | 1 | 0.83% | Flagged; retained | SUP999 absent from supplier master. |
| stores | ALL | Missing values | 0 | 0.00% | No action | PASS |
| stores | ALL | Duplicate rows | 0 | 0.00% | No action | PASS |
| transactions | date | Outside Aug 01-31 window | 2 | 0.00% | Flagged; retained | 2 fringe records (Jul-31, Sep-01). Modelling decides inclusion. |
| transactions | ALL | Exact duplicate rows | 25 | 0.02% | Removed -- kept first occurrence | Identical on all fields incl. transaction_id. Entry duplicates not repeated purchases. |
| transactions | transaction_id | Dup tx_id post-dedup | 2 | 0.00% | Flagged dup_txid_flag=1; retained | ID-generation errors. Retained with flag. |
| transactions | store_id | Orphan store_id (S99) | 1 | 0.00% | Flagged orphan_store_flag=1; excluded from master | S99 not in stores reference. |
| transactions | product_id | Orphan product_id (P9999) | 1 | 0.00% | Flagged orphan_product_flag=1; excluded from master | P9999 not in products reference. |
| transactions | quantity | Non-positive quantity | 3 | 0.00% | Flagged invalid_qty_flag=1; retained | Negative=possible return; zero=impossible. Flagged. |
| transactions | selling_price | Non-positive selling price | 1 | 0.00% | Flagged invalid_price_flag=1; excluded from revenue | Price -20 impossible. Flagged. |
| transactions | discount_pct | Discount outside [0,100] | 2 | 0.00% | Flagged; value set to NaN | Values 110 and -15 impossible. Set NaN to protect aggregates. |
| transactions | hour | Hour outside [0,23] | 2 | 0.00% | Flagged; value set to NaN | Values 27 and -3 impossible clock values. Set NaN. |
| transactions | customer_id | Missing customer_id | 4 | 0.00% | Retained as NaN | Cannot impute. NaN preserved. |
| transactions | payment_mode | Missing payment_mode | 3 | 0.00% | Retained as NaN | Cannot impute. NaN preserved. |
| transactions | hour | Missing hour | 4 | 0.00% | Retained as NaN | Cannot impute. NaN preserved. |
| inventory | store_id | Orphan store_id (S99) | 1 | 0.00% | Flagged; retained | Cannot join to reference. |
| inventory | product_id | Orphan product_id (P9999) | 1 | 0.00% | Flagged; retained | Cannot join to reference. |
| inventory | opening | Negative opening stock | 1 | 0.00% | Flagged invalid_inventory_flag=1; NOT overwritten | Physically impossible. Correct value unknown. |
| inventory | received | Negative received | 1 | 0.00% | Flagged; NOT overwritten | Physically impossible. |
| inventory | lead_days | Non-positive lead_days | 2 | 0.01% | Flagged invalid_lead_flag=1; retained | Lead<=0 days impossible. Flagged for Phase 3. |
| inventory | received | Missing received | 1 | 0.00% | Retained NaN; INSUFFICIENT_DATA | Cannot impute. |
| inventory | closing | Missing closing | 1 | 0.00% | Retained NaN; INSUFFICIENT_DATA | Cannot impute. |
| inventory | closing/opening/received/sold | Arithmetic mismatch | 2 | 0.01% | inventory_balance_gap and reconciliation_status added; NOT modified | Gap documented for Phase 3 Reconciliation Intelligence. |
| external_factors | city | City typo: 'ChennaI' | 1 | 0.32% | Corrected to 'Chennai' | Obvious typo (capital I). Corrected to enable join. |
| external_factors | temp_c | Missing temp_c | 6 | 1.94% | Imputed city-level monthly median; flagged temp_imputed_flag | 6 missing. City median best estimate without external API. |
| external_factors | rain_mm | Missing rain_mm | 1 | 0.32% | Imputed city median; flagged rain_imputed_flag | 1 missing. City median used. |
| external_factors | date+city | Duplicate date+city after typo correction | 1 | 0.32% | Resolved by mean aggregation of numeric cols; max of binary flags | Raw data has both Chennai and ChennaI rows for 2026-08-25. After typo fix two Chennai rows exist for same date. Mean/max aggregation is the least destructive resolution without external reference data. |
| external_factors | date | Inv dates without ext coverage | 1 | 3.12% | Master will have NaN for these dates | Ext ends Aug-31; inv extends to Sep-03. Dates: [datetime.date(2026, 9, 3)] |
| transactions/inventory | quantity/sold | TX demand != inv sold | 34919 | 99.83% | Both retained; inventory_demand_gap created | POS vs WMS discrepancies expected. Replacing one with other = fabrication. |
| transactions | store_id x product_id | Sparse history (>70% zero or <7 active) | 71 | 5.92% | Flagged sparse_history_flag=1; retained | Sparse combos may be new/low-velocity SKUs. Removing hides stockout risk. |

## 3. Inventory Reconciliation

| Status | Count | % |
|--------|-------|---|
| CONSISTENT | 26,899 | 99.97% |
| INVALID_INPUT | 4 | 0.01% |
| MAJOR_MISMATCH | 2 | 0.01% |
| INSUFFICIENT_DATA | 2 | 0.01% |

## 4. TX vs Inventory Conclusion
> transaction_demand and inventory.sold are DIFFERENT signals (POS vs WMS). Both retained.
> inventory_demand_gap documents the discrepancy for Phase 3.

## 5. Sparse History
- Total combos: 1,200
- Sparse: 71 (5.9%)
- Never sold: 1

## 6. Validation Results

| Check | Status | Detail |
|-------|--------|--------|
| Master grain unique | PASS |  |
| Required columns present | PASS | Missing: [] |
| No null dates | PASS |  |
| transaction_demand non-negative | PASS |  |
| Revenue non-negative | PASS |  |
| inventory_balance_gap present | PASS |  |
| reconciliation_status values valid | PASS | Unexpected: set() |
| sparse_history_flag is binary | PASS |  |
| Raw files untouched (MD5) | PASS |  |
| All cleaned files exist | PASS |  |
| All processed files exist | PASS |  |
| No future-derived columns | PASS | Found: [] |
| Product categories standardised | PASS | Bad: set() |
| External city typo ('ChennaI') fixed | PASS |  |
| No null temp_c remaining | PASS |  |
