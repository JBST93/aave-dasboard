from flask import Flask, jsonify
from sqlalchemy import desc
import sys, os
import humanize
from datetime import datetime
from sqlalchemy import func, and_

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from app import app, db
from instances.Stablecoin import Stablecoin as Table

def get_stablecoin_info_render():
    with app.app_context():
        # Subquery to get the latest timestamp for each token
        subquery = db.session.query(
            Table.token,
            func.max(Table.timestamp).label('latest_timestamp')
        ).group_by(Table.token).subquery()

        # Join the subquery with the original table to get the full records
        query = db.session.query(Table).join(
            subquery,
            and_(
                Table.token == subquery.c.token,
                Table.timestamp == subquery.c.latest_timestamp
            )
        ).filter(Table.supply > 0).order_by(desc(Table.supply))

        # Execute the query and fetch the results
        results = query.all()

        # Initialize variables for calculations
        total_supply = 0
        usd_dominance = 0
        centralized_dominance = 0
        total_tokens = len(results)

        # Format the results as a list of dictionaries
        stablecoin_info = []
        for result in results:
            supply = result.supply if result.supply is not None else 0
            total_supply += supply

            if result.pegged_against.upper() == 'USD':
                usd_dominance += supply

            if result.info.lower() == 'centralised':
                centralized_dominance += supply

            stablecoin_info.append({
                'id': result.id,
                'token': result.token,
                'supply': supply,
                'supply_formatted': f"{supply:,.0f}",
                'info': result.info,
                'price': result.price,
                'pegged_against': result.pegged_against,
                'chain': result.chain,
                'timestamp': result.timestamp,
                'timestamp_humanized': humanize.naturaltime(result.timestamp)
            })

        # Calculate dominance percentages
        usd_dominance_percentage = (usd_dominance / total_supply) * 100 if total_supply > 0 else 0
        centralized_dominance_percentage = (centralized_dominance / total_supply) * 100 if total_supply > 0 else 0

        # Add the additional calculations to the response
        summary_info = {
            'total_supply': f"{total_supply:,.0f}",
            'usd_dominance_percentage': f"{usd_dominance_percentage:.2f}%",
            'centralised_dominance_percentage': f"{centralized_dominance_percentage:.2f}%",
            'total_tokens': total_tokens
        }

        return jsonify(stablecoin_info=stablecoin_info, summary_info=summary_info)
