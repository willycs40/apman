import smtplib
from email.mime.text import MIMEText
import os

class cd:
    """Context manager for changing the current working directory"""

    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

def send_email(email_subject, email_text, email_from, email_to, smtp_address):
    """Creates a MIMEText email, and then sends it using the SMTP server specified.
    'email_from' should be an email address string, while email_to should be a list of email address strings.
    """

    msg = MIMEText(email_text)
    msg['Subject'] = email_subject
    msg['From'] = email_from
    msg['To'] = ", ".join(email_to)

    s = smtplib.SMTP(smtp_address)
    s.sendmail(email_from, [email_to], msg.as_string())    
    s.quit()
