# About
vortex_count_trilayer is a program which counts the vortices for I and B sweeps for the h5 file.
It stores the output as a pickle file. 
This uses a hardcoded lookup table. The boundaries between low and high vortex density were inspected manually.
This program only works for this concrete case (trilayer). A separate program should be run for the bare and bilayer models.
A contrast based thresholding model has been developed, but at present is not reliable.
# Requirements
The seaborn library must be downloaded into the environment.
This notebook must be run from the tdgl environment.
The output h5 file must be saved in the working directory. 
