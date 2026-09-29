"""StockSense Phase 3: Financial Exposure Features (Group M)."""
import pandas as pd
import numpy as np


def add_financial_features(df: pd.DataFrame) -> pd.DataFrame:
    """Compute point-in-time financial exposure, unit economics, and inventory carrying value.

    Features generated:
    - unit_margin: avg_selling_price - cost_price
    - margin_pct: (avg_selling_price - cost_price) / avg_selling_price
    - inventory_value: closing * cost_price
    - daily_revenue: transaction_demand * avg_selling_price
    - potential_revenue_exposure: closing * avg_selling_price
    - potential_margin_exposure: closing * unit_margin
    - stockout_exposure_value: reorder deficit value at selling price

    Leakage Prevention:
    - Uses point-in-time observed prices and cost prices available at prediction time.
    - Does NOT compute model-dependent expected loss (which belongs to Phase 4 inference).
    """
    df = df.copy()

    price = pd.to_numeric(df["avg_selling_price"], errors="coerce").fillna(
        pd.to_numeric(df.get("mrp", np.nan), errors="coerce")
    )
    cost = pd.to_numeric(df["cost_price"], errors="coerce")
    closing = pd.to_numeric(df["closing"], errors="coerce")
    reorder = pd.to_numeric(df["reorder_lvl"], errors="coerce")
    demand = pd.to_numeric(df["transaction_demand"], errors="coerce").fillna(0.0)

    # Unit economics
    df["unit_margin"] = price - cost
    df["margin_pct"] = np.where(price > 0, (price - cost) / price, np.nan)

    # Point-in-time inventory value and revenue
    df["inventory_value"] = np.where(closing.notna(), closing.clip(lower=0) * cost, np.nan)
    df["daily_revenue"] = demand * price
    df["potential_revenue_exposure"] = np.where(closing.notna(), closing.clip(lower=0) * price, np.nan)
    df["potential_margin_exposure"] = np.where(closing.notna(), closing.clip(lower=0) * df["unit_margin"], np.nan)

    # Dollar value of safety stock deficit below reorder level
    deficit = np.where(closing.notna() & reorder.notna(), (reorder - closing).clip(lower=0), np.nan)
    df["stockout_exposure_value"] = deficit * price

    return df
