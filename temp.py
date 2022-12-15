import json
import requests

import pandas as pd
import datetime as dt

from azure.storage.blob import BlobServiceClient

# set the current date
current_date = dt.datetime.now().strftime("%Y_%m_%d-%H:%M:%S")

# KubeCost API url
url = "http://20.4.129.247:9090/model/aggregatedCostModel"

# Use the requests library to make a GET request to the KubeCost API
params = (
    ("window", "7d"),   # parameter
    ("aggregation", "namespace"),
    ("format", "json"),
)

try:
    response = requests.get(
        url,
        params=params,
    )
except requests.exceptions.HTTPError as err:
    print(err)


# Parse the response as JSON
jsondata = response.json()

# insert totalCost per namespace into array
costs = []
for namespace in jsondata['data']:

    aggregation = jsondata['data'][namespace]['aggregation']
    cpuCost = jsondata['data'][namespace]['cpuCost']
    gpuCost = jsondata['data'][namespace]['gpuCost']
    ramCost = jsondata['data'][namespace]['ramCost']
    pvCost = jsondata['data'][namespace]['pvCost']
    networkCost = jsondata['data'][namespace]['networkCost']
    sharedCost = jsondata['data'][namespace]['sharedCost']
    totalCost = jsondata['data'][namespace]['totalCost']

    # append the namespace and totalCost
    costs.append([current_date, aggregation, namespace, cpuCost, gpuCost, ramCost, pvCost, networkCost, sharedCost, totalCost])


# get dataframe from costs with named columns
# df = pd.DataFrame(costs, columns = ['Date', 'Aggregation', 'NameSpace', 'CpuCost', 'GpuCost', 'RamCost', 'PvCost', 'NetworkCost', 'SharedCost', 'TotalCost'])
df = pd.DataFrame(costs)

# write data to local csv file
local_csv_file = "./kube-data.csv"
df.to_csv(local_csv_file, index=False, header=False)

## TODO: merge each csv to one ##

with open(local_csv_file, 'r') as f1:
    new_csv_file = f1.read()

with open('all.csv', 'a') as f2:
    # f2.write('\n')
    f2.write(new_csv_file)

dff = pd.read_csv('all.csv')
dff.columns = ['Date', 'Aggregation', 'NameSpace', 'CpuCost', 'GpuCost', 'RamCost', 'PvCost', 'NetworkCost', 'SharedCost', 'TotalCost']
dff.to_csv('all.csv', index=False)


## TODO: store the csv somewhere (storageAccount, sharePoint) ##

# # parameter
# CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=sqldbtest1312;AccountKey=RM907yZBkAcke+chv3xK8Fcsl1Qyj6J8TFPcXyIdmO8kvzz0WSVtUTvdp9RNPakX/gLEpuRBE7qy+AStXkR9DQ==;EndpointSuffix=core.windows.net"
# # parameter
# CONTAINERNAME = "kubecost"

# BLOBNAME = "kubecost_"+current_date+".csv"

# # instantiate new blobservice with connection string
# blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)

# # instantiate new containerclient
# container_client = blob_service_client.get_container_client(CONTAINERNAME)

# # instantiate new blob_client
# blob_client = blob_service_client.get_blob_client(container = CONTAINERNAME, blob=BLOBNAME)

# # Upload the created file
# with open(file=local_csv_file, mode="rb") as data:
#     blob_client.upload_blob(data, blob_type="BlockBlob")