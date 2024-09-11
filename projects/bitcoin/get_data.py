import requests, sys, os
from datetime import datetime

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

from app import app, db

from utils.get_price import get_price
from instances.TokenData import TokenData as Data
token = "BTC"
total_supply = 21000000

def get_data():
    r = requests.get("https://blockchain.info/q/totalbc")
    data = r.json()
    circ_supply = float(data) / 10**9
    price = get_price(token,"","")

    data = Data (
            token=token,
            price=price,
            price_source= "",
            tot_supply= float(total_supply),
            circ_supply= float(circ_supply),
            timestamp=datetime.utcnow(),
        )

    db.session.add(data)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        get_data()
