"""StockSense Phase 3: Cross-Store Intelligence (Group O - Rebalancing Signals)."""
import pandas as pd
import numpy as np


def add_cross_store_features(df: pd.DataFrame) -> pd.DataFrame:
    """Compute leakage-safe cross-store inventory and demand rebalancing indicators.

    Features generated:
    - network_product_mean_inventory: Mean closing stock across all stores for this product on date t
    - store_relative_inventory_ratio: closing / (network_product_mean_inventory + 1e-5)
    - network_product_mean_demand: Mean trailing 7-day demand across all stores for this product on date t
    - store_relative_demand_ratio: rolling_mean_7 / (network_product_mean_demand + 1e-5)
    - excess_inventory_flag: 1 if store has disproportionate inventory (>1.5x network mean) and >20 days coverage
    - shortage_risk_flag: 1 if store has low relative inventory (<0.6x network mean) and lead_time_gap < 0

    Leakage Prevention:
    - Strictly contemporaneous: compares stores only on the SAME observation date t.
    - Zero future demand or inventory from other stores is used.
    - Rebalancing signals support Phase 5 transfer logic without implementing transfers here.
    """
    df = df.copy()

    # Network-wide daily product inventory mean on date t
    net_inv = df.groupby(["date", "product_id"])["closing"].transform("mean")
    df["network_product_mean_inventory"] = net_inv
    df["store_relative_inventory_ratio"] = np.where(
        net_inv > 0,
        df["closing"] / net_inv,
        np.where(df["closing"] > 0, 1.0, 0.0)
    )

    # Network-wide trailing 7-day demand mean for product across stores
    demand_col = "rolling_mean_7" if "rolling_mean_7" in df.columns else "transaction_demand"
    net_dem = df.groupby(["date", "product_id"])[demand_col].transform("mean")
    df["network_product_mean_demand"] = net_dem
    df["store_relative_demand_ratio"] = np.where(
        net_dem > 0,
        df[demand_col] / net_dem,
        np.where(df[demand_col] > 0, 1.0, 0.0)
    )

    # Excess and shortage rebalancing flags
    cov_col = "days_of_inventory" if "days_of_inventory" in df.columns else None
    lt_gap_col = "lead_time_gap" if "lead_time_gap" in df.columns else None

    if cov_col is not None:
        df["excess_inventory_flag"] = (
            (df["store_relative_inventory_ratio"] > 1.5) & (df[cov_col] > 20.0)
        ).astype(int)
    else:
        df["excess_inventory_flag"] = 0

    if lt_gap_col is not None:
        df["shortage_risk_flag"] = (
            (df["store_relative_inventory_ratio"] < 0.6) & (df[lt_gap_col] < 0.0)
        ).astype(int)
    else:
        df["shortage_risk_flag"] = 0

    return df
