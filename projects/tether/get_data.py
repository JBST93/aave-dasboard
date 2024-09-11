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


endpoint = "https://app.tether.to/transparency.json"
r = requests.get(endpoint)
data = r.json()

def get_data():
    with app.app_context():
        for token_data in data.get("data_formatted", []):
            symbol = token_data.get("iso", "").upper()
            total_amount = token_data.get("total_liabilities", 0)

            try:
                price = get_price(symbol, "", "ethereum")
            except Exception as e:
                price = None

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
