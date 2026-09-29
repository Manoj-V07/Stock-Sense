# Data Leakage Classification

Phase 3 MUST NOT use DO_NOT_USE_AS_FEATURE columns as predictors.

## SAFE_HISTORICAL
- transaction_demand
- revenue
- transaction_count
- unique_customer_count
- avg_selling_price
- avg_discount_pct
- promotion_active
- peak_hour
- opening
- received
- inventory_sold
- closing
- reorder_lvl
- lead_days
- temp_c
- rain_mm
- holiday
- festival
- weekend
- local_event

## SAFE_STATIC_ATTRIBUTE
- category
- sub_category
- brand
- mrp
- cost_price
- shelf_life_days
- supplier_id
- city
- store_type
- floor_area_sqft
- avg_daily_customers
- region

## SAFE_DERIVED_DQ
- inventory_balance_gap
- reconciliation_status
- inventory_demand_gap
- sparse_history_flag
- zero_demand_ratio
- history_length
- active_days
- invalid_qty_count
- invalid_price_count
- invalid_inventory_flag
- invalid_lead_flag
- temp_imputed_flag
- rain_imputed_flag

## DO_NOT_USE_AS_FEATURE
- expected_closing

