"""Tests for get_project_info module."""
import sys
import os

# Set test config BEFORE any imports
os.environ['APP_SETTINGS'] = 'config.TestConfig'

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

import pytest
from datetime import datetime, timedelta


class TestBatchGetLatestTokenData:
    """Tests for _batch_get_latest_token_data function."""

    def test_returns_empty_dict_for_empty_input(self, app_context):
        """Test that empty input returns empty dict."""
        from scripts.get_project_info import _batch_get_latest_token_data

        result = _batch_get_latest_token_data([])
        assert result == {}

    def test_returns_empty_dict_for_nonexistent_tokens(self, app_context):
        """Test that nonexistent tokens return empty dict."""
        from scripts.get_project_info import _batch_get_latest_token_data

        result = _batch_get_latest_token_data(['NONEXISTENT_TOKEN_XYZ'])
        assert result == {}

    def test_returns_dict_keyed_by_token(self, app_context):
        """Test that results are keyed by token name."""
        from scripts.get_project_info import _batch_get_latest_token_data
        from instances.TokenData import TokenData
        from app import db

        # Create test data
        token_data = TokenData(
            token='TEST_TOKEN',
            price=100.0,
            circ_supply=1000000,
            tvl=5000000,
            timestamp=datetime.now()
        )
        db.session.add(token_data)
        db.session.commit()

        result = _batch_get_latest_token_data(['TEST_TOKEN'])

        assert 'TEST_TOKEN' in result
        assert result['TEST_TOKEN'].price == 100.0


class TestBatchGetTokenDataAtTime:
    """Tests for _batch_get_token_data_at_time function."""

    def test_returns_empty_dict_for_empty_input(self, app_context):
        """Test that empty input returns empty dict."""
        from scripts.get_project_info import _batch_get_token_data_at_time

        result = _batch_get_token_data_at_time([])
        assert result == {}


class TestFormatPrice:
    """Tests for _format_price function."""

    def test_small_price_has_6_decimals(self, app_context):
        """Test that prices < 1 have 6 decimal places."""
        from scripts.get_project_info import _format_price

        assert _format_price(0.123456789) == 0.123457

    def test_medium_price_has_4_decimals(self, app_context):
        """Test that prices 1-10 have 4 decimal places."""
        from scripts.get_project_info import _format_price

        assert _format_price(5.123456) == 5.1235

    def test_large_price_has_2_decimals(self, app_context):
        """Test that prices 10-1000 have 2 decimal places."""
        from scripts.get_project_info import _format_price

        assert _format_price(100.123456) == 100.12

    def test_very_large_price_has_0_decimals(self, app_context):
        """Test that prices > 1000 have no decimal places."""
        from scripts.get_project_info import _format_price

        assert _format_price(5000.99) == 5001


class TestGetProjects:
    """Tests for get_projects function."""

    def test_returns_json_response(self, app):
        """Test that get_projects returns a valid JSON response."""
        from scripts.get_project_info import get_projects

        with app.app_context():
            response = get_projects()
            assert response is not None

    def test_handles_empty_database(self, app):
        """Test that get_projects handles empty database gracefully."""
        from scripts.get_project_info import get_projects

        with app.app_context():
            response = get_projects()
            # Should return empty list, not error
            data = response.get_json()
            assert isinstance(data, list)


class TestCalculateDelta:
    """Tests for _calculate_delta function."""

    def test_returns_zero_when_previous_is_none(self, app_context):
        """Test that delta is 0 when no previous value."""
        from scripts.get_project_info import _calculate_delta

        result = _calculate_delta(None, None, 100)
        assert result == 0

    def test_returns_zero_when_current_is_zero(self, app_context):
        """Test that delta is 0 when current value is 0 (avoid division by zero)."""
        from scripts.get_project_info import _calculate_delta

        result = _calculate_delta(100, 100, 0)
        assert result == 0
