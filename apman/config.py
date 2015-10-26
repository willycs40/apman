import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    EXAMPLE_CONFIG = os.environ.get('EXAMPLE_CONFIG') or 'DEFAULT_EXAMPLE_CONFIG' 
    DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    NOTIFICATION_EMAILS_TO = ['email@email.com']
    NOTIFICATION_EMAILS_FROM = 'email@email.com'

    EMAIL_SMTP_ADDRESS = os.environ.get('EMAIL_SMTP_ADDRESS') or 'localhost'

class DevelopmentConfig(Config):
    DEBUG = True
    
config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}