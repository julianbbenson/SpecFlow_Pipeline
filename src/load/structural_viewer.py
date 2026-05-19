import py3Dmol
from stmol import showmol
import urllib.request

def render_3d_protein(pdb_id: str, style: str = "cartoon", color: str = "spectrum"):
    """
    Fetches a PDB file directly from the RCSB database and generates 
    an interactive 3D representation.
    """
    url = f"https://files.rcsb.org/download/{pdb_id.upper()}.pdb"
    
    try:
        # Download the raw atomic coordinates
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        pdb_data = response.read().decode('utf-8')
        
        # Initialize the 3D viewer
        view = py3Dmol.view(width=800, height=500)
        view.addModel(pdb_data, 'pdb')
        
        # Apply biological styling
        if style == "cartoon":
            view.setStyle({'cartoon': {'color': color}})
        elif style == "stick":
            view.setStyle({'stick': {}})
            
        view.zoomTo()
        
        # Pass the view to Streamlit's stmol wrapper
        showmol(view, height=500, width=800)
        
    except Exception as e:
        import streamlit as st
        st.error(f"Could not fetch PDB ID {pdb_id}. Ensure it is a valid RCSB ID.")