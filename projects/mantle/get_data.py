import requests
import requests, sys, os
from datetime import datetime

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

from app import app, db

from utils.get_price import get_price
from instances.TokenData import TokenData as Data

token = "MNT"

def get_data():
    r = requests.get("https://api.mantle.xyz/api/v1/token-data")
    data = r.json().get("results")
    circ_supply = data.get("circulatingSupply")
    total_supply = data.get("totalSupply")
    price = get_price(token,"0x3c3a81e81dc49a522a592e7622a7e711c06bf354","Ethereum")

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
