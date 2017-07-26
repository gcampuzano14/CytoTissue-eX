import os
basedir = os.path.abspath(os.path.dirname(__file__))


SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:pw@dbaddress:dbport/copath_parser_log'


# Uncomment the line below if you want to work with a local DB
# SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

SQLALCHEMY_POOL_RECYCLE = 3600

WTF_CSRF_ENABLED = True
SECRET_KEY = 'secret'


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):

    # APP_DATA =  os.path.join(os.getcwd(),'app', 'main',  'data', 'app_data', 'app_data.db')
    # APP_DATA =  os.path.join(os.getcwd(),'app', 'main',  'data', 'app_data', 'app_data.db')
    # APP_DATA =  os.path.join(os.getcwd(),'app', 'main',  'data', 'app_data', 'app_data.db')
    # APP_DATA =  os.path.join(os.getcwd(),'app', 'main',  'data', 'app_data', 'app_data_dev_house.db')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:pw@dbaddress:dbport/copath_parser_log'
    SQLALCHEMY_POOL_RECYCLE = 3600
    DEBUG = True
    WTF_CSRF_ENABLED = True
    SECRET_KEY = 'secret'

config = {'development': DevelopmentConfig}