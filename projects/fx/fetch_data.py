import requests
from datetime import datetime

import os
import sys

# Ensure the root directory is in the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

from app import app,db
from instances.YieldRate import YieldRate as Data
from scripts.utils import insert_yield_db

def get_text_after_underscore(input_string):
    if "_" in input_string:
        return input_string.split("_")[1:]
    else:
        return []

api_stability ="https://api.aladdin.club/api1/fx_rebalance_tvl_apy"
api_lp = "https://api.aladdin.club/api1/fx_gauge_tvl_apy"
project = "FX Protocol"
chain = "Ethereum"

def fetch_store_data():
    print("Starting to Fetch Data for FX")
    with app.app_context():
        try:
            r = requests.get(api_stability)
            data = r.json()
            dataset = data.get("data",{})

            for key, market in dataset.items():
                name = market.get("name", {})
                base_apy = 0
                reward_apy = market.get("apy", {})
                tvl = market.get("tvl", {})
                contract_address = market.get("rebalancePoolAddress",{})
                underlying = market.get("poolType",{})
                reward = get_text_after_underscore(name)[1]
                information = f"Deposit in Stability Pool for {underlying} ({reward} & FXN reward)"
                print(f"{underlying} - {reward_apy} - {information} - {tvl}")
                type = "Stability Pool"

                insert_yield_db(underlying,project,information,0,reward_apy,reward,tvl,chain,type,contract_address)


        except Exception as e:
            print(f"Error fetching {name}: {e}", 500)

        print("FX Fetched")

        db.session.commit()


if __name__ == '__main__':
    with app.app_context():
        fetch_store_data()




# r = requests.get(api_lp)
# data = r.json()
# dataset = data.get("data",{})
# for market in dataset:
#     name = market.get("name",{})
#     reward_apy = market.get("apy",{})
#     tvl = market.get("tvl",{})
#     contract_address = market.get("gauge",{})
#     information = f"Liquidity Provision for {name} (FXN reward)"


#     print(f"{name} - {reward_apy} - {information} - {tvl}")
