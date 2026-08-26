"""
This file contains all the parameter values used in the main tdgl_simulation.ipynb file. 
Select the model type (MODEL) and save method (SAVE_METHOD)
By leaving as defaults or selecting one of the alternatives.
Parameter values changed beneath will affect the simulation.

"""

MODEL = "trilayer" # Alternatives: "bilayer" or "bare"
SAVE_METHOD = "manual" # Alternative: "builtin"

# Physics constants
#------------------------------------------------
XI = 0.0537 # Coherence length
LONDON_LAMBDA = 0.4450 # Penetration depth
SIGMA = 1.3e5 # Conductivity
GAMMA = 10 # Electron-phonon scattering coefficient
#------------------------------------------------
# Applied Field Setup
#------------------------------------------------
BI_THRESH = 86
BI_THRESH2 = -86
BI_CGT_MAG = 5
TRI_THRESH_L = 10 # Coercive field of CGT lower-layer
TRI_THRESH_U = 30 # Coercive field of CGT upper-layer
TRI_THRESH_L2 = -10 # As above for down sweep
TRI_THRESH_U2 = -30 # As above for down sweep
TRI_CGT_MAG = 20
#------------------------------------------------
# Device Geometry
#------------------------------------------------
THICKNESS = 0.010 # Thickness
WIDTH = 1 # Width
LENGTH = 4 # Length
#------------------------------------------------
# Simulation Parameters
#------------------------------------------------
MAX_EDGE_LENGTH = XI/2 # Mesh max edge length
RUNS = 61 # Number of data points per sweep
LOW_B = -150 # Lowest value of magnetic field in sweeping range
HIGH_B = 150 # Highest value of magnetic field in sweeping range
SOLVE_TIME = 100 # Solve time (arbitrary units) per solution
SKIP_TIME = 50 # Skip time (arbitrary units) per solution
I_LOW = 1 # Lowest applied current for sweep
I_HIGH = 30 # Highest applied current for sweep
NUM_CURRENTS = 30 # Number of sweeping values
# ============================================================================
# UNITS
# ============================================================================
LENGTH_UNITS = "um" # Micrometers
FIELD_UNITS = "mT" # Millitesla
CURRENT_UNITS = "uA" # Microamperes