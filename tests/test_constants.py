"""Tests for centralized constants."""
import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

import pytest
from constants import MIN_TVL_THRESHOLD, DATA_FRESHNESS_HOURS, STABLECOINS, SUPPORTED_CHAINS


class TestMinTvlThreshold:
    """Tests for MIN_TVL_THRESHOLD constant."""

    def test_is_positive_number(self):
        """Test that MIN_TVL_THRESHOLD is a positive number."""
        assert MIN_TVL_THRESHOLD > 0

    def test_is_reasonable_value(self):
        """Test that MIN_TVL_THRESHOLD is a reasonable value (not too high)."""
        assert MIN_TVL_THRESHOLD <= 1000000  # Should be less than $1M


class TestDataFreshnessHours:
    """Tests for DATA_FRESHNESS_HOURS constant."""

    def test_is_positive_number(self):
        """Test that DATA_FRESHNESS_HOURS is a positive number."""
        assert DATA_FRESHNESS_HOURS > 0

    def test_is_reasonable_value(self):
        """Test that DATA_FRESHNESS_HOURS is reasonable (not too long)."""
        assert DATA_FRESHNESS_HOURS <= 24  # Should be less than 24 hours


class TestStablecoins:
    """Tests for STABLECOINS list."""

    def test_is_non_empty_list(self):
        """Test that STABLECOINS is a non-empty list."""
        assert isinstance(STABLECOINS, list)
        assert len(STABLECOINS) > 0

    def test_contains_major_stablecoins(self):
        """Test that STABLECOINS includes major stablecoins."""
        assert 'USDC' in STABLECOINS
        assert 'USDT' in STABLECOINS
        assert 'DAI' in STABLECOINS

    def test_all_entries_are_strings(self):
        """Test that all entries in STABLECOINS are strings."""
        for coin in STABLECOINS:
            assert isinstance(coin, str)
            assert len(coin) > 0


class TestSupportedChains:
    """Tests for SUPPORTED_CHAINS list."""

    def test_is_non_empty_list(self):
        """Test that SUPPORTED_CHAINS is a non-empty list."""
        assert isinstance(SUPPORTED_CHAINS, list)
        assert len(SUPPORTED_CHAINS) > 0

    def test_contains_ethereum(self):
        """Test that SUPPORTED_CHAINS includes Ethereum."""
        assert 'ethereum' in SUPPORTED_CHAINS

    def test_all_entries_are_lowercase(self):
        """Test that all chain names are lowercase."""
        for chain in SUPPORTED_CHAINS:
            assert chain == chain.lower()
