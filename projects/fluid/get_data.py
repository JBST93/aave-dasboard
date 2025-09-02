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
    abi_path = os.path.join(project_root,'projects', project, filename)
    with open(abi_path) as f:
        return json.load(f)


from utils.get_price import get_price
from utils.get_infura import select_infura


GOV_TOKEN = "FLUID"
CHAIN = "ethereum"
FTOKEN_ABI = load_abi_simple("fluid",'data.json')


web3 = select_infura(CHAIN)
contract_address = '0xC215485C572365AE87f908ad35233EC2572A3BEC'
contract = web3.eth.contract(address=contract_address, abi=FTOKEN_ABI)
dataset = contract.functions.getFTokensEntireData().call()

for data in dataset:
    token = {
        "token_symbol": data[4],
        "decimals": data[5],'fUSDC'
        "convert_to_shares": data[9],  # e.g., 876914 (scaled by 1e6)
        "convert_to_assets": data[10]
        }
    print(token)

print(data[0])
