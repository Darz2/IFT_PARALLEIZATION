#!/bin/bash

#SBATCH -J cutoff_14
#SBATCH --time 3-00:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=16
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=1G
#SBATCH --partition=compute-p2
#SBATCH --account=research-me-pe

module load 2024r1
module load fftw openmpi
export NUM_OMP_THREADS=1

lmp=~/Software/LAMMPS/omp_lammps_double/build
srun $lmp/lmp -in simulation.in -sf omp -pk omp 1 > slurm.out
wait