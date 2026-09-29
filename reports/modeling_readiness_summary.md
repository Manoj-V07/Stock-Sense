# Phase 4 Modelling Readiness Summary

## Prediction contract
- Prediction grain: Date × Store × Product
- Prediction date: last date for which point-in-time information is known to the model
- Target 1: next_7_day_demand (7-day forward regression target)
- Target 2: stockout_flag (current inventory status)

## Audit checks
- Rows: 29079
- Duplicate date-store-product rows: True
- Demand-target valid rows: 5611 missing
- Stockout-target valid rows: 8070 missing
- Infinite values: 0
- Missing numeric cells: 289346
- Stockout rate: 0.1523%
- Date range: 2026-07-31 00:00:00 to 2026-09-01 00:00:00

## Time-aware split design
- Train: 2026-07-31 00:00:00 to 2026-08-14 00:00:00
- Validation: 2026-08-15 00:00:00 to 2026-08-19 00:00:00
- Test: 2026-08-20 00:00:00 to 2026-08-25 00:00:00
