# Stock-out Error Analysis

- The classification target is operational stockout_flag evaluated at the prediction date t.
- False negatives are the highest-risk operational failure because a missed stock-out warning can trigger a missed replenishment action.
- False positives are operationally costly because they may trigger unnecessary inventory actions.
- The model is tuned with class imbalance safeguards and evaluated using precision, recall, F1 and ROC-AUC rather than accuracy alone.
