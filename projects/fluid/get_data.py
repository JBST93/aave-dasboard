from web3 import Web3
from dotenv import load_dotenv
import os
import sys
import json
from datetime import datetime

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

def load_abi_simple(project, filename):
    """Simple function to load ABI from file"""
    abi_path = os.path.join(project_root, 'abi', project, filename)
    with open(abi_path) as f:
        return json.load(f)


from utils.get_price import get_price
from utils.get_last_price_db import get_latest_price
from utils.get_infura import select_infura


GOV_TOKEN = "FLUID"
GOV_TOKEN_PRICE = get_price("FLUID")
CHAIN = "ethereum"
LENDING_FACTORY = "0x54B91A0D94cb471F37f949c60F7Fa7935b551D03"
LENDING_FACTORY_ABI = load_abi_simple("fluid",'fluid_factory_abi.json')
FTOKEN_ABI = load_abi_simple("fluid",'ftoken_abi.json')

# 1. Get all lending pools:

web3 = select_infura(CHAIN)
pool_contract = web3.eth.contract(address=LENDING_FACTORY, abi=LENDING_FACTORY_ABI)
asset_adresses = pool_contract.functions.allTokens().call()

for asset_adress in asset_adresses:
    print(asset_adress)
    pool_contract = web3.eth.contract(address=asset_adress, abi=FTOKEN_ABI)
    symbol = pool_contract.functions.symbol().call()
    totalAssets = pool_contract.functions.totalAssets().call()
    decimals = pool_contract.functions.decimals().call()
    totalAssets_usd = totalAssets / 10**decimals * GOV_TOKEN_PRICE
    print(symbol, totalAssets_usd)
