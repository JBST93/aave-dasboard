from web3 import Web3
from dotenv import load_dotenv
from sqlalchemy import desc
import os
import sys
from datetime import datetime


# Ensure the root directory is in the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

load_dotenv(os.path.join(project_root, '.env'))

from app import app, db
from instances.YieldRate import YieldRate
from instances.TokenData import TokenData as Info

from scripts.utils import load_abi, insert_yield_db

pool_abi = load_abi("clearpool",'getpool_abi.json')


smart_contracts = {
    "Ethereum":"0xdE204e5a060bA5d3B63C7A4099712959114c2D48",
    "Optimism":"0x99C10A7aBd93b2db6d1a2271e69F268a2c356b80",
    "Mantle":"0xB217D93a8f6A4b7861bB2C865a8C22105FbCdE41"
    }

infura_url = {
    "Ethereum": "https://mainnet.infura.io/v3/",
    "Optimism": "https://optimism-mainnet.infura.io/v3/",
    "Mantle": "https://mantle-mainnet.infura.io/v3/"
    }

infura_key = os.getenv('INFURA_KEY')
if not infura_key:
    raise ValueError("INFURA_KEY not found in environment variables")

def token_price():
    record = db.session.query(Info).filter(
            Info.token == 'CPOOL').order_by(desc(Info.timestamp)).first()
    return record.price if record is not None else 0.1


def get_info(total_borrow, total_lend):
    price = token_price()
    tvl_usd = total_borrow - total_lend

    info = Info(
        token="CPOOL",
        price=price,
        price_source="",
        tot_supply=1000000000,
        circ_supply=1000000000,
        tvl=tvl_usd,
        revenue=0,
        timestamp=datetime.utcnow()
    )
    db.session.add(info)
    db.session.commit()

    return

def fetch_store_rates():
    price = token_price()
    total_borrow = 0
    total_lend = 0

    for chain, contract_address in smart_contracts.items():
        web3 = Web3(Web3.HTTPProvider(infura_url[chain] + infura_key))
        pool_contract = web3.eth.contract(address=contract_address, abi=pool_abi)

        data = pool_contract.functions.getPools().call()
        with app.app_context():
            for item in data:
                clearpool_abi = load_abi("clearpool",'pool_abi.json')
                try:
                    pool_contract = web3.eth.contract(address=contract_address, abi=clearpool_abi)
                    pool_data = web3.eth.contract(address=item, abi=clearpool_abi)

                    market = pool_data.functions.symbol().call().partition("-")[2]
                    information = pool_data.functions.name().call()

                    lend_amount = pool_data.functions.poolSize().call()
                    lend_amount_transformed = lend_amount/1e6 if lend_amount != 0 else 0

                    borrow_amount = pool_data.functions.borrows().call()
                    borrow_amount_transformed = borrow_amount/1e6 if borrow_amount != 0 else 0

                    supply_rate = pool_data.functions.getSupplyRate().call()
                    supply_rate_annualised = round(float(supply_rate)/1e18*31536000 * 100,2)

                    total_borrow += borrow_amount_transformed
                    total_lend += lend_amount_transformed



                    reward_rate = pool_data.functions.rewardPerSecond().call()
                    reward_rate_transformed = round(float(reward_rate * 31536000 / 1e12 * price) / lend_amount * 100,2)

                    reward_token = "CPOOL"

                    smart_contract = item
                    business = "Lending"
                    project = "ClearPool"
                    chain = chain

                    insert_yield_db(market, project, information, supply_rate_annualised,reward_rate_transformed,reward_token,lend_amount_transformed,chain, business, smart_contract)

                except Exception as e:
                    print(f"Error fetching data for {item}: {e}")

            db.session.commit()

        return total_borrow, total_lend

if __name__ == '__main__':
        with app.app_context():
            total_borrow, total_lend = fetch_store_rates()
            get_info(total_borrow, total_lend)
