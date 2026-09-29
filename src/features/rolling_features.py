"""StockSense Phase 3: Rolling Demand Features (Group C)."""
import pandas as pd
import numpy as np


def add_rolling_features(df: pd.DataFrame) -> pd.DataFrame:
    """Compute strictly shifted rolling statistics of historical demand within Store x Product.

    Features generated:
    - rolling_mean_7: Mean demand over trailing 7 calendar days [t-7, t-1]
    - rolling_mean_14: Mean demand over trailing 14 calendar days [t-14, t-1]
    - rolling_std_7: Standard deviation of demand over trailing 7 calendar days [t-7, t-1]

    Leakage Prevention:
    - Current day t's demand is strictly excluded via shift(1).
    - True calendar spacing is enforced using a dense calendar grid.
    - Zero future information enters any window.
    """
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])

    # Extract distinct store x product pairs and full calendar date range
    sp_pairs = df[["store_id", "product_id"]].drop_duplicates()
    min_date = df["date"].min()
    max_date = df["date"].max()
    full_dates = pd.date_range(min_date, max_date, freq="D")

    # Build dense grid for true calendar rolling windows
    grid = sp_pairs.assign(key=1).merge(
        pd.DataFrame({"date": full_dates, "key": 1}), on="key"
    ).drop(columns=["key"])

    demand_slice = df[["store_id", "product_id", "date", "transaction_demand"]].drop_duplicates(
        subset=["store_id", "product_id", "date"]
    )
    grid = grid.merge(demand_slice, on=["store_id", "product_id", "date"], how="left")
    grid["cal_demand"] = grid["transaction_demand"].fillna(0.0)

    # Sort strictly by store, product, date
    grid = grid.sort_values(["store_id", "product_id", "date"]).reset_index(drop=True)

    # Shifted rolling computations: shift(1) ensures window [t-W, t-1]
    # min_periods=1 ensures early August has best available trailing signal without looking forward
    grouped = grid.groupby(["store_id", "product_id"])["cal_demand"]
    
    # Strictly shifted: t-7 to t-1
    grid["rolling_mean_7"] = grouped.transform(
        lambda s: s.shift(1).rolling(7, min_periods=1).mean()
    )
    # Strictly shifted: t-14 to t-1
    grid["rolling_mean_14"] = grouped.transform(
        lambda s: s.shift(1).rolling(14, min_periods=1).mean()
    )
    # Strictly shifted: t-7 to t-1 (std requires at least 2 observations)
    grid["rolling_std_7"] = grouped.transform(
        lambda s: s.shift(1).rolling(7, min_periods=2).std()
    ).fillna(0.0)

    # Merge rolling features back to original observations
    roll_cols = ["store_id", "product_id", "date", "rolling_mean_7", "rolling_mean_14", "rolling_std_7"]
    df = df.merge(grid[roll_cols], on=["store_id", "product_id", "date"], how="left")

    return df
