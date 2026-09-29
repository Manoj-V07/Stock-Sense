import pandas as pd

from src.decision.decision_engine import (
    compute_reorder_quantity,
    risk_level_from_probability,
)


def test_risk_thresholds_and_reorder_formula():
    assert risk_level_from_probability(0.90) == "HIGH"
    assert risk_level_from_probability(0.55) == "MEDIUM"
    assert risk_level_from_probability(0.20) == "LOW"

    row = pd.DataFrame(
        [
            {
                "forecast_demand": 120.0,
                "safety_stock": 25.0,
                "closing": 80.0,
                "received": 15.0,
            }
        ]
    )
    result = compute_reorder_quantity(row)
    assert result.iloc[0] == 50.0
