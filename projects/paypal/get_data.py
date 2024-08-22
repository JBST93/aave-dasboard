import sys, os
from dotenv import load_dotenv
from datetime import datetime

from solana.rpc.api import Client
from solders.pubkey import Pubkey

import base58
from web3 import Web3

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

load_dotenv(os.path.join(project_root, '.env'))

from app import app, db
from scripts.utils import load_abi
from utils.get_price import get_price
from instances.TokenData import TokenData as Data

provider_abi = load_abi("paypal",'pyusd_abi.json')

infura_url = "https://mainnet.infura.io/v3/"

infura_key = os.getenv('INFURA_KEY')
if not infura_key:
    raise ValueError("INFURA_KEY not found in environment variables")

token = "pyUSD"
ETH_contract = "0x6c3ea9036406852006290770BEdFcAbA0e23A0e8"
SOL_contract = "2b1kV6DkPAnxd5ixfnxCpjxmKwqjjaYmCZfHsFu24GXo"
decimals = 6

# Fetch SOL
def get_sol_supply():
    solana_client = Client("https://api.mainnet-beta.solana.com")
    SOL_contract_bytes = base58.b58decode(SOL_contract)
    SOL_contract_pubkey = Pubkey.from_bytes(SOL_contract_bytes)
    response = solana_client.get_token_supply(SOL_contract_pubkey)
    supply = float(response.value.amount) / 10**decimals
    return supply

def get_evm_supply():
    infura_url = "https://mainnet.infura.io/v3/"
    web3 = Web3(Web3.HTTPProvider(infura_url + infura_key))
    contract = web3.eth.contract(address=ETH_contract, abi=provider_abi)
    supply = contract.functions.totalSupply().call()
    supply = supply / 10 ** decimals
    return supply


def get_supply():
    price = get_price(token,ETH_contract,"ethereum")
    sol_supply = get_sol_supply()
    evm_supply = get_evm_supply()
    total_supply = sol_supply + evm_supply


    data = Data (
        token=token,
        price=price,
        price_source= "",
        tot_supply= total_supply,
        circ_supply= total_supply ,
        timestamp=datetime.utcnow(),
    )

    db.session.add(data)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        get_supply()
