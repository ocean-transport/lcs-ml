#!/bin/sh
#
# Saves spin up experiment to equilibrated state
#
#SBATCH --account=abernathey     # group account name
#SBATCH --job-name=spin_up       # job name
#SBATCH -c 1                     # number of cpu cores to use (up to 32 cores per server)
#SBATCH --time=1-06:00           # time the job will take to run in D-HH:MM
#SBATCH --mem-per-cpu=20G        # The memory the job will use per cpu core

module load anaconda/3-2021.05
conda init bash
source ~/.bashrc
conda activate lcs-ml

export CONFIG_FILE='/burg/home/hs3277/lcs-ml/config.yml'
export OUT_FILE='/burg/abernathey/users/hillary/lcs/spin_up/spin_up.zarr'

python spin_up.py $CONFIG_FILE $OUT_FILE
