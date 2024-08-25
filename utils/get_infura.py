import sys
import os
from web3 import Web3

# Add project root to sys.path for imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

def select_infura(chain):
    infura_key = os.getenv('INFURA_KEY')
    fantom_key = os.getenv("FANTOM_KEY")

    if not infura_key and chain != "fantom":
        raise ValueError("INFURA_KEY not found in environment variables")

    if chain == "fantom" and not fantom_key:
        raise ValueError("FANTOM_KEY not found in environment variables")

    infura_urls = {
        "ethereum": "https://mainnet.infura.io/v3/",
        "optimism": "https://optimism-mainnet.infura.io/v3/",
        "arbitrum": "https://arbitrum-mainnet.infura.io/v3/",
        "polygon": "https://polygon-mainnet.infura.io/v3/",
        "bsc": "https://bsc-mainnet.infura.io/v3/",
        "fantom": "https://fantom-mainnet.core.chainstack.com/",
        "base": "https://mainnet.base.org",
        "avalanche":"",
    }

    infura_url = infura_urls.get(chain)

    if infura_url is None:
        raise ValueError(f"Unsupported chain: {chain}")

    # For fantom, use the fantom key instead of infura key
    if chain == "fantom":
        return Web3(Web3.HTTPProvider(infura_url + fantom_key))

    # No key needed for the 'base' chain
    if chain == "base":
        return Web3(Web3.HTTPProvider(infura_url))

    return Web3(Web3.HTTPProvider(infura_url + infura_key))
