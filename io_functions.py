"""
Save and load functions for main tdgl_simulation file and the data analysis notebooks.

Two methods available:
1. Manual extraction (~5.7 GB for default parameters): Saves voltage, psi, current density
2. Built-in TDGL method (~30 GB for default parameters): Saves complete Solution object

Choose method in parameters.py via SAVE_METHOD variable.

"""

import h5py
import numpy as np


# ============================================================================
# MESH EXTRACTION
# ============================================================================

mesh_data_cache = None


def extract_and_cache_mesh(solution):
    """
    Extract mesh from solution and cache it globally.
    
    The mesh is the same for all solutions (same device), so extract
    it once from the first solution and cache it to avoid redundant
    extraction.
    
    Parameters
    ----------
    solution : tdgl.Solution
        A solution object with device.mesh
    
    Returns
    -------
    dict or None
        Dictionary with 'coordinates' and 'elements' keys, or None if failed
    """
    global mesh_data_cache
    
    # Return cached mesh if already extracted
    if mesh_data_cache is not None:
        return mesh_data_cache
    
    try:
        mesh = solution.device.mesh
        
        # Combine separate x and y arrays into (n_nodes, 2) array
        coordinates = np.column_stack((mesh.x, mesh.y))
        triangulation = mesh.elements
        
        # Verify shapes
        assert coordinates.shape[1] == 2, f"Coordinates should be (n, 2), got {coordinates.shape}"
        assert triangulation.shape[1] == 3, f"Triangulation should be (n, 3), got {triangulation.shape}"
        
        mesh_data_cache = {
            'coordinates': coordinates,
            'elements': triangulation
        }
        
        print(f" Mesh extracted and cached:")
        print(f" Coordinates shape: {coordinates.shape}")
        print(f" Triangulation shape: {triangulation.shape}")
        
        return mesh_data_cache
        
    except Exception as e:
        print(f" Failed to extract mesh: {e}")
        import traceback
        traceback.print_exc()
        return None

# ============================================================================
# MANUAL SAVE/LOAD
# ============================================================================

def save_all_sol_manual(all_sol, I_values, filename):
    """
    Save extracted solution data manually to HDF5 file.
    
    Extracts and saves:
    - Voltage (mean voltage)
    - Order parameter (psi magnitude and phase)
    - Current densities (total, superconducting, normal)
    - V_0 (used to scale the Voltage)
    
    Parameters
    ----------
    all_sol : dict
        Nested dictionary: all_sol[I][direction][B] = Solution object
    I_values : array
        Applied current values (μA) - used as the key
    filename : str
        Output HDF5 filename
    """
    print(f"\n{'='*70}")
    print(f"SAVING (Manual Method) to: {filename}")
    print(f"{'='*70}\n")
    
    with h5py.File(filename, 'w') as f:
        # Save metadata
        metadata = f.create_group('metadata')
        metadata.attrs['I_values'] = I_values
        metadata.attrs['save_method'] = 'manual'
        
        # Save data for each current
        for I in I_values:
            print(f"  Saving I = {I} μA...")
            I_group = f.create_group(f'I_{I}uA')
            
            # Up sweep
            up_group = I_group.create_group('up')
            for B, solution in all_sol[I]['up'].items():
                B_group = up_group.create_group(f'B_{B:.2f}mT')
                save_solution_data(B_group, solution)
            
            # Down sweep
            down_group = I_group.create_group('down')
            for B, solution in all_sol[I]['down'].items():
                B_group = down_group.create_group(f'B_{B:.2f}mT')
                save_solution_data(B_group, solution)
    
    print(f"\n{'='*70}")
    print(f" Successfully saved to: {filename}")
    print(f"{'='*70}\n")
    
def save_solution_data(B_group, solution):
    """
    Extract and save key data from a single solution.
    
    Helper function to avoid code repetition.
    All solutions have the same attributes.
    
    Parameters
    ----------
    B_group : h5py.Group
        HDF5 group for this B value
    solution : tdgl.Solution
        Solution object to extract from
    """
    # Voltage
    V = solution.dynamics.mean_voltage()
    B_group.create_dataset('voltage', data=V)
    
    # Order parameter (psi)
    psi = solution.tdgl_data.psi
    B_group.create_dataset('psi_magnitude', data=np.abs(psi))
    B_group.create_dataset('psi_phase', data=np.angle(psi))
    
    # Current densities
    J = solution.current_density
    B_group.create_dataset('current_density', data=J)
    
    J_s = solution.supercurrent_density
    B_group.create_dataset('supercurrent_density', data=J_s)
    
    J_n = solution.normal_current_density
    B_group.create_dataset('normal_current_density', data=J_n)


def load_all_sol_manual(filename):
    """
    Load manually saved solution data from HDF5 file.
    
    Returns data as dictionaries of numpy arrays (not Solution objects).
    
    Parameters
    ----------
    filename : string
        HDF5 filename of the output file.
    
    Returns
    -------
    Object with data structure:
        Nested dictionary: all_sol[I][direction][B] = dict of arrays
    Individual values of solution can be accessed by specifying keys
        Applied current values
    """
    print(f"\nLoading from: {filename}...")
    
    all_sol = {}
    
    with h5py.File(filename, 'r') as f:
        I_values = f['metadata'].attrs['I_values']
        
        for I in I_values:
            all_sol[I] = {'up': {}, 'down': {}}
            
            # Load up sweep
            if 'up' in f[f'I_{I}uA']:
                for B_str in f[f'I_{I}uA/up'].keys():
                    B = float(B_str.replace('B_', '').replace('mT', ''))
                    B_group = f[f'I_{I}uA/up/{B_str}']
                    all_sol[I]['up'][B] = {name: B_group[name][()] for name in B_group.keys()}
            
            # Load down sweep
            if 'down' in f[f'I_{I}uA']:
                for B_str in f[f'I_{I}uA/down'].keys():
                    B = float(B_str.replace('B_', '').replace('mT', ''))
                    B_group = f[f'I_{I}uA/down/{B_str}']
                    all_sol[I]['down'][B] = {name: B_group[name][()] for name in B_group.keys()}
    
    print(f" Loaded from: {filename}\n")
    return all_sol, I_values


# ============================================================================
# BUILT-IN TDGL SAVE/LOAD
# ============================================================================

def save_all_sol_builtin(all_sol, I_values, filename):
    """
    Save complete Solution objects using TDGL's built-in to_hdf5() method.
    
    Saves entire Solution objects with full reproducibility:
    - All TDGL data (psi, A, J,etc. including applied vector potential and vorticity).
    - Device mesh and metadata
    - Solver state
    - Complete solution (simulation) reconstruction possible
    
    Parameters
    ----------
    all_sol : dict
        Nested dictionary: all_sol[I][direction][B] = Solution object
    I_values : array
        Applied current values (uA)
    filename : string
        Output HDF5 filename
    """
    print(f"\n{'='*70}")
    print(f"SAVING (Built-in TDGL Method) to: {filename}")
    print(f"{'='*70}\n")
    
    with h5py.File(filename, 'w') as f:
        # Save metadata
        metadata = f.create_group('metadata')
        metadata.attrs['I_values'] = I_values
        metadata.attrs['save_method'] = 'builtin'
        
        # Save data for each current
        for I in I_values:
            print(f"  Saving I = {I} μA...")
            I_group = f.create_group(f'I_{I}uA')
            
            # Up sweep
            up_group = I_group.create_group('up')
            for B, solution in all_sol[I]['up'].items():
                B_group = up_group.create_group(f'B_{B:.2f}mT')
                solution.to_hdf5(B_group)
            
            # Down sweep
            down_group = I_group.create_group('down')
            for B, solution in all_sol[I]['down'].items():
                B_group = down_group.create_group(f'B_{B:.2f}mT')
                solution.to_hdf5(B_group)
    
    print(f"\n{'='*70}")
    print(f" Successfully saved to: {filename}")
    print(f"{'='*70}\n")


def load_all_sol_builtin(filename):
    """
    Load complete Solution objects using TDGL's loader.
    
    Returns full Solution objects (not just data arrays).
    
    Parameters
    ----------
    filename : string
        HDF5 filename
    
    Returns
    -------
    Nested dictionary: all_sol[I][direction][B] = Solution object
    The same key structure as save_all_sol_builtin
    I_values : array
        Applied current values
    """
    import tdgl
    
    print(f"\nLoading from: {filename}...")
    
    all_sol = {}
    
    with h5py.File(filename, 'r') as f:
        I_values = f['metadata'].attrs['I_values']
        
        for I in I_values:
            all_sol[I] = {'up': {}, 'down': {}}
            
            # Load up sweep
            if 'up' in f[f'I_{I}uA']:
                for B_str in f[f'I_{I}uA/up'].keys():
                    B = float(B_str.replace('B_', '').replace('mT', ''))
                    B_group = f[f'I_{I}uA/up/{B_str}']
                    all_sol[I]['up'][B] = tdgl.solution.load_tdgl_data(B_group)
            
            # Load down sweep
            if 'down' in f[f'I_{I}uA']:
                for B_str in f[f'I_{I}uA/down'].keys():
                    B = float(B_str.replace('B_', '').replace('mT', ''))
                    B_group = f[f'I_{I}uA/down/{B_str}']
                    all_sol[I]['down'][B] = tdgl.solution.load_tdgl_data(B_group)
    
    print(f" Loaded from: {filename}\n")
    return all_sol, I_values
