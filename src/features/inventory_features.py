"""StockSense Phase 3: Inventory Intelligence Features (Group D & Group P)."""
import pandas as pd
import numpy as np


def add_inventory_features(df: pd.DataFrame) -> pd.DataFrame:
    """Compute point-in-time inventory sufficiency, replenishment urgency, and shelf-life exposure.

    Features generated:
    Mandatory:
    - days_of_inventory: closing / (rolling_mean_7 + 1e-5), capped at 365
    - inventory_to_demand_ratio: closing / (rolling_mean_7 * 7 + 1e-5), capped at 52
    - reorder_gap: closing - reorder_lvl

    Operational Intelligence:
    - low_stock_flag: 1 if closing <= reorder_lvl, else 0
    - stockout_observed: 1 if closing <= 0, else 0 (NaN if closing unobserved)
    - no_observed_demand_flag: 1 if trailing 7-day demand is 0 or NaN while inventory > 0
    - days_to_stockout: point-in-time estimated days to stockout (capped at 365, NaN if missing)
    - lead_time_gap: days_to_stockout - lead_days (positive = safe buffer, negative = reorder risk)
    - shelf_life_exposure_ratio: days_to_stockout / shelf_life_days
    - high_shelf_life_exposure_flag: 1 if shelf_life_exposure_ratio > 1.0, else 0

    Zero/Missing Handling:
    - If closing inventory is missing (unobserved), ratios evaluate to NaN (no blind 0-filling).
    - If trailing demand is 0, days_to_stockout is flagged and capped, avoiding infinite values.
    """
    df = df.copy()

    # Base closing and lead time columns
    closing = pd.to_numeric(df["closing"], errors="coerce")
    reorder = pd.to_numeric(df["reorder_lvl"], errors="coerce")
    lead = pd.to_numeric(df["lead_days"], errors="coerce").fillna(
        pd.to_numeric(df.get("lead_time_days", np.nan), errors="coerce")
    )
    shelf_life = pd.to_numeric(df["shelf_life_days"], errors="coerce")
    
    # Trailing demand rate strictly available at prediction time (t-7 to t-1)
    if "rolling_mean_7" in df.columns:
        daily_rate = df["rolling_mean_7"]
    else:
        daily_rate = df["transaction_demand"]

    # 1. Mandatory reorder gap
    df["reorder_gap"] = closing - reorder
    df["low_stock_flag"] = np.where(
        closing.notna() & reorder.notna(),
        (closing <= reorder).astype(int),
        np.nan
    )

    # 2. Observed stockout at observation time t
    df["stockout_observed"] = np.where(
        closing.notna(),
        (closing <= 0).astype(int),
        np.nan
    )

    # 3. Flag zero trailing demand
    zero_demand_mask = (daily_rate <= 0) | daily_rate.isna()
    df["no_observed_demand_flag"] = np.where(
        closing.notna() & (closing > 0) & zero_demand_mask,
        1,
        0
    )

    # 4. Mandatory days of inventory & inventory-to-demand ratio
    # Capped safely to prevent inf values
    coverage = np.where(
        closing.isna(),
        np.nan,
        np.where(
            closing <= 0,
            0.0,
            np.where(
                zero_demand_mask,
                365.0,  # Operational ceiling when inventory exists but demand is zero
                np.clip(closing / daily_rate, 0.0, 365.0)
            )
        )
    )
    df["days_of_inventory"] = coverage
    df["inventory_to_demand_ratio"] = np.where(
        closing.isna(),
        np.nan,
        np.clip(coverage / 7.0, 0.0, 52.0)
    )

    # 5. Days to stockout (operational intelligence)
    df["days_to_stockout"] = coverage

    # 6. Lead time gap (days_to_stockout - lead_days)
    # Positive: coverage exceeds supplier lead time; Negative: depletion before delivery
    df["lead_time_gap"] = np.where(
        closing.notna() & lead.notna(),
        df["days_to_stockout"] - lead,
        np.nan
    )

    # 7. Shelf-life exposure ratio
    # High exposure means inventory coverage exceeds manufacturer shelf life
    shelf_ratio = np.where(
        closing.notna() & shelf_life.notna() & (shelf_life > 0),
        df["days_to_stockout"] / shelf_life,
        np.nan
    )
    df["shelf_life_exposure_ratio"] = np.clip(shelf_ratio, 0.0, 50.0)
    df["high_shelf_life_exposure_flag"] = np.where(
        df["shelf_life_exposure_ratio"].notna(),
        (df["shelf_life_exposure_ratio"] > 1.0).astype(int),
        np.nan
    )

    return df
