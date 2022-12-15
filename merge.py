import json
import requests
import glob, os
import pandas as pd
import datetime as dt


data_path = 'data/'
csv_files = glob.glob(os.path.join(data_path, '*.csv'))

df = pd.concat(map(pd.read_csv, csv_files), ignore_index=True)
print(df)

print('\n')

# calculate all costs grouped by the namespace
ddf = df.groupby(by=['Namespace'])[['CpuCost', 'GpuCost', 'RamCost', 'PvCost', 'NetworkCost', 'SharedCost', 'TotalCost']].sum()
print(ddf)

ddf.to_csv('final.csv')