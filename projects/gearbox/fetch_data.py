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


script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path to the aave_abi.json file
abi_path = os.path.join(script_dir, 'gearbox_abi.json')

with open(abi_path) as f:
    try:
        provider_abi = json.load(f)
    except FileNotFoundError:
        exit(1)


def fetch_store_data():
    print("Starting to Fetch Data for Gearbox")
    with app.app_context():
        try:
            for token,address in pool_contract_address.items():
                pool_contract = web3.eth.contract(address=address, abi=provider_abi)

                apy_base = pool_contract.functions.supplyRate().call()

            # Convert from Ray (scaled by 1e27) to a percentage
                apy_base_formatted = apy_base / 1e27 * 100

                total_supply_raw = pool_contract.functions.totalSupply().call()
                if token == "USDC" or token =="USDT":
                    total_supply = total_supply_raw/1e6
                else:
                    total_supply = total_supply_raw/1e18

                chain = "Ethereum"
                type="Lending"


                data = Data(
                    market=token,
                    project="Gearbox",
                    information="",
                    yield_rate_base=float(apy_base_formatted),
                    yield_rate_reward=None,
                    yield_token_reward=None,
                    tvl=total_supply,
                    chain=chain,
                    type=type,
                    smart_contract=address,
                    timestamp=datetime.utcnow()
                )

                db.session.add(data)


        except Exception as e:
            print(f"Error fetching {token} Saving Rate: {e}", 500)
        print("Gearbox Fetched")

        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        fetch_store_data()
