## Identification of Lagrangian Coherent Structures (LCS) and applications for machine learning

### Background and Motivation

The ocean is an energetic and turbulent environment with motions ranging from scales of a few centimeters to thousands of kilometers. Interactions across these spatial scales are very important in understanding the dynamics of large-scale circulation, as well as the transport and mixing of tracers (e.g., heat and salinity) throughout the ocean.

Ocean turbulence is dominated by mesoscale motions, which tends to self-organize into coherent vortices on the order of 100s of kilometers wide. These Lagrangian Coherent Structures (LCSs) trap and transport fluids over long distances and potentially play an important role in regulating climate. Mesoscale eddies are notoriously difficult to parametrize in coarse resolution ocean models, making their overall contribution to climate uncertain. Furthermore, identifying LCSs requires careful calculation of vorticity along Lagrangian particle paths.

### Model configuration


### LCS identification method

Lagrangian-averaged vorticity deviation



### Getting Started

#### Run and/or modify python scripts:

1. Fork the `lcs-ml` repository to your GitHub account.
2. Clone your fork locally using git.
```bash
git clone git@github.com:YOUR_GITHUB_USERNAME/lcs-ml.git
```
3. Connect to the upstream repository and create a new branch
```bash
cd ocetrac
git remote add upstream git@github.com:ocean-transport/lcs-ml.git
```
4. To fix a bug or add a feature, create your own branch of "main"
```bash
git checkout -b new-branch-name
```

5. Set up a conda environment with all the necessary dependencies.
```bash
conda env create -f environment.yml
conda activate lcs-ml
```

If you need some help with Git, follow this quick start guide: https://git.wiki.kernel.org/index.php/QuickStart


#### Access to the machine learning dataset

The dataset will be available from Zenodo. It includes a XX-member ensemble of year long simulations with daily potential vorticity fields and a mask for identified Lagrangian Coherent Structures. 


## Project Roadmap

![image](https://user-images.githubusercontent.com/1197350/111811323-4f888980-88ad-11eb-85d4-aae9a3dd4d84.png)
