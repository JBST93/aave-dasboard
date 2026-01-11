"""Tests for bootstrap module."""
import sys
import os

# Set test config BEFORE any imports
os.environ['APP_SETTINGS'] = 'config.TestConfig'

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

import pytest


class TestGetProjectRoot:
    """Tests for get_project_root function."""

    def test_returns_absolute_path(self):
        """Test that project root is an absolute path."""
        from utils.bootstrap import get_project_root

        root = get_project_root()
        assert os.path.isabs(root)

    def test_path_contains_expected_structure(self):
        """Test that project root contains expected directories."""
        from utils.bootstrap import get_project_root

        root = get_project_root()
        assert os.path.exists(os.path.join(root, 'app.py'))
        assert os.path.exists(os.path.join(root, 'utils'))
        assert os.path.exists(os.path.join(root, 'projects'))


class TestSetupPath:
    """Tests for setup_path function."""

    def test_adds_project_root_to_sys_path(self):
        """Test that project root is added to sys.path."""
        from utils.bootstrap import setup_path, get_project_root

        setup_path()
        root = get_project_root()
        assert root in sys.path


class TestGetApp:
    """Tests for get_app function."""

    def test_returns_flask_app(self, app):
        """Test that get_app returns the Flask application."""
        from utils.bootstrap import get_app

        flask_app = get_app()
        assert flask_app is not None
        assert hasattr(flask_app, 'config')

    def test_returns_same_instance(self, app):
        """Test that get_app returns the same cached instance."""
        from utils.bootstrap import get_app

        app1 = get_app()
        app2 = get_app()
        assert app1 is app2


class TestGetDb:
    """Tests for get_db function."""

    def test_returns_sqlalchemy_db(self, app):
        """Test that get_db returns the SQLAlchemy database instance."""
        from utils.bootstrap import get_db

        db = get_db()
        assert db is not None
        assert hasattr(db, 'session')

    def test_returns_same_instance(self, app):
        """Test that get_db returns the same cached instance."""
        from utils.bootstrap import get_db

        db1 = get_db()
        db2 = get_db()
        assert db1 is db2


class TestGetScriptDir:
    """Tests for get_script_dir function."""

    def test_returns_absolute_path(self):
        """Test that script dir is an absolute path."""
        from utils.bootstrap import get_script_dir

        dir_path = get_script_dir(__file__)
        assert os.path.isabs(dir_path)

    def test_returns_containing_directory(self):
        """Test that script dir contains this test file."""
        from utils.bootstrap import get_script_dir

        dir_path = get_script_dir(__file__)
        assert os.path.basename(dir_path) == 'tests'


class TestGetAbiPath:
    """Tests for get_abi_path function."""

    def test_returns_correct_path_structure(self):
        """Test that ABI path has correct structure."""
        from utils.bootstrap import get_abi_path

        path = get_abi_path('aave', 'aave_abi.json')
        assert 'projects' in path
        assert 'aave' in path
        assert 'aave_abi.json' in path

    def test_returns_absolute_path(self):
        """Test that ABI path is absolute."""
        from utils.bootstrap import get_abi_path

        path = get_abi_path('compound', 'compound_abi.json')
        assert os.path.isabs(path)
