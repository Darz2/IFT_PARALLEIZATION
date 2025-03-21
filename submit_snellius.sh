#!/bin/bash

#SBATCH -J Eff
#SBATCH -t 1-00:00:00
#SBATCH -p genoa
#SBATCH -N 1
#SBATCH --ntasks=48
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=d.raju@tudelft.nl

dir=(1 2 4 8 12 16)

module load 2024
module load foss/2024a
export I_MPI_PMI_LIBRARY=/cm/shared/apps/slurm/current/lib64/libpmi2.so
lmp=~/Software/omp_lammps/build


for D in ${dir[@]}
do  
    echo $D
    cd $D

    srun --ntasks="$D" --nodes=1 --cpus-per-task=1 --mem-per-cpu=1700 bash -c '
            echo "Directory '"$D"' has Step ID: ${SLURM_JOB_ID}.${SLURM_STEP_ID}"
            '"$lmp"'/lmp -in simulation.in -sf omp -pk omp 1
        ' > slurm_"$D".out &
    cd -

done

wait
sleep 2

echo "Elapsed times including step IDs:"
sacct -j ${SLURM_JOB_ID} --format=JobID,JobName,Elapsed,ElapsedRaw --parsable2