import requests
from datetime import datetime
import sys, os

# Ensure the root directory is in the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from app import app, db
from instances.MoneyMarketRate import MoneyMarketRate

def fetch_data():
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

    # Send the request
    response = requests.post(url, headers=headers, json={'query': query})

    if response.status_code == 200:
        data = response.json().get("data", {}).get("markets", {}).get("items", [])
        with app.app_context():

            for market in data:
                if market["state"]["supplyAssetsUsd"]:
                    try:
                        protocol = "Morpho Blue"
                        supply_token = market["loanAsset"]["symbol"]
                        collateral_token = market["collateralAsset"]["symbol"] if market["collateralAsset"] else ""
                        supply_apy = market["state"]['supplyApy']
                        borrow_apy = market["state"]['borrowApy']
                        supply_amount = market["state"]["supplyAssetsUsd"]
                        chain = market["morphoBlue"]["chain"]["network"]

                        rate = MoneyMarketRate(
                                token=supply_token,
                                collateral=collateral_token,
                                protocol="Morpho Blue",
                                liquidity_rate=supply_apy*100,
                                liquidity_reward_rate=None,
                                chain=chain.capitalize(),
                                borrow_rate=borrow_apy,
                                tvl=supply_amount,
                                timestamp=datetime.utcnow(),
                            )

                        db.session.add(rate)

                    except KeyError as e:
                        print(f"{e}")

            db.session.commit()

    else:
        print(f"Query failed to run with a {response.status_code}.")

# Call the function
if __name__ == '__main__':
    fetch_data()
