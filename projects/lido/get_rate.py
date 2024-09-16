import requests, sys, os
from web3 import Web3
from dotenv import load_dotenv
from datetime import datetime

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

load_dotenv(os.path.join(project_root, '.env'))

from app import app, db
from scripts.utils import load_abi
from instances.TokenData import TokenData as Data
from utils.get_infura import select_infura
from utils.get_price import get_price
from utils.get_last_price_db import get_latest_price

token_list = [
    {
        "token":"stETH",
        "decimals": 18,
        "endpoint":"https://eth-api.lido.fi/v1/protocol/steth/apr/sma",
        "chain":"ethereum",
        "provider_abi": load_abi("lido",'steth_abi.json')
    },
    {
        "token":"wstETH",
        "address":"0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0",
        "decimals": 18,
        "chain":"ethereum",
        "provider_abi": load_abi("lido",'wsteth_abi.json'),
        "endpoint": None,
    }
]

def get_data_steth():
    for token in token_list:
        if token["endpoint"]:
            r = requests.get(token["endpoint"])
            data = r.json()

            apr = round(data.get("data").get("aprs")[-1].get("apr"),2)
            address = data.get("meta").get("address")

        web3 = select_infura(token["chain"])
        pool_contract = web3.eth.contract(address=address, abi=token["provider_abi"])

        supply_raw = pool_contract.functions.totalSupply().call()
        supply = round(supply_raw/10**token["decimals"],2)

        if token["token"] == "wstETH":
            stETH_price = get_latest_price("stETH") or 1
            price = 1.1770 * stETH_price
        else:
            price = get_price(token["token"],address,token["chain"])

        data = Data (
            token= token["token"],
            price= price,
            price_source = "",
            tot_supply= supply,
            circ_supply= supply ,
            timestamp=datetime.utcnow(),
        )

        db.session.add(data)

    db.session.commit()



# Lido collects a percentage of the staking rewards as a protocol fee.
# The exact fee size is defined by the DAO and can be changed in the future via DAO voting.
# To collect the fee, the protocol mints new stETH token shares and assigns them to the fee recipients.
# Currently, the fee collected by Lido protocol is 10% of staking rewards with half of it going to the node operators and the other half going to the protocol treasury.
if __name__ == '__main__':
    with app.app_context():
        get_data_steth()
