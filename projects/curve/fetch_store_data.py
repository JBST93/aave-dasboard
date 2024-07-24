import os
import sys
import requests
import json
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Ensure the root directory is in the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(project_root)

from app import app, db
from instances.YieldRate import YieldRate as Data

def fetch_store_data():
    chains = {"arbitrum", "ethereum"}

    for chain in chains:
        api_url = f"https://api.curve.fi/v1/getLendingVaults/{chain}/"
        logging.info(f"Fetching data from {api_url}")

        try:
            r = requests.get(api_url)
            r.raise_for_status()

            data = r.json()["data"]["lendingVaultData"]
            logging.info(f"Starting to fetch data for Curve Lend - {chain}")

            with app.app_context():
                for pair in data:
                    try:
                        dataset = pair
                        lend_apy = dataset["rates"]["lendApyPcent"]
                        borrow_apy = dataset["rates"]["borrowApyPcent"]
                        token = dataset["assets"]["borrowed"]["symbol"]
                        collateral = dataset["assets"]["collateral"]["symbol"]
                        tvl = dataset["totalSupplied"]["usdTotal"]
                        type = "Lending"
                        contract = dataset["address"]

                        # Handle missing 'gaugeRewards'
                        if "gaugeRewards" in dataset and dataset["gaugeRewards"]:
                            liquidity_reward_rate = dataset["gaugeRewards"][0]["apy"]
                            liquidity_reward_token = dataset["gaugeRewards"][0]["symbol"]
                        else:
                            liquidity_reward_rate = None
                            liquidity_reward_token = None

                        data = Data(
                            market=token,
                            project="Curve",
                            information=collateral,
                            yield_rate_base=float(lend_apy),
                            yield_rate_reward=liquidity_reward_rate,
                            yield_token_reward=liquidity_reward_token,
                            tvl=tvl,
                            chain=chain.capitalize(),
                            type=type,
                            smart_contract=contract,
                            timestamp=datetime.utcnow()
                        )

                        db.session.add(data)

                    except KeyError as e:
                        logging.error(f"KeyError: {e} in dataset {dataset}")
                    except Exception as e:
                        logging.error(f"Error fetching data for pair: {e}")

                db.session.commit()

            logging.info(f"Data for Curve {chain} fetched and stored successfully.")

        except requests.RequestException as e:
            logging.error(f"RequestException: {e}")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")

if __name__ == '__main__':
    fetch_store_data()
