from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from web3 import Web3
import json
from datetime import datetime
from dotenv import load_dotenv
import os
import humanize


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
    tvl = db.Column(db.Float, nullable=False, default=0)
    timestamp = db.Column(db.DateTime, default=datetime.now)

@app.route('/')
def get_liquidity_rates():
      # Subquery to get the latest timestamp for each token-protocol combination
    subquery = (
        db.session.query(
            MoneyMarketRate.token,
            MoneyMarketRate.protocol,
            db.func.max(MoneyMarketRate.timestamp).label('latest')
        )
        .group_by(MoneyMarketRate.token, MoneyMarketRate.protocol)
        .subquery()
    )

    # Query to get the latest rates based on the subquery
    latest_rates = db.session.query(MoneyMarketRate).join(
        subquery,
        (MoneyMarketRate.token == subquery.c.token) &
        (MoneyMarketRate.protocol == subquery.c.protocol) &
        (MoneyMarketRate.timestamp == subquery.c.latest)
    ).order_by(MoneyMarketRate.liquidity_rate.desc()).all()

    for rate in latest_rates:
        if rate.tvl is not None:
            rate.tvl_formatted = f"{rate.tvl:,.0f}"
        else:
            rate.tvl_formatted = "N/A"  # or any default value you'd like to show

    for rate in latest_rates:
        if rate.liquidity_rate is not None:
            rate.liquidity_rate = f"{rate.liquidity_rate:,.2f}"
        else:
            rate.liquidity_rate = "N/A"  # or any default value you'd like to show

        rate.humanized_timestamp = humanize.naturaltime(datetime.utcnow() - rate.timestamp)


    return render_template('index.html', rates=latest_rates)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'MoneyMarketRate': MoneyMarketRate}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure the database and tables are created
    app.run(debug=True)
