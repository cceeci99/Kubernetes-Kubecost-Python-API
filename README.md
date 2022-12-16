# kubecost

# KubeCost-API-client
Create python script for client that talks with the KubeCost API and requests the data from the server


STEPS:

1. Create an AKS (Azure Kubernetes Services)

az group create -n myResourceGroup --location westeurope

az aks create -g myResourceGroup -n myAKSCluster --enable-managed-identity --node-count 1 --enable-addons monitoring --enable-msi-auth-for-monitoring  --generate-ssh-keys

2. Set up Kubecost running on the cluster

# Create the Kubecost namespace

kubectl create namespace kubecost

# Install Kubecost into the AKS cluster

kubectl apply -f https://raw.githubusercontent.com/kubecost/cost-analyzer-helm-chart/master/kubecost.yaml --namespace kubecost

# check kubecost pods 
kubectl get pods -n kubecost

# Connect to the Kubecost dashboard UI

kubectl port-forward -n kubecost svc/kubecost-cost-analyzer 9090:9090

3. Set up Python environment to run the script

virtualenv -p python3 /kubecost/venvkubecost
source /kubecost/venvkubecost/bin/activate
