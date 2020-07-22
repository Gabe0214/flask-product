from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL')
    SECRET_KEY = environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL')
    SECRET_KEY = environ.get('SECRET_KEY')


class DevelopmentConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = environ.get('DEBUG')
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL')
    SECRET_KEY = environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

