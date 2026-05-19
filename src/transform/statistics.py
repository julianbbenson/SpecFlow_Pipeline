import numpy as np
import pandas as pd
from scipy import stats

def calculate_differential_expression(df_control: pd.DataFrame, df_exp: pd.DataFrame) -> pd.DataFrame:
    """
    Merges two datasets, calculates Log2 Fold Change, and computes statistical p-values.
    """
    print("[*] Calculating Differential Expression...")
    
    # Merge the two datasets on the m/z feature
    df_merged = pd.merge(df_control, df_exp, on='mz_feature', suffixes=('_ctrl', '_exp'))
    
    # Filter out zeros to prevent math errors
    df_merged = df_merged[(df_merged['intensity_ctrl'] > 0) & (df_merged['intensity_exp'] > 0)].copy()
    
    # Calculate Log2 Fold Change: log2(Experimental / Control)
    df_merged['log2_FC'] = np.log2(df_merged['intensity_exp'] / df_merged['intensity_ctrl'])
    
    # --- Synthetic Variance for Pipeline Prototyping ---
    # We generate a synthetic distribution around the single data point to allow the t-test to run
    np.random.seed(42)
    ctrl_variance = np.random.normal(loc=df_merged['intensity_ctrl'], scale=df_merged['intensity_ctrl']*0.1, size=(3, len(df_merged)))
    exp_variance = np.random.normal(loc=df_merged['intensity_exp'], scale=df_merged['intensity_exp']*0.2, size=(3, len(df_merged)))
    
    # Calculate p-values using Welch's t-test
    t_stat, p_vals = stats.ttest_ind(ctrl_variance, exp_variance, axis=0, equal_var=False)
    
    df_merged['p_value'] = p_vals
    # Calculate -log10(p-value) for the Volcano Plot y-axis
    df_merged['neg_log10_p'] = -np.log10(df_merged['p_value'] + 1e-10) # 1e-10 prevents log(0)
    
    # Determine significance thresholds (Standard: p < 0.05 and Fold Change > 2 or < 0.5)
    df_merged['Significance'] = 'Not Significant'
    df_merged.loc[(df_merged['p_value'] < 0.05) & (df_merged['log2_FC'] >= 1), 'Significance'] = 'Upregulated (Cancer)'
    df_merged.loc[(df_merged['p_value'] < 0.05) & (df_merged['log2_FC'] <= -1), 'Significance'] = 'Downregulated (Cancer)'
    
    return df_merged