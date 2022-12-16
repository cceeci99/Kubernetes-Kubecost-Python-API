import json
import requests

import pandas as pd
import datetime as dt

from azure.storage.blob import BlobServiceClient

# set the current date
current_date = dt.datetime.now().strftime("%Y_%m_%d")

# KubeCost API url
url = "http://20.4.129.247:9090/model/aggregatedCostModel"

# Use the requests library to make a GET request to the KubeCost API
params = (
    ("window", "1d"),   # parameter
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

local_json_file = './data.json'
local_csv_file = "./data.csv"

with open(local_json_file, 'w') as f:
    json.dump(jsondata, f, indent=4)

# read json as pandas dataframe
df = pd.read_json(local_json_file)

# drop columns that are not needed
df = df.drop('code', axis=1)
df = df.drop('status', axis=1)
df = df.drop('message', axis=1)

# write data to local csv file
df.to_csv(local_csv_file)

# # parameter
# CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=sqldbtest1312;AccountKey=RM907yZBkAcke+chv3xK8Fcsl1Qyj6J8TFPcXyIdmO8kvzz0WSVtUTvdp9RNPakX/gLEpuRBE7qy+AStXkR9DQ==;EndpointSuffix=core.windows.net"
# # parameter
# CONTAINERNAME = "kubecost"
# # parameter
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