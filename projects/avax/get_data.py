import requests, sys, os
from datetime import datetime

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

from app import app, db

from utils.get_price import get_price
from instances.TokenData import TokenData as Data

token = "AVAX"
total_supply = 444780390

def get_data():
    r = requests.get("https://avascan.info/api/v1/supply?q=circulatingSupply")
    data = r.json()
    circ_supply = data
    price = get_price(token,"","")

    data = Data (
            token="USDe",
            price=price,
            price_source= "",
            tot_supply= total_supply,
            circ_supply= circ_supply ,
            timestamp=datetime.utcnow(),
        )

    db.session.add(data)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        get_data()
