from flask import Flask, jsonify
import sys, os
import humanize
from datetime import datetime, timedelta

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import or_, desc


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from app import app, db
from instances.YieldRate import YieldRate as Table

def clean_information(info):
    # Remove curly braces and split the string by commas
    tokens = info.strip("{}").split(",")
    # Remove any whitespace around tokens
    return [token.strip() for token in tokens]


def get_rates():
    with app.app_context():

        # Calculate the time threshold for 3 hours ago
        time_threshold = datetime.utcnow() - timedelta(hours=3)

        # Fetch all records that match the conditions
        records = db.session.query(Table).filter(
            Table.tvl > 1000,
            Table.timestamp > time_threshold,
        ).order_by(desc(Table.tvl)).all()

        # Dictionary to hold the latest entry for each combination of (token, chain, collateral, protocol)
        unique_rates = {}
        for rate in records:
            key = (rate.project, rate.chain, rate.smart_contract)  # Combining project, chain, and smart_contract

            if key not in unique_rates:
                unique_rates[key] = rate
            else:
                if rate.timestamp > unique_rates[key].timestamp:
                    unique_rates[key] = rate

        rates_list = [
            {
                **rate.to_dict(),
                'tvl_formatted': f"{rate.tvl:,.0f}" if rate.tvl is not None else 0,
                'yield_rate_base': f"{rate.yield_rate_base:,.2f}" if rate.yield_rate_base is not None else 0,
                'yield_rate_reward': f"{rate.yield_rate_reward:,.2f}" if rate.yield_rate_reward is not None else 0,

                'humanized_timestamp': humanize.naturaltime(datetime.utcnow() - rate.timestamp),
                'information_transformed': clean_information(rate.information) if rate.information else [],

            }
            for rate in unique_rates.values()
        ]

        return jsonify(rates_list)

# Run the Flask app
if __name__ == "__main__":
    app.run()
