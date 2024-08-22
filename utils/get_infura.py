import sys, os
from web3 import Web3

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

def select_infura(chain):
    infura_key = os.getenv('INFURA_KEY')
    if not infura_key:
        raise ValueError("INFURA_KEY not found in environment variables")

    if chain == "ethereum":
        infura_url = "https://mainnet.infura.io/v3/"
    elif chain == "optimism":
        infura_url = "https://optimism-mainnet.infura.io/v3/"
    elif chain == "arbitrum":
        infura_url = "https://arbitrum-mainnet.infura.io/v3/"
    elif chain == "Polygon":
        infura_url = "https://polygon-mainnet.infura.io/v3/"
    else:
        infura_url = None

    return Web3(Web3.HTTPProvider(infura_url + infura_key))
