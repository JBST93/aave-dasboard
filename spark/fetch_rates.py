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

pool_contract_address = "0x197E90f9FAD81970bA7976f33CbD77088E5D7cf7" #DSR contract
token = "DAI"

with open('sdai_abi.json') as f:
    try:
        provider_abi = json.load(f)
    except FileNotFoundError:
        print("ABI file not found. Please make sure 'sdai_abi.json' is in the current directory.")
        exit(1)

pool_contract = web3.eth.contract(address=pool_contract_address, abi=provider_abi)


def fetch_store_rates():
    try:
        with app.app_context():

         # Fetch DAI savings rate per second
            dai_saving_rate_second = pool_contract.functions.dsr().call()

            # Convert from Ray (scaled by 1e27) to a percentage
            dai_saving_rate_second_transformed = dai_saving_rate_second / 1e27

            # Calculate APR using continuous compounding formula
            apr_continuous = math.exp(math.log(dai_saving_rate_second_transformed) * 31536000) - 1

            # Convert to percentage
            APY = apr_continuous * 100 #DSR rate

            rate = MoneyMarketRate(
                token=token,
                protocol="DSR",
                liquidity_rate=APY,
                borrow_rate=0,
                timestamp=datetime.utcnow()
            )
            db.session.add(rate)
            db.session.commit()
            print("Fetched")


    except Exception as e:
        print(f"Error fetching {token} Saving Rate: {e}", 500)

    # return "Fetched"



fetch_store_rates()
