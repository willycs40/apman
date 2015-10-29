import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:

    DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    SMTP_ADDRESS = os.environ.get('EMAIL_SMTP_ADDRESS') or 'localhost'
    SMTP_USERNAME = os.environ.get('SMTP_USERNAME') or ''
    SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD') or ''

    LOG_RUN_TO_DB = True
    SEND_NOTIFICATION_EMAILS = True
    NOTIFY_SUCCESS = False

    NOTIFICATION_EMAILS_FROM = 'a@b.co.uk'
    NOTIFICATION_EMAILS_TO = ['a@b.co.uk'] 

class DevelopmentConfig(Config):
    DEBUG = True


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig,
    'production': Config
}