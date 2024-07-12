from web3 import Web3
from dotenv import load_dotenv
import os
import sys
import json
from datetime import datetime

# Ensure the root directory is in the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
load_dotenv(os.path.join(project_root, '.env'))

# Import app and db from the root directory
from app import app, db
from instances.MoneyMarketRate import MoneyMarketRate

# Construct the absolute path to the aave_abi.json file
script_dir = os.path.dirname(os.path.abspath(__file__))
abi_path = os.path.join(script_dir, 'compound_abi.json')

with open(abi_path) as f:
    try:
        provider_abi = json.load(f)
    except FileNotFoundError:
        exit(1)

# Connect to an Ethereum node
infura_url = os.getenv('INFURA_URL')
web3 = Web3(Web3.HTTPProvider(infura_url))

#Compounds contracts
contracts= {
    "USDC":"0xc3d688B66703497DAA19211EEdff47f25384cdc3",
    "USDT":"0x3Afdc9BCA9213A35503b077a6072F3D0d5AB0840",
}


def fetch_store_rates():
    print("Starting Fetching Data for CompoundV3")
    with app.app_context():
        for token, address in contracts.items():
            pool_contract = web3.eth.contract(address=address, abi=provider_abi)
            try:
                # getSupplyRate(Utilization) / (10 ^ 18) * Seconds Per Year (3,154e+7) * 100
                utilization = pool_contract.functions.getUtilization().call()
                supply_rate = pool_contract.functions.getSupplyRate(utilization).call()
                liquidity_rate = supply_rate / 1e18 * 60 * 60 * 24 * 365 * 100

                # Total supply
                tvl = pool_contract.functions.totalSupply().call()
                tvl_transformed = tvl / 1e6

                rate = MoneyMarketRate(
                    token=token,
                    protocol="Compound V3",
                    liquidity_rate=liquidity_rate,
                    borrow_rate=0,
                    chain='Ethereum',
                    tvl=tvl_transformed,
                    timestamp=datetime.utcnow()
                )

                db.session.add(rate)
            except Exception as e:
                print(f"Error fetching data for {token}: {e}")

        db.session.commit()
        print("Coumpound Date Fetched")

if __name__ == '__main__':
    fetch_store_rates()
