#!/usr/bin/env python
import sys
import logging
import traceback
from packagemanager import PackageManager

def main():

    # Print Diagnostic Information
    logging.info("Running ApMan with python executable location: {}".format(sys.prefix))

    # Retrieve package config file path as first argument
    try:
        package_path = sys.argv[1]
    except:
        logging.error("ApMan expects package configuration path as the first argument.")
        exit()
        
    # Load package configuration file
    logging.info('Loading package configuration file: {}'.format(package_path))
    try:
    	package = PackageManager(package_path)
    except:
    	logging.error("Could not load package config file:\n{}".format(traceback.format_exc()))
    	exit()

    # Run the package
    logging.info("Starting package ({}), with time-out ({} seconds), command ({})".format(package.parameters['id'],package.parameters['timeout'],package.parameters['command']))
    try:
    	package.run_package(log_run_to_db=False, send_notification_emails=True)
    except:
    	logging.error("Problem running package:\n{}".format(traceback.format_exc()))
    	exit()

    logging.info("Run Complete.")

if __name__ == '__main__':

    # Calling directly so set up logging
    logging.basicConfig(
        format='%(asctime)s|%(levelname)s|%(message)s',
        datefmt='%m/%d/%Y %I:%M:%S',
        level=logging.DEBUG)
    
    main()
