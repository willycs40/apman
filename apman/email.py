import smtplib
from email.mime.text import MIMEText

def send_email(email_subject, email_text, email_from, email_to, smtp_address):
	"""Send email utility. Creates a MIMEText email, and then sends it using the SMTP server specified.

	'email_from' should be an email address string, while email_to should be a list of email address strings.
	"""

	msg = MIMEText('Message text')
    msg['Subject'] = 'Some Subject'
    msg['From'] = email_from
    msg['To'] = ", ".join(email_to)

    try:
        s = smtplib.SMTP(smtp_address)
        s.sendmail(email_from, [email_to], msg.as_string())
        s.quit()
    except:
        pass