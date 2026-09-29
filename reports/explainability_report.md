# Explainability and Manager-Facing Interpretation

- Global feature importance is derived from the XGBoost model.
- Permutation importance is used to test whether top drivers are stable under small perturbations.
- The phrase 'Feature X contributed strongly to the model prediction' is used instead of claiming a direct causal effect.

## Example manager-facing explanation
STORE: S01
PRODUCT: Milk
Stock-out probability: 0.89
Risk: HIGH
Main model drivers:
- recent demand increase
- low inventory coverage
- promotion active
- approaching weekend

