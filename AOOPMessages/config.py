"""AOOPMessages config module.

This module provides classes for the configuration of the app in different
environments.
"""

import os
from tempfile import gettempdir


class Config:
    """Config base class.

    This class contains the shared configurations for all environments.

    Attributes
    ----------
        SECRET_KEY : str
            Secret key to use. Retrieves value from the SECRET_KEY
            environment variable. Defaults to 'AOOPMessages'
    """

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'AOOPMessages'
    # MAIL_SERVER = os.environ.get('MAIL_SERVER')
    # MAIL_PORT = os.


class DevelopmentConfig(Config):
    """Config for Development environment class.

    This class contains the configurations for the development environment.

    Attributes
    ----------
        DEBUG : bool
            Enable Flask debug mode. Defaults to True.
        SQLALCHEMY_DATABASE_URI : str
            Database URI to use. Retrieves value from the DEV_DATABASE_URI
            environment variable.
    """

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI')


class TestingConfig(Config):
    """Config for Testing environment class.

    This class contains the configurations for the testing environment.

    Attributes
    ----------
        TESTING : bool
            Enable Flask testing mode. Defaults to True.
        DEBUG : bool
            Enable Flask debug mode. Defaults to False.
        SQLALCHEMY_DATABASE_URI : str
            Database URI to use. Defaults to 'test.db' SQLite file in
            OS temp directory.
    """

    TESTING = True
    DEBUG = False
    LOGIN_DISABLED = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(gettempdir(), 'test.db')


class ProductionConfig(Config):
    """Config for Production environment class.

    This class contains the configurations for the production environment.

    Attributes
    ----------
        SQLALCHEMY_DATABASE_URI : str
            Database URI to use. Retrieves value from the
            PRODUCTION_DATABASE_URI environment variable.
    """

    SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URI')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
