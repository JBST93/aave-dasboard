from flask import jsonify
import sys
import os
from sqlalchemy import desc, func
from app import app
from datetime import timedelta


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from app import db
from instances.TokenData import TokenData
from instances.Projects import Project


def _batch_get_latest_token_data(tokens):
    """Batch fetch latest token data for multiple tokens in a single query."""
    if not tokens:
        return {}

    # Subquery to get the max timestamp for each token
    subquery = db.session.query(
        TokenData.token,
        func.max(TokenData.timestamp).label('max_timestamp')
    ).filter(
        TokenData.token.in_(tokens)
    ).group_by(TokenData.token).subquery()

    # Join to get the full records
    results = db.session.query(TokenData).join(
        subquery,
        db.and_(
            TokenData.token == subquery.c.token,
            TokenData.timestamp == subquery.c.max_timestamp
        )
    ).all()

    return {r.token: r for r in results}


def _batch_get_token_data_at_time(token_time_pairs):
    """Batch fetch token data at specific times for multiple tokens."""
    if not token_time_pairs:
        return {}

    results = {}
    # Process in batches to avoid overly complex queries
    for token, target_time in token_time_pairs:
        data = TokenData.query.filter(
            db.and_(
                TokenData.token == token,
                TokenData.timestamp <= target_time
            )
        ).order_by(desc(TokenData.timestamp)).first()
        results[(token, target_time)] = data

    return results


def _format_price(price):
    """Format price based on magnitude."""
    if price < 1:
        return round(price, 6)
    elif price <= 10:
        return round(price, 4)
    elif price <= 1000:
        return round(price, 2)
    else:
        return round(price, 0)


def _calculate_delta(current, previous, current_value):
    """Calculate percentage delta safely."""
    if previous is not None and current_value != 0:
        prev_val = previous or 0
        return (current_value - prev_val) / current_value * 100
    return 0


def get_projects():
    with app.app_context():
        try:
            # Fetch all projects from the database (1 query)
            projects_data = Project.query.all()

            # Collect all tokens we need data for
            tokens = [p.token_ticker for p in projects_data]

            # Batch fetch latest token data (1 query instead of N)
            latest_data = _batch_get_latest_token_data(tokens)

            # Prepare time-based queries
            time_queries_24h = []
            time_queries_7d = []
            for token, data in latest_data.items():
                if data and data.timestamp:
                    time_queries_24h.append((token, data.timestamp - timedelta(hours=24)))
                    time_queries_7d.append((token, data.timestamp - timedelta(days=7)))

            # Batch fetch historical data (reduces N+N queries to 2N lookups, but with optimization potential)
            data_24h = _batch_get_token_data_at_time(time_queries_24h)
            data_7d = _batch_get_token_data_at_time(time_queries_7d)

            projects = []
            for project in projects_data:
                token = project.token_ticker
                token_data = latest_data.get(token)

                if token_data:
                    price = token_data.price or 0
                    circ_supply = token_data.circ_supply or 0
                    timestamp = token_data.timestamp
                    tvl = token_data.tvl or 0

                    time_24h_ago = timestamp - timedelta(hours=24)
                    time_7d_ago = timestamp - timedelta(days=7)

                    token_data_24h = data_24h.get((token, time_24h_ago))
                    token_data_7d = data_7d.get((token, time_7d_ago))

                    price_day_delta = _calculate_delta(
                        token_data_24h.price if token_data_24h else None,
                        token_data_24h.price if token_data_24h else None,
                        price
                    ) if token_data_24h else 0

                    if token_data_24h and price != 0:
                        price_24h_ago = token_data_24h.price or 0
                        price_day_delta = (price - price_24h_ago) / price * 100
                    else:
                        price_day_delta = 0

                    if token_data_7d and price != 0:
                        price_7d_ago = token_data_7d.price or 0
                        price_7day_delta = (price - price_7d_ago) / price * 100
                    else:
                        price_7day_delta = 0

                    if token_data_24h and tvl != 0:
                        tvl_24h_ago = token_data_24h.tvl or 0
                        tvl_day_delta = (tvl - tvl_24h_ago) / tvl * 100
                    else:
                        tvl_day_delta = 0

                    formatted_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S') if timestamp else "NEW"
                else:
                    price = 0
                    circ_supply = 0
                    price_day_delta = 0
                    price_7day_delta = 0
                    tvl = 0
                    tvl_day_delta = 0
                    formatted_timestamp = "NEW"

                marketCap = price * circ_supply

                projects.append({
                    'project': project.protocol_name,
                    'description': project.description,
                    'token': project.token_ticker,
                    'supply_formatted': float(circ_supply),
                    'price': _format_price(price),
                    'tvl': float(tvl),
                    'tvl_day_delta': float(tvl_day_delta),
                    'price_day_delta': float(price_day_delta),
                    'price_7d_delta': float(price_7day_delta),
                    'marketCap': float(marketCap),
                    'website': project.website,
                    'forum': project.forum,
                    'type': project.category_main,
                    'logo': project.logo_url or "",
                    'timestamp': formatted_timestamp,
                    'alert': project.alert,
                    'token_decimals': project.token_decimals,
                    'chain_main': project.chain_main,
                    'contract_main': project.contract_main,
                    'snapshot_name': project.snapshot_name,
                    'github_link': project.github_link
                })

            projects.sort(key=lambda x: x['marketCap'], reverse=True)

            return jsonify(projects)

        except Exception as e:
            return jsonify({"error": str(e)}), 500
