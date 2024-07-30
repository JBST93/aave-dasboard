from web3 import Web3
from dotenv import load_dotenv
import os
import sys
import json
from datetime import datetime
import requests

# Ensure the root directory is in the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)
load_dotenv(os.path.join(project_root, '.env'))

# Import app and db from the root directory
from app import app, db
from instances.YieldRate import YieldRate as Data

# Construct the absolute path to the aave_abi.json file
script_dir = os.path.dirname(os.path.abspath(__file__))

#Compounds contracts
contracts= [
    {
        "token":"USDC",
        "address":"0xc3d688B66703497DAA19211EEdff47f25384cdc3",
        "chain":"ethereum"
    },
    {
        "token": "USDT",
        "address":"0x3Afdc9BCA9213A35503b077a6072F3D0d5AB0840",
        "chain": "ethereum"
    },
    {
        "token": "USDC",
        "address":"0x9c4ec768c28520B50860ea7a15bd7213a9fF58bf",
        "chain": "arbitrum"
    },
    {
        "token": "USDC",
        "address":"0x2e44e174f7D53F0212823acC11C01A11d58c5bCB",
        "chain": "optimism"
    },
    {
        "token": "USDT",
        "address": "0xd98Be00b5D27fc98112BdE293e487f8D4cA57d07",
        "chain": "arbitrum"
    },
    {
        "token":"USDT",
        "address":"0x2e44e174f7D53F0212823acC11C01A11d58c5bCB",
        "chain":"optimism"
    },
    {
        "token":"wETH",
        "address":"0xA17581A9E3356d9A858b789D68B4d866e593aE94",
        "chain":"ethereum"
    }


]

def get_comp_price():
    r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=COMPUSDT")
    data = r.json()
    price = data.get("price",{})
    if price is not None:
            return float(price)
    else:
            return 0

def fetch_store_rates():
    print("Starting Fetching Data for Compound V3")
    with app.app_context():
        for contract in contracts:
            market = contract["token"]
            address = contract["address"]
            chain = contract["chain"]
            comp_price = get_comp_price()


            abi_path = os.path.join(script_dir, f'compound_abi_{chain}.json')

            with open(abi_path) as f:
                try:
                    provider_abi = json.load(f)
                except FileNotFoundError:
                    exit(1)

                if chain=="ethereum":
                    # Connect to an Ethereum node
                    infura_url = os.getenv('INFURA_URL')
                else:
                    infura_url=(f"https://{chain}-mainnet.infura.io/v3/{os.getenv('INFURA_KEY')}")


            web3 = Web3(Web3.HTTPProvider(infura_url))
            pool_contract = web3.eth.contract(address=address, abi=provider_abi)
            try:
                # getSupplyRate(Utilization) / (10 ^ 18) * Seconds Per Year (3,154e+7) * 100
                utilization = pool_contract.functions.getUtilization().call()
                supply_rate = pool_contract.functions.getSupplyRate(utilization).call()
                apy_base_formatted = supply_rate / 1e18 * 60 * 60 * 24 * 365 * 100


                # Total supply
                tvl = pool_contract.functions.totalSupply().call()
                tvl_transformed = tvl / 1e6

                baseTrackingSupplySpeed = float(pool_contract.functions.baseTrackingBorrowSpeed().call())
                trackingIndexScale = float(pool_contract.functions.trackingIndexScale().call())

                reward_apy = (baseTrackingSupplySpeed/trackingIndexScale) * 60*60*24*365 * comp_price / tvl * 100


                data = Data(
                    market=market,
                    project="Compound v3",
                    information="",
                    yield_rate_base=float(apy_base_formatted),
                    yield_rate_reward=float(reward_apy),
                    yield_token_reward="COMP",
                    tvl=tvl_transformed,
                    chain=chain.capitalize(),
                    type='',
                    smart_contract=address,
                    timestamp=datetime.utcnow()
                )

                db.session.add(data)

            except Exception as e:
                print(f"Error fetching data for {market}: {e}")

        db.session.commit()
        print("Compound Data Fetched")


if __name__ == '__main__':
    fetch_store_rates()
