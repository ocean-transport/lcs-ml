#!/bin/sh
#
# Generates ensembles of QG model run from equilibrated state
#
#SBATCH --account=abernathey     # group account name
#SBATCH --job-name=ensembles     # job name
#SBATCH -c 5                     # number of cpu cores to use (up to 32 cores per server)
#SBATCH --time=0-02:00           # time the job will take to run in D-HH:MM
#SBATCH --mem-per-cpu=20G         # The memory the job will use per cpu core
 
echo "$SLURM_ARRAY_TASK_ID"

module load anaconda/3-2021.05
conda init bash

source ~/.bashrc
conda activate lcs-ml

export PICKUP_FILE='/burg/abernathey/users/hillary/pyqg_spin_up/84672000.nc'
export CONFIG_FILE='/burg/home/hs3277/lcs-ml/config.yml'

python ensemble_generator.py $SLURM_ARRAY_TASK_ID $PICKUP_FILE $CONFIG_FILE
