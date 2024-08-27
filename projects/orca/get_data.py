
import sys, os
from dotenv import load_dotenv
from datetime import datetime
import requests

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

from app import app, db

from utils.get_supply_solana import get_sol_supply
from utils.get_last_price_db import get_latest_price
from utils.get_price import get_price

from instances.TokenData import TokenData as Info

token_info = [
    {
        "token":"ORCA",
        "circ_supply": "https://api.mainnet.orca.so/v1/stats/totalorca",
        "tot_supply": 100000000,
        "contract": "orcaEKTdK7LKz57vaAYr9QeNsVEPfiu6QeMU1kektZE",
        "decimals": 6
    }
]

def get_info():
    for item in token_info:
        try:
            price = get_price(item["token"])
            tot_supply = item["tot_supply"]

            # Fetch circulating supply if the URL is provided, otherwise use total supply
            if "circ_supply" in item and item["circ_supply"]:
                circ_supply = requests.get(item["circ_supply"]).json()
            else:
                circ_supply = tot_supply

            data = Info (
                token=item["token"],
                price=price,
                price_source= "",
                tot_supply= tot_supply,
                circ_supply= circ_supply,
                tvl = 0,
                timestamp=datetime.utcnow(),
            )

            db.session.add(data)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {item['token']}: {e}")
        except KeyError as e:
            print(f"Error parsing data for {item['token']}: {e}")

    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        get_info()
