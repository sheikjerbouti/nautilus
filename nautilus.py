#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml
import argparse

from kubernetes import client, config
from kubernetes.config.config_exception import ConfigException
from termcolor import colored, cprint

class DescribeK8s:
    def __init__(self, namespace):
        self.config = config.load_kube_config()    
        #self.namespace = namespace
        self.v1 = client.CoreV1Api()
        
    def get_cluster_info(self):
        api_resources = self.get_api_resources()
        if api_resources:
            print(f"API Resources: {len(api_resources.resources)}")

        host = self.v1.api_client.configuration.host
        print(
            f"KubeDNS is running at http://{host}/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy")
        print(f"Kubernetes control plane is running at {host}")

    def set_namespace(self, namespace):
        self.namespace = namespace

    def get_api_resources(self):
        """Get API resources information."""
        try:
            return self.v1.get_api_resources()
        except client.ApiException as e:
            print(f"Error getting API resources: {e}")
            return None

    def get_api_server(self):
        apiserver = self.v1.api_client.configuration.host
        return f"Kubernetes control plane is running at {apiserver}"

    def print_api_versions(self):
        try:
            api_client = client.ApiClient()
            version_api = client.VersionApi(api_client)
            api_versions = version_api.get_code()
            print("Kubernetes API Versions:")
            print(f"Major: {api_versions.major}")
            print(f"Minor: {api_versions.minor}")
            print(f"Platform: {api_versions.platform}")
        except client.ApiException as e:
            print(f"Error getting API versions: {e}")
            
    def get_kube_dns_info(self):
        try:
            return self.v1.list_namespaced_service(self.namespace)
        except client.ApiException as e:
            print(f"Error getting KubeDNS info: {e}")
            return None
        
    def set_namespace(self, namespace):
        self.namespace = namespace

    def get_api_resources(self):
        try:
            return self.v1.get_api_resources()
        except client.ApiException as e:
            print(f"Error getting API resources: {e}")
            return None

    def get_api_server(self):
        apiserver = self.v1.api_client.configuration.host
        return f"Kubernetes control plane is running at {apiserver}"
    
    def get_nodes(self):
        try:
            nodes = self.v1.list_node()
            return nodes.items
        except client.ApiException as e:
            print(f"Error getting nodes: {e}")
            return None


    def print_nodes_info(self):
        nodes = self.get_nodes()
        if nodes:
            print("Cluster Nodes:")
            for node in nodes:
                print(f"  Name: {node.metadata.name}")
                print(f"    Status: {node.status.phase}")
                print(
                    f"    Kubernetes Version: {node.status.node_info.kubelet_version}")
                print(f"    OS Image: {node.status.node_info.os_image}")
                print(
                    f"    Container Runtime: {node.status.node_info.container_runtime_version}")
                print("    Addresses:")
                for address in node.status.addresses:
                    print(f"      {address.type}: {address.address}")
                print()
        else:
            print("No nodes found or error occurred while fetching nodes.")

    def get_kube_dns_info(self):
        try:
            return self.v1.list_namespaced_service(self.namespace)
        except client.ApiException as e:
            print(f"Error getting KubeDNS info: {e}")
            return None
   
        pass


def main():
    print("\n")
    print(colored("Nautilus - minimal Kubernetes CLI", "green"))    
    print("\n")
    
    
    parser = argparse.ArgumentParser(
        description="Describe Kubernetes cluster information")
    parser.add_argument(
        "--namespace", help="Set the namespace to get the information")
    parser.add_argument("--cluster-info", "--cluster",
                        help="Print the cluster information", action="store_true")
    parser.add_argument(
        "--api-versions", help="Print the API versions", action="store_true")
    parser.add_argument(
        "--nodes", help="Print information about all nodes", action="store_true")

    args = parser.parse_args()

    try:
         k8s_cluster = DescribeK8s("default")
    except ConfigException:
         cprint("Invalid kube-config file. No configuration found.", "red")
         return

    if args.namespace:
        k8s_cluster.set_namespace(args.namespace)

    if args.cluster_info:
        k8s_cluster.get_cluster_info()
    elif args.api_versions:
        k8s_cluster.print_api_versions()
    elif args.nodes:
        k8s_cluster.print_nodes_info()
    else:
        print("No arguments provided. Use --help for more information.")

if __name__ == "__main__":
    main()
