"""StockSense Phase 3: Time and Calendar Features (Group A)."""
import pandas as pd
import numpy as np


def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """Derive leakage-safe calendar and temporal features from the observation date.

    Features generated:
    - day_of_week: 1 (Monday) to 7 (Sunday)
    - weekend_flag: 1 if Saturday or Sunday, else 0
    - month: Calendar month (e.g., 8 for August)
    - week_no: ISO calendar week number (e.g., 31 to 35)
    - festival_flag: Binary flag indicating local/regional festival
    - day_of_month: Day of the month (1 to 31)
    - is_month_end: Binary flag for end of month (day >= 28), capturing payday retail cycle
    """
    df = df.copy()
    dates = pd.to_datetime(df["date"])

    # Mandatory challenge features
    df["day_of_week"] = dates.dt.dayofweek + 1  # 1=Monday, 7=Sunday
    df["weekend_flag"] = (dates.dt.dayofweek >= 5).astype(int)
    df["month"] = dates.dt.month.astype(int)
    df["week_no"] = dates.dt.isocalendar().week.astype(int)
    
    # Festival flag: map from existing festival column or external factors
    if "festival" in df.columns:
        df["festival_flag"] = df["festival"].fillna(0).astype(int)
    else:
        df["festival_flag"] = 0

    # Justified Phase 2 additions
    df["day_of_month"] = dates.dt.day.astype(int)
    df["is_month_end"] = (dates.dt.day >= 28).astype(int)

    return df
