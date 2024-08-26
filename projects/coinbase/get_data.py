import requests
import os, sys
from datetime import datetime

# Ensure the root directory is in the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)


endpoint = "https://api-public.sandbox.exchange.coinbase.com/wrapped-assets/CBETH/"

r = requests.get(endpoint)
data = r.json()

from app import app, db
from instances.TokenData import TokenData as Info
from instances.YieldRate import YieldRate as Yield
from utils.get_price import get_price


def token_data():
    with app.app_context():
        token = "cbETH"
        circulating_supply = float(data.get("circulating_supply"))
        total_supply = float(data.get("total_supply"))
        apy = round(float(data.get("apy"))*100,2)
        conversion_rate = data.get("conversion_rate")
        address = "0xBe9895146f7AF43049ca1c1AE358B0541Ea49704"
        chain = "ethereum"
        price = (get_price(token,address,chain))
        tot_supply_usd = total_supply
        circ_supply_usd = circulating_supply

        info = Info(
            token=token,
            price=price,
            price_source="",
            tot_supply=tot_supply_usd,
            circ_supply=circ_supply_usd,
            tvl=0,
            revenue=0,
            timestamp=datetime.utcnow()
        )
        db.session.add(info)
        db.session.commit()
        print(info)

if __name__ == '__main__':
    with app.app_context():
        token_data()
