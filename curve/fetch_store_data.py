import os
import sys
import requests
import json
from datetime import datetime
from app import app,db
from instances.MoneyMarketRate import MoneyMarketRate


# Ensure the root directory is in the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)



def fetch_store_data():
    chains = {"arbitrum","ethereum"}

    for chain in chains:
        api_url="https://api.curve.fi/v1/getLendingVaults/all/"
        r = requests.get(api_url+chain)
        data = r.json()["data"]["lendingVaultData"]
        print(f"Starting to fetch data for Curve Lend - {chain}")
        with app.app_context():
            for pair in data:
                try:
                    dataset = pair
                    lend_apy = dataset["rates"]["lendApyPcent"]
                    borrow_apy = dataset["rates"]["borrowApyPcent"]
                    token = dataset["assets"]["borrowed"]["symbol"]
                    collateral = dataset["assets"]["collateral"]["symbol"]
                    tvl = dataset["totalSupplied"]["usdTotal"]

                    rate = MoneyMarketRate(
                                    token=token,
                                    collateral=collateral,
                                    protocol="Curve Lend",
                                    liquidity_rate=lend_apy,
                                    chain=chain.capitalize(),
                                    borrow_rate=borrow_apy,
                                    tvl=tvl,
                                    timestamp=datetime.utcnow()
                                )


                    db.session.add(rate)

                except Exception as e:
                    print(f"Error fetching: {e}", 500)
            db.session.commit()
        print("Data for Curve Fetched")


if __name__ == '__main__':
    fetch_store_data()
