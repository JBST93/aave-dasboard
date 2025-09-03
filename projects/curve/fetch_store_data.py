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
from instances.TokenData import TokenData as TokenData

from utils.get_price import get_price



def get_crvusd():
    crvUSD_contract="0xf939E0A03FB07F59A73314E73794Be0E57ac1b4E"
    chain = "ethereum"
    token ="crvUSD"

    crvUSD_endpoint = "https://api.curve.fi/v1/getCrvusdTotalSupply"
    r = requests.get(crvUSD_endpoint)
    data = r.json()

    supply = data.get("data",{}).get("crvusdTotalSupply")
    price = get_price(token, crvUSD_contract, chain)
    supply_transformed = supply

    data = TokenData (
        token= token,
        price=price,
        price_source= "",
        tot_supply= supply_transformed,
        circ_supply= supply_transformed ,
        timestamp=datetime.utcnow(),
    )

    db.session.add(data)
    db.session.commit()


def fetch_store_data():
    chains = {"arbitrum", "ethereum", "optimism", "fraxtal"}  # Removed base due to API issues
    processed_count = 0
    skipped_count = 0
    error_count = 0

    for chain in chains:
        api_url = f"https://api.curve.fi/v1/getLendingVaults/{chain}/"
        reward_api = "https://api.curve.fi/v1/getAllGauges"

        try:
            logging.info(f"Fetching Curve lending vaults for {chain}")
            r = requests.get(api_url, timeout=30)
            r.raise_for_status()

            response_data = r.json()
            if "data" not in response_data or "lendingVaultData" not in response_data["data"]:
                logging.warning(f"No lending vault data for {chain}")
                continue

            data = response_data["data"]["lendingVaultData"]
            logging.info(f"Found {len(data)} lending vaults for {chain}")

            # Get reward data once
            reward_response = requests.get(reward_api, timeout=30)
            reward_data = reward_response.json().get("data", {}) if reward_response.status_code == 200 else {}

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
                        information = f"Collateral: {collateral}"
                        action = f"Lend in the {collateral} pool"

                        # Handle gauge rewards - look in the dataset first
                        liquidity_reward_rate = 0
                        liquidity_reward_token = None

                        if "gaugeRewards" in dataset and dataset["gaugeRewards"]:
                            gauge_rewards = dataset["gaugeRewards"]
                            if isinstance(gauge_rewards, list) and len(gauge_rewards) > 0:
                                liquidity_reward_rate = gauge_rewards[0].get("apy", 0)
                                liquidity_reward_token = gauge_rewards[0].get("symbol", "CRV")
                        elif "gaugeAddress" in dataset and dataset["gaugeAddress"]:
                            # Try to find reward data from the global reward API
                            gauge_address = dataset["gaugeAddress"]
                            for reward_key, reward_info in reward_data.items():
                                if isinstance(reward_info, dict) and reward_info.get("gauge") == gauge_address:
                                    if "gaugeRewards" in reward_info and reward_info["gaugeRewards"]:
                                        gauge_rewards = reward_info["gaugeRewards"]
                                        if isinstance(gauge_rewards, list) and len(gauge_rewards) > 0:
                                            liquidity_reward_rate = gauge_rewards[0].get("apy", 0)
                                            liquidity_reward_token = gauge_rewards[0].get("symbol", "CRV")
                                    break

                        # Only process if we have valid data
                        if tvl and tvl > 0:
                            data_record = Data(
                                market=token,
                                project="Curve",
                                information=information,
                                yield_rate_base=float(lend_apy),
                                yield_rate_reward=liquidity_reward_rate,
                                yield_token_reward=liquidity_reward_token,
                                tvl=tvl,
                                chain=chain.capitalize(),
                                type=type,
                                action=action,
                                smart_contract=contract,
                                timestamp=datetime.utcnow()
                            )

                            db.session.add(data_record)
                            processed_count += 1
                        else:
                            skipped_count += 1

                    except KeyError as e:
                        logging.error(f"KeyError: {e} in dataset for {chain}")
                        error_count += 1
                    except Exception as e:
                        logging.error(f"Error processing vault for {chain}: {e}")
                        error_count += 1

                db.session.commit()
                logging.info(f"Curve {chain}: {processed_count} processed, {skipped_count} skipped, {error_count} errors")

        except requests.RequestException as e:
            logging.error(f"RequestException for {chain}: {e}")
        except Exception as e:
            logging.error(f"Unexpected error for {chain}: {e}")

    logging.info(f"Curve lending vaults complete: {processed_count} total processed")

if __name__ == '__main__':
    with app.app_context():
        fetch_store_data()
        get_crvusd()
