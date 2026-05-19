# SpecFlow: Automated Mass Spectrometry ETL & Quantification Pipeline

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