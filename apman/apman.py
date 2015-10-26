import subprocess
import threading
import sys
import json
import os
import shlex
import logging
from config import Config
from models import LogEntry as main_log
from models import PackageLogEntry as package_log
from database import db_session

import smtplib
from email.mime.text import MIMEText


class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

class RunScript(threading.Thread):
    def __init__(self, cmd, timeout):
        threading.Thread.__init__(self)
        self.cmd = cmd
        self.timeout = timeout
        self.script_timed_out = False
        self.script_exceptioned = False
        self.out = ''
        self.err = ''
            
    def run(self):
        self.p = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (self.out, self.err) = self.p.communicate()
        self.p.wait()
        if self.p.returncode > 0:
            self.script_exceptioned = True

    def Run(self):
        self.start()
        self.join(self.timeout)

        if self.is_alive():
            self.p.terminate()      #use self.p.kill() if process needs a kill -9
            self.join()
            self.script_timed_out = True

def main():

    # Print Diagnostic Information
    logging.info("Running ApMan with python executable location: {}".format(sys.prefix))
    main_log.add('Testing helper')

    # Get package configuration file location
    try:
        package_path = sys.argv[1]
    except:
        logging.error("Program expects the path to a configuration script as the first argument")
        exit()
        
    # Load package configuration file
    logging.debug('Opening config file')
    try:
        with open(package_path,'r') as file:
            package = json.load(file)
    except:
        logging.error("Error loading the package configuration script. Check the supplied path and verify is valid json (could use http://jsonlint.com/).")
        exit()
    
    # Check all required parameters are present in the configuration
    logging.debug('Reading config file')
    required_parameters = ['id','description','command', 'timeout']
    missing_parameters = []
    for param in required_parameters:
        if param not in package:
            missing_parameters.append(param)
    if len(missing_parameters)>0:
        raise Exception("Parameters {} missing from package configuration".format(str(missing_parameters)))

    # Get config path and work from there...
    package['absolute_path'] = os.path.abspath(package_path)
    package['directory'] = os.path.dirname(package['absolute_path'])
    
    ####################################
    ###        Run the Package       ###
    ####################################

    logging.debug("Switching to package directory... {}".format(package['directory']))   
    
    # Work from package directory
    with cd(package['directory']):

        # Begin script execution
        logging.info("Starting package ({}), with time-out ({} seconds), command ({})".format(package['id'],package['timeout'],package['command']))
        package_run_log = package_log.start(package['id'], package['timeout'])
        
        # Split the package command, add on the parameters, if they exist, then kick off the thread
        command = shlex.split(package['command'])
        if 'parameters' in package:
            command.append(str(package['parameters']))
        script_thread = RunScript(command, package['timeout'])
        script_thread.Run()
        
        logging.info("Package Execution Complete")
    
    # Update the package execution log
    package_run_log.stdout = script_thread.out
    package_run_log.stderr = script_thread.err
    package_run_log.timed_out = script_thread.script_timed_out
    package_run_log = script_thread.script_exceptioned        
    package_log.finish(package_run_log)
    
    # Log results to standard out assuming interactive run
    logging.debug("Timed Out: {}".format(str(script_thread.script_timed_out)))
    logging.debug("Errored Out: {}".format(str(script_thread.script_exceptioned)))
    logging.debug("Standard Out:\n{}".format(script_thread.out))
    logging.debug("Standard Error:\n{}".format(script_thread.err))

    ####################################
    ###      Notification Emails     ###
    ####################################

    email_to = Config.NOTIFICATION_EMAILS_TO
    email_from = Config.NOTIFICATION_EMAILS_FROM

    # Add any package specific email addresses
    if 'notification-emails' in package:
        email_to.extend(package['notification-emails'])

    msg = MIMEText('Message text')
    msg['Subject'] = 'Some Subject'
    msg['From'] = email_from
    msg['To'] = ", ".join(email_to)

    logging.debug(msg.as_string())

    try:
        s = smtplib.SMTP(Config.EMAIL_SMTP_ADDRESS)
        s.sendmail(email_from, [email_to], msg.as_string())
        s.quit()
    except:
        pass

if __name__ == '__main__':

    # Calling directly so set up logging
    logging.basicConfig(
        format='%(asctime)s|%(levelname)s|%(message)s',
        datefmt='%m/%d/%Y %I:%M:%S',
        level=logging.DEBUG)
    
    main()
