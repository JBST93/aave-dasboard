import requests, sys, os
from web3 import Web3
from dotenv import load_dotenv
from datetime import datetime

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

load_dotenv(os.path.join(project_root, '.env'))

from app import app, db
from scripts.utils import load_abi
from utils.get_price import get_price
from instances.TokenData import TokenData as Data

infura_url = "https://mainnet.infura.io/v3/"
infura_key = os.getenv('INFURA_KEY')
if not infura_key:
    raise ValueError("INFURA_KEY not found in environment variables")


tokens = [
    {
        "token": "USDe",
        "address": "0x4c9EDD5852cd905f086C759E8383e09bff1E68B3",
        "chain": "ethereum",
        "decimals":18,
        "abi": load_abi("ethena",'USDe_abi.json')
    },
    {
        "token": "ENA",
        "address": "0x57e114B691Db790C35207b2e685D4A43181e6061",
        "chain": "ethereum",
        "decimals":18,
        "abi": load_abi("ethena",'ENA_abi.json')
    }
]


def get_data():
    with app.app_context():

        for token in tokens:
            try:
                web3 = Web3(Web3.HTTPProvider(infura_url + infura_key))
                pool_contract = web3.eth.contract(address=token["address"], abi=token["abi"])
                supply_raw = float(pool_contract.functions.totalSupply().call())
                supply_transformed = float(supply_raw / 10**token["decimals"])
                price = get_price(token["token"], token["address"], token["chain"])

                data = Data (
                    token=token["token"],
                    price=price,
                    price_source= None,
                    tot_supply= float(supply_transformed),
                    circ_supply= float(supply_transformed),
                    timestamp=datetime.utcnow(),
                )

                db.session.add(data)

                print(data)
                print(supply_transformed)

                db.session.add(data)
            except Exception as e:
                print(e)

        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        get_data()
