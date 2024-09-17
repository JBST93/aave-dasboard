import sys, os, requests
from datetime import datetime

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

from app import app, db

from utils.get_price import get_price

from instances.TokenData import TokenData as Data

api = "https://stacks-node-api.mainnet.stacks.co/extended/v1/stx_supply"

def get_store_data():
    with app.app_context():
        try:
            r = requests.get(api)
            data = r.json()
            tot_supply = data.get("total_stx")
            circ_supply = data.get("unlocked_stx")
            price = get_price("STX")

            data = Data (
                token="STX",
                price=price,
                price_source= "",
                tot_supply= tot_supply,
                circ_supply= circ_supply,
                tvl=0,
                timestamp=datetime.utcnow(),
            )

            db.session.add(data)
            db.session.commit()

        except Exception as e:
            print(f"Error processing token STX: {e}")


if __name__ == '__main__':
        get_store_data()
