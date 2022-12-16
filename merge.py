import os
import glob
import pandas as pd


data_path = 'data/'
csv_files = glob.glob(os.path.join(data_path, '*.csv'))

# merge all csv files untill current day to one
df = pd.concat(map(pd.read_csv, csv_files), ignore_index=True)
df.to_csv('all.csv', index=False)

# calculate all costs grouped by namespace
dff = df.groupby(by=['Namespace'])[['CpuCost', 'GpuCost', 'RamCost', 'PvCost', 'NetworkCost', 'SharedCost', 'TotalCost']].sum()

# export the final csv which contains current cost per namespace untill current day
dff.to_csv('final.csv', index=False)