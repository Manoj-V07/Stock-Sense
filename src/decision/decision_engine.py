from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
FEATURES_PATH = ROOT / "data" / "processed" / "features" / "feature_master.csv"
PREDICTIONS_PATH = ROOT / "reports" / "final_prediction_table.csv"
DECISION_OUTPUT = ROOT / "data" / "processed" / "decision_recommendations.csv"
REPORT_OUTPUT = ROOT / "reports" / "decision_recommendations_summary.md"

RISK_THRESHOLDS = {"HIGH": 0.70, "MEDIUM": 0.40}


def risk_level_from_probability(probability: float) -> str:
    """Map a probability to the challenge's required operational risk bands."""
    p = float(probability) if pd.notna(probability) else 0.0
    if p >= RISK_THRESHOLDS["HIGH"]:
        return "HIGH"
    if p >= RISK_THRESHOLDS["MEDIUM"]:
        return "MEDIUM"
    return "LOW"


def _safe_numeric(series: pd.Series | Iterable[object] | None, default: float = 0.0) -> pd.Series:
    if series is None:
        return pd.Series([default] * 1, dtype=float)
    return pd.to_numeric(series, errors="coerce").fillna(default)


def _safety_stock_value(row: pd.Series) -> float:
    lead_days = _safe_numeric(pd.Series([row.get("lead_days")]), default=0.0).iloc[0]
    daily_demand = _safe_numeric(pd.Series([row.get("rolling_mean_7")]), default=0.0).iloc[0]
    if daily_demand == 0:
        daily_demand = _safe_numeric(pd.Series([row.get("mean_daily_demand")]), default=0.0).iloc[0]
    volatility = _safe_numeric(pd.Series([row.get("demand_cv_7")]), default=0.0).iloc[0]
    safety_stock = lead_days * max(daily_demand, 0.0) * (0.5 + min(max(volatility, 0.0), 1.5) * 0.25)
    return float(max(safety_stock, 0.0))


def compute_reorder_quantity(df: pd.DataFrame) -> pd.Series:
    """Compute reorder quantity using the required formula: max(0, Recommended Stock - Current Stock - Incoming Stock)."""
    frame = df.copy()

    if "predicted_7_day_demand" in frame.columns:
        forecast_demand = pd.to_numeric(frame["predicted_7_day_demand"], errors="coerce")
    elif "forecast_demand" in frame.columns:
        forecast_demand = pd.to_numeric(frame["forecast_demand"], errors="coerce")
    else:
        forecast_demand = pd.Series(0.0, index=frame.index)

    if "next_7_day_demand" in frame.columns:
        forecast_demand = forecast_demand.fillna(
            pd.to_numeric(frame["next_7_day_demand"], errors="coerce").fillna(0.0)
        )
    else:
        forecast_demand = forecast_demand.fillna(0.0)

    if "safety_stock" in frame.columns:
        safety_stock = pd.to_numeric(frame["safety_stock"], errors="coerce")
    else:
        safety_stock = frame.apply(lambda row: _safety_stock_value(row), axis=1)

    recommended_stock = forecast_demand.fillna(0.0) + safety_stock.fillna(0.0)
    current_stock = pd.to_numeric(frame.get("closing"), errors="coerce").fillna(0.0)
    incoming_stock = pd.to_numeric(frame.get("received"), errors="coerce").fillna(0.0)

    frame["forecast_demand"] = forecast_demand
    frame["safety_stock"] = safety_stock
    frame["recommended_stock"] = recommended_stock
    frame["current_stock"] = current_stock
    frame["incoming_stock"] = incoming_stock
    frame["reorder_quantity"] = np.maximum(0.0, recommended_stock - current_stock - incoming_stock)
    return frame["reorder_quantity"]


def _lead_time_feasible(days_to_stockout: float, lead_days: float) -> str:
    if pd.isna(days_to_stockout) or pd.isna(lead_days):
        return "UNKNOWN"
    return "YES" if float(days_to_stockout) >= float(lead_days) else "NO"


def _manager_action(row: pd.Series) -> str:
    risk = row.get("risk_level", "LOW")
    transfer = bool(row.get("transfer_candidate", False))
    lead_ready = row.get("lead_time_feasible", "UNKNOWN")
    shelf_exposure = bool(row.get("high_shelf_life_exposure_flag", 0) == 1 or row.get("shelf_life_exposure_ratio", 0) > 1.0)
    reorder_qty = float(row.get("reorder_quantity", 0.0) or 0.0)

    if transfer and risk in {"HIGH", "MEDIUM"}:
        return "TRANSFER FROM ANOTHER STORE"
    if risk == "HIGH":
        if lead_ready == "NO":
            return "URGENT REORDER"
        return "REORDER"
    if risk == "MEDIUM":
        if lead_ready == "NO":
            return "MONITOR"
        return "MONITOR"
    if shelf_exposure and reorder_qty <= 0:
        return "REDUCE / HOLD REORDER"
    return "NO ACTION"


def _manager_recommendation(row: pd.Series) -> str:
    risk = row.get("risk_level", "LOW")
    forecast = float(row.get("predicted_7_day_demand") or 0.0)
    probability = float(row.get("stockout_probability") or 0.0)
    reorder_qty = float(row.get("reorder_quantity") or 0.0)
    lead_ready = row.get("lead_time_feasible", "UNKNOWN")
    transfer = bool(row.get("transfer_candidate", False))
    shelf_exposure = bool(row.get("high_shelf_life_exposure_flag", 0) == 1 or row.get("shelf_life_exposure_ratio", 0) > 1.0)

    reasons = [
        f"forecast demand of {forecast:.1f} units",
        f"stock-out probability {probability:.2f} ({risk})",
    ]
    if reorder_qty > 0:
        reasons.append(f"recommended reorder of {reorder_qty:.1f} units")
    if lead_ready == "NO":
        reasons.append("supplier lead time exceeds the depletion window")
    if transfer:
        reasons.append("another store has excess stock to transfer")
    if shelf_exposure:
        reasons.append("shelf-life exposure is elevated")

    if risk == "HIGH":
        return "Urgent replenishment is warranted because " + "; ".join(reasons) + "."
    if risk == "MEDIUM":
        return "Monitor this SKU closely because " + "; ".join(reasons) + "."
    if shelf_exposure:
        return "Hold or reduce orders because " + "; ".join(reasons) + "."
    return "No immediate intervention needed because " + "; ".join(reasons) + "."


def build_decision_table() -> pd.DataFrame:
    """Build the final decision matrix from the Phase 4 prediction dataset and Phase 3 feature master."""
    feature_df = pd.read_csv(FEATURES_PATH, parse_dates=["date"]).copy()
    prediction_df = pd.read_csv(PREDICTIONS_PATH, parse_dates=["date"]).copy()

    if feature_df.empty:
        raise FileNotFoundError(f"Feature master not found: {FEATURES_PATH}")
    if prediction_df.empty:
        raise FileNotFoundError(f"Prediction table not found: {PREDICTIONS_PATH}")

    merge_columns = ["date", "store_id", "product_id"]
    decision_df = prediction_df.merge(
        feature_df[[
            "date",
            "store_id",
            "product_id",
            "closing",
            "received",
            "reorder_lvl",
            "lead_days",
            "days_to_stockout",
            "lead_time_gap",
            "shelf_life_exposure_ratio",
            "high_shelf_life_exposure_flag",
            "potential_revenue_exposure",
            "potential_margin_exposure",
            "inventory_value",
            "supplier_id",
            "network_product_mean_inventory",
            "store_relative_inventory_ratio",
            "rolling_mean_7",
            "mean_daily_demand",
            "demand_cv_7",
            "stockout_exposure_value",
            "inventory_balance_gap",
        ]],
        on=merge_columns,
        how="left",
        suffixes=("", "_feature"),
    )

    decision_df["stockout_probability"] = pd.to_numeric(decision_df.get("stockout_probability"), errors="coerce")
    decision_df["stockout_probability"] = decision_df["stockout_probability"].fillna(
        pd.to_numeric(decision_df.get("actual_stockout_flag"), errors="coerce").fillna(0.0)
    )
    decision_df["risk_level"] = decision_df["stockout_probability"].apply(risk_level_from_probability)

    decision_df["predicted_7_day_demand"] = pd.to_numeric(decision_df.get("predicted_7_day_demand"), errors="coerce").fillna(
        pd.to_numeric(decision_df.get("actual_demand"), errors="coerce").fillna(0.0)
    )

    decision_df["daily_rate"] = pd.to_numeric(decision_df.get("rolling_mean_7"), errors="coerce").fillna(
        pd.to_numeric(decision_df.get("mean_daily_demand"), errors="coerce").fillna(0.0)
    )
    fallback_days_to_stockout = pd.Series(
        np.where(
            decision_df["closing"].notna() & (decision_df["closing"] > 0) & (decision_df["daily_rate"] > 0),
            (decision_df["closing"] / decision_df["daily_rate"]).clip(lower=0, upper=365),
            np.nan,
        ),
        index=decision_df.index,
    )
    decision_df["days_to_stockout"] = pd.to_numeric(decision_df.get("days_to_stockout"), errors="coerce").fillna(
        fallback_days_to_stockout
    )
    decision_df["safety_stock"] = decision_df.apply(_safety_stock_value, axis=1)
    decision_df["recommended_stock"] = decision_df["predicted_7_day_demand"] + decision_df["safety_stock"]
    decision_df["reorder_quantity"] = np.maximum(
        0.0,
        decision_df["recommended_stock"] - pd.to_numeric(decision_df["closing"], errors="coerce").fillna(0.0) - pd.to_numeric(decision_df["received"], errors="coerce").fillna(0.0),
    )

    decision_df["lead_time_feasible"] = decision_df.apply(
        lambda row: _lead_time_feasible(row.get("days_to_stockout"), row.get("lead_days")),
        axis=1,
    )
    decision_df["revenue_at_risk"] = pd.to_numeric(decision_df.get("potential_revenue_exposure"), errors="coerce").fillna(0.0) * decision_df["stockout_probability"].fillna(0.0)
    decision_df["margin_at_risk"] = pd.to_numeric(decision_df.get("potential_margin_exposure"), errors="coerce").fillna(0.0) * decision_df["stockout_probability"].fillna(0.0)

    decision_df["transfer_candidate"] = (
        pd.to_numeric(decision_df.get("network_product_mean_inventory"), errors="coerce").fillna(0.0)
        > pd.to_numeric(decision_df.get("closing"), errors="coerce").fillna(0.0)
    ) & (decision_df["reorder_quantity"] > 0)

    decision_df["action"] = decision_df.apply(_manager_action, axis=1)
    decision_df["manager_recommendation"] = decision_df.apply(_manager_recommendation, axis=1)

    output_columns = [
        "date",
        "store_id",
        "product_id",
        "supplier_id",
        "closing",
        "received",
        "reorder_lvl",
        "lead_days",
        "days_to_stockout",
        "lead_time_feasible",
        "predicted_7_day_demand",
        "safety_stock",
        "recommended_stock",
        "reorder_quantity",
        "stockout_probability",
        "risk_level",
        "prediction_reliability",
        "revenue_at_risk",
        "margin_at_risk",
        "transfer_candidate",
        "high_shelf_life_exposure_flag",
        "shelf_life_exposure_ratio",
        "action",
        "manager_recommendation",
    ]
    decision_df = decision_df[output_columns]
    decision_df = decision_df.sort_values(["date", "store_id", "product_id"]).reset_index(drop=True)
    decision_df.to_csv(DECISION_OUTPUT, index=False)

    summary = _build_summary(decision_df)
    REPORT_OUTPUT.write_text(summary, encoding="utf-8")
    return decision_df


def _build_summary(decision_df: pd.DataFrame) -> str:
    high_risk = decision_df[decision_df["risk_level"] == "HIGH"].copy()
    medium_risk = decision_df[decision_df["risk_level"] == "MEDIUM"].copy()
    low_risk = decision_df[decision_df["risk_level"] == "LOW"].copy()

    total_reorder = float(decision_df["reorder_quantity"].sum())
    high_risk_count = int(len(high_risk))
    medium_risk_count = int(len(medium_risk))
    urgent_reorders = int((decision_df["action"] == "URGENT REORDER").sum())
    transfers = int((decision_df["action"] == "TRANSFER FROM ANOTHER STORE").sum())
    reduce_hold = int((decision_df["action"] == "REDUCE / HOLD REORDER").sum())

    risk_counts = (
        decision_df["risk_level"].value_counts().rename_axis("risk_level").reset_index(name="count")
    )
    risk_counts["risk_level"] = risk_counts["risk_level"].astype(str)

    top_examples = decision_df.nlargest(5, "reorder_quantity")[[
        "store_id",
        "product_id",
        "risk_level",
        "predicted_7_day_demand",
        "reorder_quantity",
        "action",
    ]]

    risk_table = risk_counts.to_string(index=False)
    example_table = top_examples.to_string(index=False)

    return f"# Decision Intelligence Summary\n\n" \
        f"## Operating risk overview\n\n" \
        f"- Total recommended reorder quantity: {total_reorder:,.1f} units\n" \
        f"- High-risk store-product rows: {high_risk_count}\n" \
        f"- Medium-risk store-product rows: {medium_risk_count}\n" \
        f"- Low-risk store-product rows: {len(low_risk)}\n" \
        f"- Urgent reorder actions: {urgent_reorders}\n" \
        f"- Transfer candidates: {transfers}\n" \
        f"- Hold/reduce reorder actions: {reduce_hold}\n\n" \
        f"## Risk counts\n\n{risk_table}\n\n" \
        f"## Priority action examples\n\n{example_table}\n"


if __name__ == "__main__":
    build_decision_table()
