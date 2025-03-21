#!/usr/bin/env python

############# Required Packages ############
import os, subprocess, pandas as pd, numpy as np, matplotlib.pyplot as plt, CoolProp.CoolProp as CP
import PLOT_SETTINGS as ps
from matplotlib.ticker import MultipleLocator
REFPROP_PATH = os.path.expanduser('~/Software/REFPROP/REFPROP-cmake/build')
subprocess.run(["julia", "POST.jl"], check=True)

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
CP.set_config_string(CP.ALTERNATIVE_REFPROP_PATH, REFPROP_PATH)
fluid = "CO2"
state = CP.AbstractState("REFPROP", fluid)

############# Required Inputs #################
timestep        = 0.5
eq_ns           = 5
pr_ns           = 15
nbin            = 100
equilibration   = int(eq_ns*timestep*1e3)
production      = int(pr_ns*timestep*1e3)
z_length        = int(bash('grep "lz=" CO2.log | awk \'NR==2\' | cut -d\'=\' -f2'))
T               = int(bash('grep "TEMP_INDEX" CO2.log | awk \'NR==1\' | cut -d \' \' -f11'))
rho_liquid_RP   = CP.PropsSI("D", "T", T, "Q", 0, fluid)
rho_vapor_RP    = CP.PropsSI("D", "T", T, "Q", 1, fluid)

print(f"########### Densities from {state.backend_name()} ##############")
print(f"Saturated vapor density at {T} K: {rho_vapor_RP:.2f}  [kg/m3]")
print(f"Saturated liquid density at {T} K: {rho_liquid_RP:.2f} [kg/m3]")

data            = pd.read_csv('dens.csv', delimiter=',', header=None)
density         = data.to_numpy()
nrows           = density.shape[0]
ncolumns        = density.shape[1]
ave_dens        = density[equilibration:production,0:ncolumns].mean(axis =0)
ave_dens        = ave_dens*1000                     # Kg/m3
z_interval      = np.linspace(0.005, 0.995, nbin)
z_spacings      = z_interval * z_length

slope           = np.diff(ave_dens) / np.diff(z_spacings)
plateau_indices = np.where(np.abs(slope) < 1)[0]
plateau_x       = z_spacings[plateau_indices]
gaps            = np.diff(plateau_indices)
split_indices   = np.where(gaps > 1)[0]
plateau_groups  = np.split(plateau_indices, split_indices + 1)
plateau_regions = []

for group in plateau_groups:
    if len(group) > 0:
        plateau_regions.append((z_spacings[group], ave_dens[group]))      

if len(plateau_regions) >= 3:
    print("Number of plateau regions is:", len(plateau_regions))
    for i, region in enumerate(plateau_regions):
        print(f"Plateau {i+1} shape: {region[0].shape}")
        
    print("########### Filtration ##############")
    plateau_regions = [(index, arr) for index, arr in plateau_regions if arr.shape[0] >= 10]

    for i, region in enumerate(plateau_regions):
        if i == 0 :
            print(f"Left region gas data points: {region[0].shape}")
        elif i == 1 :
            print(f"Liquid data points: {region[0].shape}")
        elif i == 2:
            print(f"Right region gas data points: {region[0].shape}")
            
rho_gas_left    = np.mean(plateau_regions[0][1])
rho_gas_right   = np.mean(plateau_regions[2][1])
rho_gas         = 0.5*(rho_gas_left + rho_gas_right)
rho_liquid      = np.mean(plateau_regions[1][1])

print("########### Densities from MD ##############")
print(rf"Saturated vapor density at {T} K: {rho_gas:.4f} [kg/m3]")
print(rf"Saturated liquid density at {T} K: {rho_liquid:.4f} [kg/m3]")

thickness_start             = rho_liquid + 0.9*(rho_gas-rho_liquid)
thickness_end               = rho_liquid + 0.1*(rho_gas-rho_liquid)
thickness_indices_start_1   = np.abs(ave_dens[:50] - thickness_start).argmin()
thickness_indices_end_1     = np.abs(ave_dens[:50] - thickness_end).argmin()
thickness_indices_start_2   = (np.abs(ave_dens[-50:] - thickness_start).argmin()) + 50
thickness_indices_end_2     = (np.abs(ave_dens[-50:] - thickness_end).argmin()) + 50
left_delta                  = z_spacings[thickness_indices_end_1]   - z_spacings[thickness_indices_start_1]
right_delta                 = z_spacings[thickness_indices_start_2] - z_spacings[thickness_indices_end_2]
delta                       = 0.5*(left_delta + right_delta)

print("########### Interfacial thickness ##############")
print(rf"Interfacial Thickness (Delta):  {delta*0.1:.4f} [nm] ")

# z0 = z_spacings[thickness_indices_start_1]+(0.5*delta)
# print(rf"Reference Coordinate (Z0):  {z0:.4f}")

#################### PLOT #####################
fig, ax = ps.plot_init()

plt.plot(z_spacings, ave_dens, markersize=ps.markersize,
            markerfacecolor='r',
            markeredgecolor='k',
            markeredgewidth=ps.markeredgewidth,
            linestyle='solid',
            linewidth= ps.linewidth,
            color='r')

plt.plot(plateau_regions[0][0],plateau_regions[0][1], marker='o',
            markersize=ps.markersize, markeredgewidth=ps.markeredgewidth, linestyle='', color='b', label='Gas')
plt.plot(plateau_regions[1][0],plateau_regions[1][1], marker='o',
            markersize=ps.markersize, markeredgewidth=ps.markeredgewidth, linestyle='', color='g', label='Liquid')
plt.plot(plateau_regions[2][0],plateau_regions[2][1], marker='o',
            markersize=ps.markersize, markeredgewidth=ps.markeredgewidth, linestyle='', color='b')

plt.ylabel(r"Density / [kg/m3]")
plt.xlabel(r"Z / [A]")
    
ax.xaxis.set_major_locator(MultipleLocator(50))
ax.xaxis.set_minor_locator(MultipleLocator(25))
ax.yaxis.set_major_locator(MultipleLocator(200))
ax.yaxis.set_minor_locator(MultipleLocator(100))

ps.style_legend(ax, loc=1, ncol=1, borderaxespad=1)
ps.save_figure(fig, f"density_CO2.jpg")

############################# END OF CODE ###########################