import os
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL2')

class ProductionConfig(Config):
    DEVELOPMENT = True
    DEBUG = False

class StagingConfig(Config):
    DEVELOPMENT = False
    TESTING = True

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
