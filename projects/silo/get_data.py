import requests
import sys,os
from datetime import datetime

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(project_root)

from app import app, db
from instances.YieldRate import YieldRate as Data
from instances.TokenData import TokenData as TokenData
from utils.get_price import get_price

token = "SILO"
total_supply = 1000000000
chain = "ethereum"
address = "0x6f80310CA7F2C654691D1383149Fa1A57d8AB1f8"
endpoint_circ_supply = "https://supply-api-kappa.vercel.app/api/circulatingSupply"


def get_token_data():
    with app.app_context():
        r = requests.get(endpoint_circ_supply)
        circ_supply = float(r.json())
        price = get_price(token,address,chain)
        circ_supply_usd = price * circ_supply


        data = TokenData (
                token= token,
                price=price,
                price_source= "",
                tot_supply= total_supply,
                circ_supply= circ_supply ,
                timestamp=datetime.utcnow(),
            )

        db.session.add(data)
        db.session.commit()

if __name__ == '__main__':
   get_token_data()
