"""StockSense Phase 3: Demand Lag Features (Group B)."""
import pandas as pd
import numpy as np


def add_lag_features(df: pd.DataFrame) -> pd.DataFrame:
    """Compute true calendar demand lag features independently within each Store x Product.

    Features generated:
    - lag_1: transaction demand exactly 1 calendar day earlier (t - 1)
    - lag_7: transaction demand exactly 7 calendar days earlier (t - 7)
    - lag_14: transaction demand exactly 14 calendar days earlier (t - 14)

    Leakage prevention:
    - Computed strictly on past calendar dates (t - lag).
    - Unobserved historical days within the active window are treated as 0 demand.
    - Dates prior to dataset start (where t - lag < min_date) evaluate to NaN.
    """
    df = df.copy()
    orig_cols = df.columns.tolist()
    df["date"] = pd.to_datetime(df["date"])

    # Extract distinct store x product pairs and full calendar date range
    sp_pairs = df[["store_id", "product_id"]].drop_duplicates()
    min_date = df["date"].min()
    max_date = df["date"].max()
    full_dates = pd.date_range(min_date, max_date, freq="D")

    # Build dense grid to ensure true calendar alignment
    grid = sp_pairs.assign(key=1).merge(
        pd.DataFrame({"date": full_dates, "key": 1}), on="key"
    ).drop(columns=["key"])

    # Merge observed transaction demand onto grid
    demand_slice = df[["store_id", "product_id", "date", "transaction_demand"]].drop_duplicates(
        subset=["store_id", "product_id", "date"]
    )
    grid = grid.merge(demand_slice, on=["store_id", "product_id", "date"], how="left")
    
    # Within the observation window, unobserved days represent 0 sales
    grid["cal_demand"] = grid["transaction_demand"].fillna(0.0)

    # Sort strictly by store, product, date
    grid = grid.sort_values(["store_id", "product_id", "date"]).reset_index(drop=True)

    # Grouped shifts by true calendar step
    grouped = grid.groupby(["store_id", "product_id"])["cal_demand"]
    grid["lag_1"] = grouped.shift(1)
    grid["lag_7"] = grouped.shift(7)
    grid["lag_14"] = grouped.shift(14)

    # Merge lag features back to original observations
    lag_cols = ["store_id", "product_id", "date", "lag_1", "lag_7", "lag_14"]
    df = df.merge(grid[lag_cols], on=["store_id", "product_id", "date"], how="left")

    return df
