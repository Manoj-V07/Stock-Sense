"""StockSense Phase 3: Master Feature Pipeline Orchestrator."""
import sys
from pathlib import Path
import warnings
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.features.time_features import add_time_features
from src.features.lag_features import add_lag_features
from src.features.rolling_features import add_rolling_features
from src.features.inventory_features import add_inventory_features
from src.features.demand_intelligence import add_demand_intelligence
from src.features.financial_features import add_financial_features
from src.features.supplier_features import add_supplier_features
from src.features.cross_store_features import add_cross_store_features

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parents[2]
PROC_DIR = ROOT / "data" / "processed"
FEATURES_DIR = PROC_DIR / "features"
FEATURES_DIR.mkdir(parents=True, exist_ok=True)


def compute_targets(df: pd.DataFrame) -> pd.DataFrame:
    """Compute target variables strictly without leakage.

    Targets:
    1. next_7_day_demand: Sum of calendar demand over [t+1, t+7].
       Evaluates to NaN if the complete 7-day future window is unobserved.
    2. stockout_flag: Operational stock-out label on observation date t (closing <= 0).
       Evaluates to NaN if inventory is unobserved on date t.
    3. next_7_day_stockout: Forward classification target (1 if any closing <= 0 in [t+1, t+7]).
    """
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])

    # Build continuous calendar grid for forward window calculations
    sp_pairs = df[["store_id", "product_id"]].drop_duplicates()
    min_date = df["date"].min()
    max_date = df["date"].max()
    full_dates = pd.date_range(min_date, max_date, freq="D")

    grid = sp_pairs.assign(key=1).merge(
        pd.DataFrame({"date": full_dates, "key": 1}), on="key"
    ).drop(columns=["key"])

    # Merge demand and inventory onto grid
    sub = df[["store_id", "product_id", "date", "transaction_demand", "closing"]].drop_duplicates(
        subset=["store_id", "product_id", "date"]
    )
    grid = grid.merge(sub, on=["store_id", "product_id", "date"], how="left")
    grid["cal_demand"] = grid["transaction_demand"].fillna(0.0)
    grid = grid.sort_values(["store_id", "product_id", "date"]).reset_index(drop=True)

    # 1. Target: next_7_day_demand
    # Reverse rolling sum of 7 future days, shifted by -1
    grouped = grid.groupby(["store_id", "product_id"])
    grid["next_7_day_demand"] = grouped["cal_demand"].transform(
        lambda s: s.iloc[::-1].rolling(7, min_periods=7).sum().iloc[::-1].shift(-1)
    )

    # 2. Forward stockout target: any closing <= 0 in [t+1, t+7]
    grid["stockout_binary"] = np.where(grid["closing"].notna(), (grid["closing"] <= 0).astype(float), np.nan)
    grid["next_7_day_stockout"] = grouped["stockout_binary"].transform(
        lambda s: s.iloc[::-1].rolling(7, min_periods=4).max().iloc[::-1].shift(-1)
    )

    # Merge targets back onto master
    target_cols = ["store_id", "product_id", "date", "next_7_day_demand", "next_7_day_stockout"]
    df = df.merge(grid[target_cols], on=["store_id", "product_id", "date"], how="left")

    # Current operational stockout flag
    df["stockout_flag"] = np.where(
        df["closing"].notna(),
        (df["closing"] <= 0).astype(int),
        np.nan
    )

    return df


def add_price_promotion_features(df: pd.DataFrame) -> pd.DataFrame:
    """Derive point-in-time price, discount, and promotion features (Group E)."""
    df = df.copy()

    # Mandatory challenge features
    df["discount_pct"] = pd.to_numeric(df.get("avg_discount_pct", 0.0), errors="coerce").fillna(0.0)
    df["promotion_flag"] = pd.to_numeric(df.get("promotion_active", 0), errors="coerce").fillna(0).astype(int)

    # Price change relative to catalogue MRP
    price = pd.to_numeric(df.get("avg_selling_price", np.nan), errors="coerce")
    mrp = pd.to_numeric(df.get("mrp", np.nan), errors="coerce")
    
    df["price_change"] = price - mrp
    df["price_change_pct"] = np.where(mrp > 0, (price - mrp) / mrp * 100.0, 0.0)

    return df


def add_interaction_features(df: pd.DataFrame) -> pd.DataFrame:
    """Derive selected high-signal interactions supported by Phase 2 EDA."""
    df = df.copy()

    # Promotion x Weekend interaction
    df["promo_x_weekend"] = df["promotion_flag"] * df["weekend_flag"]

    # Discount x Promotion interaction
    df["discount_x_promo"] = df["discount_pct"] * df["promotion_flag"]

    # Lead time x Volatility interaction
    lead = pd.to_numeric(df["lead_days"], errors="coerce").fillna(df.get("lead_time_days", 3.0))
    cv = df.get("demand_cv_7", 0.0).fillna(0.0)
    df["lead_time_x_volatility"] = lead * cv

    # Reorder gap normalized by lead time
    gap = df.get("reorder_gap", 0.0)
    df["reorder_gap_x_lead_time"] = np.where(lead > 0, gap / lead, gap)

    return df


def add_reconciliation_features(df: pd.DataFrame) -> pd.DataFrame:
    """Preserve and enhance Phase 1 reconciliation and data-quality signals (Group L)."""
    df = df.copy()

    # Binary consistency flag
    df["inventory_consistency_flag"] = (df["reconciliation_status"] == "CONSISTENT").astype(int)

    # Data quality score: baseline 1.0, deducted for anomalies
    score = np.ones(len(df), dtype=float)
    score -= (df["reconciliation_status"] != "CONSISTENT").astype(float) * 0.3
    score -= df["invalid_inventory_flag"].fillna(0).astype(float) * 0.3
    score -= df["invalid_lead_flag"].fillna(0).astype(float) * 0.2
    score -= (df["sparse_history_flag"].fillna(0).astype(float)) * 0.2
    df["inventory_data_quality_score"] = np.clip(score, 0.0, 1.0)

    return df


def build_feature_pipeline(master_csv_path: str = None) -> pd.DataFrame:
    """Execute end-to-end reproducible feature pipeline."""
    if master_csv_path is None:
        master_csv_path = PROC_DIR / "master_dataset.csv"

    print(">>> Phase 3 Feature Pipeline Starting...")
    df = pd.read_csv(master_csv_path, parse_dates=["date"])
    print(f"  Loaded master dataset: {len(df):,} rows x {len(df.columns)} columns")

    # Step 2: Sort correctly
    df = df.sort_values(["store_id", "product_id", "date"]).reset_index(drop=True)

    # Step 3: Mandatory Time Features (Group A)
    print("  [1/10] Adding Time Features (Group A)...")
    df = add_time_features(df)

    # Step 4: Demand Lag Features (Group B)
    print("  [2/10] Adding Demand Lags (Group B)...")
    df = add_lag_features(df)

    # Step 5: Rolling Features (Group C)
    print("  [3/10] Adding Rolling Demand (Group C)...")
    df = add_rolling_features(df)

    # Step 7: Price and Promotion (Group E)
    print("  [4/10] Adding Price & Promotion Features (Group E)...")
    df = add_price_promotion_features(df)

    # Step 6, 12-14: Inventory & Shelf Life (Groups D & P)
    print("  [5/10] Adding Inventory & Shelf-Life Intelligence (Groups D & P)...")
    df = add_inventory_features(df)

    # Step 9-11: Demand Intelligence (Groups I, J, K)
    print("  [6/10] Adding Demand Intelligence: Momentum, Volatility, Regime (Groups I, J, K)...")
    df = add_demand_intelligence(df)

    # Step 15: Reconciliation & Data Quality (Group L)
    print("  [7/10] Adding Reconciliation & Quality Intelligence (Group L)...")
    df = add_reconciliation_features(df)

    # Step 16: Financial Exposure (Group M)
    print("  [8/10] Adding Financial Exposure Features (Group M)...")
    df = add_financial_features(df)

    # Step 18: Supplier Exposure (Group N)
    print("  [9/10] Adding Supplier Exposure Features (Group N)...")
    df = add_supplier_features(df)

    # Step 17: Cross-Store Rebalancing Signals (Group O)
    print("  [10/10] Adding Cross-Store Rebalancing Signals (Group O)...")
    df = add_cross_store_features(df)

    # Step 20: Interaction Features
    df = add_interaction_features(df)

    # Step 21: Target Creation
    print("  Calculating Target Variables (next_7_day_demand, stockout_flag)...")
    df = compute_targets(df)

    # Final sort and verification
    df = df.sort_values(["store_id", "product_id", "date"]).reset_index(drop=True)

    # Save final feature datasets
    print(">>> Saving Feature Datasets...")
    master_out = FEATURES_DIR / "feature_master.csv"
    demand_out = FEATURES_DIR / "demand_features.csv"
    stockout_out = FEATURES_DIR / "stockout_features.csv"

    df.to_csv(master_out, index=False)
    print(f"  Saved master feature dataset: {master_out.name} ({len(df):,} rows x {len(df.columns)} columns)")

    # Demand dataset: rows with valid next_7_day_demand target
    demand_df = df[df["next_7_day_demand"].notna()].copy()
    demand_df.to_csv(demand_out, index=False)
    print(f"  Saved demand forecasting dataset: {demand_out.name} ({len(demand_df):,} rows x {len(demand_df.columns)} columns)")

    # Stockout dataset: rows with valid stockout_flag target (inventory observed)
    stockout_df = df[df["stockout_flag"].notna()].copy()
    stockout_df.to_csv(stockout_out, index=False)
    print(f"  Saved stockout classification dataset: {stockout_out.name} ({len(stockout_df):,} rows x {len(stockout_df.columns)} columns)")

    return df


if __name__ == "__main__":
    build_feature_pipeline()
