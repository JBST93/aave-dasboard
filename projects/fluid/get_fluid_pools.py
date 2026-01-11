from web3 import Web3
from dotenv import load_dotenv
import os
import sys
import json
import logging

logger = logging.getLogger(__name__)

# Setup paths
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

# Load environment variables
load_dotenv(os.path.join(project_root, '.env'))

def load_abi_simple(project, filename):
    """Simple function to load ABI from file"""
    abi_path = os.path.join(project_root, 'projects', project, filename)
    with open(abi_path) as f:
        return json.load(f)

def get_web3():
    """Simple function to get Web3 instance"""
    infura_url = f"https://mainnet.infura.io/v3/{os.getenv('INFURA_KEY')}"
    return Web3(Web3.HTTPProvider(infura_url))

# Constants
LENDING_FACTORY = "0x54B91A0D94cb471F37f949c60F7Fa7935b551D03"
LENDING_FACTORY_ABI = load_abi_simple("fluid", 'fluid_factory_abi.json')
FTOKEN_ABI = load_abi_simple("fluid",'ftoken_abi.json')

def main():
    # Get Web3 instance
    web3 = get_web3()

    # Create contract instance
    pool_contract = web3.eth.contract(address=LENDING_FACTORY, abi=LENDING_FACTORY_ABI)

    # Get all lending pools
    asset_adresses = pool_contract.functions.allTokens().call()

    for asset_adress in asset_adresses:
        pool_contract = web3.eth.contract(address=asset_adress, abi=FTOKEN_ABI)
        symbol = pool_contract.functions.symbol().call()
        totalAssets = pool_contract.functions.totalAssets().call()
        decimals = pool_contract.functions.decimals().call()
        totalAssets_usd = totalAssets / 10**decimals
        logger.info(f"{symbol} {totalAssets_usd}")

if __name__ == "__main__":
    main()
