import os
from tempfile import gettempdir


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'AOOPMessages'
    # MAIL_SERVER = os.environ.get('MAIL_SERVER')
    # MAIL_PORT = os.


class DevelopmentConfig(Config):

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI')


class TestingConfig(Config):

    TESTING = True
    DEBUG = False
    LOGIN_DISABLED = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(gettempdir(), 'test.db')


class ProductionConfig(Config):

    SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URI')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
