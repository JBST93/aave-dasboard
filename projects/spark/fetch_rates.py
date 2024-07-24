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

infura_url = os.getenv('INFURA_URL')
web3 = Web3(Web3.HTTPProvider(infura_url))

abi_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'spark_abi.json')
with open(abi_path) as f:
    try:
        provider_abi = json.load(f)
    except FileNotFoundError:
        print("ABI file not found. Please make sure 'dsr_abi.json' is in the current directory.")
        exit(1)

def fetch_store_sparklend():
    print("Starting Fetching Data for SparkLend")
    pool_contract = "0xFc21d6d146E6086B8359705C8b28512a983db0cb"
    web3 = Web3(Web3.HTTPProvider(infura_url))
    pool_contract = web3.eth.contract(address=pool_contract, abi=provider_abi)

    data = pool_contract.functions.getAllReservesTokens().call()
    for item in data:
        try:
            token = item[0]
            contract = item[1]
            reserve_data = pool_contract.functions.getReserveData(contract).call()

            apy_base = reserve_data[5] / 1e27 * 100  # Convert from Ray to percentage
            apy_base_formatted = round(apy_base, 2)

            raw_tvl = pool_contract.functions.getATokenTotalSupply(contract).call()

            chain = "ethereum"

            if token in ['USDC', 'pyUSD', 'USDT']:  # TVL in LCY - need to find USD
                tvl = raw_tvl / 1e6  # These tokens have 6 decimal places
            else:
                tvl = raw_tvl / 1e18  # Default to 18 decimal places for other tokens

                        # Need to find TVL_USD
            tvl_usd = tvl
            information = ""
            type = "Lending market"

            print(f"Inserting data: {token}, {apy_base_formatted}, {tvl_usd}, {chain}, {contract}")

            data = Data(
                    market=token,
                    project="Spark Lend",
                    information=information,
                    yield_rate_base=float(apy_base_formatted),
                    yield_rate_reward=None,
                    yield_token_reward=None,
                    tvl=tvl_usd,
                    chain=chain.capitalize(),
                    type=type,
                    smart_contract=contract,
                    timestamp=datetime.utcnow()
                )

            db.session.add(data)

        except Exception as e:
                print(f"Error fetching data for {token}: {e}")
        db.session.commit()





pool_contract_address = "0x197E90f9FAD81970bA7976f33CbD77088E5D7cf7" #DSR contract
token = "DAI"



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

            tvl = pool_contract.functions.Pie().call()
            tvl_transformed = tvl / 1e18

            rate = MoneyMarketRate(
                token=token,
                protocol="Maker (DSR)",
                liquidity_rate=APY,
                tvl=tvl_transformed,
                timestamp=datetime.utcnow(),
                chain="Ethereum",
                borrow_rate=0
            )
            db.session.add(rate)
            db.session.commit()

    except Exception as e:
        print(f"Error fetching {token} Saving Rate: {e}", 500)

# return "Fetched"
if __name__ == '__main__':
    with app.app_context():

        fetch_store_sparklend()
