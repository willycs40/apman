#!/usr/bin/env python

import logging
import traceback
import argparse
from packagemanager import PackageManager

def main():

    # logging setup
    logging.basicConfig(
        format='%(asctime)s|%(levelname)s|%(message)s',
        datefmt='%m/%d/%Y %I:%M:%S',
        level=logging.DEBUG)

    # Some parser set up
    parser = argparse.ArgumentParser(description='Run an ApMan Package.')
    parser.add_argument("config", help="Path to the configuration file of the ApMan Package you wish to run.")
    parser.add_argument("-nn", "--no_notify", help="Do not send email notifications", action="store_true")
    parser.add_argument("-nl","--no_log", help="Do not log to ApMan DB log", action="store_true")
    args = parser.parse_args()

    # Load package configuration file
    logging.info('Loading package configuration file: {}'.format(args.config))
    try:
    	package = PackageManager(args.config)
    except:
    	logging.error("Could not load package config file:\n{}".format(traceback.format_exc()))
    	exit()

    # Run the package
    logging.info("Starting package ({}), with time-out ({} seconds), command ({})".format(package.parameters['id'],package.parameters['timeout'],package.parameters['command']))
    try:
    	package.run_package(log_run_to_db=not args.no_log, send_notification_emails=not args.no_notify)
    except:
    	logging.error("Problem running package:\n{}".format(traceback.format_exc()))
    	exit()

    logging.info("Package ({}) complete".format(package.parameters['id']))

if __name__ == '__main__':
    
    main()
