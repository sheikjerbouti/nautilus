#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml
import argparse

from kubernetes import client, config
from kubernetes.config.config_exception import ConfigException
from termcolor import colored, cprint

class DescribeK8s:
    """
    A class to interact with Kubernetes resources within a specified namespace.

    Attributes:
    -----------
    namespace : str
        The namespace to interact with in the Kubernetes cluster.
    config : object
        The Kubernetes configuration loaded from the kubeconfig file.
    v1 : CoreV1Api
        The CoreV1Api instance to interact with core Kubernetes resources.

    Methods:
    --------
    __init__(namespace):
        Initializes the DescribeK8s object with the given namespace.
    """

    def __init__(self, namespace):
        self.config = config.load_kube_config()    
        self.namespace = namespace
        self.v1 = client.CoreV1Api()


def main():
    
    print("\n")
    print("Nautilus - minimal Kubernetes CLI")
    print("\n")
    
    try:
        k8s_cluster = DescribeK8s("default")
    except ConfigException:
        print("Invalid kube-config file. No configuration found.")
    


if __name__ == "__main__":
    main()
