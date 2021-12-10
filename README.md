# Simulation and Identification of Lagrangian Coherent Structures

## 1. Background & Motivation

The ocean is an energetic and turbulent environment with motions ranging from scales of a few centimeters to thousands of kilometers. Interactions across these spatial scales are very important in setting up the large-scale circulation of the ocean, as well as transporting and mixing tracer fields (e.g., heat and salinity).

<p align="center">
  <img src="https://github.com/ocean-transport/lcs-ml/blob/main/media/perpetual_ocean.gif">
</p>

Ocean turbulence is dominated by mesoscale motions, which tend to self-organize into coherent vortices on the order of 100s of kilometers in scale. These **Lagrangian Coherent Structures** (LCSs) trap and transport fluids over long distances and potentially play an important role in regulating climate. Mesoscale eddies are notoriously difficult to parametrize in coarse resolution ocean models, making their overall contribution to the climate uncertain. Furthermore, identifying LCSs requires careful calculations of vorticity along Lagrangian particle paths. The goals of this project are to simulate and identify LCSs using the **Lagrangian-Averaged Vorticity Deviation** (LAVD) method. A new labeled dataset of LCSs, PV, and strain fields are produced as a training dataset for machine learning applications. 

## 2. Model Initialization 

We use `pyqg` to simulate a two-layer quasigeostrophic (QG) turbulent system driven by eastward mean shear. We configure the model to mimic the dynamics of the Southern Ocean following the set-up by Zhang et al. [(2020)](https://github.com/ocean-transport/lcs-ml/blob/main/papers/Zhang_etal_2020.pdf). The model is run with a double-periodic domain that is 1200 km on each side and has a horizontal resolution of 512 x 512 grid points. The parameters of the simulation are stored in a [`config.yml`](https://github.com/ocean-transport/lcs-ml/blob/main/config.yml) file. 

The model is spun up from an initial random state, and after some time, coherent vortices begin to self organize. Below are four snapshots of the upper layer potential vorticity anomaly evolving during the begining of the initial spin up.  

<p align="center">
  <img width=40% height=40% src="https://github.com/ocean-transport/lcs-ml/blob/main/media/spin_up.gif">
</p>

<p align="center">
  <img src="https://github.com/ocean-transport/lcs-ml/blob/main/media/spin_up_PV.png">
</p>

The model is spun up for 50 years and saved at monthly (30-day) intervals. There are no leap years, so each year has 365 days. 

As the model gets spun up, the mean eddy kinetic energy (EKE) increases until it reaches an equilibrated state. When the EKE plateaus the model is considered to be in a stable state. The time series of EKE in each layer levels off around 50 years.

<p align="center">
  <img src="https://github.com/ocean-transport/lcs-ml/blob/main/media/spin_up_EKE_semilog.png">
</p>

<p align="center">
  <img src="https://github.com/ocean-transport/lcs-ml/blob/main/media/spin_up_EKE_central_diff.png">
</p>

The equilibrated model state is saved at year 50 and used to initialize the large ensemble of lagrangian particles.


## 3. Large Ensemble

The Large Ensemble is initialized with the year 50 PV anomaly field from the equilibrated state using the same model configuration. Each ensemble member differs slightly by perturbing the PV anomaly at a single grid cell near the middle of the domain. This randomness is enough for the members to diverge. The perturbation for each ensemble member is dictated by a unique seed number. This ensures that the ensemble members are completely reproducible. 

A total of 1,048,576 lagrangian particles are seeded every half grid point and advanced using the gridded u and v velocity fields. In addition to the X and Y position, two scalar quantities are computed along particle paths. They are relative vorticity, 

![eq](https://latex.codecogs.com/svg.latex?\Large&space;\zeta=\nabla^{2}\psi) ,

and strain magnitude,
 
![eq](https://latex.codecogs.com/svg.latex?\Large&space;\sigma=\sqrt{\sigma_n^2+\sigma_s^2}) ,

where ![eq1](https://latex.codecogs.com/svg.latex?\Large&space;\sigma_n) and ![eq1](https://latex.codecogs.com/svg.latex?\Large&space;\sigma_s) are the normal and shear strain respectively, such that

![eq](https://latex.codecogs.com/svg.latex?\Large&space;\sigma_n=-2\frac{\partial^2}{\partial_x\partial_y}\psi) 

and 

![eq](https://latex.codecogs.com/svg.latex?\Large&space;\sigma_s=\frac{\partial^2\psi}{\partial_x^2}-\frac{\partial^2\psi}{\partial_y^2}).

We solve the above equations in spectral space before using the inverse FFT to transform back to the time domain. Spectral computations are faster and computationally more efficient. 

The stream function is also saved for the model domain at each time integration. 


## 4. Getting Started

### Run and/or modify python scripts:

1. Fork the `lcs-ml` repository to your GitHub account.

2. Clone your fork locally using git.
```bash
git clone git@github.com:YOUR_GITHUB_USERNAME/lcs-ml.git
```

3. Connect to the upstream repository and create a new branch
```bash
cd lcs-ml
git remote add upstream git@github.com:ocean-transport/lcs-ml.git
```

4. To fix a bug or add a feature, create your own branch off "main"
```bash
git checkout -b new-branch-name main
```

5. Set up a conda environment with all the necessary dependencies.
```bash
conda env create -f environment.yml
conda activate lcs-ml
```
If you need some help with Git, follow this [quick start guide](https://git.wiki.kernel.org/index.php/QuickStart).

6. To rerun the control simulation, submit the [batch script](https://github.com/ocean-transport/lcs-ml/blob/main/spin_up/spin_up.sh) via slurm. You will need to modifuly the config and output file directories accordingly. 
```bash
sbatch spin_up.sh
```

7. To generate the ensemble, submit this [batch script](https://github.com/ocean-transport/lcs-ml/blob/main/ensemble_particle_generator/ensemble_generator.sh) using [job array](https://slurm.schedmd.com/job_array.html), again modifying file paths to match your directory. In this example, we are generature 40,000 ensemble members. 
```bash
sbatch --array=1-40000 ensemble_generator.sh
```

To check the progress of sbatch jobs, you can either check the auto-generated `slurm-******.out` file or type
```bash
squeue -u [$USER_NAME]
```

### Access the labeled dataset:

Each ensemble member is saved as a unique zarr store on Ginsburg and can be accessed here: `/burg/abernathey/users/hillary/lcs/pyqg_ensemble/####.zarr`
The entire 50 year spin is saved as a zarr store and can be accessed here: `/burg/abernathey/users/hillary/lcs/spin_up/spin_up.zarr`
The 50 year snapshot is stored as netCDF and can be accessed here: `/burg/abernathey/users/hillary/lcs/spin_up/QG_steady_50.nc`

The dataset will be available from Zenodo. It includes the XX-member ensemble of 90-day simulations with daily particle position, vorticity, strain, and background streamfunction.

This ensemble will also become available on the cloud via Pangeo-forge. More details will be provided soon. 

# Load data from Ginsburg

## Origonal Project Roadmap

![image](https://user-images.githubusercontent.com/1197350/111811323-4f888980-88ad-11eb-85d4-aae9a3dd4d84.png)
