"""Tests for database models."""
import sys
import os

# Set test config BEFORE any imports
os.environ['APP_SETTINGS'] = 'config.TestConfig'

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

import pytest
from datetime import datetime


class TestYieldRateModel:
    """Tests for YieldRate model."""

    def test_to_dict_has_unique_keys(self, app_context):
        """Test that to_dict() returns unique keys (no duplicates)."""
        from instances.YieldRate import YieldRate

        rate = YieldRate(
            market='USDC',
            project='Aave',
            information='Main Market',
            yield_rate_base=5.25,
            yield_rate_reward=1.5,
            yield_token_reward='AAVE',
            tvl=1000000.0,
            chain='ethereum',
            type='lending',
            smart_contract='0x1234567890abcdef',
            timestamp=datetime.now()
        )

        result = rate.to_dict()

        # Check that yield_rate_base contains the actual value, not None
        assert result['yield_rate_base'] == 5.25, \
            f"yield_rate_base should be 5.25, got {result['yield_rate_base']}"

        # Check that yield_rate_base_formatted is a separate key
        assert 'yield_rate_base_formatted' in result, \
            "yield_rate_base_formatted key should exist"

        # Verify all expected keys exist and are unique
        expected_keys = [
            'id', 'market', 'project', 'information',
            'yield_rate_base', 'yield_rate_base_formatted',
            'yield_rate_reward', 'yield_token_reward',
            'tvl', 'tvl_formatted', 'chain', 'type',
            'smart_contract', 'timestamp', 'humanized_timestamp'
        ]
        for key in expected_keys:
            assert key in result, f"Missing key: {key}"

        # Count keys to ensure no duplicates (dict automatically dedupes, so check count)
        assert len(result) == len(expected_keys), \
            f"Expected {len(expected_keys)} keys, got {len(result)}"

    def test_to_dict_preserves_all_values(self, app_context):
        """Test that to_dict() preserves all model values correctly."""
        from instances.YieldRate import YieldRate

        timestamp = datetime.now()
        rate = YieldRate(
            market='ETH',
            project='Compound',
            information='V3',
            yield_rate_base=3.75,
            yield_rate_reward=0.5,
            yield_token_reward='COMP',
            tvl=5000000.0,
            chain='arbitrum',
            type='lending',
            smart_contract='0xabcdef1234567890',
            timestamp=timestamp
        )

        result = rate.to_dict()

        assert result['market'] == 'ETH'
        assert result['project'] == 'Compound'
        assert result['information'] == 'V3'
        assert result['yield_rate_base'] == 3.75
        assert result['yield_rate_reward'] == 0.5
        assert result['yield_token_reward'] == 'COMP'
        assert result['tvl'] == 5000000.0
        assert result['chain'] == 'arbitrum'
        assert result['type'] == 'lending'
        assert result['smart_contract'] == '0xabcdef1234567890'


class TestMoneyMarketRateModel:
    """Tests for MoneyMarketRate model."""

    def test_model_fields_exist(self, app_context):
        """Test that MoneyMarketRate has expected fields."""
        from instances.MoneyMarketRate import MoneyMarketRate

        # Check model has required columns
        assert hasattr(MoneyMarketRate, 'protocol')
        assert hasattr(MoneyMarketRate, 'token')
        assert hasattr(MoneyMarketRate, 'liquidity_rate')
        assert hasattr(MoneyMarketRate, 'borrow_rate')
        assert hasattr(MoneyMarketRate, 'chain')


class TestTokenDataModel:
    """Tests for TokenData model."""

    def test_model_fields_exist(self, app_context):
        """Test that TokenData has expected fields."""
        from instances.TokenData import TokenData

        assert hasattr(TokenData, 'token')
        assert hasattr(TokenData, 'price')
        assert hasattr(TokenData, 'tot_supply')
        assert hasattr(TokenData, 'circ_supply')
        assert hasattr(TokenData, 'tvl')


class TestProjectModel:
    """Tests for Project model."""

    def test_model_fields_exist(self, app_context):
        """Test that Project has expected fields."""
        from instances.Projects import Project

        assert hasattr(Project, 'protocol_name')
        assert hasattr(Project, 'token_ticker')
        assert hasattr(Project, 'chain_main')
