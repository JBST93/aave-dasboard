from flask import jsonify
import sys
import os
import humanize
from datetime import datetime, timedelta

from sqlalchemy import desc


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from app import app, db
from instances.YieldRate import YieldRate as Table
from constants import MIN_TVL_THRESHOLD, DATA_FRESHNESS_HOURS, STABLECOINS

def clean_information(info):
    # Remove curly braces and split the string by commas
    tokens = info.strip("{}").split(",")
    # Remove any whitespace around tokens
    return [token.strip() for token in tokens]


def is_valid_stablecoin_market(market):
    """Check if a market contains a recognized stablecoin."""
    market_upper = market.upper()
    tokens = [token.strip() for token in market_upper.replace('/', ' ').split()]
    stablecoin_list_upper = [s.upper() for s in STABLECOINS]
    return any(token == stablecoin for token in tokens for stablecoin in stablecoin_list_upper)


def get_stablecoin_rates():
    with app.app_context():
        time_threshold = datetime.utcnow() - timedelta(hours=DATA_FRESHNESS_HOURS)

        records = db.session.query(Table).filter(
            Table.tvl > MIN_TVL_THRESHOLD,
            Table.timestamp > time_threshold,
        ).order_by(desc(Table.tvl)).all()

        # Dictionary to hold the latest entry for each combination of (project, chain, smart_contract, information)
        # This allows multiple instances per project (e.g., Aave v3 Main, Aave v3 Prime, etc.)
        unique_rates = {}
        for rate in records:
            key = (rate.project, rate.chain, rate.smart_contract, rate.information)  # Include instance information

            if key not in unique_rates:
                unique_rates[key] = rate
            else:
                if rate.timestamp > unique_rates[key].timestamp:
                    unique_rates[key] = rate

        # Filter the rates before creating the rates_list
        filtered_rates = [
            rate for rate in unique_rates.values()
            if is_valid_stablecoin_market(rate.market)
        ]

        # Re-sort by TVL after deduplication to maintain proper order
        filtered_rates.sort(key=lambda x: x.tvl, reverse=True)

        # Debug: Log what's being filtered out
        for rate in unique_rates.values():
            if not is_valid_stablecoin_market(rate.market):
                print(f"FILTERED OUT: {rate.project} - {rate.market} - {rate.information}")

        rates_list = [
            {
                **rate.to_dict(),
                'tvl_formatted': f"{rate.tvl:,.0f}" if rate.tvl is not None else 0,
                'yield_rate_base': f"{rate.yield_rate_base:,.2f}" if rate.yield_rate_base is not None else 0,
                'yield_rate_reward': f"{rate.yield_rate_reward:,.2f}" if rate.yield_rate_reward is not None else 0,

                'humanized_timestamp': humanize.naturaltime(datetime.utcnow() - rate.timestamp),
                'information_transformed': clean_information(rate.information) if rate.information else [],
            }
            for rate in filtered_rates
        ]

        return jsonify(rates_list)

# Run the Flask app
if __name__ == "__main__":
    app.run()
