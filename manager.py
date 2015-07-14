# PyManager Framework for running python jobs against ER
# Creation date 14/07/2015
# Author: Will Cubitt-Smith

import time
import os
import datetime
import imp
import json
import config
import subprocess

# Settings
log_path = 'log.txt'
packages_file = 'packages.json'
config_file = 'config.json'

# Set up objects
log = open(log_path, 'a')

def write_log(msg, verbosity=1):
	log.write(msg +'\n')

if __name__ == '__main__':

	with open(packages_file,'r') as file:
		packages = json.load(file)

	print(config.SOME_PARAM)
	print(packages[0])
	write_log('uh oh')
	
	
	