from flask import Flask, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
import humanize
from datetime import datetime
from flask_cors import CORS

load_dotenv()

app = Flask(__name__, static_folder='frontend/dist', static_url_path='')
app.config.from_object(os.getenv('APP_SETTINGS', 'config.DevelopmentConfig'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

CORS(app)

from scripts.stablecoin_yield import get_stablecoin_rates
from scripts.eth_yield_api import get_ethereum_yields

from scripts.stablecoin_info_render import get_stablecoin_info_render


@app.route('/api/stablecoin_yield_rates', methods=['GET'])
def liquidity_rates():
    return get_stablecoin_rates()

@app.route('/api/eth_yield_rates', methods=['GET'])
def get_ethereum_yields():
    return get_ethereum_yields()

@app.route('/api/stablecoin_info', methods=['GET'])
def stablecoin_info():
    return get_stablecoin_info_render()


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

@app.errorhandler(404)
def not_found(e):
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run()
