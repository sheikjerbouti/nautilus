#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml
import argparse

from kubernetes import client, config
from termcolor import colored, cprint




def main():
    print("\n")
    print(colored('Nautilus - minimal Kubernetes CLI', 'green', attrs=['bold', 'underline']))
    print(colored('Author: @sheikyerbouti', 'white'))
    print(colored('Version: 1.0.0', 'white'))
    print(colored('Usage: nautilus [options]', 'white'))
    print("\n")

if __name__ == "__main__":
    main()
