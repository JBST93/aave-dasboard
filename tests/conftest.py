"""Pytest configuration and fixtures."""
import sys
import os

# Set test config BEFORE importing app
os.environ['APP_SETTINGS'] = 'config.TestConfig'

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

import pytest


@pytest.fixture(scope='session')
def app():
    """Create application for testing."""
    from app import app as flask_app, db
    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.drop_all()


@pytest.fixture(scope='function')
def app_context(app):
    """Create application context."""
    with app.app_context():
        yield


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()
