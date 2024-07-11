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

@app.route('/api/liquidity_rates')
def get_liquidity_rates():
    from instances.MoneyMarketRate import MoneyMarketRate as MMR

    subquery = (
        db.session.query(
            MMR.token,
            MMR.protocol,
            MMR.collateral,
            MMR.chain,
            db.func.max(MMR.timestamp).label('latest')
        )
        .group_by(MMR.token, MMR.protocol, MMR.collateral, MMR.chain)
        .subquery()
    )

    latest_rates = db.session.query(MMR).join(
        subquery,
        (MMR.token == subquery.c.token) &
        (MMR.protocol == subquery.c.protocol) &
        (MMR.chain == subquery.c.chain) &
        ((MMR.collateral == subquery.c.collateral) | (MMR.collateral.is_(None) & subquery.c.collateral.is_(None))) &
        (MMR.timestamp == subquery.c.latest)
    ).order_by(MMR.liquidity_rate.desc()).all()

    rates_list = [
        {
            **rate.to_dict(),
            'tvl_formatted': f"{rate.tvl:,.0f}" if rate.tvl is not None else "N/A",
            'liquidity_rate_formatted': f"{rate.liquidity_rate:,.2f}" if rate.liquidity_rate is not None else "N/A",
            'humanized_timestamp': humanize.naturaltime(datetime.utcnow() - rate.timestamp)
        }
        for rate in latest_rates
    ]

    return jsonify(rates_list)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react_app(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        print("Serving static file.")
        return send_from_directory(app.static_folder, path)
    else:
        print("Serving index.html")
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    from jobs.fetch_store_data import fetch_store_data, start_scheduler
    with app.app_context():
        fetch_store_data()
        db.create_all()  # Ensure the database and tables are created
        scheduler = start_scheduler()
    app.run(debug=True)
