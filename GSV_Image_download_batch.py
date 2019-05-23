#!/bin/bash -1
#SBATCH -J GSV_Images
#SBATCH -e GSVImage_error_%j
#SBATCH -o GSVImage_out_%j
#SBATCH --mail-type=ALL
#SBATCH --mail-user=email
#SBATCH -t 01:00:00
#SBATCH -n 1
#SBATCH -p serial

module load geoconda
cd /wrk/username
srun GSV_image_downloader.py