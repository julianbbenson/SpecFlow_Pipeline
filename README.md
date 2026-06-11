# SpecFlow: Automated Mass Spectrometry ETL & Quantification Pipeline

> **Note:** The lanthanide-DOTA / ion-mobility CL-MS parser has been moved to its
> own repository: [clms-parser](https://github.com/julianbbenson/clms-parser).
> Development continues there.

**Author:** Julian Benson  
**Domain:** Computational Biology / Proteomics  

---

## 🔬 Project Abstract
High-throughput proteomics generates massive datasets that frequently suffer from manual processing bottlenecks. **SpecFlow** is a containerized Extract, Transform, Load (ETL) pipeline designed to automate the ingestion, statistical filtering, and visualization of mass spectrometry data. 

By prioritizing reproducibility via Docker and strict modular architecture, this pipeline provides a robust infrastructure for downstream quantitative biology and machine learning applications.

## ⚙️ Pipeline Architecture

### 1. Extract (Data Ingestion)
- Automated parsing of `.mzML` open-source mass spectrometry formats.
- Extraction of retention times, m/z ratios, and ion intensities using `pyteomics`.

### 2. Transform (Statistical Quantification)
- **Quality Control:** Algorithmic noise-reduction and background peak filtering.
- **Quantification:** Area Under the Curve (AUC) integration for relative protein abundance.
- **Statistical Filtering:** Rigorous fold-change and p-value thresholding.

### 3. Load (Automated Visualization)
- Programmatic generation of Total Ion Chromatograms (TIC).
- Automated Volcano Plots mapping quantitative differential expression.

---
title: SpecFlow ETL
emoji: 🚀
colorFrom: red
colorTo: red
sdk: docker
app_port: 8501
tags:
- streamlit
pinned: false
short_description: Streamlit template space
license: mit
---

# Welcome to Streamlit!

Edit `/src/streamlit_app.py` to customize this app to your heart's desire. :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

