<img src="images/nautilus.jpg" alt="nautilus logo" width="200" height="200">

# nautilus
Minimal command line interface "kubectl like" for interacting with Kubernetes clusters. A basic exercise for obtain a minimal console for interact with Kubernetes clusters and experimenting with basic operations ( load balancer creation , observability tools, etc ..)

## pre-requisites

- Python 3.x
- Kubernetes Python client library (`kubernetes`)
- PyYAML library (pyyaml)

Is highly suggested to create a virtual environment (aka venv)  and activate it, before experimenting witg this tool. 

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## How to play with this tool and Kind 

In order to test basic commannds and interact with Kubernetes clusters, you can create a simple test cluster with Kind. Here how:
```sh
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.24.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind
```

```sh
kind create cluster --name my-cluster
```
Test the nodes coomnd , running 
```sh
python3 nautilus.py --nodes
```


## Documentation and references

For more information, browse the following links:

- "The" Kubernetes Documentation  : <https://kubernetes.io/docs/home/>
- The kubectl client documentation : <https://kubernetes.io/docs/reference/kubectl/>
- Kubernetes v1 API Reference  : <https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.24/>
- Kubernetes Python Client : : <https://github.com/kubernetes-client/python>


