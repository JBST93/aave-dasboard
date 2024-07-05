from web3 import Web3
from dotenv import load_dotenv
import os
import sys
import json
import math
from datetime import datetime

# Ensure the root directory is in the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

# Import the db and MoneyMarketRate from db_config
from db_config import app, db, MoneyMarketRate

# Load environment variables
load_dotenv(os.path.join(project_root, '.env'))


# Connect to an Ethereum node
infura_url = os.getenv('INFURA_URL')
web3 = Web3(Web3.HTTPProvider(infura_url))

pool_contract_address = {
    "USDC":"0xda00000035fef4082F78dEF6A8903bee419FbF8E",
    "USDT":"0x05A811275fE9b4DE503B3311F51edF6A856D936e",
    "GHO": "0x4d56c9cBa373AD39dF69Eb18F076b7348000AE09",
    "DAI": "0xe7146F53dBcae9D6Fa3555FE502648deb0B2F823"
}
with open('gearbox_abi.json') as f:
    try:
        provider_abi = json.load(f)
    except FileNotFoundError:
        exit(1)


def fetch_store_rates():
    with app.app_context():
        try:
            for token,value in pool_contract_address.items():
                pool_contract = web3.eth.contract(address=value, abi=provider_abi)

            # Fetch lending rates
                supply_apy_raw = pool_contract.functions.supplyRate().call()

            # Convert from Ray (scaled by 1e27) to a percentage
                supply_apy = supply_apy_raw / 1e27 * 100

                total_supply_raw = pool_contract.functions.totalSupply().call()
                total_supply = total_supply_raw/1e6

                print(total_supply)


                rate = MoneyMarketRate(
                    token=token,
                    protocol="Gearbox",
                    liquidity_rate=supply_apy,
                    borrow_rate=0,
                    tvl=total_supply,
                    timestamp=datetime.utcnow()
                )
                db.session.add(rate)
                print("Fetched")


        except Exception as e:
            print(f"Error fetching {token} Saving Rate: {e}", 500)

        db.session.commit()


    # return "Fetched"



fetch_store_rates()
