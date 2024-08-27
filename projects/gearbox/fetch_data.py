from web3 import Web3
from dotenv import load_dotenv
import os
import sys
import json
from datetime import datetime


# Ensure the root directory is in the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

from app import app,db
from instances.YieldRate import YieldRate as Data
from scripts.utils import load_abi, insert_yield_db

# Load environment variables
load_dotenv(os.path.join(project_root, '.env'))

# Connect to an Ethereum node
infura_url = os.getenv('INFURA_URL')
web3 = Web3(Web3.HTTPProvider(infura_url))

pool_contract_address = {
    "USDC":"0xda00000035fef4082F78dEF6A8903bee419FbF8E",
    "USDT":"0x05A811275fE9b4DE503B3311F51edF6A856D936e",
    "GHO": "0x4d56c9cBa373AD39dF69Eb18F076b7348000AE09",
    "DAI": "0xe7146F53dBcae9D6Fa3555FE502648deb0B2F823",
    "crvUSD":"0x8ef73f036feec873d0b2fd20892215df5b8bdd72",
}

provider_abi = load_abi("gearbox","gearbox_abi.json")


def fetch_store_data():
    with app.app_context():
        try:
            for token,address in pool_contract_address.items():
                pool_contract = web3.eth.contract(address=address, abi=provider_abi)

                apy_base = pool_contract.functions.supplyRate().call()

            # Convert from Ray (scaled by 1e27) to a percentage
                yield_rate_base = apy_base / 1e27 * 100
                yield_rate_reward = None
                yield_token_reward=None

                total_supply_raw = pool_contract.functions.totalSupply().call()
                if token == "USDC" or token =="USDT":
                    tvl = total_supply_raw/1e6
                else:
                    tvl = total_supply_raw/1e18

                project = "Gearbox"
                chain = "Ethereum"
                type="Lending"
                information=None

                insert_yield_db(token,project,information,yield_rate_base,yield_rate_reward,yield_token_reward,tvl,chain,type,address)



        except Exception as e:
            print(f"Error fetching {token} Saving Rate: {e}", 500)

        print("Gearbox Fetched")

        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        fetch_store_data()
