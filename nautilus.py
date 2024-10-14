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
        
    def get_cluster_info(self):
        """
        Retrieve and print information about the Kubernetes cluster.

        This method fetches the API resources available in the cluster and prints
        the number of resources. It also prints the URLs for the KubeDNS service
        and the Kubernetes control plane.

        Returns:
            None
        """
        
        api_resources = self.get_api_resources()
        if api_resources:
            print(f"API Resources: {len(api_resources.resources)}")

        host = self.v1.api_client.configuration.host
        print(
            f"KubeDNS is running at http://{host}/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy")
        print(f"Kubernetes control plane is running at {host}")


def main():
    
    print("\n")
    print("Nautilus - minimal Kubernetes CLI")
    print("\n")
    
    try:
        k8s_cluster = DescribeK8s("default")
    except ConfigException:
        cprint("Invalid kube-config file. No configuration found.", "red")
        return


if __name__ == "__main__":
    main()
