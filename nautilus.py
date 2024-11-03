#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml
import argparse

from kubernetes import client, config
from kubernetes.config.config_exception import ConfigException
from termcolor import colored, cprint

class DescribeK8s:
    def __init__(self, namespace):
        try:
            self.config = config.load_kube_config()
        except Exception as e:
            print(f"Error loading kubeconfig: {e}")
            exit(1)
        self.namespace = namespace
        self.v1 = client.CoreV1Api()
        # Create the API client instance properly
        self.api_client = client.ApiClient()
        self.apps_v1 = client.AppsV1Api(self.api_client)
        
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
        
    def create_namespace(self,new_namespace):
        """Create a new namespace in the Kubernetes cluster."""
        try:
            namespace = client.V1Namespace(
                metadata=client.V1ObjectMeta(
                    name=new_namespace
                )
            )
            self.v1.create_namespace(namespace)
            print(f"Namespace '{new_namespace}' created successfully")
            return True
        except client.ApiException as e:
            if e.status == 409:
                print(f"Namespace '{new_namespace}' already exists")
            else:
                print(f"Error creating namespace: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error creating namespace: {e}")
            return False
        

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
            try:
                api_versions = version_api.get_code()
            except Exception as e:
                print(f"Error getting API versions: {e}")
                return  
            print("Kubernetes API Versions:")
            print(f"Major: {api_versions.major}")
            print(f"Minor: {api_versions.minor}")
            print(f"Platform: {api_versions.platform}")
        except Exception as e:
            print(f"Error getting API versions: {e}")
            return
            
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
        print(f"Listing nodes in namespace '{self.namespace}'")
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
    
    def apply(self, filename):
        """Apply a configuration file to create or update resources."""
        try:
            with open(filename, 'r') as f:
                docs = yaml.safe_load_all(f)
                for doc in docs:
                    kind = doc.get("kind", "").lower()
                    name = doc["metadata"]["name"]
                    
                    if kind == "deployment":
                        api_instance = self.apps_v1
                        api_func = api_instance.create_namespaced_deployment
                        update_func = api_instance.patch_namespaced_deployment
                    elif kind == "service":
                        api_instance = self.v1
                        api_func = api_instance.create_namespaced_service
                        update_func = api_instance.patch_namespaced_service
                    elif kind == "pod":
                        api_instance = self.v1
                        api_func = api_instance.create_namespaced_pod
                        update_func = api_instance.patch_namespaced_pod
                    else:
                        print(f"Unsupported resource kind: {kind}")
                        continue
                    
                    try:
                        api_func(body=doc, namespace=self.namespace)
                        print(f"{kind.capitalize()} '{name}' created.")
                    except client.ApiException as e:
                        if e.status == 409:  # Conflict, resource already exists
                            update_func(name=name, namespace=self.namespace, body=doc)
                            print(f"{kind.capitalize()} '{name}' updated.")
                        else:
                            print(f"Error applying {kind} '{name}': {e}")
        except Exception as e:
            print(f"Error applying configuration: {e}")
    
    def create(self, resource_type, name, image=None, replicas=None):
        """Create a new resource."""
        try:
            if resource_type.lower() == "deployment":
                body = client.V1Deployment(
                    metadata=client.V1ObjectMeta(name=name),
                    spec=client.V1DeploymentSpec(
                        replicas=replicas,
                        selector=client.V1LabelSelector(
                            match_labels={"app": name}
                        ),
                        template=client.V1PodTemplateSpec(
                            metadata=client.V1ObjectMeta(labels={"app": name}),
                            spec=client.V1PodSpec(
                                containers=[client.V1Container(
                                    name=name,
                                    image=image
                                )]
                            )
                        )
                    )
                )
                self.apps_v1.create_namespaced_deployment(namespace=self.namespace, body=body)
                print(f"Deployment '{name}' created.")
            elif resource_type.lower() == "service":
                body = client.V1Service(
                    metadata=client.V1ObjectMeta(name=name),
                    spec=client.V1ServiceSpec(
                        selector={"app": name},
                        ports=[client.V1ServicePort(port=80)]
                    )
                )
                self.v1.create_namespaced_service(namespace=self.namespace, body=body)
                print(f"Service '{name}' created.")
            else:
                print(f"Unsupported resource type: {resource_type}")
        except client.ApiException as e:
            print(f"Error creating {resource_type}: {e}")
            
    def list_pods(self):
        """List all pods in the current namespace."""
        print(f"Listing pods in namespace '{self.namespace}'")  
        try:
            api_instance = client.CoreV1Api()
            pod_list = api_instance.list_namespaced_pod(namespace=self.namespace)
            print(pod_list)
        except client.ApiException as e:
            print(f"Exception when calling CoreV1Api->list_namespaced_pod: {e}")
        
def main():
    print("\n")
    print(colored("Nautilus - minimal Kubernetes CLI", "green"))    
    print("\n")
    
    
    parser = argparse.ArgumentParser(description="Kubernetes cluster tool")
    parser.add_argument("--namespace", help="Set namespace")
    parser.add_argument("--create-namespace",action="store_true", help="create a new namespace")
    parser.add_argument("--cluster-info", "--cluster", action="store_true", help="Show cluster info") 
    parser.add_argument("--api-versions", action="store_true", help="Show API versions")
    parser.add_argument("--nodes", action="store_true", help="Show node info")
    parser.add_argument("--apply", help="Apply config file")
    parser.add_argument("--create", nargs=3, metavar=("TYPE", "NAME", "IMAGE"), help="Create resource")
    parser.add_argument("--list-pods", action="store_true", help="List pods")


    args = parser.parse_args()

    try:
         k8s_cluster = DescribeK8s("default")
    except ConfigException:
         cprint("Invalid kube-config file. No configuration found.", "red")
         return

    if args.namespace:
        k8s_cluster.set_namespace(args.namespace)
    if args.create_namespace:
        k8s_cluster.create_namespace(args.namespace)
    if args.cluster_info:
        k8s_cluster.get_cluster_info()
    elif args.api_versions:
        k8s_cluster.print_api_versions()
    elif args.nodes:
        k8s_cluster.print_nodes_info()
    elif args.list_pods:
        k8s_cluster.list_pods()
    elif args.apply:
        k8s_cluster.apply(args.apply)
    elif args.create:
        k8s_cluster.create(args.create[0], args.create[1], args.create[2])  
    else:
        print("No arguments provided. Use --help for more information.")

if __name__ == "__main__":
    main()
