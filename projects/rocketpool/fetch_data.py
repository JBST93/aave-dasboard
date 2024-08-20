import requests, sys, os
from web3 import Web3
from dotenv import load_dotenv
from datetime import datetime

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

load_dotenv(os.path.join(project_root, '.env'))

from app import app, db
from scripts.utils import load_abi, get_curve_price
from utils.get_price import get_price
from instances.TokenData import TokenData as Data


provider_abi = load_abi("rocketpool",'rocketpool_abi.json')

infura_url = "https://mainnet.infura.io/v3/"
infura_key = os.getenv('INFURA_KEY')
if not infura_key:
    raise ValueError("INFURA_KEY not found in environment variables")


rETH_contract = "0xae78736Cd615f374D3085123A210448E74Fc6393"
token = "rETH"
chain = "ethereum"

def get_data_reth():
    web3 = Web3(Web3.HTTPProvider(infura_url + infura_key))
    pool_contract = web3.eth.contract(address=rETH_contract, abi=provider_abi)
    supply_raw = float(pool_contract.functions.totalSupply().call())
    decimals = 18

    supply_transformed = supply_raw / 10**decimals

    price = get_price(token, rETH_contract, chain)

    supply_usd = supply_transformed * price

    print(f"{token} - {price} - {supply_usd}")

    data = Data (
        token= token,
        price=price,
        price_source= "",
        tot_supply= supply_transformed,
        circ_supply= supply_transformed ,
        timestamp=datetime.utcnow(),
    )

    db.session.add(data)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        get_data_reth()
