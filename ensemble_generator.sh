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

module load anaconda
source ~/.bashrc
conda activate lcs-dev

python ensemble_generator.py