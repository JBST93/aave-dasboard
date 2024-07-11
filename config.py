import os
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL_DEV').replace("postgres://", "postgresql://")

class ProductionConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL2').replace("postgres://", "postgresql://")


class StagingConfig(Config):
    DEVELOPMENT = False
    TESTING = True

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
