#!/usr/bin/env python

############# Required Packages ############
import os, subprocess, pandas as pd, numpy as np, CoolProp.CoolProp as CP
REFPROP_PATH = os.path.expanduser('~/Software/REFPROP/REFPROP-cmake/build')

############# Required Functions ############
def bash(command):
    try:
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        result.check_returncode()
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}\nError: {e.stderr.strip()}")
        return None
    
########################### REFPROP ##########################
CP.set_config_string(CP.ALTERNATIVE_REFPROP_PATH, '~/Software/REFPROP/REFPROP-cmake/build')
fluid = "CO2"
state = CP.AbstractState("REFPROP", fluid)

############# Conversion Constants ############
A2m     = 1e-10         # Angstrom to meter
atm2Pa  = 101325        # Atmosphere to Pascal
N2mN    = 1e3           # Newton to milliNewton

############# Required Inputs #################
z_length        = int(bash('grep "lz=" CO2.log | awk \'NR==2\' | cut -d\'=\' -f2'))
T               = int(bash('grep "TEMP_INDEX" CO2.log | awk \'NR==1\' | cut -d \' \' -f11'))
timestep        = 0.5
IFT_RP          = round(CP.PropsSI('I','T',T,'Q', 1,fluid),6)
data            = pd.read_csv('pressure_tensor.dat', delimiter=' ', header=None,skiprows=1)
p_tensor        = data.to_numpy()
eq_ns           = 10
pr_ns           = 50

# print(p_tensor.shape)
# print(pxx.shape)

############# Interfacial Tension Computation #################
equilibration             = int(eq_ns*timestep*1e3)
production                = int(pr_ns*timestep*1e3)
pxx, pyy, pzz             = (p_tensor[equilibration:production, i] for i in range(1, 4))
pxx_avg, pyy_avg, pzz_avg = (np.mean(p) for p in (pxx, pyy, pzz))
IT_real                   = 0.5*z_length*(pzz_avg-(0.5*(pxx_avg+pyy_avg)))
IT_SI                     = IT_real*A2m*atm2Pa*N2mN

print("########### Interfacial Tension ##############")
print(rf"Interfacial Tension at {T} K from MD : {IT_SI:.4f} [mN/m]")
print(rf'The Interfacial Tension at {T} K from {state.backend_name()} [mN/m]: {round(IFT_RP*1e3,4)} [mN/m]')

############################# END OF CODE ###########################