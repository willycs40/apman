import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:

    DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    SMTP_ADDRESS = os.environ.get('EMAIL_SMTP_ADDRESS') or 'localhost'

    LOG_RUN_TO_DB = True
    SEND_NOTIFICATION_EMAILS = True
    NOTIFY_SUCCESS = True

    NOTIFICATION_EMAILS_FROM = 'email@email.com'
    NOTIFICATION_EMAILS_TO = ['email@email.com'] 

class DevelopmentConfig(Config):
    DEBUG = True


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig,
    'production': Config
}