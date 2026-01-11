"""
Centralized configuration constants for the Aave Dashboard.

This module contains all configurable thresholds and lists that were
previously hardcoded across multiple files.
"""

# Minimum TVL (in USD) for a yield rate to be included in API responses
MIN_TVL_THRESHOLD = 1000

# Maximum age (in hours) for yield data to be considered fresh
DATA_FRESHNESS_HOURS = 3

# List of recognized stablecoins for filtering stablecoin-specific yields
STABLECOINS = [
    'USDC',
    'USDT',
    'DAI',
    'GHO',
    'USDe',
    'LUSD',
    'crvUSD',
    'PYUSD',
    'FRAX',
    'RLUSD',
    'USTB',
    'USCC',
    'USYC',
    'USDS',
]

# Supported blockchain networks
SUPPORTED_CHAINS = [
    'ethereum',
    'arbitrum',
    'optimism',
    'polygon',
    'avalanche',
    'base',
]
