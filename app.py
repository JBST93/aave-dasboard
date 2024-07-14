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

@app.route('/api/liquidity_rates', methods=['GET'])
def liquidity_rates():
    return get_stablecoin_rates()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react_app(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    from jobs.schedule import fetch_store_data
    with app.app_context():
        liquidity_rates()
        db.create_all()  # Ensure the database and tables are created
    app.run(debug=False)
