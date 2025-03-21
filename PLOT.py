#!/usr/bin/env python

############# Required Packages ############
import pandas as pd, numpy as np, matplotlib.pyplot as plt
import PLOT_SETTINGS as ps
from matplotlib.ticker import MultipleLocator

############# Functions ############

def compute_speedup(serial_time, parallel_time, num_processors):
    """
    Computes the speedup and parallel efficiency of a parallel program.

    Parameters:
        serial_time (float): Execution time using one processor (sequential).
        parallel_time (float): Execution time using multiple processors.
        num_processors (int): Number of processors used.

    Returns:
        tuple: (speedup, parallel_efficiency)
    """
    speedup = serial_time / parallel_time
    parallel_efficiency = (speedup / num_processors)*100
    
    return speedup, parallel_efficiency

############# Required Inputs #################
energy_dat          = pd.read_csv('runtime.dat', delimiter=' ',skiprows=2, header=None)
energy              = energy_dat.to_numpy()
CPUs                = energy[:,0]
TIME_s              = energy[:,1]
SPEEDUP             = []
EFF                 = []

# print(CPUs[0])
# print(TIME_s[0])

for i, j in zip(CPUs,TIME_s):
    
    speedup, efficiency = compute_speedup(TIME_s[0], j , i)
    SPEEDUP.append(speedup)
    EFF.append(efficiency)

print(SPEEDUP)
print(EFF)

##################### PLOT #####################
fig, ax = ps.plot_init()

plt.plot(CPUs, SPEEDUP, marker= 'o',
                markersize=ps.markersize,
                markerfacecolor=ps.face_colors[0],
                markeredgecolor='k',
                markeredgewidth=ps.markeredgewidth,
                linestyle='solid',
                linewidth= ps.linewidth,
                color=ps.colors[0])
    
plt.grid(True)
# plt.axvline(x=40, color='b', linestyle='--', linewidth=1)
# plt.axhline(y=-730, color='b', linestyle='--', linewidth=1)
    
plt.ylabel(rf"Speedup",fontsize=12)
plt.xlabel(rf"Number of cores",fontsize=12)
plt.xticks([0, 4, 8, 12, 16, 20, 24, 28, 32])
plt.xlim(0,33)
plt.ylim(0,20)
ax.yaxis.set_major_locator(MultipleLocator(4))
ax.yaxis.set_minor_locator(MultipleLocator(2))
ax.xaxis.set_major_locator(MultipleLocator(4))
ax.xaxis.set_minor_locator(MultipleLocator(2))
   
ps.save_figure(fig, f"speedup.jpg")

plt.clf()

##################### END OF PLOT-1 #####################

fig, ax = ps.plot_init()

plt.plot(CPUs, EFF, marker= 'o',
                markersize=ps.markersize,
                markerfacecolor=ps.face_colors[0],
                markeredgecolor='k',
                markeredgewidth=ps.markeredgewidth,
                linestyle='solid',
                linewidth= ps.linewidth,
                color=ps.colors[0])
  
plt.grid(True)
# plt.axvline(x=40, color='b', linestyle='--', linewidth=1)
# plt.axhline(y=-730, color='b', linestyle='--', linewidth=1)
    
plt.ylabel(rf"Parallel Efficiency (%) ",fontsize=12)
plt.xlabel(rf"Number of cores",fontsize=12)
plt.xlim(0,33)
plt.ylim(45,102)
ax.yaxis.set_major_locator(MultipleLocator(10))
ax.yaxis.set_minor_locator(MultipleLocator(5))
ax.xaxis.set_major_locator(MultipleLocator(4))
ax.xaxis.set_minor_locator(MultipleLocator(2))
    
ps.save_figure(fig, f"efficiency.jpg")

plt.clf()

##################### END OF PLOT-2 #####################