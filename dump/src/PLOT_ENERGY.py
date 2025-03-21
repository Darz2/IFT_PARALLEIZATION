#!/usr/bin/env python

############# Required Packages s############
import pandas as pd, numpy as np, matplotlib.pyplot as plt
import PLOT_SETTINGS as ps
from matplotlib.ticker import MultipleLocator

############# Required Inputs #################
data                = pd.read_csv('TotEnergy.dat', delimiter=' ',skiprows=2, header=None)
tot_energy          = data.to_numpy()
timestep            = 0.5                               # fs
timestep            = tot_energy[:,0]*timestep*1e-6     # ns
T_energy            = tot_energy[:,1]
T_filtered          = pd.DataFrame(T_energy, columns=['Energy']).rolling(window=2000, win_type='gaussian', center=True).mean(std=500).to_numpy()

# print(T_energy.shape)
# print(timestep.shape)

#################### PLOT #####################
fig, ax = ps.plot_init()
    
plt.plot(timestep, T_energy, markersize=ps.markersize,
                markerfacecolor=ps.face_colors[0],
                markeredgecolor='k',
                markeredgewidth=ps.markeredgewidth,
                linestyle='solid',
                linewidth= ps.linewidth,
                color=ps.colors[0])
    
plt.plot(timestep, T_filtered, markersize=ps.markersize,
                linestyle='solid',
                linewidth= ps.linewidth,
                color='b')
    
plt.grid(True)
# plt.axvline(x=40, color='b', linestyle='--', linewidth=1)
# plt.axhline(y=-730, color='b', linestyle='--', linewidth=1)
    
plt.ylabel("Total_Energy")
plt.xlabel("t / [ns]")
ax.xaxis.set_major_locator(MultipleLocator(10))
    
ps.save_figure(fig, f"tot_energy.jpg")

#################### END OF CODE #####################