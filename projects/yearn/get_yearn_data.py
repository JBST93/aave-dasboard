import requests
from datetime import datetime
import sys, os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure the app's directory is in the system path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(project_root)

# Import Flask app and db from your application
from app import app, db
from instances.YieldRate import YieldRate as Data

# Define the chain_id dictionary
chain_id = {
    "Ethereum": 1,
    "Base": 8453,
    "BSC": 56,
    "Optimism": 10,
    "Arbitrum": 42161,
    "Polygon": 137,
    "Avalanche": 43114
}

def fetch_yearn():
    for chain_name, chain_number in chain_id.items():
        api_url = f"https://api.yexporter.io/v1/chains/{chain_number}/vaults/all"

        try:
            r = requests.get(api_url)
            r.raise_for_status()  # Raise HTTPError for bad responses
            data = r.json()

            with app.app_context():
                try:
                    for vault in data:
                        name = vault["name"]
                        tvl = vault["tvl"]["tvl"]
                        apy = vault["apy"]["net_apy"] * 100
                        token_deposit = vault["token"]["symbol"]
                        contract_address = vault["address"]
                        chain = chain_name
                        type = "Active Management"

                        if len(token_deposit) < 6 and tvl and tvl > 0:
                            rate = Data(
                                market=token_deposit,
                                project="Yearn",
                                information="",
                                yield_rate_base=apy,
                                yield_rate_reward=None,
                                yield_token_reward=None,
                                tvl=tvl,
                                chain=chain.capitalize(),
                                type=type,
                                smart_contract=contract_address,
                                timestamp=datetime.utcnow()
                            )

                            db.session.add(rate)
                            db.session.commit()

                except Exception as e:
                    logger.error(f"Error processing market data for {chain_name}: {e}")

        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed for {chain_name}: {e}")
        except ValueError as e:
            logger.error(f"Error parsing JSON response for {chain_name}: {e}")

if __name__ == '__main__':
    fetch_yearn()
