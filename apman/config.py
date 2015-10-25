import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    EXAMPLE_CONFIG = os.environ.get('EXAMPLE_CONFIG') or 'DEFAULT_EXAMPLE_CONFIG' 
    DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    NOTIFICATION_EMAILS_TO = ['datainsightmailbox@royalmail.com']
    NOTIFICATION_EMAILS_FROM = 'datainsightmailbox@royalmail.com'

    EMAIL_SMTP_ADDRESS = os.environ.get('EMAIL_SMTP_ADDRESS') or 'localhost'
    EMAIL_SMTP_USER = os.environ.get('EMAIL_SMTP_USER') or 'test'
    EMAIL_SMTP_PASS = os.environ.get('EMAIL_SMTP_PASS') or 'test'

class DevelopmentConfig(Config):
    DEBUG = True
    
config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}