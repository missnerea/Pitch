import os

class Config:
    '''
    General configuration parent class
    '''
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://missnerea:Ea150697@localhost/pitch'

    SECRET_KEY = "try harder" #os.environ.get("SECRET_KEY")
    UPLOADED_PHOTOS_DEST = 'app/static/photos'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

class ProdConfig(Config):
    '''
    Production  configuration child class

    Args:
        Config: The parent configuration class with General configuration settings
    '''
    'postgresql+psycopg2://missnerea:password@localhost/pitch'

class DevConfig(Config):
    '''
    Development  configuration child class

    Args:
        Config: The parent configuration class with General configuration settings
    '''
    DEBUG = True


config_options = {
'development':DevConfig,
'production':ProdConfig
}
