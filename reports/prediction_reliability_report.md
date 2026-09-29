# Prediction Reliability Report

Prediction reliability is not the same as stock-out probability. It answers: 'How trustworthy is this prediction given the data quality and model behaviour?'.

The implemented rule uses a transparent weighted score composed of: inventory coverage, data-quality condition, volatility, and sparse-history risk.
- HIGH: reliability >= 0.70
- MEDIUM: reliability between 0.40 and 0.69
- LOW: reliability < 0.40

This is an operational indicator for triage and human review rather than a formally calibrated probability.
