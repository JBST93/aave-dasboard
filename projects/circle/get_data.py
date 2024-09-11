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
        for i in range(len(data.get("data"))):
            symbol = data.get("data")[i].get("symbol")
            totalAmount = data.get("data")[i].get("totalAmount")
            price = get_price(symbol,"","")
            info = Info(
                token=symbol,
                price=price,
                price_source= "",
                tot_supply= float(totalAmount),
                circ_supply= float(totalAmount),
                timestamp=datetime.utcnow(),
            )

            db.session.add(info)
        db.session.commit()
