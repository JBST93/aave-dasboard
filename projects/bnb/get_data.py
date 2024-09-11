import requests
import requests, sys, os
from datetime import datetime

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

from app import app, db

from utils.get_price import get_price
from instances.TokenData import TokenData as Data

token = "BNB"
circ_supply = 145887575
max_supply = 200000000

def get_data():
    price = get_price(token,"","")
    total_supply = max_supply
    circ_supply = circ_supply


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
