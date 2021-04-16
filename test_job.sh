#!/bin/sh
#
# Simple "Hello World" submit script for Slurm.
#
# Replace ACCOUNT with your account name before submitting.
#
#SBATCH --account=abernathey        # Replace ACCOUNT with your group account name
#SBATCH --job-name=HelloWorld    # The job name
#SBATCH -c 1                     # The number of cpu cores to use (up to 32 cores per server)
#SBATCH --time=0-0:30            # The time the job will take to run in D-HH:MM
#SBATCH --mem-per-cpu=5G         # The memory the job will use per cpu core
 

 
echo "Hello World $SLURM_ARRAY_TASK_ID"
sleep 10
date
 
# End of script