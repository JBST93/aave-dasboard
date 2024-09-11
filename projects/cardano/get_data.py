import requests
import os, sys
from datetime import datetime

# Ensure the root directory is in the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)


endpoint = "https://api.cardanoscan.io/api/v1/network/state"

r = requests.get(endpoint)
data = r.json()

from app import app, db
from instances.TokenData import TokenData as Info
from instances.YieldRate import YieldRate as Yield
from utils.get_price import get_price

def token_data():
    with app.app_context():
        token = "ADA"
        price = get_price(token,"","")
        circulating_supply_raw = requests.get(endpoint).json().get("circulatingSupply",{})
        circulating_supply = float(circulating_supply_raw)/10**6

        total_supply = 45000000000
        info = Info(
            token=token,
            price=price,
            price_source="",
            tot_supply=total_supply,
            circ_supply=circulating_supply,
            tvl=0,
            revenue=0,
            timestamp=datetime.utcnow()
        )

        db.session.add(info)
        db.session.commit()


if __name__ == '__main__':
    with app.app_context():
        token_data()
