# STOCKSENSE --- 6-PHASE PROJECT PLAN

## Table of Contents

1.  [Phase 1 --- Data Understanding, Quality Audit & Data
    Integration](#phase-1--data-understanding-quality-audit--data-integration)
2.  [Phase 2 --- EDA, Statistical Analysis & Business
    Intelligence](#phase-2--eda-statistical-analysis--business-intelligence)
3.  [Phase 3 --- Feature Engineering & Demand
    Intelligence](#phase-3--feature-engineering--demand-intelligence)
4.  [Phase 4 --- Machine Learning, Validation &
    Explainability](#phase-4--machine-learning-validation--explainability)
5.  [Phase 5 --- Decision Intelligence & Recommendation
    Engine](#phase-5--decision-intelligence--recommendation-engine)
6.  [Phase 6 --- Management Dashboard, Prototype, Testing & Final
    Pitch](#phase-6--management-dashboard-prototype-testing--final-pitch)
7.  [Final System Architecture](#final-system-architecture)
8.  [Deliverables at the End](#deliverables-at-the-end)

------------------------------------------------------------------------

## Phase 1 --- Data Understanding, Quality Audit & Data Integration

### Objective

Understand every raw dataset, identify every quality issue, preserve the
raw data, clean/reconcile the sources, and produce the master analytical
dataset at:

> **ONE ROW = ONE DATE × ONE STORE × ONE PRODUCT**

This is explicitly required by the challenge.

### Datasets

We have:

-   `transactions.csv`
-   `products.csv`
-   `stores.csv`
-   `inventory.csv`
-   `external_factors.csv`

The transaction data contains transaction date, store, product,
quantity, price, discount, promotion, customer, payment mode and hour.

The other datasets provide product, store, inventory and external-factor
information.

### Tasks

#### 1. Dataset profiling

For every CSV:

-   row count
-   column count
-   data types
-   unique values
-   cardinality
-   missing values
-   duplicate rows
-   duplicate IDs
-   date range
-   categorical distributions
-   numerical distributions
-   impossible values
-   foreign-key integrity

#### 2. Data-quality audit

Explicitly investigate all documented traps:

-   Missing temperature/external values
-   Duplicate transactions
-   Duplicate transaction IDs
-   Category inconsistencies
-   Negative/impossible quantities
-   Invalid prices/discounts
-   Invalid IDs
-   Inventory arithmetic mismatch
-   Sparse product histories
-   Missing inventory fields

The challenge specifically requires these checks.

#### 3. Inventory reconciliation

Validate:

    closing = opening + received - sold

Do **not** blindly overwrite values.

Create reconciliation indicators such as:

    inventory_balance_gap
    inventory_consistency_flag

Also compare aggregated transaction demand against inventory movement
rather than silently forcing them to agree.

#### 4. Transaction aggregation

Convert transaction-level data into:

    Date × Store × Product

with appropriate aggregation of:

-   units sold
-   revenue
-   average selling price
-   discount
-   promotion
-   transaction count
-   customer count
-   hourly activity

#### 5. Merge all sources

Merge:

    transactions
            +
    products
            +
    stores
            +
    inventory
            +
    external_factors

into the master analytical dataset.

### Expected outcome

Deliver:

    data/
    ├── raw/
    ├── cleaned/
    ├── processed/
    └── master_dataset.csv

and:

    reports/data_quality_report.md

The Data Quality Report must document:

> issue → count → action → justification

as required by the challenge.

------------------------------------------------------------------------

# Phase 2 --- EDA, Statistical Analysis & Business Intelligence

## Objective

Understand **why demand and stock-outs occur**, not merely produce
charts.

The challenge explicitly says every chart must answer a business
question.

### Required EDA

#### Revenue

-   Revenue by category
-   Revenue by store
-   Revenue by product
-   Pareto analysis

#### Store performance

-   Daily store trend
-   Weekly store trend
-   Growing/declining stores

#### Promotion

-   Promotion vs non-promotion demand
-   Discount vs demand
-   Promotion lift

#### Time

-   Weekday vs weekend
-   Day-of-week behaviour
-   Monthly/weekly patterns

#### Demand volatility

-   Coefficient of variation
-   Rolling standard deviation
-   Volatile products
-   Intermittent-demand products

#### Stock-out analysis

-   Stock-outs by store
-   Stock-outs by category
-   Store × category heatmap
-   Repeated stock-out locations

These directly correspond to the prescribed EDA questions.

### Required statistical analysis

At least **three statistical analyses**.

For every test document:

    Business Question
    H0
    H1
    Statistical Test
    p-value
    Interpretation
    Business implication

Required areas include:

1.  Promotion → sales
2.  Store type → demand
3.  Promotion status → stock-out frequency

These are explicitly specified.

### Our additional intelligence

Start identifying:

#### A. Demand Momentum

Compare recent demand against previous demand windows.

    recent demand
          /
    previous demand

Classify:

-   accelerating
-   stable
-   declining
-   highly volatile
-   intermittent

#### B. Store × Product Behaviour Profiles

Identify combinations such as:

-   stable/high demand
-   volatile/high demand
-   intermittent demand
-   declining demand
-   rapidly accelerating demand

### Expected outcome

Produce:

-   EDA notebook
-   statistical analysis report
-   business insight report
-   demand behaviour classification
-   EDA visualizations

------------------------------------------------------------------------

# Phase 3 --- Feature Engineering & Demand Intelligence

## Objective

Build all mandatory features and then extend them with the unique
features that the dataset supports.

The challenge specifies the following feature groups.

------------------------------------------------------------------------

## Mandatory features

### Time

    day_of_week
    weekend_flag
    month
    week_no
    festival_flag

### Lag

    lag_1
    lag_7
    lag_14

### Rolling

    rolling_mean_7
    rolling_mean_14
    rolling_std_7

### Inventory

    days_of_inventory
    inventory_to_demand_ratio
    reorder_gap

### Price / Promotion

    discount_pct
    price_change
    promotion_flag

### Store / Product

    store_type
    category
    brand
    shelf_life
    lead_time

And enforce the challenge's **no-data-leakage rule**: future information
must never enter a prediction feature.

------------------------------------------------------------------------

# Our additional feature layer

This is where your project starts differentiating.

### 1. Demand Momentum Index

Measure whether demand is accelerating or declining.

### 2. Demand Regime

Classify:

    Stable
    Accelerating
    Declining
    Volatile
    Intermittent

### 3. Days-to-Stockout

    current_stock / predicted_daily_demand

### 4. Lead-Time Gap

    days_to_stockout - supplier_lead_time

This answers:

> Can the supplier replenish the product before expected depletion?

### 5. Shelf-Life Exposure

Compare projected inventory coverage with shelf life.

Important: call this an **exposure indicator**, not actual expiry
prediction, because there is no batch-age information.

### 6. Inventory Reconciliation Score

Use:

    inventory balance gap
    +
    transaction/inventory discrepancy
    +
    data quality indicators

### 7. Financial Risk Features

Create:

    expected_lost_revenue
    expected_margin_at_risk

using the available selling price and cost price.

### 8. Store-Level Product Availability Features

Measure how the same product behaves across stores.

This creates the foundation for the **inventory transfer/rebalancing
layer**.

------------------------------------------------------------------------

## Expected outcome

A leakage-safe feature dataset containing:

    mandatory features
    +
    demand intelligence
    +
    inventory intelligence
    +
    financial risk
    +
    data reliability signals

------------------------------------------------------------------------

# Phase 4 --- Machine Learning, Validation & Explainability

This phase must satisfy the mandatory modelling requirements.

The challenge requires **two ML problems**.

------------------------------------------------------------------------

## Model 1 --- 7-Day Demand Forecast

### Target

    next_7_day_demand

### Baseline

First create:

    previous_7_day_mean

The challenge explicitly requires a simple baseline before the ML
models.

### Candidate algorithms

Only use the permitted algorithms:

-   Linear Regression
-   Decision Tree
-   SVM
-   XGBoost
-   KNN
-   Random Forest

The challenge's permitted list must be respected; deep learning is not
permitted.

### Validation

Use:

**time-aware train → validation → test**

Never randomly mix future observations into training.

### Metrics

Calculate:

-   MAE
-   RMSE
-   MAPE
-   R²

and explain which metric matters most for the business.

------------------------------------------------------------------------

# Model 2 --- Stock-Out Risk

### Target

    stockout_flag

and produce:

    stockout_probability

### Models

Compare appropriate permitted classification algorithms.

### Required metrics

-   Accuracy
-   Precision
-   Recall
-   F1
-   ROC-AUC
-   Confusion Matrix

Handle class imbalance appropriately.

------------------------------------------------------------------------

# Explainability

This is mandatory.

Use:

-   Feature importance
-   Permutation importance

The system must explain why an item is predicted to be at risk.

Example:

    STORE S01 — MILK

    Stock-out probability: 89%

    Main drivers:
    • Recent demand growth
    • Promotion
    • Weekend approaching
    • Low inventory coverage
    • Festival effect

------------------------------------------------------------------------

# Our additional ML intelligence

### Prediction Reliability

Don't only output:

    Stock-out probability = 89%

Also calculate:

    Prediction reliability

based on things such as:

-   historical coverage
-   demand volatility
-   sparse history
-   missingness
-   reconciliation quality
-   recent model performance

This is **not another prediction target**. It is a trust layer around
the prediction.

### Expected outcome

You should have:

    models/
    ├── demand_model
    ├── stockout_model
    └── preprocessing_pipeline

plus:

    model_comparison.csv
    evaluation_report
    explainability_report

------------------------------------------------------------------------

# Phase 5 --- Decision Intelligence & Recommendation Engine

This is where I would make your project substantially different.

The challenge says:

> **A prediction without an action is not complete.**

The required system must provide:

-   reorder quantity
-   risk level
-   key reasons
-   manager-friendly recommendation.

------------------------------------------------------------------------

## Mandatory risk classification

Use the prescribed thresholds:

    ≥ 0.70 → HIGH
    0.40–0.69 → MEDIUM
    < 0.40 → LOW

as specified in the document.

------------------------------------------------------------------------

## Mandatory reorder calculation

Implement:

    Recommended Stock
    =
    Forecast Demand + Safety Stock

and:

    Reorder Quantity
    =
    max(
        0,
        Recommended Stock
        - Current Stock
        - Incoming Stock
    )

------------------------------------------------------------------------

# Our Decision Intelligence layer

### 1. Financial Risk

Calculate:

    Revenue at Risk
    Margin at Risk

This allows prioritization by financial exposure rather than probability
alone.

### 2. Stock-out Timing

Calculate:

    Expected Days to Stock-out

and compare with:

    Supplier Lead Time

Result:

    Can replenish before depletion?
    YES / NO

### 3. Overstock / Shelf-Life Intelligence

Identify inventory that may remain unsold relative to shelf life.

### 4. Store-to-Store Rebalancing

Before recommending a new supplier order:

    Does another store have excess stock?
           ↓
    YES → consider transfer
    NO  → supplier replenishment

This is one of the strongest extensions because it changes the
recommendation from simply:

> **"Order more."**

to:

> **"Transfer from another store first."**

### 5. Supplier Risk

Aggregate:

-   products supplied
-   high-risk products
-   lead time
-   inventory exposure

to identify supplier-level operational exposure.

------------------------------------------------------------------------

# Final recommendation engine

For every Store × Product:

    Forecast
        ↓
    Stock-out probability
        ↓
    Risk level
        ↓
    Prediction reliability
        ↓
    Days to stock-out
        ↓
    Lead-time feasibility
        ↓
    Overstock/shelf-life exposure
        ↓
    Financial exposure
        ↓
    Store-to-store availability
        ↓
    FINAL ACTION

Possible actions:

    NO ACTION
    MONITOR
    REORDER
    URGENT REORDER
    TRANSFER FROM ANOTHER STORE
    REDUCE / HOLD REORDER

The exact action should be determined by transparent rules and model
outputs, not arbitrary labels.

------------------------------------------------------------------------

# Phase 6 --- Management Dashboard, Prototype, Testing & Final Pitch

The challenge specifies the minimum dashboard sections.

We should implement **all of them**.

------------------------------------------------------------------------

## 1. Executive Summary

Show:

-   Revenue
-   Growth
-   Stock-out rate
-   Inventory value
-   Products at risk

------------------------------------------------------------------------

## 2. Demand Intelligence

Show:

-   Actual vs forecast
-   Category trends
-   Store trends
-   Forecast error

------------------------------------------------------------------------

## 3. Inventory Risk

Show:

-   High / Medium / Low
-   Risk table
-   Heatmap

------------------------------------------------------------------------

## 4. Manager Action Centre

Show:

-   Recommended reorder
-   Reason
-   Priority
-   Financial exposure
-   Days to stock-out
-   Supplier lead time

------------------------------------------------------------------------

## 5. Model Performance

Show:

-   Regression metrics
-   Classification metrics
-   Confusion matrix
-   Residual/error analysis

------------------------------------------------------------------------

## 6. Explainability

Show:

-   Top features
-   Feature importance
-   Per-product reasons

------------------------------------------------------------------------

# Additional dashboard modules

### A. Inventory Health Matrix

                    STOCK-OUT RISK
                          ↑
                          │
           URGENT         │       CRITICAL
                          │
    ──────────────────────┼──────────────────
                          │
           HEALTHY        │       OVERSTOCK
                          │
                          ↓

### B. Prediction Reliability

Every high-risk prediction gets:

    Risk: HIGH
    Probability: 84%
    Reliability: 91%

### C. Financial Exposure

    Products at risk
    Revenue at risk
    Margin at risk

### D. Rebalancing Opportunities

    S02 → S04
    Product: PXXX
    Transfer quantity: XXX
    Reason: S04 shortage / S02 excess

### E. What-If Analysis

The challenge explicitly lists What-If analysis as optional for:

-   discount
-   supplier delay
-   festival-demand changes.

We'll implement it if the core system is stable.

For example:

    Supplier delay:
    3 days → 6 days

            ↓

    Stock-out probability:
    42% → 78%

------------------------------------------------------------------------

# Final system architecture

Your final project should conceptually become:

                             ┌────────────────────┐
                             │    RAW DATA        │
                             └─────────┬──────────┘
                                       ↓
                        ┌──────────────────────────┐
                        │ DATA QUALITY &           │
                        │ RECONCILIATION ENGINE    │
                        └────────────┬─────────────┘
                                     ↓
                        ┌──────────────────────────┐
                        │ MASTER DATASET           │
                        │ Date × Store × Product   │
                        └────────────┬─────────────┘
                                     ↓
                 ┌───────────────────┴───────────────────┐
                 ↓                                       ↓
         ┌────────────────┐                      ┌─────────────────┐
         │ EDA & STATISTICS│                      │ FEATURE ENGINE │
         └────────┬───────┘                      └────────┬────────┘
                  └──────────────────┬────────────────────┘
                                     ↓
                       ┌────────────────────────┐
                       │      ML ENGINE         │
                       ├────────────────────────┤
                       │ 7-Day Demand Forecast  │
                       │ Stock-out Risk         │
                       └────────────┬───────────┘
                                    ↓
                       ┌────────────────────────┐
                       │ EXPLAINABILITY         │
                       │ + PREDICTION RELIABILITY│
                       └────────────┬───────────┘
                                    ↓
                 ┌────────────────────────────────────┐
                 │     DECISION INTELLIGENCE          │
                 ├────────────────────────────────────┤
                 │ Reorder                            │
                 │ Stock-out timing                   │
                 │ Financial risk                     │
                 │ Shelf-life exposure                │
                 │ Supplier risk                      │
                 │ Store-to-store transfer            │
                 │ What-if analysis                   │
                 └──────────────────┬─────────────────┘
                                    ↓
                       ┌────────────────────────┐
                       │ MANAGER ACTION CENTRE  │
                       └────────────┬───────────┘
                                    ↓
                       ┌────────────────────────┐
                       │ DASHBOARD / PROTOTYPE  │
                       └────────────────────────┘

## Deliverables at the end

The challenge requires the following deliverables: cleaned master
dataset, EDA/modeling notebooks, Data Quality Report, model
comparison/justification, saved reproducible model pipeline,
dashboard/prototype, README, final presentation and GitHub repository.

So our final repository should contain something close to:

    STOCKSENSE/
    │
    ├── data/
    │   ├── raw/
    │   ├── cleaned/
    │   └── processed/
    │
    ├── notebooks/
    │   ├── 01_data_quality.ipynb
    │   ├── 02_eda_statistics.ipynb
    │   ├── 03_feature_engineering.ipynb
    │   ├── 04_demand_forecasting.ipynb
    │   ├── 05_stockout_prediction.ipynb
    │   └── 06_explainability.ipynb
    │
    ├── src/
    │   ├── preprocessing/
    │   ├── features/
    │   ├── models/
    │   ├── explainability/
    │   ├── decision_engine/
    │   └── utilities/
    │
    ├── models/
    │
    ├── dashboard/
    │
    ├── reports/
    │   ├── data_quality_report
    │   ├── eda_report
    │   └── model_report
    │
    ├── README.md
    ├── requirements.txt
    └── presentation/

This also follows the submission structure specified in the challenge.

### The critical rule for execution

**Do not start coding the dashboard now.**

Follow the dependency chain:

**Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5 → Phase 6**

And don't build the "unique features" separately from the mandatory
requirements. They should be **derived from the same master dataset and
model outputs**, so your project remains one coherent StockSense system
rather than a collection of unrelated features.
