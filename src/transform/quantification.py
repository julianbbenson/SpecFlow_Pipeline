import numpy as np
import pandas as pd

def smooth_signal(df: pd.DataFrame, window: int = 3) -> pd.DataFrame:
    """
    Applies a rolling average to the total_intensity to smooth out 
    detector noise and baseline static.
    """
    print(f"[*] Applying rolling average smoothing (window={window})...")
    # We use min_periods=1 so the edges don't become NaN
    df['smoothed_intensity'] = df['total_intensity'].rolling(window=window, min_periods=1).mean()
    return df

def calculate_total_auc(df: pd.DataFrame) -> float:
    """
    Calculates the Total Area Under the Curve (AUC) using the trapezoidal rule.
    This provides a single quantitative metric for total run abundance.
    """
    print("[*] Integrating Area Under the Curve (AUC)...")
    
    # Ensure data is sorted by time before integrating
    df = df.sort_values(by='retention_time_min')
    
    # Updated for NumPy 2.0+: trapz is now trapezoid
    auc = np.trapezoid(y=df['smoothed_intensity'], x=df['retention_time_min'])
    return auc

if __name__ == "__main__":
    print("SpecFlow Transformation Module Ready.")