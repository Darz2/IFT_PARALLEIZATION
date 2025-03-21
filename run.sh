#!/bin/bash

src="src"
fluid="CO2"
temperatures=(220) 
iter=1
block=1
sim=2

# Box dimensions
box_x=40
box_y=40
box_z=240

# Define regions dimensions
vapor1_zmin=0
liquid_zmin=75
liquid_zmax=165
vapor1_zmax=$liquid_zmin
vapor2_zmin=$liquid_zmax
vapor2_zmax=$box_z
liquid_width=$((liquid_zmax - liquid_zmin))
vapor1_width=$((vapor1_zmax - vapor1_zmin))
vapor2_width=$((vapor2_zmax - vapor2_zmin))

# echo "$liquid_width"
# echo "$vapor1_width"
# echo "$vapor2_width"

for T in ${temperatures[@]}
do
    for ((i=1; i<=block; i++))
    do
        for ((j=1; j<=sim; j++))
        do

            seed=$(( $iter * 1000))
            fold="T_${T}/block_${i}/sim_${j}"

            if [ "$1" == "single" ]; then
                fold="T_${T}"
            fi

            if [ -d ${fold} ]; then
                    rm -r ${fold}
            fi

            mkdir -p ${fold}
            
            molecules_RP_V=$(python REFPROP_input.py ${T} "${fluid}" 1 "[${box_x}, ${box_y}, ${vapor1_width}]")
            molecules_RP_L=$(python REFPROP_input.py ${T} "${fluid}" 0 "[${box_x}, ${box_y}, ${liquid_width}]")
            wait

            echo "The saturated liquid density at ${T} - molecules calculated by REFPROP is: $molecules_RP_L"
            echo "The saturated vapor  density at ${T} - molecules calculated by REFPROP is: $molecules_RP_V"

            cp src/simulation.in                        ./
            cp src/submit_D_NPT.sh                      ./
            cp src/submit_snellius.sh                   ./

            sed -i "s/T_VAL/${T}/g"                     simulation.in 
            sed -i "s/R_VAL/${seed}/g"                  simulation.in 
            sed -i "s/MOLECULES_L/${molecules_RP_L}/g"  simulation.in
            sed -i "s/MOLECULES_V/${molecules_RP_V}/g"  simulation.in
            sed -i "s/BOX_X/${box_x}/g"                 simulation.in
            sed -i "s/BOX_Y/${box_y}/g"                 simulation.in
            sed -i "s/BOX_Z/${box_z}/g"                 simulation.in
            sed -i "s/LIQUID_ZMIN/${liquid_zmin}/g"     simulation.in
            sed -i "s/LIQUID_ZMAX/${liquid_zmax}/g"     simulation.in
            sed -i "s/VAPOR1_ZMIN/${vapor1_zmin}/g"     simulation.in
            sed -i "s/VAPOR1_ZMAX/${vapor1_zmax}/g"     simulation.in
            sed -i "s/VAPOR2_ZMIN/${vapor2_zmin}/g"     simulation.in
            sed -i "s/VAPOR2_ZMAX/${vapor2_zmax}/g"     simulation.in

            sed -i "s/TEMP/${T}/g"                      submit_D_NPT.sh
            sed -i "s/BLOCK/${i}/g"                     submit_D_NPT.sh
            sed -i "s/SIM/${j}/g"                       submit_D_NPT.sh

            sed -i "s/TEMP/${T}/g"                      submit_snellius.sh
            sed -i "s/BLOCK/${i}/g"                     submit_snellius.sh
            sed -i "s/SIM/${j}/g"                       submit_snellius.sh

            mv simulation.in                            ${fold}
            mv submit_D_NPT.sh                          ${fold}
            mv submit_snellius.sh                       ${fold}

            cp src/CO2.mol                              ${fold}
            cp src/trappe_flex.FF                       ${fold}

            if [ "$1" == "single" ]; then
                break 2
            else
                iter=$((iter+1))
            fi

        done
    done
done