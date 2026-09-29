"""StockSense Phase 2: reproducible EDA, statistical evidence, and hypotheses."""
from pathlib import Path
import warnings

import numpy as np
import pandas as pd
from scipy import stats

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

warnings.filterwarnings("ignore")
sns.set_theme(style="whitegrid", context="notebook")

ROOT = Path(__file__).resolve().parents[1]
MASTER_PATH = ROOT / "data" / "processed" / "master_dataset.csv"
REC_PATH = ROOT / "data" / "processed" / "tx_inv_reconciliation.csv"
TABLE_DIR = ROOT / "data" / "processed" / "eda_summary_tables"
PLOT_DIR = TABLE_DIR / "plots"
REPORT_DIR = ROOT / "reports"
TABLE_DIR.mkdir(parents=True, exist_ok=True)
PLOT_DIR.mkdir(parents=True, exist_ok=True)


def save_table(df, name):
    df.to_csv(TABLE_DIR / name, index=False)


def safe_divide(num, den):
    return np.where(pd.to_numeric(den, errors="coerce") != 0, num / den, np.nan)


def fmt(value, digits=2):
    if pd.isna(value):
        return "NA"
    return f"{value:,.{digits}f}"


def markdown_table(frame):
    headers = list(frame.columns)
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in frame.fillna("").astype(str).itertuples(index=False, name=None):
        lines.append("| " + " | ".join(value.replace("|", "\\|") for value in row) + " |")
    return "\n".join(lines)


def effect_size(a, b):
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    pooled = np.sqrt(((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / (len(a) + len(b) - 2))
    return (a.mean() - b.mean()) / pooled if pooled else np.nan


def write_plot(fig, name):
    fig.tight_layout()
    fig.savefig(PLOT_DIR / name, dpi=150, bbox_inches="tight")
    plt.close(fig)


def main():
    df = pd.read_csv(MASTER_PATH, parse_dates=["date"])
    df = df.sort_values(["store_id", "product_id", "date"]).reset_index(drop=True)
    df["weekday"] = df.date.dt.day_name()
    df["week_no"] = df.date.dt.isocalendar().week.astype(int)
    df["month"] = df.date.dt.month
    df["weekend_flag"] = df.date.dt.dayofweek >= 5
    df["stockout_observed"] = df.closing.notna() & (df.closing <= 0)
    df["inventory_observed"] = df.closing.notna()
    df["stockout_event"] = df["stockout_observed"].where(df["inventory_observed"])
    df["inventory_value"] = df.closing * df.cost_price
    df["cogs"] = df.inventory_sold.clip(lower=0) * df.cost_price
    df["daily_demand_rate"] = df["transaction_demand"]
    df["days_of_inventory"] = safe_divide(df.closing, df.daily_demand_rate)
    df["inventory_to_demand_ratio"] = safe_divide(df.closing, df.daily_demand_rate)
    df["days_to_stockout"] = df["days_of_inventory"]
    df["lead_time_gap"] = df["days_of_inventory"] - df.lead_days
    df["shelf_life_exposure_ratio"] = safe_divide(df.days_of_inventory, df.shelf_life_days)
    df["potential_lost_sales_units"] = np.where(df.stockout_observed, df.transaction_demand, np.nan)
    df["potential_lost_revenue"] = df.potential_lost_sales_units * df.avg_selling_price
    df["potential_lost_margin"] = df.potential_lost_sales_units * (df.avg_selling_price - df.cost_price)
    df["realized_margin"] = df.revenue - (df.transaction_demand * df.cost_price)

    # Step 1: readiness, explicitly retaining missing coverage information.
    readiness = pd.DataFrame([
        ["rows", len(df)], ["columns", len(df.columns)], ["date_min", df.date.min()], ["date_max", df.date.max()],
        ["unique_stores", df.store_id.nunique()], ["unique_products", df.product_id.nunique()],
        ["unique_date_store_product", df[["date", "store_id", "product_id"]].drop_duplicates().shape[0]],
        ["duplicate_grains", int(df.duplicated(["date", "store_id", "product_id"]).sum())],
        ["missing_cells", int(df.isna().sum().sum())], ["demand_coverage_rows", int(df.transaction_demand.notna().sum())],
        ["inventory_coverage_rows", int(df.inventory_observed.sum())],
        ["external_coverage_rows", int(df.temp_c.notna().sum())],
        ["categorical_category_levels", df.category.nunique()], ["categorical_store_type_levels", df.store_type.nunique()],
    ], columns=["metric", "value"])
    save_table(readiness, "data_readiness.csv")
    missingness = df.isna().sum().rename("missing_count").reset_index()
    missingness.columns = ["column", "missing_count"]
    save_table(missingness, "missingness.csv")
    for col in ["category", "store_type", "promotion_active", "weekend_flag", "holiday", "festival", "local_event"]:
        save_table(df[col].value_counts(dropna=False).rename("count").reset_index(), f"distribution_{col}.csv")

    # Step 2: baseline KPIs. Inventory turnover is available only where both COGS and inventory value exist.
    inv = df[df.inventory_observed].copy()
    normal = df[df.promotion_active == 0].transaction_demand.sum()
    promoted = df[df.promotion_active == 1].transaction_demand.sum()
    kpis = pd.DataFrame([
        ["Revenue", df.revenue.sum(), "Sum of aggregated transaction revenue"],
        ["Units sold", df.transaction_demand.sum(), "Sum of transaction_demand"],
        ["Stock-out rate", df.stockout_observed.sum() / len(inv) if len(inv) else np.nan, "Observed closing <= 0 / rows with closing inventory"],
        ["Inventory turnover", inv.cogs.sum() / inv.inventory_value.mean() if inv.inventory_value.mean() > 0 else np.nan, "COGS using inventory_sold x cost / mean closing inventory value; inventory rows only"],
        ["Days of inventory", inv.days_of_inventory.replace([np.inf, -np.inf], np.nan).mean(), "Closing stock / same-row transaction demand; positive-demand rows only"],
        ["Promotion lift", (promoted / (df[df.promotion_active == 1].shape[0])) / (normal / (df[df.promotion_active == 0].shape[0])) - 1 if normal and len(df[df.promotion_active == 0]) else np.nan, "Mean row demand promoted vs normal minus 1; association, not causation"],
        ["Estimated lost sales", df.potential_lost_revenue.sum(), "Observed stock-out rows x transaction demand x average selling price; descriptive proxy"],
    ], columns=["kpi", "value", "definition"])
    save_table(kpis, "baseline_kpis.csv")

    # Category, store, time and promotion summaries.
    cat = df.groupby("category", as_index=False).agg(revenue=("revenue", "sum"), units_sold=("transaction_demand", "sum"), observations=("date", "size"))
    cat["revenue_share"] = cat.revenue / cat.revenue.sum()
    cat = cat.sort_values("revenue", ascending=False)
    cat["cumulative_revenue_share"] = cat.revenue_share.cumsum()
    save_table(cat, "category_revenue_pareto.csv")
    store = df.groupby(["store_id", "store_type"], as_index=False).agg(revenue=("revenue", "sum"), units_sold=("transaction_demand", "sum"), observations=("date", "size"), stockout_rate=("stockout_event", "mean"), average_inventory=("closing", "mean"), demand_volatility=("transaction_demand", "std"))
    save_table(store, "store_performance.csv")
    daily_store = df.groupby(["date", "store_id"], as_index=False).agg(demand=("transaction_demand", "sum"), revenue=("revenue", "sum"), stockouts=("stockout_observed", "sum"))
    save_table(daily_store, "daily_store_trend.csv")
    weekly = df.assign(week=df.date.dt.to_period("W").astype(str)).groupby(["week", "store_id"], as_index=False).agg(demand=("transaction_demand", "sum"), revenue=("revenue", "sum"))
    save_table(weekly, "weekly_store_trend.csv")
    promo = df.groupby("promotion_active", as_index=False).agg(mean_demand=("transaction_demand", "mean"), total_demand=("transaction_demand", "sum"), mean_revenue=("revenue", "mean"), observations=("date", "size"), stockout_rate=("stockout_event", "mean"), mean_discount=("avg_discount_pct", "mean"))
    save_table(promo, "promotion_summary.csv")
    promo_cat = df.groupby(["category", "promotion_active"], as_index=False).agg(mean_demand=("transaction_demand", "mean"), mean_revenue=("revenue", "mean"), observations=("date", "size"))
    pivot = promo_cat.pivot(index="category", columns="promotion_active", values="mean_demand").rename(columns={0: "normal_mean_demand", 1: "promoted_mean_demand"})
    pivot["promotion_lift"] = pivot.promoted_mean_demand / pivot.normal_mean_demand - 1
    save_table(pivot.reset_index(), "promotion_lift_by_category.csv")
    save_table(df.groupby(["weekend_flag", "category"], as_index=False).agg(mean_demand=("transaction_demand", "mean"), total_demand=("transaction_demand", "sum"), observations=("date", "size")), "weekend_category.csv")
    save_table(df.groupby(["weekend_flag", "store_id"], as_index=False).agg(mean_demand=("transaction_demand", "mean"), total_demand=("transaction_demand", "sum"), observations=("date", "size")), "weekend_store.csv")
    save_table(df.groupby("weekday", as_index=False).agg(mean_demand=("transaction_demand", "mean"), total_demand=("transaction_demand", "sum"), observations=("date", "size")), "weekday_summary.csv")

    # Volatility and regime evidence at Store x Product grain.
    def volatility(group):
        demand = group.transaction_demand.fillna(0)
        mean = demand.mean()
        return pd.Series({"mean_demand": mean, "median_demand": demand.median(), "demand_std": demand.std(ddof=1), "demand_cv": demand.std(ddof=1) / mean if mean else np.nan, "zero_demand_ratio": (demand == 0).mean(), "demand_range": demand.max() - demand.min(), "observations": len(demand), "rolling_std_7_last": demand.rolling(7, min_periods=3).std().iloc[-1]})
    volatility_table = df.groupby(["store_id", "product_id"], group_keys=False).apply(volatility).reset_index()
    volatility_table["intermittent_demand_flag"] = ((volatility_table.zero_demand_ratio >= 0.5) & (volatility_table.mean_demand > 0)).astype(int)
    volatility_table["volatility_band"] = pd.cut(volatility_table.demand_cv, [-np.inf, .5, 1.0, np.inf], labels=["stable", "moderate", "high"])
    save_table(volatility_table, "store_product_volatility.csv")

    # Momentum uses trailing observed daily windows and never looks beyond the row's date.
    def momentum(group):
        s = group.set_index("date").transaction_demand.resample("D").sum().fillna(0)
        recent = s.tail(7).sum()
        previous = s.iloc[-14:-7].sum() if len(s) >= 14 else np.nan
        return pd.Series({"recent_7_day_demand": recent, "previous_7_day_demand": previous, "demand_momentum_ratio": recent / previous if previous and not pd.isna(previous) else np.nan, "demand_change_percentage": (recent / previous - 1) * 100 if previous and not pd.isna(previous) else np.nan, "history_days": len(s)})
    momentum_table = df.groupby(["store_id", "product_id"], group_keys=False).apply(momentum).reset_index()
    momentum_table["momentum_regime"] = pd.cut(momentum_table.demand_momentum_ratio, [-np.inf, .8, 1.2, np.inf], labels=["declining", "stable", "accelerating"])
    save_table(momentum_table, "demand_momentum.csv")

    # Inventory, stock-out, shelf-life, supplier, cross-store and financial summaries.
    inv["low_stock_flag"] = inv.closing <= inv.reorder_lvl
    inv["excess_coverage_flag"] = inv.shelf_life_exposure_ratio > 1
    save_table(df.groupby(["store_id", "category"], as_index=False).agg(stockout_rate=("stockout_event", "mean"), stockout_events=("stockout_event", "sum"), observations=("date", "size")), "stockout_store_category.csv")
    save_table(df.groupby("category", as_index=False).agg(stockout_rate=("stockout_event", "mean"), stockout_events=("stockout_event", "sum"), observations=("date", "size")), "stockout_category.csv")
    save_table(df.groupby("supplier_id", as_index=False).agg(products=("product_id", "nunique"), mean_lead_days=("lead_days", "mean"), stockout_rate=("stockout_event", "mean"), inventory_value=("inventory_value", "sum"), observations=("date", "size")), "supplier_exposure.csv")
    save_table(df.groupby(["store_id", "product_id"], as_index=False).agg(mean_demand=("transaction_demand", "mean"), mean_inventory=("closing", "mean"), stockout_rate=("stockout_event", "mean"), inventory_value=("inventory_value", "mean"), category=("category", "first")), "store_product_cross_store.csv")
    save_table(df.groupby("lead_days", as_index=False).agg(stockout_rate=("stockout_event", "mean"), mean_days_inventory=("days_of_inventory", "mean"), mean_demand=("transaction_demand", "mean"), observations=("date", "size")), "lead_time_stockout.csv")
    save_table(df.groupby("date", as_index=False).agg(stockouts=("stockout_event", "sum"), stockout_rate=("stockout_event", "mean"), demand=("transaction_demand", "sum")), "stockout_temporal.csv")
    save_table(df.groupby("reconciliation_status", dropna=False, as_index=False).agg(observations=("date", "size"), mean_gap=("inventory_demand_gap", "mean"), abs_gap=("inventory_demand_gap", lambda x: x.abs().mean())), "reconciliation_summary.csv")
    external = []
    for col in ["temp_c", "rain_mm", "holiday", "festival", "weekend", "local_event", "avg_discount_pct", "avg_selling_price", "closing", "lead_days", "cost_price", "shelf_life_days"]:
        valid = df[[col, "transaction_demand", "stockout_observed"]].dropna()
        external.append([col, len(valid), valid[col].corr(valid.transaction_demand, method="spearman"), valid[col].corr(valid.stockout_observed.astype(float), method="spearman")])
    save_table(pd.DataFrame(external, columns=["variable", "n", "spearman_demand", "spearman_stockout"]), "external_numeric_relationships.csv")

    # Required formal tests with assumptions and business interpretation documented below.
    normal = df.loc[df.promotion_active == 0, "transaction_demand"].dropna()
    promoted = df.loc[df.promotion_active == 1, "transaction_demand"].dropna()
    promo_test = stats.mannwhitneyu(promoted, normal, alternative="two-sided")
    groups = [g.transaction_demand.dropna().values for _, g in df.groupby("store_type")]
    store_test = stats.kruskal(*groups)
    test_rows = df[df.inventory_observed].copy()
    contingency = pd.crosstab(test_rows.promotion_active, test_rows.stockout_observed)
    chi_test = stats.chi2_contingency(contingency)
    tests = pd.DataFrame([
        ["Promotion and demand", "Promotion does not change demand distributions", "Promotion changes demand distributions", "Mann-Whitney U", promo_test.statistic, promo_test.pvalue, effect_size(promoted, normal), "Reject" if promo_test.pvalue < .05 else "Do not reject", "Independent observations; ordinal/rank test; distributions need not be normal", "All observed rows with valid demand", "Association is statistically assessed; confounding by product, store, timing remains"],
        ["Mean demand across store types", "Demand distributions are equal across store types", "At least one store type differs", "Kruskal-Wallis", store_test.statistic, store_test.pvalue, np.nan, "Reject" if store_test.pvalue < .05 else "Do not reject", "Independent groups; rank-based test; similar distribution shape is desirable", "All observed rows grouped by store_type", "A significant result identifies a difference, not its cause"],
        ["Promotion status and stock-out frequency", "Promotion and stock-out status are independent", "They are associated", "Chi-square independence", chi_test[0], chi_test[1], np.nan, "Reject" if chi_test[1] < .05 else "Do not reject", "Expected cell counts should be adequate; rows independent", "Rows with observed closing inventory", "Stock-out observations may be affected by assortment and missing inventory coverage"],
    ], columns=["business_question", "h0", "h1", "test", "statistic", "p_value", "effect_size", "decision", "assumptions", "sample_definition", "limitations"])
    save_table(tests, "statistical_tests.csv")

    # High-signal charts: each title is a business question.
    fig, ax = plt.subplots(figsize=(9, 5)); sns.barplot(data=cat, x="revenue", y="category", ax=ax, color="#176b87"); ax.set(title="Which categories generate the most revenue?", xlabel="Revenue", ylabel="Category"); write_plot(fig, "revenue_by_category.png")
    fig, ax = plt.subplots(figsize=(10, 5)); sns.lineplot(data=daily_store, x="date", y="demand", hue="store_id", marker="o", ax=ax); ax.set(title="Which stores are growing or declining in daily demand?", xlabel="Date", ylabel="Units sold"); write_plot(fig, "daily_store_demand.png")
    fig, ax = plt.subplots(figsize=(7, 5)); sns.boxplot(data=df, x="promotion_active", y="transaction_demand", ax=ax); ax.set(title="Do promoted observations have different demand?", xlabel="Promotion active (0=no, 1=yes)", ylabel="Units sold"); write_plot(fig, "promotion_demand.png")
    fig, ax = plt.subplots(figsize=(7, 5)); sns.barplot(data=promo, x="promotion_active", y="stockout_rate", ax=ax, color="#d95f59"); ax.set(title="Is observed stock-out frequency different during promotions?", xlabel="Promotion active", ylabel="Stock-out rate"); write_plot(fig, "promotion_stockout.png")
    heat = df.pivot_table(index="store_id", columns="category", values="stockout_observed", aggfunc="mean"); fig, ax = plt.subplots(figsize=(10, 5)); sns.heatmap(heat, annot=True, fmt=".1%", cmap="YlOrRd", ax=ax); ax.set(title="Where do stock-outs repeat by store and category?", xlabel="Category", ylabel="Store"); write_plot(fig, "stockout_store_category_heatmap.png")
    fig, ax = plt.subplots(figsize=(8, 5)); sns.scatterplot(data=volatility_table, x="mean_demand", y="demand_cv", hue="volatility_band", ax=ax); ax.set(title="Which Store x Product combinations are volatile?", xlabel="Mean daily demand", ylabel="Coefficient of variation"); write_plot(fig, "demand_volatility.png")

    write_reports(df, kpis, cat, store, promo, volatility_table, momentum_table, tests, readiness)
    print(f"Phase 2 complete: {len(df):,} rows, {len(df.columns):,} analytical columns, {len(tests)} statistical tests")


def write_reports(df, kpis, cat, store, promo, volatility, momentum, tests, readiness):
    top_category = cat.iloc[0]
    top_store = store.sort_values("revenue", ascending=False).iloc[0]
    highest_stockout_store = store.sort_values("stockout_rate", ascending=False).iloc[0]
    high_vol = volatility.sort_values("demand_cv", ascending=False).head(5)
    accelerating = momentum[momentum.momentum_regime == "accelerating"]
    kpi_text = "\n".join(f"| {r.kpi} | {fmt(r.value, 4)} | {r.definition} |" for r in kpis.itertuples())
    test_text = "\n".join(f"### {r.business_question}\n- **H0:** {r.h0}\n- **H1:** {r.h1}\n- **Test:** {r.test}; statistic={fmt(r.statistic, 4)}, p-value={r.p_value:.4g}; effect size={fmt(r.effect_size, 4)}\n- **Decision:** {r.decision}.\n- **Assumptions/sample:** {r.assumptions}; {r.sample_definition}.\n- **Interpretation/limitation:** {r.limitations}." for r in tests.itertuples())
    insights = f"""# StockSense Phase 2 Business Insights

## Executive Summary
- **Revenue:** {top_category.category} has the highest observed revenue contribution ({top_category.revenue_share:.1%}); {top_store.store_id} has the highest observed store revenue.
- **Demand:** Demand is observed at {len(df):,} date-store-product rows. The highest-volume category is {cat.sort_values('units_sold', ascending=False).iloc[0].category}.
- **Stores:** {highest_stockout_store.store_id} has the highest observed stock-out rate among stores with inventory observations; this is descriptive, not an arbitrary composite rank.
- **Promotion:** Promoted and normal observations are compared by rank test; the result is association, not causal uplift.
- **Weekend:** Weekend effects are stored by category and store in `weekend_category.csv` and `weekend_store.csv`; the short August window limits generalisation.
- **Volatility:** Store-product volatility is retained as signal; the highest-CV combinations are in `store_product_volatility.csv`.
- **Inventory/shelf-life:** Coverage and shelf-life exposure are only interpretable where closing inventory and positive demand are available. `shelf_life_exposure_ratio > 1` means projected coverage exceeds shelf life, not that expiry occurred.
- **Momentum:** {len(accelerating)} combinations are classified as accelerating under the exploratory 7-day ratio thresholds; this is a hypothesis for Phase 3, not a production feature.
- **Lead time:** `lead_time_stockout.csv` compares lead days, coverage, demand, and stock-outs without causal claims.
- **Financial exposure:** Potential lost revenue is a descriptive stock-out proxy based on observed demand and price; it is not model-based expected loss.
- **Cross-store:** `store_product_cross_store.csv` is the candidate input for rebalancing review; no transfer recommendation is made in Phase 2.
- **Supplier:** `supplier_exposure.csv` describes operational exposure by supplier, not supplier fault.
- **Reconciliation:** `reconciliation_summary.csv` preserves the Phase 1 conclusion that POS demand and inventory sold are different operational signals.
- **External factors:** Spearman associations are in `external_numeric_relationships.csv`; limited history means weak relationships should not be promoted automatically to features.

## KPI Baseline
| KPI | Value | Definition |
|---|---:|---|
{kpi_text}

## Limitations
- The master covers observed combinations rather than a complete calendar; absent rows cannot be treated as zero demand.
- Inventory coverage is incomplete for transaction-only observations, so stock-out and inventory KPIs use valid closing-inventory rows.
- The main history is roughly one month, making momentum, seasonality, and regime evidence provisional.
- Transaction demand and `inventory_sold` are not interchangeable.
- No causal claims, expiry claims, or model-based lost-sales claims are made.
"""
    (REPORT_DIR / "eda_business_insights.md").write_text(insights, encoding="utf-8")
    statistical = f"""# StockSense Phase 2 Statistical Analysis

All tests use alpha = 0.05. Statistical significance is distinct from practical business significance.

{test_text}

## Supporting relationship analysis
Spearman relationships for demand and stock-out status are saved in `data/processed/eda_summary_tables/external_numeric_relationships.csv`. Correlation is descriptive association, not causation; nonlinear effects and confounding remain possible.
"""
    (REPORT_DIR / "statistical_analysis.md").write_text(statistical, encoding="utf-8")
    feature_rows = [
        ("day_of_week / weekend_flag / month / week_no", "Calendar and weekend summaries are available", "Represent recurring time patterns", "Useful for short-horizon demand", "Low, if built from prediction-date calendar", "Available", "Required Phase 3 baseline"),
        ("lag_1 / lag_7 / lag_14 / rolling_mean_7 / rolling_std_7", "Daily Store x Product history supports trailing windows", "Recent demand level and variability", "Core forecast signal", "Must be strictly past-only", "Available after feature construction", "Required Phase 3 baseline"),
        ("days_of_inventory / inventory_to_demand_ratio / reorder_gap", "Coverage varies and low-stock rows exist", "Inventory sufficiency relative to demand", "Supports stock-out risk and action", "Closing stock must be point-in-time", "Available with inventory coverage", "Required Phase 3 with missingness flags"),
        ("promotion_flag / discount_pct / price_change", "Promotion and discount groups differ descriptively and are testable", "Commercial context", "Potential demand adjustment", "Promotion assignment is confounded", "Available", "Required Phase 3, interpret cautiously"),
        ("demand_momentum", "Exploratory recent/previous 7-day ratios classify accelerating, stable, declining", "Recent direction", "May improve short-horizon forecasts", "Requires enough history and past-only windows", "Available for 31-day histories", "Carry forward for validation"),
        ("demand_volatility / demand_cv / rolling_std_7", "CV and rolling dispersion vary materially across Store x Product", "Uncertainty and replenishment sensitivity", "Useful for risk calibration", "Sparse histories make CV unstable", "Available", "Carry forward with minimum-history rule"),
        ("zero_demand_ratio / intermittent_demand_flag", "Sparse and frequent-zero combinations are present", "Intermittent demand behaviour", "Supports specialised forecast handling", "Observed zeros may reflect missing observation coverage", "Available", "Carry forward with coverage caveat"),
        ("demand_regime", "Stable/accelerating/declining bands are exploratory only", "Behavioural segment", "Potential explanation layer", "Thresholds are arbitrary until validated", "Available", "Pilot only; reject as production feature until validated"),
        ("days_to_stockout / lead_time_gap", "Coverage can be compared with lead days", "Replenishment urgency", "Direct decision-support value", "Demand rate and closing stock are noisy", "Available on inventory rows", "Carry forward with guards"),
        ("shelf_life_exposure", "Coverage-to-shelf-life ratio identifies potential exposure", "Risk of holding beyond shelf-life horizon", "Supports rotation review", "Not expiry prediction; positive demand required", "Available for shelf-life products", "Carry forward as exploratory"),
        ("inventory_reconciliation_score", "POS and inventory sold mismatch on most matched observations", "Source reliability/context", "Prevents blind substitution", "Not a demand truth label", "Available", "Carry forward as diagnostic, not target"),
        ("financial_exposure", "Observed stock-out rows imply descriptive lost revenue/margin", "Business consequence", "Prioritises review", "Not expected loss and demand is censored", "Available", "Use for explanation, not target leakage"),
        ("store_product_demand_difference", "Cross-store summary supports demand/inventory comparison", "Potential rebalancing signal", "Could identify transfer candidates", "Requires aligned time and stock quality", "Available", "Carry forward to Phase 5 candidate layer"),
        ("supplier_exposure", "Supplier summaries differ in lead time and stock-out exposure", "Operational concentration", "Supports supplier-risk review", "No causal supplier attribution", "Available", "Use descriptive only"),
        ("customers", "Unique customer counts are available", "Traffic context", "May explain demand variation", "Aggregated count and sparse coverage", "Available as unique_customer_count", "Evaluate in Phase 3"),
        ("temperature / rainfall / events", "External relationships are measured in summary table", "Contextual demand signal", "Unknown until validation", "Limited one-month history and imputation flags", "Available", "Include only if validation supports"),
        ("final dashboard / recommendation engine", "Out of scope for Phase 2", "Not an EDA feature", "None yet", "Would mix phases", "Not applicable", "Rejected for Phase 2"),
    ]
    register = pd.DataFrame(feature_rows, columns=["feature", "evidence_in_eda", "business_meaning", "expected_usefulness", "potential_leakage_risk", "data_availability", "recommendation_phase_3"])
    register.to_csv(TABLE_DIR / "feature_hypothesis_register.csv", index=False)
    (REPORT_DIR / "feature_hypothesis_register.md").write_text("# StockSense Phase 2 Feature Hypothesis Register\n\n" + markdown_table(register) + "\n\nFeatures rejected or deferred are explicitly marked in the recommendation column; no candidate is automatically implemented here.\n", encoding="utf-8")


if __name__ == "__main__":
    main()