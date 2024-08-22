
import sys, os
from dotenv import load_dotenv
from datetime import datetime
import requests

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

from app import app, db

from utils.get_supply_solana import get_sol_supply
from instances.TokenData import TokenData as Data

token_info = [
    {
        "token":"JTO",
        "circ_supply": "https://metadata.jito.network/token/jto/supply/circulating",
        "tot_supply": 1000000000,
        "contract": "jtojtomepa8beP8AuQc6eXt5FriJwfFMwQx2v2f9mCL",
        "decimals": 9
    },
    {
        "token":"JitoSOL",
        "contract":"J1toso1uCk3RLmjorhTtrVwY9HJ7X8V9yYac6Y7kGCPn",
        "decimals": 9

    }
]


def get_price_sol(token):
    endpoint = "https://price.jup.ag/v6/price?ids=" + token
    data = requests.get(endpoint).json()
    return data.get("data", {}).get(token, {}).get("price")

def get_supply():
    for item in token_info:
        try:
            tot_supply = get_sol_supply(item["contract"])

            # Fetch circulating supply if the URL is provided, otherwise use total supply
            if "circ_supply" in item and item["circ_supply"]:
                circ_supply = requests.get(item["circ_supply"]).json()
            else:
                circ_supply = tot_supply

            price = get_price_sol(item["token"])

            data = Data (
                token=item["token"],
                price=price,
                price_source= "",
                tot_supply= tot_supply,
                circ_supply= circ_supply ,
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
        get_supply()
