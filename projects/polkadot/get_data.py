import requests
import sys, os
from dotenv import load_dotenv
from datetime import datetime

token = "DOT"
address = "0x4200000000000000000000000000000000000042"
chain = 'Polkadot'
decimals = 10

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

from app import app, db
from utils.get_price import get_price
from instances.TokenData import TokenData as Data


load_dotenv(os.path.join(project_root, '.env'))

def get_token_data():
    with app.app_context():
        endpoint = "https://polkadot.api.subscan.io/api/scan/token"
        r = requests.get(endpoint)
        data = r.json()
        data_circ = data['data']['detail']['DOT']['total_issuance']
        data_tot = data['data']['detail']['DOT']['total_issuance']

        circSupply = float(data_circ)
        totSupply = float(data_tot)
        price = get_price(token, address, chain)

        data = Data (
                token= token,
                price=price,
                price_source= "",
                tot_supply= totSupply,
                circ_supply= circSupply ,
                timestamp=datetime.utcnow(),
            )

        db.session.add(data)
        db.session.commit()

if __name__ == '__main__':
   get_token_data()
