"""StockSense Phase 3: Supplier Exposure Features (Group N)."""
import pandas as pd
import numpy as np


def add_supplier_features(df: pd.DataFrame) -> pd.DataFrame:
    """Compute leakage-safe supplier operational concentration and lead-time characteristics.

    Features generated:
    - supplier_product_count: Total unique products sourced from this supplier
    - supplier_avg_lead_time: Mean lead time (days) for this supplier's product catalog
    - supplier_lead_time_std: Lead time variability across supplier catalog
    - supplier_dependency: Ratio of supplier products to total category products

    Leakage Prevention:
    - Computed strictly from static catalog master attributes available prior to prediction.
    - No future stockouts or future fulfillment statistics are used.
    """
    df = df.copy()

    # Base reference slice of products catalog
    prod_ref = df[["product_id", "category", "supplier_id", "lead_days"]].drop_duplicates(
        subset=["product_id"]
    ).copy()
    prod_ref["lead_days"] = pd.to_numeric(prod_ref["lead_days"], errors="coerce")

    # Supplier catalog aggregations
    supp_stats = prod_ref.groupby("supplier_id").agg(
        supplier_product_count=("product_id", "nunique"),
        supplier_avg_lead_time=("lead_days", "mean"),
        supplier_lead_time_std=("lead_days", lambda s: s.std(ddof=1) if len(s) > 1 else 0.0)
    ).reset_index()

    # Category concentration
    cat_counts = prod_ref.groupby("category")["product_id"].nunique().rename("cat_total_products")
    supp_cat = prod_ref.groupby(["supplier_id", "category"])["product_id"].nunique().rename("supp_cat_products").reset_index()
    supp_cat = supp_cat.merge(cat_counts, on="category", how="left")
    supp_cat["supplier_dependency"] = supp_cat["supp_cat_products"] / supp_cat["cat_total_products"]

    # Merge supplier aggregations onto dataset
    df = df.merge(supp_stats, on="supplier_id", how="left")
    df = df.merge(
        supp_cat[["supplier_id", "category", "supplier_dependency"]],
        on=["supplier_id", "category"],
        how="left"
    )

    global_median_lead = prod_ref["lead_days"].median()
    df["supplier_product_count"] = df["supplier_product_count"].fillna(1).astype(int)
    df["supplier_avg_lead_time"] = df["supplier_avg_lead_time"].fillna(df["lead_days"]).fillna(global_median_lead)
    df["supplier_lead_time_std"] = df["supplier_lead_time_std"].fillna(0.0)
    df["supplier_dependency"] = df["supplier_dependency"].fillna(0.0)

    return df
