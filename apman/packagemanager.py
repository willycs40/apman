import sys
import json
import os
import shlex
import logging

from config import Config
from models import LogEntry
from models import PackageLogEntry
from database import db_session
from utilities import cd, send_email
from scriptrunner import ScriptRunner

class PackageManager():

    def __init__(self, package_config_path):

        self.package_path = package_config_path
        self.parameters = []
        self.command = []
        self.script_thread = None

        self._read_config_file()
        self._validate_package_config()
        self._add_extra_parameters()
        self._build_command()

    def _read_config_file(self):

        try:
            with open(self.package_path,'r') as file:
                self.parameters = json.load(file)
        except:
            raise Exception("Error loading the package configuration script. Check the supplied path and verify is valid json (could use http://jsonlint.com/).")

    def _validate_package_config(self):
        """Check inside the loaded parameters to ensure all the required parameters are present"""

        required_parameters = ['id','description','command', 'timeout']
        missing_parameters = []
        
        for parameter in required_parameters:
            if parameter not in self.parameters:
                missing_parameters.append(parameter)
        
        if len(missing_parameters)>0:
            raise Exception("Parameters {} missing from package configuration".format(str(missing_parameters)))

    def _add_extra_parameters(self):
        """Use os path to add a few more path parameters"""

        try:
            self.parameters['absolute_path'] = os.path.abspath(self.package_path)
            self.parameters['directory'] = os.path.dirname(self.parameters['absolute_path'])
        except:
            raise Exception("Problem adding path parameters to package parameters.")

    def _build_command(self):

        self.command = shlex.split(self.parameters['command'])
        if 'parameters' in self.parameters:
            self.command.append(str(self.parameters['parameters'])) 

    def _log_package_start_to_db(self):
        """Record package start to the central ApMan database log."""

        # store the returned log record so we can use it to update the database in '_log_package_end_to_db()'
        try:
            self._db_log_record = PackageLogEntry.start(self.parameters['id'], self.parameters['timeout'])
        except:
            logging.error("Cannot log package start to ApMan DB Log.")
            #raise Exception("Cannot log package execution to ApMan DB Log.")

    def _log_package_end_to_db(self):
        """Record package end to the central apman database log."""

        # note we are using self._db_log_record, stored by' _log_package_start_to_db()'
        try:
            self._db_log_record.stdout = self._script_thread.out
            self._db_log_record.stderr = self._script_thread.err
            self._db_log_record.timed_out = self._script_thread.script_timed_out
            self._db_log_record.errored = self._script_thread.script_exceptioned    

            PackageLogEntry.finish(self._db_log_record)
        except:
            logging.error("Cannot log package end to ApMan DB Log.")
            #raise Exception("Cannot log package execution to ApMan DB Log.")

    def _get_email_text(self):
        """Function to return readable summary and detail text (subject and body) report of package execution."""

        if self._script_thread.script_timed_out:
            text_result = "Failed (Timed Out)"
        elif self._script_thread.script_exceptioned:
            text_result = "Failed (Runtime Error)"
        else:
            text_result = "Completed Successfully"

        subject = "Package ({}) {}".format(self.parameters['id'], text_result)

        body = """
        ID: {}
        Timeout: {}
        Parameters: {}
        Start: {}
        End: {}
        Result: {}
        Standard Out:\n{}
        Standard Error:\n{}
        """.format(self.parameters['id'], self.parameters['timeout'], self.parameters['parameters'], str(self._script_thread.start_timestamp), str(self._script_thread.end_timestamp), text_result, self._script_thread.out, self._script_thread.err)

        return subject, body

    def _send_notification_email(self):
        """Send an email with package execution details, depending on package result.
        Whether emails are sent depends on the global and package settings. e.g. send_on_success"""

        # Get the global email addresses
        email_to = Config.NOTIFICATION_EMAILS_TO
        email_from = Config.NOTIFICATION_EMAILS_FROM

        # Add any package-specific email addresses
        if 'notification-emails' in self.parameters:
            email_to.extend(self.parameters['notification-emails'])

        subject, body = self._get_email_text()

        try:
            send_email(subject, body, email_from, email_to, Config.SMTP_ADDRESS)
        except:
            logging.error("Unable to send notification email")
            #raise Exception("Problem sending email.")

    def run_package(self, log_run_to_db=None, send_notification_emails=None, print_notification=True): 
        
        # Set defaults - if caller doesn't specify whether they want database logging and email notification turned on, using the package global defaults
        if log_run_to_db is None:
            log_run_to_db = Config.LOG_RUN_TO_DB
        if send_notification_emails is None:
            send_notification_emails = Config.SEND_NOTIFICATION_EMAILS
        
        if log_run_to_db:
            logging.debug("Logging package start to DB.")
            self._log_package_start_to_db()

        # switch to package directory with cd - so that paths are relative to the config file location.
        logging.debug("Executing package command.")
        with cd(self.parameters['directory']):
            self._script_thread = ScriptRunner(self.command, self.parameters['timeout'])
            self._script_thread.run_script()
        
        if log_run_to_db:
            logging.debug("Logging package end to DB.")
            self._log_package_end_to_db()

        if send_notification_emails:
            if self._script_thread.script_timed_out or self._script_thread.script_exceptioned or Config.NOTIFY_SUCCESS:            
                logging.debug("Sending notification emails.")
                self._send_notification_email()

        if print_notification:
            subject, body = self._get_email_text()
            logging.debug(subject)
            logging.debug(body)