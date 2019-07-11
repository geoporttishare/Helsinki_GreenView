#!/bin/bash -l
#SBATCH -J GVI_calculation
#SBATCH -e GVI_array_error_%A_%a
#SBATCH -o GVI_array_out_%A_%a
#SBATCH -t 23:59:00
#SBATCH -n 1
#SBATCH -p serial
#SBATCH --array=0,10,11,12,14,15,16,17,18,19,2,20,22,23,24,25,26,27,29,3,30,31,32,33,34,37,38,39,4,40,41,42,43,44,46,48,5,50,52,54,59,6,63,8

module purge
module load gcc/4.9.3
module load intelmpi/5.1.1
module load mkl/11.3.0
module load python/2.7.10
source /homeappl/home/username/venv_treepedia/bin/activate 
cd /wrk/username
srun python GreenView_local_calculator.py $SLURM_ARRAY_TASK_ID
