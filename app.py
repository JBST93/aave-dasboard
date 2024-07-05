from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


from web3 import Web3
import json
import sqlite3
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from datetime import datetime

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///liquidity_rates.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
migrate = Migrate(app, db)

class MoneyMarketRate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    protocol = db.Column(db.String(15), nullable=False)
    token = db.Column(db.String(10), nullable=False)
    liquidity_rate = db.Column(db.Float, nullable=False)
    borrow_rate = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now)


# Initialize Web3
infura_url = os.getenv('INFURA_URL')
web3 = Web3(Web3.HTTPProvider(infura_url))

# Load ABI from JSON files
with open('APDP.json') as f:
    provider_abi = json.load(f)

pool_address = "0x7B4EB56E7CD4b454BA8ff71E4518426369a138a3" # AaveProtocolDataProvider
pool_contract = web3.eth.contract(address=pool_address, abi=provider_abi)


token_addresses = {
    "USDC": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
    "USDT": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
    "DAI": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
    "USDe": "0x4c9EDD5852cd905f086C759E8383e09bff1E68B3",
    "pyUSD": "0x6c3ea9036406852006290770BEdFcAbA0e23A0e8",
    "LUSD":"0x5f98805A4E8be255a32880FDeC7F6728C6568bA0",
    "crvUSD":"0xf939E0A03FB07F59A73314E73794Be0E57ac1b4E",
}



@app.route('/')
def get_liquidity_rates():
    subquery = (
        db.session.query(
            MoneyMarketRate.token,
            db.func.max(MoneyMarketRate.timestamp).label('latest')
        )
        .group_by(MoneyMarketRate.token)
        .subquery()
    )

    latest_rates = db.session.query(MoneyMarketRate).join(
        subquery,
        (MoneyMarketRate.token == subquery.c.token) &
        (MoneyMarketRate.timestamp == subquery.c.latest)
    ).order_by(MoneyMarketRate.liquidity_rate.desc()).all()

    return render_template('index.html', rates=latest_rates)

@app.route('/fetch_rates')
def fetch_rates():
    return fetch_store_rates()



def fetch_store_rates():
    from datetime import datetime
    for token in token_addresses:
        try:
            print(f"Fetching data for {token}...")
            reserve_data = pool_contract.functions.getReserveData(token_addresses[token]).call()
            liquidity_rate = reserve_data[5] / 1e27 * 100 # Convert from Ray to percentage
            borrow_rate = reserve_data[6] / 1e27 * 100 # Convert from Ray to percentage

            transformed_liquidity_rate = ((round(liquidity_rate,2)))
            transformed_borrow_rate = ((round(borrow_rate,2)))

            rate = MoneyMarketRate(
                token=token,
                protocol="Aave V3",
                liquidity_rate=float(transformed_liquidity_rate),
                borrow_rate=float(transformed_borrow_rate),
                timestamp=datetime.utcnow()

            )
            db.session.add(rate)


        except Exception as e:
            return f"Error fetching USDC liquidity rate: {e}", 500
    db.session.commit()
    return "Fetched"




@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'MoneyMarketRate': MoneyMarketRate}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure the database and tables are created
    app.run(debug=True)
