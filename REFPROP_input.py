#!/usr/bin/env python

import sys, os, CoolProp.CoolProp as CP, numpy as np, json
from scipy.constants import Avogadro
from molmass import Formula

refprop_path = os.path.expanduser('~/Software/REFPROP/REFPROP-cmake/build')
CP.set_config_string(CP.ALTERNATIVE_REFPROP_PATH, refprop_path)

def calculate_molecules(temperature, fluid, quality, box_dimensions):
    
    state = CP.AbstractState("REFPROP", fluid)
    formula = Formula(fluid)
    molar_mass = formula.mass  # g/mol
    
    # Determine density based on quality
    if quality == 0:
        density = CP.PropsSI("D", "T", temperature, "Q", 0, fluid)  # Liquid density
    elif quality == 1:
        density = CP.PropsSI("D", "T", temperature, "Q", 1, fluid)  # Vapor density
    else:
        raise ValueError("Quality must be 0 (liquid) or 1 (vapor)")
    
    # print(box_dimensions)
    
    # Convert box dimensions to meters
    box_dimensions = [dim * 1e-10 for dim in box_dimensions]
    
    # Calculate volume in cubic meters
    volume = box_dimensions[0] * box_dimensions[1] * box_dimensions[2]
    
    # Calculate mass in grams
    mass = (density * volume) * 1e3
    
    # Convert mass to moles
    moles = mass / molar_mass
    
    # Calculate number of molecules
    molecules = moles * Avogadro
    
    return molecules

if __name__ == "__main__":
    temperature     = int(sys.argv[1])
    fluid           = str(sys.argv[2])
    quality         = int(sys.argv[3])          # System quality (0 for liquid, 1 for vapor)
    box_dimensions  = json.loads(sys.argv[4])   # Angstrom
    molecules       = calculate_molecules(temperature, fluid, quality, box_dimensions)

    print(f"{molecules:.0f}")