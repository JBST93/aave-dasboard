import os
import sys
import requests
import json
from datetime import datetime

# Ensure the root directory is in the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

# Import the db and MoneyMarketRate from db_config
from db_config import app, db, MoneyMarketRate



def fetch_store_data():
    r = requests.get('https://api.curve.fi/v1/getLendingVaults/all/ethereum')
    data = r.json()["data"]["lendingVaultData"]


    with app.app_context():
        for pair in data:
            try:
                dataset = pair
                lend_apy = dataset["rates"]["lendApyPcent"]
                borrow_apy = dataset["rates"]["borrowApyPcent"]
                token = dataset["assets"]["borrowed"]["symbol"]
                collateral = dataset["assets"]["collateral"]["symbol"]
                tvl = dataset["totalSupplied"]["usdTotal"]

                print("got data")

                rate = MoneyMarketRate(
                                token=token + "(" + collateral +" as collateral)",
                                protocol="Curve Lend",
                                liquidity_rate=lend_apy,
                                borrow_rate=borrow_apy,
                                tvl=tvl,
                                timestamp=datetime.utcnow()
                            )
                db.session.add(rate)
                print(rate.liquidity_rate)

            except Exception as e:
                print(f"Error fetching: {e}", 500)

        db.session.commit()


fetch_store_data()
