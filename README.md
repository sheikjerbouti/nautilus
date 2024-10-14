<img src="images/nautilus.jpg" alt="nautilus logo" width="200" height="200">
=============

# nautilus
Minimal command line interface "kubectl like" for interacting with Kubernetes clusters. nautilus is using and leveraging the Python Kubernetes API. It uses Kind for test
and navigate different clusters for test and fun. 

## pre-requisites

- python 3.10+
- kind 
- pip
- pip install kubernetes

create a venv and activate it

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## installation

Install kind and create a cluster. 
