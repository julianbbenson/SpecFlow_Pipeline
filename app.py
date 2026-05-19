import streamlit as st
import os
import pandas as pd
import numpy as np
import plotly.express as px

from src.extract.mzml_parser import parse_mzml_to_dataframe, extract_mz_features
from src.transform.quantification import smooth_signal, calculate_total_auc
from src.transform.statistics import calculate_differential_expression

st.set_page_config(page_title="SpecFlow Pipeline", layout="wide")
st.title("🔬 SpecFlow: Differential Proteomics")
st.markdown("Upload a Control and an Experimental `.mzML` file to quantify differential protein expression.")

col1, col2 = st.columns(2)
with col1:
    control_file = st.file_uploader("Upload Control .mzML (Healthy)", type=['mzML'], key="ctrl")
with col2:
    exp_file = st.file_uploader("Upload Experimental .mzML (Cancer)", type=['mzML'], key="exp")

if control_file and exp_file:
    st.success("Files uploaded successfully! Running statistical pipeline...")
    
    # Save temp files
    ctrl_path = os.path.join("data", "raw", "ctrl_temp.mzML")
    exp_path = os.path.join("data", "raw", "exp_temp.mzML")
    with open(ctrl_path, "wb") as f: f.write(control_file.getbuffer())
    with open(exp_path, "wb") as f: f.write(exp_file.getbuffer())
    
    with st.spinner('Extracting m/z features and calculating statistics...'):
        # 1. Extract Features
        df_ctrl_features = extract_mz_features(ctrl_path)
        df_exp_features = extract_mz_features(exp_path)
        
        # 2. Calculate Differential Expression
        df_results = calculate_differential_expression(df_ctrl_features, df_exp_features)
    
    st.markdown("---")
    st.subheader("🌋 Differential Expression (Volcano Plot)")
    
    # 3. Render Interactive Volcano Plot
    fig = px.scatter(
        df_results, 
        x='log2_FC', 
        y='neg_log10_p',
        color='Significance',
        color_discrete_map={'Not Significant': 'grey', 'Upregulated (Cancer)': 'red', 'Downregulated (Cancer)': 'blue'},
        hover_data=['mz_feature'],
        labels={'log2_FC': 'Log2 Fold Change', 'neg_log10_p': '-Log10(p-value)'},
        title="Protein Expression: Cancer vs. Control"
    )
    
    # Add boundary lines for visual thresholds
    fig.add_hline(y=-np.log10(0.05), line_dash="dash", line_color="black", annotation_text="p = 0.05")
    fig.add_vline(x=1, line_dash="dash", line_color="black")
    fig.add_vline(x=-1, line_dash="dash", line_color="black")
    
    st.plotly_chart(fig, use_container_width=True)
    
    with st.expander("View Statistical Data Table"):
        st.dataframe(df_results.sort_values('p_value'))

    # Cleanup
    os.remove(ctrl_path)
    os.remove(exp_path)

    # Export Data Feature
    st.markdown("---")
    csv = df_results.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Statistical Results (CSV)",
        data=csv,
        file_name="specflow_differential_expression.csv",
        mime="text/csv",
    )