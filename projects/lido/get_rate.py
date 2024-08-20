import requests, sys, os
from web3 import Web3
from dotenv import load_dotenv
from datetime import datetime

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

load_dotenv(os.path.join(project_root, '.env'))

from app import app, db
from scripts.utils import load_abi, get_curve_price
from instances.TokenData import TokenData as Data


provider_abi = load_abi("lido",'lido_abi.json')

infura_url = "https://mainnet.infura.io/v3/"

infura_key = os.getenv('INFURA_KEY')
if not infura_key:
    raise ValueError("INFURA_KEY not found in environment variables")

def get_curve_price(address):
    endpoint = f"https://prices.curve.fi/v1/usd_price/ethereum/{address}"
    try:
        r = requests.get(endpoint, timeout=10)
        r.raise_for_status()
        data = r.json()
        price = data.get("data", {}).get("usd_price")
        return float(price)
    except requests.RequestException as e:
        print(f"Error fetching price from Curve: {e}")
    return None


def get_data_steth():
    endpoint = "https://eth-api.lido.fi/v1/protocol/steth/apr/sma"
    r = requests.get(endpoint)
    data = r.json()

    apr = round(data.get("data").get("aprs")[-1].get("apr"),2)
    symbol = data.get("meta").get("symbol")
    address = data.get("meta").get("address")
    decimals = 18

    web3 = Web3(Web3.HTTPProvider(infura_url + infura_key))
    pool_contract = web3.eth.contract(address=address, abi=provider_abi)

    supply_raw = pool_contract.functions.totalSupply().call()
    supply = round(supply_raw/10**decimals,2)

    price = (get_curve_price(address))
    tot_supply_usd = round(supply * price,2)
    circ_supply_usd = round(supply * price,2)


    data = Data (
        token= "stETH",
        price= price,
        supply= supply,
        price_source= "Curve",
        tot_supply= tot_supply_usd,
        circ_supply= circ_supply_usd ,
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
