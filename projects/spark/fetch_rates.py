from web3 import Web3
from dotenv import load_dotenv
import os
import sys
import json
import math
from datetime import datetime

# Ensure the root directory is in the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(project_root)

load_dotenv(os.path.join(project_root, '.env'))

from app import app, db

from instances.YieldRate import YieldRate as Data
from instances.TokenData import TokenData as Info

from utils.get_last_price_db import get_latest_price

infura_url = os.getenv('INFURA_URL')
web3 = Web3(Web3.HTTPProvider(infura_url))



def token_data(total_lend_usd, total_borrowed_usd, dsr_tvl):
    tvl_usd = total_lend_usd - total_borrowed_usd + dsr_tvl
    gov_token = "SPARK"
    gov_token_price = 0
    tot_supply=0,
    circ_supply=0,

    info = Info(
        token=gov_token,
        price=gov_token_price,
        price_source="",
        tot_supply=tot_supply,
        circ_supply=circ_supply,
        tvl=tvl_usd,
        revenue=0,
        timestamp=datetime.utcnow()
    )
    db.session.add(info)
    db.session.commit()

def fetch_store_sparklend():
    print("Starting Fetching Data for SparkLend")
    abi_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'spark_abi.json')
    with open(abi_path) as f:
        try:
            provider_abi = json.load(f)
        except FileNotFoundError:
            print("ABI file not found. Please make sure 'dsr_abi.json' is in the current directory.")
            exit(1)
    total_lend_usd = 0
    total_borrowed_usd = 0

    pool_contract = "0xFc21d6d146E6086B8359705C8b28512a983db0cb"
    web3 = Web3(Web3.HTTPProvider(infura_url))
    pool_contract = web3.eth.contract(address=pool_contract, abi=provider_abi)

    data = pool_contract.functions.getAllReservesTokens().call()
    for item in data:
        try:
            token = item[0]
            contract = item[1]

            price = get_latest_price(token) or 0

            reserve_data = pool_contract.functions.getReserveData(contract).call()

            apy_base = reserve_data[5] / 1e27 * 100  # Convert from Ray to percentage
            apy_base_formatted = round(apy_base, 2)

            lend_amount_raw = reserve_data[2]
            borrowed_amount_raw = reserve_data[3]+reserve_data[4]

            if token in ['USDC', 'pyUSD', 'USDT']:
                lend_amount = lend_amount_raw / 1e6
                borrowed_amount = borrowed_amount_raw /1e6
            elif token == "WBTC":
                lend_amount = lend_amount_raw / 1e8
                borrowed_amount = borrowed_amount_raw/1e8
            else:
                lend_amount = lend_amount_raw / 1e18
                borrowed_amount = borrowed_amount_raw / 1e18

            supply_amount_usd = lend_amount * price
            borrowed_amount_usd = borrowed_amount * price

            total_lend_usd += supply_amount_usd
            total_borrowed_usd += borrowed_amount_usd

            type = "Lending market"

            data = Data(
                    market=token,
                    project="Spark Lend",
                    information=None,
                    yield_rate_base=float(apy_base_formatted),
                    yield_rate_reward=None,
                    yield_token_reward=None,
                    tvl=supply_amount_usd,
                    chain="Ethereum",
                    type=type,
                    smart_contract=contract,
                    timestamp=datetime.utcnow()
                )

            db.session.add(data)

        except Exception as e:
            print(f"Error fetching data for {token}: {e}")

    db.session.commit()
    print("SparkLend data fetched and committed")

    return total_lend_usd, total_borrowed_usd


def fetch_store_DSR():
    pool_contract_address = "0x197E90f9FAD81970bA7976f33CbD77088E5D7cf7" #DSR contract
    token = "DAI"
    abi_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dsr_abi.json')
    with open(abi_path) as f:
        try:
            provider_abi = json.load(f)
        except FileNotFoundError:
            print("ABI file not found. Please make sure 'dsr_abi.json' is in the current directory.")
            exit(1)
    pool_contract = web3.eth.contract(address=pool_contract_address, abi=provider_abi)
    dsr_tvl = 0

    try:
        with app.app_context():

         # Fetch DAI savings rate per second
            dai_saving_rate_second = pool_contract.functions.dsr().call()

            # Convert from Ray (scaled by 1e27) to a percentage
            dai_saving_rate_second_transformed = dai_saving_rate_second / 1e27

            # Calculate APR using continuous compounding formula
            apr_continuous = math.exp(math.log(dai_saving_rate_second_transformed) * 31536000) - 1

            # Convert to percentage
            apy = apr_continuous * 100 #DSR rate

            tvl = pool_contract.functions.Pie().call()
            tvl_transformed = tvl / 1e18
            dsr_tvl += tvl_transformed

            data = Data(
                    market=token,
                    project="Maker DAO (DSR)",
                    information=None,
                    yield_rate_base=float(apy),
                    yield_rate_reward=None,
                    yield_token_reward=None,
                    tvl=tvl_transformed,
                    chain="Ethereum",
                    type="Saving Rate",
                    smart_contract=pool_contract_address,
                    timestamp=datetime.utcnow()
                )

            db.session.add(data)
            db.session.commit()


    except Exception as e:
        print(f"Error fetching {token} Saving Rate: {e}", 500)

    return dsr_tvl

def get_all_data():
    with app.app_context():
        total_lend_usd, total_borrowed_usd = fetch_store_sparklend()
        dsr_tvl = fetch_store_DSR()
        token_data(total_lend_usd, total_borrowed_usd, dsr_tvl)


# return "Fetched"
if __name__ == '__main__':
    get_all_data()
