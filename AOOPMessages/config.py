import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'AOOPMessages'
    # MAIL_SERVER = os.environ.get('MAIL_SERVER')
    # MAIL_PORT = os.


class DevelopmentConfig(Config):

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI')


class TestingConfig(Config):

    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI')


class ProductionConfig(Config):

    SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URI')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
