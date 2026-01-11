"""
Flask application configuration.

Supports SQLite for development and PostgreSQL for production.
"""
import os
from dotenv import load_dotenv

load_dotenv()


def get_database_uri(default='sqlite:///instance/local.db'):
    """Get database URI with postgres:// to postgresql:// conversion."""
    db_url = os.getenv('DATABASE_URL2', default)
    if db_url:
        # Heroku uses postgres:// but SQLAlchemy requires postgresql://
        return db_url.replace("postgres://", "postgresql://")
    return default


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = get_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    """Production configuration - requires DATABASE_URL2 environment variable."""
    DEVELOPMENT = False
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = False
    TESTING = True


class DevelopmentConfig(Config):
    """Development configuration - defaults to SQLite if no DATABASE_URL2 set."""
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = get_database_uri('sqlite:///instance/local.db')


class TestConfig(Config):
    """Test configuration - uses in-memory SQLite for fast tests."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
