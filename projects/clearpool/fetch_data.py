from web3 import Web3
from dotenv import load_dotenv
from sqlalchemy import desc
import os
import sys


# Ensure the root directory is in the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

load_dotenv(os.path.join(project_root, '.env'))

from app import app, db
from instances.YieldRate import YieldRate
from instances.TokenData import TokenData as Price

from scripts.utils import load_abi, insert_yield_db

pool_abi = load_abi("clearpool",'getpool_abi.json')

# 0xdE204e5a060bA5d3B63C7A4099712959114c2D48 -> To get pool getPools


smart_contracts = {
    "Ethereum":"0xdE204e5a060bA5d3B63C7A4099712959114c2D48"}

infura_url ={
    "Ethereum":"https://mainnet.infura.io/v3/"}

infura_key = os.getenv('INFURA_KEY')
if not infura_key:
    raise ValueError("INFURA_KEY not found in environment variables")

def token_price():
    record = db.session.query(Price).filter(
            Price.token == 'COMP').order_by(desc(Price.timestamp)).first()
    return record.price if record is not None else 0.1



def fetch_store_rates():
    price = token_price()

    print("Starting Fetching Data for Clearpool")
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



                    borrow_amount = pool_data.functions.poolSize().call()

                    supply_rate = pool_data.functions.getSupplyRate().call()
                    supply_rate_annualised = round(float(supply_rate)/1e18*31536000 * 100,2)

                    reward_rate = pool_data.functions.rewardPerSecond().call()
                    reward_rate_transformed = round(float(reward_rate) * 31536000 / 1e12 * price / borrow_amount * 100,2)

                    reward_token = "CPOOL"

                    smart_contract = item
                    business = "Lending"
                    project = "ClearPool"
                    chain = "ethereum"

                    insert_yield_db(market, project, information, supply_rate_annualised ,None,None,borrow_amount,chain, type, smart_contract)

                    print(f"{information} - {market} - {supply_rate_annualised} - {borrow_amount} - {reward_rate_transformed} {smart_contract}")

                except Exception as e:
                    print(f"Error fetching data for {item}: {e}")

            db.session.commit()
            print("Clearpool data fetched and committed")


if __name__ == '__main__':
        fetch_store_rates()
