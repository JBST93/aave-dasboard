"""
Bootstrap module for project initialization.

This module provides a centralized way to set up the Python path and
load environment variables, eliminating duplicate boilerplate code
across protocol fetchers.

Usage:
    from utils.bootstrap import get_app, get_db, get_project_root

    app = get_app()
    db = get_db()
    project_root = get_project_root()
"""
import os
import sys
from functools import lru_cache


def get_project_root():
    """Get the absolute path to the project root directory."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def setup_path():
    """Add project root to Python path if not already present."""
    project_root = get_project_root()
    if project_root not in sys.path:
        sys.path.insert(0, project_root)


def load_env():
    """Load environment variables from .env file."""
    from dotenv import load_dotenv
    project_root = get_project_root()
    env_path = os.path.join(project_root, '.env')
    load_dotenv(env_path)


def init():
    """Initialize the project environment (path + env vars)."""
    setup_path()
    load_env()


# Run initialization on import
init()


@lru_cache(maxsize=1)
def get_app():
    """Get the Flask application instance."""
    from app import app
    return app


@lru_cache(maxsize=1)
def get_db():
    """Get the SQLAlchemy database instance."""
    from app import db
    return db


def get_script_dir(file_path):
    """Get the directory containing a script file.

    Args:
        file_path: The __file__ variable from the calling script.

    Returns:
        The absolute path to the directory containing the script.
    """
    return os.path.dirname(os.path.abspath(file_path))


def get_abi_path(protocol_name, abi_filename):
    """Get the absolute path to an ABI JSON file.

    Args:
        protocol_name: The protocol directory name (e.g., 'aave', 'compound')
        abi_filename: The ABI JSON filename (e.g., 'aave_abi.json')

    Returns:
        The absolute path to the ABI file.
    """
    project_root = get_project_root()
    return os.path.join(project_root, 'projects', protocol_name, abi_filename)
