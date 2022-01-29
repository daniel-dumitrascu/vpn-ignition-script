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

selected_country = ""
openvpn_conf_files_path = "/etc/openvpn/client"

if len(sys.argv) < 2:
	print("User password must be passed as the first argument")
	sys.exit(0)

user_pass = sys.argv[1]

if len(sys.argv) == 3:
	selected_country = sys.argv[2].lower()

countries = glob.glob(openvpn_conf_files_path + "/*.conf")
if len(countries) == 0:
	print("No configuration files have been found in: " + openvpn_conf_files_path)
	sys.exit(0)

for i, country in enumerate(countries):
	country = os.path.basename(country)
	country = country.split(".conf")[0]
	countries[i] = country

if selected_country == "":
	index = random.randint(0,len(countries)-1)
	selected_country = countries[index]
	print("Selected country is: " + selected_country)
elif selected_country not in countries:
	print("A configuration file was not found for the selected country: " + selected_country)
	sys.exit(0)

p1 = subprocess.Popen(split("echo " + user_pass), stdout=subprocess.PIPE)
p2 = subprocess.Popen(split("sudo -S openvpn " + openvpn_conf_files_path + "/" + selected_country + ".conf"), stdin=p1.stdout)

#process = subprocess.Popen(bashCmd, stdout=subprocess.PIPE)
output, error = p2.communicate()
print(output)
		
	
