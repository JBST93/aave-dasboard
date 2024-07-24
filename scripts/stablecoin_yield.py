from flask import Flask, jsonify
import sys, os
import humanize
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import or_


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from app import app, db
from instances.YieldRate import YieldRate as Table

stablecoins = [
    "USDC", "USDT", "DAI", "USDe", "USDD", "pyUSD",
    "FRAX", "crvUSD", "GHO", "LUSD", "USDA", "sDai",
    "sFrax", "FRAX", "eUSD"
]

conditions = [Table.market.ilike(f"%{coin}%") for coin in stablecoins]


def get_stablecoin_rates():
    with app.app_context():
        # Fetch all records that match the conditions
        records = db.session.query(Table).filter(
            Table.tvl > 1000,
            or_(*conditions)
        ).order_by(Table.market, Table.chain, Table.project, Table.timestamp.desc()).all()

        # Dictionary to hold the latest entry for each combination of (token, chain, collateral, protocol)
        unique_rates = {}
        for rate in records:
            smart_contract = rate.smart_contract  # Assuming there is a `smart_contract` field
            if smart_contract not in unique_rates:
                unique_rates[smart_contract] = rate
            else:
                if rate.timestamp > unique_rates[smart_contract].timestamp:
                    unique_rates[smart_contract] = rate


        rates_list = [
            {
                **rate.to_dict(),
                'tvl_formatted': f"{rate.tvl:,.0f}" if rate.tvl is not None else 0,
                'yield_rate_base': f"{rate.yield_rate_base:,.2f}" if rate.yield_rate_base is not None else 0,
                'humanized_timestamp': humanize.naturaltime(datetime.utcnow() - rate.timestamp)
            }
            for rate in unique_rates.values()
        ]

        return jsonify(rates_list)

# Run the Flask app
if __name__ == "__main__":
    app.run()
