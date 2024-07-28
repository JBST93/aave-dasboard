import os
import json
import sys
from datetime import datetime
import requests

# Ensure the root directory is in the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

from app import db
from instances.YieldRate import YieldRate as Data


def load_abi(project, abi_filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    abi_path = os.path.join(script_dir, '..', "projects", project ,abi_filename)  # Adjust this line
    print(abi_path)
    with open(abi_path) as f:
        try:
            return json.load(f)
        except FileNotFoundError:
            print(f"{abi_filename} file not found at {abi_path}")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {abi_path}")
            sys.exit(1)


def insert_yield_db(market, project, information, yield_rate_base, yield_rate_reward, yield_token_reward, tvl, chain, type, smart_contract):
    try:
        data = Data(
            market=market,
            project=project,
            information=information,
            yield_rate_base=float(yield_rate_base),
            yield_rate_reward=float(yield_rate_reward) if yield_rate_reward else None,
            yield_token_reward=yield_token_reward,
            tvl=tvl,
            chain=chain.capitalize(),
            type=type,
            smart_contract=smart_contract,
            timestamp=datetime.utcnow()
        )

        db.session.add(data)

    except Exception as e:
        db.session.rollback()
        print(f"Error inserting data into DB: {e}")

def get_curve_price(contract_address, chain):
    curve_api = f"https://prices.curve.fi/v1/usd_price/{chain}"
    r = requests.get(curve_api)
    data = r.json()
    data = data["data"] ## Gives a lits
    ## iterate through the list to match the contract address
    for pool in data:
        if pool.get("address").lower() == contract_address.lower():  # Ensure case-insensitive comparison
            return round(float(pool.get("usd_price")),2)
