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
      vaults {
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
    print("Started to fetch Metamorpho")

    if response.status_code == 200:
        data = response.json().get("data", {}).get("vaults", {}).get("items", [])
        with app.app_context():
            for market in data:
                try:
                    if market and market["state"] and market["state"].get("totalAssetsUsd"):
                        if market["state"].get("allocation") and market["state"]["allocation"][0].get("market"):
                            supply_token = market["state"]["allocation"][0]["market"]["loanAsset"]["symbol"]
                        else:
                            continue
                        supply_apy = market["state"].get("apy", 0)
                        chain = market["chain"]["network"]
                        supply_amount = market["state"].get("totalAssetsUsd", 0)
                        contract= market["address"]
                        type="Lending"

                        collaterals = []
                        collateral_data = market.get("state",{}).get("allocation",{})
                        for item in collateral_data:
                            collateral_asset = item.get("market",{}).get("collateralAsset",{})
                            if collateral_asset:
                                collateral = collateral_asset.get("symbol")
                                collaterals.append(collateral)

                        if market["state"].get("rewards"):
                            reward_rate = market["state"].get("rewards")[0].get("supplyApr")
                            reward_asset = market["state"].get("rewards")[0].get("asset").get("symbol")
                        else:
                            reward_rate = 0
                            reward_asset = ""

                        data = Data(
                            market=supply_token,
                            project="Morpho",
                            information=collaterals,
                            yield_rate_base=supply_apy * 100,
                            yield_rate_reward=reward_rate * 100,
                            yield_token_reward=None,
                            tvl=supply_amount,
                            chain=chain.capitalize(),
                            type=type,
                            smart_contract=contract,
                            timestamp=datetime.utcnow()
                        )

                        db.session.add(data)

                        db.session.commit()

                except Exception as e:
                    logger.error(f"Error processing vault data: {e}")

            print("MetaMorpho comitted")


    else:
        logger.error(f"Query failed to run with a {response.status_code}.")


if __name__ == '__main__':
    fetch_data_metamorpho()
