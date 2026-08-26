# tdgl
MSc dissertation work using pyTDGL, including simulation code and analysis notebooks.

# How to use this repository:

- Firstly, tdgl is introduced and the basic physics theory is explained
- Secondly, there is a QUICKSTART.
- Thirdly, a comprehensive table of values used in the MSc project are given and where they come from. 
- Fourthly, there are some tips about simulation parameters to use.
- Fifthly, system requirements are covered. 
- Sixthly, I explain the file structure, how to use these files and the data structures.
# Introduction

This is a pyTDGL simulation script aiming to simulate the superconductivity physics. Documentation can be found here: https://py-tdgl.readthedocs.io/en/latest/ 
This is based on a paper: pyTDGL: Time-dependent Ginzburg-Landau in Python by L. Bishop Van-Horn (2023)

This models a rectangular strip with an applied current source and sink at ends of the rectangle. The voltage is measured across the probe points, which can be used to determine the device's resistance (and by extension its conductivity behaviour) as a function of applied field (which is swept).

There are physics variables defined: xi, lambda which depend on the type of Superconductor.
The literature values for $\xi_0$ and $\lambda_0$ are taken from literature for NbSe2. 

The simulation parameters, such as solve_time, skip_time and so on can affect the accuracy and precision of the simulation and also the wall time.

This script aims to model a CGT | NbSe2 trilayer by adding an offset to the applied field, which starts off as -20mT, then at the threshold value of +10mT the magnetization of the CGT flips and it adds +20mT to the applied field. This remains until the reverse magnetization flip which occurs at -10mT on the down sweep and adds -20mT to the applied field. 

Validity of pyTDGL:
- 'Strictly speaking, the model is only valid for temperatures very close to the critical temperature' docs. $T/T_c$ $\approx$ 1
- 'By “thin” or “two-dimensional” we mean that the film thickness is smaller than the coherence length and the London penetration depth' docs
- 'for dirty superconductors where the inelastic diffusion length much smaller than the coherence length'. docs

# QUICKSTART

1. Download this repository (tdgl_simulation.ipynb, parameters.py and io_functions.py into the same wd)
2. Install requirements (see Software Requirements)
3. Run tdgl_simulation.ipynb
4. Results will be saved to .h5 file

_____________________________________________________________________________________________________________________________________________________________________________________________________________________
Here are the parameters we have control over, in order:
- Physical constants
- Device geometry
- Variables
- Simulation parameters

| Parameter  | Meaning | Value used | Source | 
| -------- | ------- | ------------- | ------- |
|  $\xi_{0ab}$    | coherence length in-plane (0K) | 7.6 nm | Prober et al 1980 |
|  $\lambda_{0ab}$ | penetration depth in-plane (0K) | 124 nm | Finley & Denver 1980 |
|  $\xi_{ab}$    | coherence length in-plane (T = 0.98 $T_c$) |  53.7 nm | eqn. [1] below |
|  $\lambda_{ab}$ | penetration depth in-plane (T = 0.98 $T_c$)) | 445.0 nm | eqn. [2] below |
|$\gamma$| electron-phonon scattering coefficient| 10 | between 5.8 and 10 is reasonable, pyDGL docs used value |
|LENGTH | device length | 4 $\mu$m| reasonable estimate |
|WIDTH| device width | 1 $\mu$m | reasonable estimate |
|THICKNESS| device thickness | 10 nm| reasonable estimate (~14 atomic layers) |
|I| applied current| 1-30 uA | see [3] below * (geometry)|
|B_up / B_down|applied magnetic field (out-of-plane)|-150 to 150 mT| reasonable range (similar to D. Nutting)|
|B_up_tot / B_down_tot |effective magnetic field (out-of-plane)|B_up/B_down $\pm$20 mT| reasonable estimate for CGT magnetization |
|thresh_l| value at which CGT magnetization flips| $\pm$10 mT| various (D. Nutting), between 50 to 200 mT is sensible |
| |data-points/ sweep|61| reasonable, enough for 5mT resolution|
|solution.dynamics.mean_voltage()|time-averaged Voltage in simulation window|outputted - in units V$_0$|pyTDGL docs, see conversion [4]|
|solve_time|time solver takes values over|100 (arb. units)|reasonable value|
|skip_time|time solver waits for stable before recording | 50 (arb. units)|reasonable value|
|seed_solution|the initial conditions of the solve|previous iteration|N/A|

# Relevant Equations:

### [0] Ginzburg Landau equation

The equation the solver uses in each mesh quadrant is this:

$$
\frac{u}{\sqrt{1+\gamma^2|\psi|^2}}
\left(
\frac{\partial}{\partial t}
+i\mu
+\frac{\gamma^2}{2}\frac{\partial |\psi|^2}{\partial t}
\right)\psi
= (\epsilon-|\psi|^2)\psi
+
(\nabla-i\mathbf{A})^2\psi
$$

Source: pyTDGL docs.


### [1] $\xi$ as function of T eqn.

$$
\xi(T)=\frac{\xi_0}{\sqrt{1-\frac{T}{T_c}}}
$$

Source: M. Tinkham, Introduction to Superconductivity, 2nd ed., McGraw-Hill, New York, 1996.

### [2] $\lambda$ as function of T eqn.

$$
\lambda(T)=\frac{\lambda_0}{\sqrt{1-\left(\frac{T}{T_c}\right)^4}}
$$

source: M. Tinkham, Introduction to Superconductivity, 2nd ed., McGraw-Hill, New York, 1996. (chapter 2, page 19)

### [3] Critical current density NbSe2

$$ J_c \approx 2 × 10^5 A/cm2 $$

Soruce: Enhanced Superconductivity and Critical Current Density Due to the Interaction of InSe2 Bonded Layer in (InSe2)0.12NbS Riu Niu et al (2024)

1x4x0.01 um device gives I_c $\approx$ 20 uA 

### [4] Conversion of $V_0$ output to V ($\Omega$)

'The TDGL model is solved in dimensionless units, where the scale factors are given in terms of fundamental constants and material parameters, namely the superconducting coherence length , London penetration depth , normal state conductivity , and film thickness . The Ginzburg-Landau parameter is defined as . is the vacuum permeability and is the superconducting flux quantum.' docs

The length, current, and applied field scales are all overridden with explicit units in the code.


The method solution.dynamics.mean_voltage() measures the current in units of $V_0$

$$
V_0=\frac{\xi J_0}{\sigma} = \frac{4 \xi^2 B_{c2}}{\mu_0 \sigma \lambda ^2}
$$

Where:
- $B_{c2}$ is the upper critical field
- $\sigma$ is the normal state conductivity

The characteristic current density is given by:

$$
J_0=\frac{\Phi_0}{\mu_0\lambda^2\xi}
$$

Substituting this into the first equation gives:

$$
V_0=\frac{\Phi_0}{\mu_0\lambda^2\sigma}
$$

Where they are all constants, we define $\lambda$. The only thing left to consider is $\sigma$

$\sigma$ for NbSe2 (few nm thick), room temperature (normal-state) 8.2 × 10^4 to 1.8 × 10^5 S/m <br>
Source: Transport properties of few-layer NbSe2: From electronic structure to
thermoelectric properties (Zhu et al. 2022) <br>
Use: 1.3 e5 S/m (halfway in their samples' range) as a reasonable estimate.

# Friendly Simulation Advice

This is based on experience and not necessarily taken as gospel.

- Do not make the mesh bigger than max_edge_length = xi/2 if you do the physics might start to break down. I tried xi or 1.3*xi or 1.5*xi and it often does not work. Stick with xi/2
- solve_time as low as 30-50 might be too low for it to work. If it is as high as 150-200 sometimes it could even have negative effect or will take ages.
- skip_time needs to be at least I would say 50 to let the physics stabilize. Lower is risky. But not too high either.
- In certain device domain sizes/ parameter regions cpu might be faster than gpu.
- If there are too few data points for B-sweep, the jump between the two iterations can be too large and you get could not solve in ^2 error, where it stops running. This can also be caused by too coarse a mesh.
- Recommended 5mT resolution (e.g -150mT to +150mT with 61 data points).

# System Requirements

### Hardware requirements

These are fairly computationally heavy simulations. This section covers approximate wall times for various setups, and the minimum basic requirements.
The simulations were run on three types of computers:

1) Research-grade high performance computing machines
2) Solid PC with dedicated GPU
3) Laptop with integrated graphics card

Type (1) specification: Ryzen Threadripper PRO 5975WX, NVIDIA GeForce RTX 5060, 32 cores (64 threads), 64GB RAM
Type (2): Ryzen 5, NVIDIA GeForce GTX 1660, 6 cores (12 threads), 16GB RAM
Type (3): AMD Ryzen 7 3700U with Radeon Vega Mobile Gfx (2.30 GHz), 4 cores (8 threads), 16 GB RAM

Firstly note that type (3) is not powerful enough for full B,I sweeps saving the solution for each data point. This setup crashed after approx. 8-10 hours.
Type (2) is capable but about twice as slow as type (1) depending heavily on the exact specifications.
If access to type (1) computer is available that would be the best option.

A wall time example - bare NbSe2 simulation, 1-30 uA (step=1 uA), -150 to 150mT (61 points), up & down sweeps on device Type (2):

## Simulation Performance

**Total simulation time: 282.6 hours**

| Current (uA) | Time (hrs) |
|---|---|
| 1 | 10.0 |
| 2 | 10.8 |
| 3 | 10.2 |
| 4 | 10.2 |
| 5 | 10.4 |
| 6 | 10.5 |
| 7 | 10.5 |
| 8 | 10.7 |
| 9 | 10.5 |
| 10 | 10.5 |
| 11 | 10.5 |
| 12 | 10.0 |
| 13 | 9.9 |
| 14 | 9.8 |
| 15 | 9.9 |
| 16 | 9.8 |
| 17 | 10.0 |
| 18 | 9.9 |
| 19 | 10.0 |
| 20 | 9.8 |
| 21 | 9.7 |
| 22 | 9.6 |
| 23 | 9.6 |
| 24 | 9.5 |
| 25 | 9.3 |
| 26 | 9.1 |
| 27 | 8.3 |
| 28 | 7.1 |
| 29 | 3.1 |
| 30 | 3.2 |

* This same simulation on device Type (1) takes about 5-6 days.
* There is some variance in the time taken due to vortex dynamics and how the solver handles that. I = 29 uA e.g. is > I_c so it is fully superconducting.

It is possible to run these simulations on the CPU, but having a GPU speeds it up significantly.

### Software requirements

All the standard python libraries are required, such as numpy, matplotlib etc.
In addition, tdgl is required.
If running on the GPU, a version of cupy compatible with cuda for the GPU must be installed.
The recommended approach is to create an environment.
To do this, open anaconda prompt and type:
conda create --name tdgl python=3.10
conda activate tdgl
pip install tdgl
pip install cupy13x
Then to go in the environment type
conda activate tdgl
jupyter notebook

Ensure the tdgl_simulation.ipynb, parameters.py and io_functions.py files are all present in the working directory. It should then run.

Example of Type (2) system used to develop and run this code:

| Package | Version |
|---------|---------|
| Python | 3.11.15 |
| pyTDGL | 0.9.0 |
| NumPy | 1.26.4 |
| SciPy | 1.17.1 |
| Matplotlib | 3.7.5 |
| CuPy | 13.3.0 |
| Numba | 0.65.1 |

**Hardware:**
- CPU: 6 physical cores, 12 logical cores
- OS: Windows 10/11
- BLAS: Generic (consider installing Intel MKL or OpenBLAS for better performance)
 
# Data Structures

This project is written using a modular structure so the code is maintainable and different simulations can be run without changing the source code.

To run the script tdgl_simulation.ipynb one must load the modules parameters.py and io_functions.py into the same working directory.
io_functions contains the save/load functions:
- Here there is the option to choose between saving manually only useful attributes or saving the full solution.
- For the MSc project only the manual method was used, as it is computationally cheaper (~6 GB output H5 files rather than ~30GB) and the extra attributes saved in the full solution were not required. The main benefit of the full solution is it contains the applied vector potential and vorticity everywhere on the device for all regions of phase space.
- The structure of the output H5 file is a nested dictionary: all_sol[I_value][direction][B_value][dataset_name] e.g. accessed using:  voltage = all_sol[10]['up'][50.0]['voltage']
- parameters.py file contains all the constants, simulation parameters, and field setup values and can be modified to simulate different materials than NbSe2, and different sized devices (importantly thickness).
- Before running the tdgl_simulation.ipynb script, determine the heterostructure type: NbSe2 | CGT bilayer or CGT | NbSe2 | CGT trilayer using the MODEL variable in parameters.py

