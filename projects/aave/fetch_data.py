from web3 import Web3
import requests
from dotenv import load_dotenv
import os
import sys
import json
from datetime import datetime

from sqlalchemy import inspect


# Ensure the root directory is in the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

# Load environment variables
load_dotenv(os.path.join(project_root, '.env'))

# Import app and db from the root directory
from app import app, db
from instances.YieldRate import YieldRate



script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path to the aave_abi.json file
abi_path = os.path.join(script_dir, 'aave_abi.json')

with open(abi_path) as f:
    try:
        provider_abi = json.load(f)
    except FileNotFoundError:
        exit(1)

smart_contracts = {
    "Ethereum":"0x7B4EB56E7CD4b454BA8ff71E4518426369a138a3",
    "Arbitrum":"0x69FA688f1Dc47d4B5d8029D5a35FB7a548310654",
    "Optimism":"0x69FA688f1Dc47d4B5d8029D5a35FB7a548310654",
    "Polygon":"0x69FA688f1Dc47d4B5d8029D5a35FB7a548310654",
}

infura_url ={
    "Ethereum":"https://mainnet.infura.io/v3/",
    "Arbitrum":"https://arbitrum-mainnet.infura.io/v3/",
    "Optimism":"https://optimism-mainnet.infura.io/v3/",
    "Polygon":"https://polygon-mainnet.infura.io/v3/",
}

# Connect to an Ethereum node
infura_key = os.getenv('INFURA_KEY')
if not infura_key:
    raise ValueError("INFURA_KEY not found in environment variables")


def get_curve_price(contract_address):
    curve_api = "https://prices.curve.fi/v1/usd_price/ethereum"
    r = requests.get(curve_api)
    data = r.json()
    data = data["data"] ## Gives a lits
    ## iterate through the list to match the contract address
    for pool in data:
        if pool.get("address").lower() == contract_address.lower():  # Ensure case-insensitive comparison
            return round(float(pool.get("usd_price")),2)

def fetch_store_rates():

    print("Starting Fetching Data for AaveV3")
    for chain, contract_address in smart_contracts.items():
        print(f"Fetching Aave v3 data for {chain}...")

        web3 = Web3(Web3.HTTPProvider(infura_url[chain] + infura_key))
        pool_contract = web3.eth.contract(address=contract_address, abi=provider_abi)

        data = pool_contract.functions.getAllReservesTokens().call()
        for item in data:
            try:
                token = item[0]
                contract = item[1]
                reserve_data = pool_contract.functions.getReserveData(contract).call()

                apy_base = reserve_data[5] / 1e27 * 100  # Convert from Ray to percentage
                apy_base_formatted = round(apy_base, 2)

                raw_tvl = pool_contract.functions.getATokenTotalSupply(contract).call()

                if token in ['USDC', 'pyUSD', 'USDT']:  # TVL in LCY - need to find USD
                    tvl = raw_tvl / 1e6  # These tokens have 6 decimal places
                else:
                    tvl = raw_tvl / 1e18  # Default to 18 decimal places for other tokens

                # Need to find TVL_USD
                tvl_usd = tvl
                information = ""
                type = "lending market"

                print(f"Inserting data: {token}, {apy_base_formatted}, {tvl_usd}, {chain}, {contract}")

                data = YieldRate(
                    market=token,
                    project="Aave v3",
                    information=information,
                    yield_rate_base=float(apy_base_formatted),
                    yield_rate_reward=None,
                    yield_token_reward=None,
                    tvl=tvl_usd,
                    chain=chain,
                    type=type,
                    smart_contract=contract,
                    timestamp=datetime.utcnow()
                )

                db.session.add(data)

            except Exception as e:
                print(f"Error fetching data for {token}: {e}")

            db.session.commit()
        print("Aave v3 data fetched and committed")

if __name__ == '__main__':
    with app.app_context():
        fetch_store_rates()
