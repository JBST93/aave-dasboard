import requests
from dotenv import load_dotenv
import os, sys
from datetime import datetime

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)
load_dotenv(os.path.join(project_root, '.env'))

from app import app, db
from instances.TokenData import TokenData as Info
from utils.get_price import get_price


endpoint = "https://api.circle.com/v1/stablecoins"
r = requests.get(endpoint)
data = r.json()

def get_data():
    with app.app_context():
        for token_data in data.get("data", []):
            symbol = token_data.get("symbol")
            total_amount = float(token_data.get("totalAmount", 0))

            try:
                price = get_price(symbol, "0x1aBaEA1f7C830bD89Acc67eC4af516284b1bC33c" "ethereum")
            except Exception as e:
                price = None

            print(f"{symbol} : {price}")

            if price is not None:
                info = Info(
                    token=symbol,
                    price=price,
                    price_source="",
                    tot_supply=total_amount,
                    circ_supply=total_amount,
                    timestamp=datetime.utcnow(),
                )
                db.session.add(info)

        db.session.commit()
