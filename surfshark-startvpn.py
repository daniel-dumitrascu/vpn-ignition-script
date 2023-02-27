#!/usr/bin/python
import sys
import glob
import os
import random
import subprocess
import signal
from shlex import split

interupt_handler = lambda signum, frame: sys.exit(1)
signal.signal(signal.SIGINT, interupt_handler)

if len(sys.argv) < 4:
    print("Script wasn't executed with the correct parameters.")
    print("Example: script <user password> <path to configs> <selected config>")
    sys.exit(0)

user_pass = sys.argv[1]
openvpn_conf_files_path = sys.argv[2]
selected_config = sys.argv[3]

configs = glob.glob(openvpn_conf_files_path + "/*.prod.surfshark.com_tcp.ovpn")
if len(configs) == 0:
    print("No configuration files have been found in: " + openvpn_conf_files_path)
    sys.exit(0)

selected_config = openvpn_conf_files_path + "/" + selected_config

if selected_config not in configs:
    print("The selected configuration is not available: " + selected_config)
    sys.exit(0)

p1 = subprocess.Popen(split("echo " + user_pass), stdout=subprocess.PIPE)
p2 = subprocess.Popen(split("sudo -S openvpn " + selected_config), stdin=p1.stdout)

output, error = p2.communicate()
print(output)
