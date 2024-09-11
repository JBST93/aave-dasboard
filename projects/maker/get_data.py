import requests, sys, os
from datetime import datetime

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

from app import app, db

from utils.get_price import get_price
from instances.TokenData import TokenData

import requests

tokens = [
    {
        "token": "DAI",
         "contract":"0x83F20F44975D03b1b09e64809B757c47f942BEeA",
        "decimals":18,
        "chain":"ethereum",
        "type":"stablecoin"
    },
    {
        "token": "MKR",
        "contract":"0x83F20F44975D03b1b09e64809B757c47f942BEeA",
        "decimals":18,
        "chain":"ethereum",
        "type":"governance"
    },
    {
        "token": "sDAI",
        "contract":"0x83F20F44975D03b1b09e64809B757c47f942BEeA",
        "decimals":18,
        "chain":"ethereum",
        "type":"stablecoin"
    }
]
endpoint ="https://cortex.blockanalitica.com/api/v1/maker/"


def get_data():
    r = requests.get(endpoint)
    data = r.json()
    for item in tokens:
        token = item["token"]
        contract = item["contract"]
        chain = item["chain"]
        decimals = item["decimals"]
        total_supply = data.get(f"{token.lower()}_total_supply")
        if item["type"] == "stablecoin":
            circ_supply = data.get(f"{token.lower()}_total_supply")
        else:
            circ_supply = data.get(f"{token.lower()}_circulating_supply")
        price = get_price(token,contract,chain)

        info = TokenData (
                token=token,
                price=price,
                price_source= "",
                tot_supply= float(total_supply),
                circ_supply= float(circ_supply),
                timestamp=datetime.utcnow(),
            )

        db.session.add(info)
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        get_data()
