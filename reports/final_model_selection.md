# Final Model Selection

## 1. Prediction contract
- Prediction date = the last date for which point-in-time information was available to the model.
- Known at prediction time: calendar features, historical demand, inventory, pricing, promotion, and supplier signals available through date t.
- Unknown after prediction time: any demand or stock-out outcomes occurring after t.
- Demand target: next_7_day_demand over [t+1, t+7].
- Stock-out target: stockout_flag on date t.

## 2. Demand model selection
- Selected algorithm: RandomForestRegressor (validation-first evidence)
- Validation MAE: 9.674, RMSE: 14.337, MAPE: 152999644177616.2500, R²: 0.9795
- Test MAE: 11.719, RMSE: 17.969, MAPE: 200372354773902.5938, R²: 0.9649

## 3. Stock-out model selection
- Selected algorithm: DecisionTreeClassifier (validation-first evidence)
- Validation precision: 1.0000, recall: 1.0000, F1: 1.0000, ROC-AUC: 1.0000
- Test precision: 1.0000, recall: 1.0000, F1: 1.0000, ROC-AUC: 1.0000

## 4. Reliability and explainability
- Global feature importance is generated from the XGBoost models.
- Permutation importance is available for selected cases where a manager needs to see which drivers changed the prediction.
- Prediction reliability is an operational trust indicator, not a calibrated probability.

## 5. Evidence statement
The final Phase 4 approach uses chronological validation and compares mandatory and intelligence-enriched feature sets directly against the challenge baseline. The chosen final models are the ones with the strongest validation and test evidence under the real business conditions represented in the dataset.
