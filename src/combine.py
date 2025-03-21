#!/usr/bin/env python

import pandas as pd
import numpy as np

# Total energy File Combining

eq = pd.read_csv('TotEnergy_eq.dat', delimiter=' ', header=None,skiprows=2)
pr = pd.read_csv('TotEnergy_pr.dat', delimiter=' ', header=None,skiprows=2)

pr.iloc[:, 0] = pr.iloc[:, 0].astype(int) + 30000000
combined_df = pd.concat([eq, pr], ignore_index=True)
column_names = ["TimeStep","v_TotEn"]
combined_df.columns = column_names
combined_df.to_csv('TotEnergy.dat', index=False, header=True, sep=' ')

# Tensor File Combining

eq = pd.read_csv('pressure_tensor_eq.dat', delimiter=' ', header=None,skiprows=1)
pr = pd.read_csv('pressure_tensor_pr.dat', delimiter=' ', header=None,skiprows=2)

pr.iloc[:, 0] = pr.iloc[:, 0].astype(int) + 30000000
combined_df = pd.concat([eq, pr], ignore_index=True)
column_names = ['#STEP', 'Pxx', 'Pyy', 'Pzz']
combined_df.columns = column_names
combined_df.to_csv('pressure_tensor.dat', index=False, header=True, sep=' ')


# Density File Combining

eq = pd.read_csv('dens_eq.csv', delimiter=',', header=None,skiprows=1)
pr = pd.read_csv('dens_pr.csv', delimiter=',', header=None,skiprows=1)

pr.iloc[:, 0] = pr.iloc[:, 0].astype(int) + 30000000
combined_df = pd.concat([eq, pr], ignore_index=True)
column_names = ['#STEP'] + [f'group{i}' for i in range(1, 101)]
combined_df.columns = column_names
combined_df.to_csv('dens.csv', index=False, header=True, sep=' ')
