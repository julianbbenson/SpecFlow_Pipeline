import os
from pyteomics import mzml
import pandas as pd

def parse_mzml_to_dataframe(filepath: str) -> pd.DataFrame:
    """
    Ingests an .mzML file and extracts spectral data into a normalized Pandas DataFrame.
    Filters for MS1 (precursor) scans to establish a baseline Total Ion Chromatogram (TIC).
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Could not locate mass spec data at: {filepath}")
    
    print(f"[*] Initializing Pyteomics parser for: {filepath}")
    
    spectra_data = []
    
    # pyteomics.mzml.read creates an efficient iterator to prevent RAM overload
    with mzml.read(filepath) as reader:
        for spectrum in reader:
            # We are primarily interested in MS1 scans for quantitative abundance
            if spectrum['ms level'] == 1:
                scan_time = spectrum['scanList']['scan'][0]['scan start time']
                
                # Extract the parallel arrays
                mz_array = spectrum['m/z array']
                intensity_array = spectrum['intensity array']
                
                # Sum intensities for a quick Total Ion Current (TIC) mapping
                total_intensity = intensity_array.sum()
                
                spectra_data.append({
                    'scan_id': spectrum['id'],
                    'retention_time_min': scan_time,
                    'total_intensity': total_intensity
                })
                
    df = pd.DataFrame(spectra_data)
    print(f"[✔] Successfully parsed {len(df)} MS1 spectra.")
    return df

if __name__ == "__main__":
    # Placeholder for local testing. 
    # Tomorrow, we will download a sample .mzML file to test this exact execution.
    print("SpecFlow Extraction Module Ready.")