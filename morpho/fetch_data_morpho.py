import requests
import json

def fetch_data():
    # Define the GraphQL query
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

    # List of stablecoin symbols
    stablecoins = {"USDT", "USDC", "DAI", "BUSD", "TUSD", "PAX", "GUSD"}

    # Send the request
    response = requests.post(url, headers=headers, json={'query': query})

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response JSON
        data = response.json().get("data", {}).get("markets", {}).get("items", [])

        # Filter out items with zero or None TVL and non-stablecoins
        filtered_data = [
            market for market in data
            if market.get("state", {}).get("supplyAssetsUsd") not in (0, None) and
            (
                (market.get("loanAsset") and market["loanAsset"].get("symbol") in stablecoins) or
                (market.get("collateralAsset") and market["collateralAsset"].get("symbol") in stablecoins)
            )
        ]

        # Process the filtered data
        for market in filtered_data:
            try:
                loan_asset = market.get("loanAsset")
                if loan_asset:
                    token = loan_asset.get("symbol", "N/A")
                else:
                    token = "N/A"

                collateral_asset = market.get("collateralAsset")
                if collateral_asset:
                    collateral = collateral_asset.get("symbol", "N/A")
                else:
                    collateral = "N/A"

                state = market.get("state")
                if state:
                    supply_apy = state.get("supplyApy", "N/A")
                    tvl = state.get("supplyAssetsUsd", "N/A")
                else:
                    supply_apy = "N/A"
                    tvl = "N/A"

                print(f"Token: {token}, Collateral: {collateral}, Supply APY: {supply_apy}, TVL: {tvl}")

            except Exception as e:
                print(f"Error processing market: {market}, error: {e}")

    else:
        print(f"Query failed to run with a {response.status_code}.")

# Call the function
fetch_data()
