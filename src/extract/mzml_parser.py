import sys
import os
# Add the src directory to the path so python can find your modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.transform.quantification import smooth_signal, calculate_total_auc
import pandas as pd
from pyteomics import mzml

def parse_mzml_to_dataframe(filepath: str) -> pd.DataFrame:
    """
    Ingests an .mzML file and extracts spectral data into a normalized Pandas DataFrame.
    Filters for MS1 (precursor) scans to establish a baseline Total Ion Chromatogram (TIC).
    """
    # 1. Defensive Check
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Could not locate mass spec data at: {filepath}")
    
    print(f"[*] Initializing Pyteomics parser for: {filepath}")
    
    spectra_data = []
    
    # 2. The Iterator (Memory Efficient)
    with mzml.read(filepath) as reader:
        for spectrum in reader:
            
            # 3. Filter for Quantitative Scans (MS1)
            if spectrum['ms level'] == 1:
                scan_time = spectrum['scanList']['scan'][0]['scan start time']
                
                # Extract the parallel arrays
                mz_array = spectrum['m/z array']
                intensity_array = spectrum['intensity array']
                
                # Sum intensities for a quick Total Ion Current (TIC) mapping
                total_intensity = intensity_array.sum()
                
                # 4. Package the extracted data
                spectra_data.append({
                    'scan_id': spectrum['id'],
                    'retention_time_min': scan_time,
                    'total_intensity': total_intensity
                })
                
    # 5. Convert to an analytical format
    df = pd.DataFrame(spectra_data)
    print(f"[✔] Successfully parsed {len(df)} MS1 spectra.")
    
    return df

def extract_mz_features(filepath: str, round_decimals: int = 1) -> pd.DataFrame:
    """
    Extracts individual m/z signals and bins them to simulate peptide features.
    This allows us to track specific biological molecules, not just total noise.
    """
    from pyteomics import mzml
    import numpy as np
    
    features = {}
    
    with mzml.read(filepath) as reader:
        for spectrum in reader:
            if spectrum['ms level'] == 1:
                mz_array = spectrum['m/z array']
                intensity_array = spectrum['intensity array']
                
                # Round m/z to group identical peptides together (Binning)
                mz_rounded = np.round(mz_array, round_decimals)
                
                for mz, intensity in zip(mz_rounded, intensity_array):
                    if mz in features:
                        features[mz] += intensity
                    else:
                        features[mz] = intensity
                        
    # Convert to DataFrame
    df = pd.DataFrame(list(features.items()), columns=['mz_feature', 'intensity'])
    return df