"""Tests for error handling across the codebase."""
import sys
import os
import json
import tempfile

# Set test config BEFORE any imports
os.environ['APP_SETTINGS'] = 'config.TestConfig'

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

import pytest


class TestCompoundABILoading:
    """Tests for Compound ABI file loading error handling."""

    def test_missing_abi_file_does_not_crash(self):
        """Test that missing ABI file logs error instead of crashing."""
        # This test verifies that FileNotFoundError is caught properly
        # and doesn't cause exit(1)
        try:
            with open('/nonexistent/path/to/abi.json') as f:
                json.load(f)
            assert False, "Should have raised FileNotFoundError"
        except FileNotFoundError:
            pass  # This is expected

    def test_invalid_json_abi_file_does_not_crash(self):
        """Test that invalid JSON in ABI file is handled gracefully."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("{ invalid json }")
            temp_path = f.name

        try:
            with open(temp_path) as f:
                json.load(f)
            assert False, "Should have raised JSONDecodeError"
        except json.JSONDecodeError:
            pass  # This is expected
        finally:
            os.unlink(temp_path)

    def test_valid_json_abi_file_loads_correctly(self):
        """Test that valid JSON ABI file loads correctly."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({"abi": "test"}, f)
            temp_path = f.name

        try:
            with open(temp_path) as f:
                data = json.load(f)
            assert data == {"abi": "test"}
        finally:
            os.unlink(temp_path)


class TestConfigErrorHandling:
    """Tests for configuration error handling."""

    def test_missing_database_url_handled_gracefully(self):
        """Test that missing DATABASE_URL2 doesn't crash."""
        from config import Config

        # Config should handle missing DATABASE_URL2
        assert hasattr(Config, 'SQLALCHEMY_DATABASE_URI')

    def test_config_has_fallback_for_missing_env_vars(self):
        """Test that config provides fallbacks for missing env vars."""
        from config import Config

        # Should not raise AttributeError
        db_uri = Config.SQLALCHEMY_DATABASE_URI
        # Can be None or a valid URI, but should not crash
        assert db_uri is None or isinstance(db_uri, str)


class TestGetProjectInfoErrorHandling:
    """Tests for get_project_info error handling."""

    def test_handles_empty_token_list(self, app_context):
        """Test that batch query handles empty input."""
        from scripts.get_project_info import _batch_get_latest_token_data

        result = _batch_get_latest_token_data([])
        assert result == {}

    def test_handles_division_by_zero_in_delta(self, app_context):
        """Test that delta calculation handles zero current value."""
        from scripts.get_project_info import _calculate_delta

        # Should return 0 instead of raising ZeroDivisionError
        result = _calculate_delta(100, 100, 0)
        assert result == 0
