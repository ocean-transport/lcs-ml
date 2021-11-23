# Simulation and Identification of Lagrangian Coherent Structures

## 1. Background & Motivation

The ocean is an energetic and turbulent environment with motions ranging from scales of a few centimeters to thousands of kilometers. Interactions across these spatial scales are very important in setting up the large-scale circulation of the ocean, as well as transporting and mixing tracer fields (e.g., heat and salinity).

![Perpetual Ocean](https://github.com/ocean-transport/lcs-ml/blob/main/media/perpetual_ocean.gif)

Ocean turbulence is dominated by mesoscale motions, which tend to self-organize into coherent vortices on the order of 100s of kilometers in scale. These **Lagrangian Coherent Structures** (LCSs) trap and transport fluids over long distances and potentially play an important role in regulating climate. Mesoscale eddies are notoriously difficult to parametrize in coarse resolution ocean models, making their overall contribution to the climate uncertain. Furthermore, identifying LCSs requires careful calculations of vorticity along Lagrangian particle paths. The goals of this project are to simulate and identify LCSs using the **Lagrangian-Averaged Vorticity Deviation** (LAVD) method. A new labeled dataset of LCSs, PV, and strain fields are produced as a training dataset for machine learning applications. 

## 2. Model Initialization 

We use `pyqg` to simulate a two-layer quasigeostrophic (QG) turbulent system driven by eastward mean shear. We configure the model to mimic the dynamics of the Southern Ocean following the set-up by Zhang et al. [(2020)](https://github.com/ocean-transport/lcs-ml/blob/main/papers/Zhang_etal_2020.pdf). The model is run with a double-periodic domain that is 1200 km on each side and has a horizontal resolution of 512 x 512 grid points. The parameters of the simulation are stored in a [`config.yml`](https://github.com/ocean-transport/lcs-ml/blob/main/config.yml) file. 

The model is spun up from an initial random state, and after some time, coherent vortices begin to self organize. Below are four snapshots of the upper layer potential vorticity anomaly evolving during the begining of the initial spin up.  

![sping_up_mov](/https://github.com/ocean-transport/lcs-ml/blob/main/spin_up.mov)

![spin_up_PV](https://github.com/ocean-transport/lcs-ml/blob/main/media/spin_up_PV.png)

The model is spun up for a total of 10 years and saved at pentad (5-day) intervals. 

As the model gets spun up, the mean eddy kinetic energy (EKE) increases until it reaches an equilibrated state. When the EKE plateaus the model is considered to be in a stable state. The time series of EKE in each layer levels off around **XX** years.

![spin_up_EKE](https://github.com/ocean-transport/lcs-ml/blob/main/media/spin_up_EKE.png)

The equilibrated model state is saved and used to initialize the large ensemble of `pyqg` simulations.


## 3. `pyqg` Large Ensemble

The Large Ensemble is initialized with the PV anomaly field from the equilibrated state using the same model configuration. Each ensemble member differs slightly by perturbing the PV anomaly at a single grid cell near the middle of the domain. This randomness is enough for the members to diverge and is generated using a unique seed number. This ensures that the ensemble member perturbations are completely reproducible. 

A total of 1,048,576 lagrangian particles are seeded every half grid point and advanced using the gridded velocity field. Relative vorticity (eq. 1) and strain magnitude (eq. 1) are caclulated for each particle. 


Test equation

![eq1](https://latex.codecogs.com/svg.latex?\Large&space;x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}) 




## 4. LCS Identification 


Lagrangian-averaged vorticity deviation ...


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
If you need some help with Git, follow this quick start guide: https://git.wiki.kernel.org/index.php/QuickStart




### Access the labeled dataset:

The dataset will be available from Zenodo. It includes an XX-member ensemble of year long simulations with daily potential vorticity and strain fields, as well as a mask for identified LCSs. 


## Project Roadmap

![image](https://user-images.githubusercontent.com/1197350/111811323-4f888980-88ad-11eb-85d4-aae9a3dd4d84.png)
