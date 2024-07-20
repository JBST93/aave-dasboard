import requests
from datetime import datetime
import sys, os
import logging

# Ensure the root directory is in the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from app import app, db
from instances.MoneyMarketRate import MoneyMarketRate

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

def fetch_data_morpho():
    query = """
    query {
      markets {
        items {
          uniqueKey
          lltv
          oracleAddress
          irmAddress
          loanAsset {
            address
            symbol
            decimals
          }
          collateralAsset {
            address
            symbol
            decimals
          }
          state {
            borrowApy
            borrowAssets
            borrowAssetsUsd
            supplyApy
            supplyAssets
            supplyAssetsUsd
            fee
            utilization
          }
          morphoBlue {
            chain {
              id
              network
              currency
            }
          }
        }
      }
    }
    """

    # Send the request
    response = requests.post(url, headers=headers, json={'query': query})

    if response.status_code == 200:
        data = response.json().get("data", {}).get("markets", {}).get("items", [])
        with app.app_context():
            for market in data:
                try:
                    if market and market["state"] and market["state"].get("supplyAssetsUsd"):
                        protocol = "Morpho Blue"
                        supply_token = market["loanAsset"]["symbol"]
                        collateral_token = market["collateralAsset"]["symbol"] if market.get("collateralAsset") else ""
                        supply_apy = market["state"].get('supplyApy', 0)
                        borrow_apy = market["state"].get('borrowApy', 0)
                        supply_amount = market["state"].get("supplyAssetsUsd", 0)
                        chain = market["morphoBlue"]["chain"]["network"]

                        rate = MoneyMarketRate(
                            token=supply_token,
                            collateral=collateral_token,
                            protocol="Morpho Blue",
                            liquidity_rate=supply_apy * 100,
                            liquidity_reward_rate=None,
                            chain=chain.capitalize(),
                            borrow_rate=borrow_apy,
                            tvl=supply_amount,
                            timestamp=datetime.utcnow(),
                        )

                        db.session.add(rate)
                        db.session.commit()

                except Exception as e:
                    logger.error(f"Error processing market data: {e}")
            print("Morpho Blue comitted")
    else:
        logger.error(f"Query failed to run with a {response.status_code}.")

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

    if response.status_code == 200:
        data = response.json().get("data", {}).get("vaults", {}).get("items", [])
        with app.app_context():
            for market in data:
                try:
                    if market and market["state"] and market["state"].get("totalAssetsUsd"):
                        protocol = "MetaMorpho"
                        if market["state"].get("allocation") and market["state"]["allocation"][0].get("market"):
                            supply_token = market["state"]["allocation"][0]["market"]["loanAsset"]["symbol"]
                        else:
                            continue
                        supply_apy = market["state"].get("apy", 0)
                        chain = market["chain"]["network"]
                        supply_amount = market["state"].get("totalAssetsUsd", 0)

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


                        rate = MoneyMarketRate(
                        token=supply_token,
                        collateral=collaterals,
                        protocol=protocol,
                        liquidity_rate=supply_apy * 100,
                        liquidity_reward_rate=reward_rate * 100,
                        liquidity_reward_token=reward_asset,
                        chain=chain.capitalize(),
                        borrow_rate=0,
                        tvl=supply_amount,
                        timestamp=datetime.utcnow(),
                        )

                        db.session.add(rate)
                        db.session.commit()


                except Exception as e:
                    logger.error(f"Error processing vault data: {e}")

            print("MetaMorpho comitted")


    else:
        logger.error(f"Query failed to run with a {response.status_code}.")

def fetch_data():
    fetch_data_morpho()
    fetch_data_metamorpho()

if __name__ == '__main__':
    fetch_data()
