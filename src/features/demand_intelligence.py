"""StockSense Phase 3: Demand Intelligence (Groups I, J, K - Momentum, Volatility, Regime)."""
import pandas as pd
import numpy as np


def add_demand_intelligence(df: pd.DataFrame) -> pd.DataFrame:
    """Compute leakage-safe demand momentum, volatility, and behavioural regime indicators.

    Features generated:
    Group I - Demand Momentum:
    - recent_7_day_demand: sum of demand over trailing calendar window [t-7, t-1]
    - previous_7_day_demand: sum of demand over prior calendar window [t-14, t-8]
    - demand_momentum_ratio: recent_7_day_demand / (previous_7_day_demand + 1e-5)
    - demand_change_pct: percentage change from previous to recent 7-day demand
    - momentum_class: Accelerating (>1.20), Stable [0.80, 1.20], Declining (<0.80)

    Group J - Demand Volatility:
    - demand_cv_7: rolling coefficient of variation over trailing [t-7, t-1]
    - zero_demand_ratio_7: proportion of 0-demand days in [t-7, t-1]
    - demand_range_7: max - min daily demand in trailing [t-7, t-1]
    - intermittent_demand_flag: 1 if zero_demand_ratio_7 >= 0.50 and positive mean demand

    Group K - Demand Regime:
    - demand_regime: Categorical segment based on trailing characteristics:
      Intermittent, Volatile, Accelerating, Declining, Stable

    Leakage Prevention:
    - Shifted trailing windows ensure no current (t) or future (t+1..t+7) information enters.
    """
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])

    # Extract distinct store x product pairs and full calendar date range
    sp_pairs = df[["store_id", "product_id"]].drop_duplicates()
    min_date = df["date"].min()
    max_date = df["date"].max()
    full_dates = pd.date_range(min_date, max_date, freq="D")

    # Dense grid
    grid = sp_pairs.assign(key=1).merge(
        pd.DataFrame({"date": full_dates, "key": 1}), on="key"
    ).drop(columns=["key"])

    demand_slice = df[["store_id", "product_id", "date", "transaction_demand"]].drop_duplicates(
        subset=["store_id", "product_id", "date"]
    )
    grid = grid.merge(demand_slice, on=["store_id", "product_id", "date"], how="left")
    grid["cal_demand"] = grid["transaction_demand"].fillna(0.0)
    grid = grid.sort_values(["store_id", "product_id", "date"]).reset_index(drop=True)

    grouped = grid.groupby(["store_id", "product_id"])["cal_demand"]

    # 1. Momentum: recent [t-7, t-1] vs previous [t-14, t-8]
    recent_sum = grouped.transform(lambda s: s.shift(1).rolling(7, min_periods=1).sum())
    # 14-day sum shifted by 1: sum from t-14 to t-1
    sum_14 = grouped.transform(lambda s: s.shift(1).rolling(14, min_periods=1).sum())
    # Previous 7-day sum is sum_14 - recent_sum (sum from t-14 to t-8)
    # Only valid when at least 8 days of history exist
    prev_sum = sum_14 - recent_sum
    prev_sum = np.where(grid.groupby(["store_id", "product_id"]).cumcount() >= 8, prev_sum, np.nan)

    grid["recent_7_day_demand"] = recent_sum
    grid["previous_7_day_demand"] = prev_sum

    # Safe ratio calculation
    momentum_ratio = np.where(
        grid["previous_7_day_demand"].isna(),
        np.nan,
        np.where(
            grid["previous_7_day_demand"] <= 0,
            np.where(grid["recent_7_day_demand"] > 0, 2.0, 1.0),
            np.clip(grid["recent_7_day_demand"] / grid["previous_7_day_demand"], 0.0, 10.0)
        )
    )
    grid["demand_momentum_ratio"] = momentum_ratio
    grid["demand_change_pct"] = np.where(
        grid["demand_momentum_ratio"].notna(),
        (grid["demand_momentum_ratio"] - 1.0) * 100.0,
        np.nan
    )
    grid["momentum_class"] = pd.cut(
        grid["demand_momentum_ratio"],
        bins=[-np.inf, 0.80, 1.20, np.inf],
        labels=["Declining", "Stable", "Accelerating"]
    ).astype(str).replace({"nan": "Unclassified"})

    # 2. Volatility over trailing [t-7, t-1]
    mean_7 = grouped.transform(lambda s: s.shift(1).rolling(7, min_periods=1).mean())
    std_7 = grouped.transform(lambda s: s.shift(1).rolling(7, min_periods=2).std()).fillna(0.0)
    grid["demand_cv_7"] = np.where(mean_7 > 0, std_7 / mean_7, 0.0)

    # Zero demand ratio in trailing 7 days
    zero_ratio = grouped.transform(
        lambda s: (s.shift(1) == 0).rolling(7, min_periods=1).mean()
    )
    grid["zero_demand_ratio_7"] = zero_ratio

    # Demand range in trailing 7 days
    max_7 = grouped.transform(lambda s: s.shift(1).rolling(7, min_periods=1).max())
    min_7 = grouped.transform(lambda s: s.shift(1).rolling(7, min_periods=1).min())
    grid["demand_range_7"] = (max_7 - min_7).fillna(0.0)

    # Intermittent demand flag
    grid["intermittent_demand_flag"] = (
        (grid["zero_demand_ratio_7"] >= 0.50) & (mean_7 > 0)
    ).astype(int)

    # 3. Demand Regime classification
    conditions = [
        grid["intermittent_demand_flag"] == 1,
        grid["demand_cv_7"] > 1.0,
        grid["demand_momentum_ratio"] > 1.20,
        grid["demand_momentum_ratio"] < 0.80,
    ]
    choices = ["Intermittent", "Volatile", "Accelerating", "Declining"]
    grid["demand_regime"] = np.select(conditions, choices, default="Stable")

    # Merge features back onto master observations
    intel_cols = [
        "store_id", "product_id", "date",
        "recent_7_day_demand", "previous_7_day_demand",
        "demand_momentum_ratio", "demand_change_pct", "momentum_class",
        "demand_cv_7", "zero_demand_ratio_7", "demand_range_7",
        "intermittent_demand_flag", "demand_regime"
    ]
    df = df.merge(grid[intel_cols], on=["store_id", "product_id", "date"], how="left")

    return df
