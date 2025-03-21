#!/usr/bin/env python

############# Required Packages s############
import pandas as pd, numpy as np, matplotlib.pyplot as plt
import PLOT_SETTINGS as ps
from matplotlib.ticker import MultipleLocator

############# Required Inputs #################
energy_dat          = pd.read_csv('Energy.dat', delimiter=' ',skiprows=2, header=None)
energy              = energy_dat.to_numpy()
timestep            = 0.5                             # fs
timestep            = energy[:,0]*timestep*1e-6
T_energy            = energy[:,5]
T_ecouple           = energy[:,6]
T_econserve         = energy[:,7]
T_filtered          = pd.DataFrame(T_energy, columns=['Energy']).rolling(window=500, win_type='gaussian', center=True).mean(std=100).to_numpy()
ecouple_filtered    = pd.DataFrame(T_ecouple, columns=['ecouple']).rolling(window=500, win_type='gaussian', center=True).mean(std=100).to_numpy()
enonserve_filtered  = pd.DataFrame(T_econserve, columns=['econserve']).rolling(window=500, win_type='gaussian', center=True).mean(std=100).to_numpy()

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
    
plt.ylabel(rf"Total Energy / [Kcal/mol]")
plt.xlabel(rf"t / [ns] ")
# plt.xlim(-10,1000)
# ax.xaxis.set_major_locator(MultipleLocator(10))
    
ps.save_figure(fig, f"tot_energy.jpg")

plt.clf()

#################### END OF PLOT-1 #####################

fig, ax = ps.plot_init()

plt.plot(timestep, T_econserve, markersize=ps.markersize,
                markerfacecolor=ps.face_colors[0],
                markeredgecolor='k',
                markeredgewidth=ps.markeredgewidth,
                linestyle='solid',
                linewidth= ps.linewidth,
                color=ps.colors[0])

plt.plot(timestep, enonserve_filtered, markersize=ps.markersize,
                linestyle='solid',
                linewidth= ps.linewidth,
                color='b')
  
plt.grid(True)
# plt.axvline(x=40, color='b', linestyle='--', linewidth=1)
# plt.axhline(y=-730, color='b', linestyle='--', linewidth=1)
    
plt.ylabel(rf"Nose-hoover Hamiltonian / [Kcal/mol]")
plt.xlabel(rf"t / [ns] ")
# plt.xlim(-10,1000)
# ax.xaxis.set_major_locator(MultipleLocator(10))
    
ps.save_figure(fig, f"econserve.jpg")

plt.clf()

#################### END OF PLOT-1 #####################

fig, ax = ps.plot_init()

plt.plot(timestep, T_ecouple, markersize=ps.markersize,
                markerfacecolor=ps.face_colors[0],
                markeredgecolor='k',
                markeredgewidth=ps.markeredgewidth,
                linestyle='solid',
                linewidth= ps.linewidth,
                color=ps.colors[0])

plt.plot(timestep, ecouple_filtered, markersize=ps.markersize,
                linestyle='solid',
                linewidth= ps.linewidth,
                color='b')
  
plt.grid(True)
# plt.axvline(x=40, color='b', linestyle='--', linewidth=1)
# plt.axhline(y=-730, color='b', linestyle='--', linewidth=1)
    
plt.ylabel(rf"Energy (thermostat) / [Kcal/mol]")
plt.xlabel(rf"t / [ns] ")
# plt.xlim(-10,1000)
# ax.xaxis.set_major_locator(MultipleLocator(10))
    
ps.save_figure(fig, f"ecouple.jpg")

plt.clf()

#################### END OF PLOT-2 #####################

def magnitude(px, py, pz):
    """
    Compute the magnitude of the vector from its x, y, and z components.

    Parameters:
    px (numpy array): component along x-axis
    py (numpy array): component along y-axis
    pz (numpy array): component along z-axis

    Returns:
    numpy array: Magnitude of the vector
    """
    return np.sqrt(px**2 + py**2 + pz**2)

momentum_dat        = pd.read_csv('Momentum.dat', delimiter=' ',skiprows=2, header=None)
momentum            = momentum_dat.to_numpy()
timestep            = 0.5  
timestep            = momentum[:,0]*timestep*1e-6
px                  = momentum[:,1]
py                  = momentum[:,2]
pz                  = momentum[:,3]
p_mag               = magnitude(px,py,pz)

fig, ax = ps.plot_init()


plt.plot(timestep, px, markersize=ps.markersize,
                markerfacecolor=ps.face_colors[0],
                markeredgecolor='b',
                markeredgewidth=ps.markeredgewidth,
                linestyle='solid',
                linewidth= ps.linewidth,
                color='b',
                label='px')

plt.plot(timestep, py, markersize=ps.markersize,
                markerfacecolor=ps.face_colors[0],
                markeredgecolor='c',
                markeredgewidth=ps.markeredgewidth,
                linestyle='solid',
                linewidth= ps.linewidth,
                color='c',
                label='py')

plt.plot(timestep, pz, markersize=ps.markersize,
                markerfacecolor=ps.face_colors[0],
                markeredgecolor='g',
                markeredgewidth=ps.markeredgewidth,
                linestyle='solid',
                linewidth= ps.linewidth,
                color='g',
                label='pz')

plt.plot(timestep, p_mag, markersize=ps.markersize,
                markerfacecolor=ps.face_colors[0],
                markeredgecolor='k',
                markeredgewidth=ps.markeredgewidth,
                linestyle='solid',
                linewidth= ps.linewidth,
                color=ps.colors[0],
                label='Magnitude')
  
plt.grid(True)
# plt.axvline(x=40, color='b', linestyle='--', linewidth=1)
# plt.axhline(y=-730, color='b', linestyle='--', linewidth=1)

ps.style_legend(ax, loc=2, ncol=1, borderaxespad=1)    
plt.ylabel(rf"Momentum / [$\AA$ g/fs mole]")
plt.xlabel(rf"t / [ns] ")
# plt.xlim(-10,1000)
# ax.xaxis.set_major_locator(MultipleLocator(10))
    
ps.save_figure(fig, f"momentum.jpg")

plt.clf()

#################### END OF PLOT-3 #####################

vx                  = momentum[:,4]
vy                  = momentum[:,5]
vz                  = momentum[:,6]

fig, ax = ps.plot_init()


plt.plot(timestep, vx, markersize=ps.markersize,
                markerfacecolor=ps.face_colors[0],
                markeredgecolor='b',
                markeredgewidth=ps.markeredgewidth,
                linestyle='solid',
                linewidth= ps.linewidth,
                color='b',
                label='v_x')

plt.plot(timestep, vy, markersize=ps.markersize,
                markerfacecolor=ps.face_colors[0],
                markeredgecolor='c',
                markeredgewidth=ps.markeredgewidth,
                linestyle='solid',
                linewidth= ps.linewidth,
                color='c',
                label='v_y')

plt.plot(timestep, vz, markersize=ps.markersize,
                markerfacecolor=ps.face_colors[0],
                markeredgecolor='g',
                markeredgewidth=ps.markeredgewidth,
                linestyle='solid',
                linewidth= ps.linewidth,
                color='g',
                label='v_z')

plt.grid(True)
# plt.axvline(x=40, color='b', linestyle='--', linewidth=1)
# plt.axhline(y=-730, color='b', linestyle='--', linewidth=1)

ps.style_legend(ax, loc=3, ncol=1, borderaxespad=1)    
plt.ylabel(rf"COM velocity / [$\AA/fs$]")
plt.xlabel(rf"t / [ns] ")
# plt.xlim(-10,1000)
# ax.xaxis.set_major_locator(MultipleLocator(10))
    
ps.save_figure(fig, f"COM_velocity.jpg")

plt.clf()

#################### END OF PLOT-4 #####################