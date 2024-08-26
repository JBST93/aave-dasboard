
import sys, os
from dotenv import load_dotenv
from datetime import datetime
import requests

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

from app import app, db
from instances.TokenData import TokenData as Info
from utils.get_infura import select_infura
from utils.get_price import get_price
from utils.load_abi import load_abi

tokens_info = [
    {
        "token": "LUSD",
        "decimals": 18,
        "contract_address":"0x5f98805A4E8be255a32880FDeC7F6728C6568bA0",
        "provider_abi": load_abi("liquity",'LUSD_abi.json'),
        "chain":"ethereum",

    },
    {
        "token": "LQTY",
        "decimals": 18,
        "contract_address":"0x6dea81c8171d0ba574754ef6f8b412f2ed88c54d",
        "api": "https://api.liquity.org/v1/lqty_circulating_supply.txt",
        "chain":"ethereum",
        "tot_supply":100000000

    }

]

def get_token():
    with app.app_context():
        for token in tokens_info:
            price = get_price(token["token"], token["contract_address"], token["chain"])

            if "api" in token:
                circl_supply = float(requests.get(token["api"]).text.strip())
            else:
                web3 = select_infura(token["chain"])
                pool_contract = web3.eth.contract(address=token["contract_address"], abi=token["provider_abi"])
                circ_supply_raw = pool_contract.functions.totalSupply().call()
                circl_supply = circ_supply_raw / 10**token["decimals"]

            circ_supply_usd = circl_supply * price

            if "tot_supply" in token:
                tot_supply = float(token["tot_supply"])
            else:
                tot_supply = float(circl_supply)

            info = Info(
                token=token["token"],
                price=price,
                price_source="",
                tot_supply=10000000,
                circ_supply=tot_supply,
                tvl=0,
                revenue=0,
                timestamp=datetime.utcnow()
            )
            db.session.add(info)
            db.session.commit()
