
import sys, os
from dotenv import load_dotenv
from datetime import datetime
import requests

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

from app import app, db
from utils.get_infura import select_infura
from utils.get_price import get_price
from utils.load_abi import load_abi


token = "LUSD"
decimals = 18

token_2 = "LQTY"
decimals_2 = 18

contracts = {
    "ethereum":"0x5f98805A4E8be255a32880FDeC7F6728C6568bA0",
}

provider_abi = load_abi("liquity",'LUSD_abi.json')

for chain, contract in contracts.items():

    web3 = select_infura(chain)
    pool_contract = web3.eth.contract(address=contract, abi=provider_abi)

    price = get_price(token,contract,chain)

    circ_supply_raw = pool_contract.functions.totalSupply().call()
    circl_supply = circ_supply_raw / 10**18
    circ_supply_usd = circl_supply / price

    tvl = circ_supply_usd

    print(f"{price} - {circ_supply}")
