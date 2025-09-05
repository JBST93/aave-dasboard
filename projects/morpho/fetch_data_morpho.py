import requests
import json
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

    try:
        # Make request with explicit decompression handling
        # Try with session to ensure proper connection handling
        session = requests.Session()
        response = session.post(url, headers=headers, json={'query': query}, timeout=30)
        response.raise_for_status()  # Raise exception for bad status codes

        # Check if response has content
        if not response.content:
            logger.error("Morpho API returned empty response")
            return

        # Check content type
        content_type = response.headers.get('content-type', '')
        if 'application/json' not in content_type:
            logger.error(f"Morpho API returned non-JSON content: {content_type}")
            logger.error(f"Response content: {response.text[:500]}")
            return

        # Parse JSON with error handling and explicit decompression
        try:
            # Try to get text content first to ensure proper decompression
            response_text = response.text
            if not response_text.strip():
                logger.error("Morpho API returned empty text content")
                return

            json_data = json.loads(response_text)
        except json.JSONDecodeError as e:
            logger.error(f"Morpho API returned invalid JSON: {e}")
            logger.error(f"Response content type: {content_type}")
            logger.error(f"Response encoding: {response.encoding}")
            logger.error(f"Response content (first 500 chars): {response_text[:500] if 'response_text' in locals() else response.text[:500]}")
            return

        # Check for GraphQL errors
        if "errors" in json_data:
            logger.error(f"Morpho GraphQL errors: {json_data['errors']}")
            return

        # Extract data safely
        data = json_data.get("data", {}).get("vaults", {}).get("items", [])
        logger.info(f"Fetched {len(data)} vaults from Morpho API")

    except requests.RequestException as e:
        logger.error(f"Morpho API request failed: {e}")
        return
    except Exception as e:
        logger.error(f"Unexpected error fetching Morpho data: {e}")
        return

    if data:  # Only process if we have data
        with app.app_context():
            processed_count = 0
            skipped_count = 0

            for market in data:
                try:
                    # More flexible conditions - process vaults with valid APY even if TVL is 0
                    if market and market.get("state") and market["state"].get("apy") is not None:
                        state = market["state"]
                        supply_apy = state.get("apy", 0)
                        
                        # Smart APY conversion: if APY < 1, assume it's a decimal and convert to percentage
                        # If APY >= 1, assume it's already a percentage
                        if supply_apy < 1 and supply_apy > 0:
                            supply_apy = supply_apy * 100
                        
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

                        # Use vault name for better user identification
                        formatted_collaterals = f"Vault Name: {vault_name}"

                        # Ensure the final string doesn't exceed 200 characters
                        if len(formatted_collaterals) > 200:
                            formatted_collaterals = formatted_collaterals[:197] + "..."

                        # Process rewards
                        reward_rate = 0
                        reward_asset = ""
                        if state.get("rewards") and len(state["rewards"]) > 0:
                            reward = state["rewards"][0]
                            reward_rate = reward.get("supplyApr", 0)
                            
                            # Smart reward rate conversion: if rate < 1, assume it's a decimal and convert to percentage
                            if reward_rate < 1 and reward_rate > 0:
                                reward_rate = reward_rate * 100
                                
                            if reward.get("asset"):
                                reward_asset = reward["asset"].get("symbol", "")

                        # Debug APY conversion for specific vaults
                        if "Spark DAI" in vault_name or "Relend USDC" in vault_name:
                            raw_apy = state.get("apy", 0)
                            print(f"🔍 APY CONVERSION: {vault_name}")
                            print(f"    Raw APY: {raw_apy:.6f}")
                            print(f"    Converted APY: {supply_apy:.2f}%")
                            print(f"    TVL: ${supply_amount:,.2f}")
                            print(f"    Contract: {contract}")

                        # Only skip if both APY and TVL are 0 (truly inactive vaults)
                        if supply_apy == 0 and supply_amount == 0:
                            skipped_count += 1
                            continue

                        data_record = Data(
                            market=supply_token,
                            project="Morpho",
                            information=formatted_collaterals,
                            yield_rate_base=supply_apy,
                            yield_rate_reward=reward_rate,
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
        logger.warning("No Morpho data to process")


if __name__ == '__main__':
    fetch_data_metamorpho()
