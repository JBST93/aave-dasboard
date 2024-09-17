from flask import Flask, jsonify
import sys, os
import humanize
from datetime import datetime, timedelta

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import or_


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from app import app, db
from instances.YieldRate import YieldRate as Table

coins = ["ETH", "wETH"]

conditions = [Table.market.ilike(f"%{coin}%") for coin in coins]


def get_ethereum_yields():
    with app.app_context():

        # Calculate the time threshold for 3 hours ago
        time_threshold = datetime.utcnow() - timedelta(hours=3)

        # Fetch all records that match the conditions
        records = db.session.query(Table).filter(
            Table.timestamp > time_threshold,
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
                'yield_rate_reward': f"{rate.yield_rate_reward:,.2f}" if rate.yield_rate_reward is not None else 0,

                'humanized_timestamp': humanize.naturaltime(datetime.utcnow() - rate.timestamp),
                'information_transformed': rate.information if isinstance(rate.information, list) else [],

            }
            for rate in unique_rates.values()
        ]

        return jsonify(rates_list)

# Run the Flask app
if __name__ == "__main__":
    get_ethereum_yields()
