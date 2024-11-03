<img src="images/nautilus.jpg" alt="nautilus logo" width="200" height="200">

# nautilus - Build your own kubectl like tool 

Minimal command line interface "kubectl like" for interacting with Kubernetes clusters. A basic exercise for obtain a minimal console for interact with Kubernetes clusters and experimenting with basic operations ( deployments, load balancer creation , observability tools, etc ..). Re-creating favorite technologies from scratch.

## pre-requisites

- Python 3.x
- Kubernetes Python client library (`kubernetes`)
- PyYAML library (pyyaml)

Is highly suggested to create a virtual environment (aka venv)  and activate it, before experimenting witg this tool. 

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## How to play with nautilus and Kind 

In order to test basic commannds and interact with Kubernetes clusters, we can create a simple cluster using Kind, available at the following address <https://kind.sigs.k8s.io/>.

```sh
#install Kind.
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.24.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind
```

```sh
#create a test cluster with kind
kind create cluster --name my-cluster
```
Test the nodes coomnd , running 
```sh
nautilus.py --nodes
```
## Basic commands implemented 
```sh
usage: nautilus.py [-h] [--namespace NAMESPACE] [--cluster-info] [--api-versions] [--nodes]

Describe Kubernetes cluster information

options:
  -h, --help            show this help message and exit
  --namespace NAMESPACE
                        Set the namespace to get the information
  --cluster-info, --cluster
                        Print the cluster information
  --api-versions        Print the API versions
  --nodes               Print information about all nodes
  --apply APPLY         Apply a configuration file
  --create RESOURCE_TYPE NAME IMAGE
                        Create a new resource (deployment or service)
  --list-pods           List all pods in the current namespace
```
## Documentation and references

For more information, browse the following links:

- "The" Kubernetes Documentation  : <https://kubernetes.io/docs/home/>
- The kubectl client documentation : <https://kubernetes.io/docs/reference/kubectl/>
- Kubernetes v1 API Reference  : <https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/>
- Kubernetes Python Client : : <https://github.com/kubernetes-client/python>


