import sys, os
from web3 import Web3

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

def select_infura(chain):
    infura_key = os.getenv('INFURA_KEY')
    if not infura_key:
        raise ValueError("INFURA_KEY not found in environment variables")

    fantom_key = os.getenv("FANTOM_KEY")
    if not fantom_key:
        raise ValueError("FANTOM_KEY not found in environment variables")

    if chain == "ethereum":
        infura_url = "https://mainnet.infura.io/v3/"
        return Web3(Web3.HTTPProvider(infura_url + infura_key))
    elif chain == "optimism":
        infura_url = "https://optimism-mainnet.infura.io/v3/"
        return Web3(Web3.HTTPProvider(infura_url + infura_key))
    elif chain == "arbitrum":
        infura_url = "https://arbitrum-mainnet.infura.io/v3/"
        return Web3(Web3.HTTPProvider(infura_url + infura_key))

    elif chain == "polygon":
        infura_url = "https://polygon-mainnet.infura.io/v3/"
        return Web3(Web3.HTTPProvider(infura_url + infura_key))

    elif chain == "bsc":
        infura_url = "https://bsc-mainnet.infura.io/v3/"
        return Web3(Web3.HTTPProvider(infura_url + infura_key))

    elif chain =="base":
        infura_url ="https://mainnet.base.org"
        return Web3(Web3.HTTPProvider(infura_url))

    elif chain =="fantom":
        infura_url = "https://fantom-mainnet.core.chainstack.com/"
        return Web3(Web3.HTTPProvider(infura_url + fantom_key))

    else:
        infura_url = None
