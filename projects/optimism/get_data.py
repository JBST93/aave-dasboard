import requests
import sys, os
from dotenv import load_dotenv
from datetime import datetime

token = "OP"
address = "0x4200000000000000000000000000000000000042"
chain = 'optimism'
decimals = 18

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

from app import app, db
from utils.get_price import get_price
from instances.TokenData import TokenData as Data


load_dotenv(os.path.join(project_root, '.env'))

def get_token_data():
    with app.app_context():
        endpoint_circ_supply = "https://static.optimism.io/tokenomics/circulatingSupply.txt"
        endpoint_tot_supply = "https://static.optimism.io/tokenomics/totalSupply.txt"

        r_circ = requests.get(endpoint_circ_supply)
        r_tot = requests.get(endpoint_tot_supply)

        data_circ = r_circ.json()
        data_tot = r_tot.json()

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
