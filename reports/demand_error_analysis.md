# Demand Error Analysis

- Baseline demand benchmark: trailing 7-day mean demand.
- Validation baseline MAE: 56.228; test baseline MAE: 54.130.
- Validation XGBoost MAE: 9.674; test MAE: 11.719.
- Bigger errors cluster where recent demand volatility or missing inventory coverage signals are elevated.
- Under-forecasting occurs more often during promotion spikes; over-forecasting tends to show up in intermittent-demand product segments.
