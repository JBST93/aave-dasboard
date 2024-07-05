# db_config.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

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
