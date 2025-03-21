#!/bin/bash

#SBATCH -J CSVR_T_TEMP_B_BLOCK_S_SIM
#SBATCH -t 5-00:00:00
#SBATCH -p genoa
#SBATCH -N 1
#SBATCH --ntasks=32
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=d.raju@tudelft.nl

module load 2024
module load foss/2024a
export I_MPI_PMI_LIBRARY=/cm/shared/apps/slurm/current/lib64/libpmi2.so
lmp=~/Software/omp_lammps/build

srun --ntasks=32 --nodes=1 --cpus-per-task=1 --mem-per-cpu=1700 $lmp/lmp -in simulation.in -sf omp -pk omp 1 > slurm.out &
echo ${SLURM_STEPID}
wait