# XVS
# VAI - stable


# isolated pool & core pools


import sys, os
from dotenv import load_dotenv
from datetime import datetime

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

load_dotenv(os.path.join(project_root, '.env'))

from app import app, db

from scripts.utils import load_abi
from utils.get_infura import select_infura
from utils.get_price import get_price

from instances.TokenData import TokenData as Data

token_info = [
    {
    "token": "XVS",
    "contract": "0xcF6BB5389c92Bdda8a3747Ddb454cB7a64626C63",
    "decimals": 18,
    "chain":"bsc",
    "abi": load_abi("venus",'abi.json')
    },
    {
    "token": "VAI",
    "contract": "0x4BD17003473389A42DAF6a0a729f6Fdb328BbBd7",
    "decimals": 18,
    "chain":"bsc",
    "abi": load_abi("venus",'abi.json')
    }
]

def get_store_data():
    with app.app_context():
        for token in token_info:
            try:

                web3 = select_infura(token["chain"])
                contract = web3.eth.contract(address=token["contract"], abi=token["abi"])
                supply = contract.functions.totalSupply().call()
                tot_supply = supply / 10 ** token["decimals"]

                price = float(get_price(token["token"],token["contract"],token["chain"]))
                tvl = tot_supply*price

                data = Data (
                    token=token["token"],
                    price=price,
                    price_source= "",
                    tot_supply= tot_supply,
                    circ_supply= tot_supply,
                    tvl=0,
                    timestamp=datetime.utcnow(),
                )

                print(data)

                db.session.add(data)
            except Exception as e:
                print(f"Error processing token {token['token']}: {e}")

        db.session.commit()

if __name__ == '__main__':
        get_store_data()
