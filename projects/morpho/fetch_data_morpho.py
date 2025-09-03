import requests
from datetime import datetime
import sys, os
import logging

# Ensure the root directory is in the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(project_root)

from app import app, db
from instances.YieldRate import YieldRate as Data

# Define the endpoint and headers
url = 'https://blue-api.morpho.org/graphql'
headers = {
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Origin': 'https://blue-api.morpho.org'
}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def fetch_data_metamorpho():
    query = """
    query {
      vaults(first: 1000) {
        items {
          address
          symbol
          name
          creationBlockNumber
          creationTimestamp
          creatorAddress
          whitelisted
          asset {
            id
            address
            decimals
          }
          chain {
            id
            network
          }
          state {
            id
            apy
            netApy
            totalAssets
            totalAssetsUsd
            fee
            rewards {
                yearlySupplyTokens
                supplyApr
                amountPerSuppliedToken
                asset {
                        symbol
                        yield
                            {
                                apr
                            }
                        }
                    }
            timelock
            allocation {
              market {
                uniqueKey
                loanAsset {
                  name
                  symbol
                }
                collateralAsset {
                  name
                  symbol
                }
                oracleAddress
                irmAddress
                lltv
              }
              supplyCap
              supplyAssets
              supplyAssetsUsd
            }
          }
        }
      }
    }
    """

    response = requests.post(url, headers=headers, json={'query': query})

    if response.status_code == 200:
        data = response.json().get("data", {}).get("vaults", {}).get("items", [])
        logger.info(f"Fetched {len(data)} vaults from Morpho API")

        with app.app_context():
            processed_count = 0
            skipped_count = 0

            for market in data:
                try:
                    # More flexible conditions - process vaults with valid APY even if TVL is 0
                    if market and market.get("state") and market["state"].get("apy") is not None:
                        state = market["state"]
                        supply_apy = state.get("apy", 0)
                        supply_amount = state.get("totalAssetsUsd", 0)
                        chain = market.get("chain", {}).get("network", "Unknown")
                        contract = market.get("address", "Unknown")
                        vault_symbol = market.get("symbol", "Unknown")
                        vault_name = market.get("name", "Unknown Vault")

                        # Try to get supply token from allocation, fallback to vault symbol
                        supply_token = vault_symbol
                        if state.get("allocation") and len(state["allocation"]) > 0:
                            allocation = state["allocation"][0]
                            if allocation.get("market") and allocation["market"].get("loanAsset"):
                                supply_token = allocation["market"]["loanAsset"]["symbol"]

                        type = "Lending"

                        # Process collaterals
                        collaterals = []
                        if state.get("allocation"):
                            for item in state["allocation"]:
                                if item.get("market") and item["market"].get("collateralAsset"):
                                    collateral_asset = item["market"]["collateralAsset"]
                                    if collateral_asset:
                                        collateral = collateral_asset.get("symbol")
                                        if collateral:
                                            collaterals.append(collateral)

                        if collaterals:
                            formatted_collaterals = f"Collaterals for pool: {', '.join(collaterals)}"
                        else:
                            formatted_collaterals = f"Vault: {vault_name}"

                        # Process rewards
                        reward_rate = 0
                        reward_asset = ""
                        if state.get("rewards") and len(state["rewards"]) > 0:
                            reward = state["rewards"][0]
                            reward_rate = reward.get("supplyApr", 0)
                            if reward.get("asset"):
                                reward_asset = reward["asset"].get("symbol", "")

                        # Only skip if both APY and TVL are 0 (truly inactive vaults)
                        if supply_apy == 0 and supply_amount == 0:
                            skipped_count += 1
                            continue

                        data_record = Data(
                            market=supply_token,
                            project="Morpho",
                            information=formatted_collaterals,
                            yield_rate_base=supply_apy * 100,
                            yield_rate_reward=reward_rate * 100,
                            yield_token_reward=reward_asset if reward_asset else None,
                            tvl=supply_amount,
                            chain=chain.capitalize(),
                            type=type,
                            smart_contract=contract,
                            timestamp=datetime.utcnow()
                        )

                        db.session.add(data_record)
                        processed_count += 1

                except Exception as e:
                    logger.error(f"Error processing vault data: {e}")
                    skipped_count += 1

            # Commit all changes at once for better performance
            try:
                db.session.commit()
                logger.info(f"Morpho data processing complete: {processed_count} processed, {skipped_count} skipped")
            except Exception as e:
                db.session.rollback()
                logger.error(f"Error committing Morpho data: {e}")

    else:
        logger.error(f"Morpho API query failed with status code: {response.status_code}")
        logger.error(f"Response: {response.text}")


if __name__ == '__main__':
    fetch_data_metamorpho()
