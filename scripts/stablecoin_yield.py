from flask import Flask, jsonify
import sys, os
import humanize
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from app import app, db
from instances.MoneyMarketRate import MoneyMarketRate as Table

stablecoins = [
    "USDC", "USDT", "DAI", "USDe", "USDD", "pyUSD",
    "FRAX", "crvUSD", "GHO", "LUSD", "USDA", "sDai",
    "sFrax", "FRAX", "eUSD"
]

def get_stablecoin_rates():
    with app.app_context():
        # Fetch all records that match the conditions
        records = db.session.query(Table).filter(
            Table.tvl > 1000,
            Table.token.in_(stablecoins)
        ).order_by(Table.token, Table.chain, Table.protocol, Table.timestamp.desc()).all()

        print(f"Found {len(records)} records")  # Debugging statement

        # Dictionary to hold the latest entry for each combination of (token, chain, collateral, protocol)
        unique_rates = {}
        for rate in records:
            collateral_key = tuple(sorted(rate.collateral)) if isinstance(rate.collateral, list) else rate.collateral
            key = (rate.token, rate.chain, collateral_key, rate.protocol)
            if key not in unique_rates:
                unique_rates[key] = rate

        rates_list = [
            {
                **rate.to_dict(),
                'tvl_formatted': f"{rate.tvl:,.0f}" if rate.tvl is not None else 0,
                'liquidity_rate_formatted': f"{rate.liquidity_rate:,.2f}" if rate.liquidity_rate is not None else 0,
                'humanized_timestamp': humanize.naturaltime(datetime.utcnow() - rate.timestamp)
            }
            for rate in unique_rates.values()
        ]

        return jsonify(rates_list)

# Run the Flask app
if __name__ == "__main__":
    app.run()
