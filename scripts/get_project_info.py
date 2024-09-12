from flask import Flask, jsonify
import sys, os, json
import requests
from sqlalchemy import desc, and_
from app import app
from datetime import datetime, timedelta


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
json_file_path = os.path.join(project_root, 'projects', 'projects.json')

from app import db
from instances.TokenData import TokenData
from instances.Projects import Project

def get_latest_token_data(token):
    """Fetch the latest token data from the database based on timestamp."""
    return TokenData.query.filter_by(token=token).order_by(desc(TokenData.timestamp)).first()

def get_token_data_at_time(token, target_time):
    """Fetch the token data closest to a specific time."""
    return TokenData.query.filter(
        and_(
            TokenData.token == token,
            TokenData.timestamp <= target_time
        )
    ).order_by(desc(TokenData.timestamp)).first()


def get_projects():
    with app.app_context():
        try:
            # Fetch all projects from the database
            projects_data = Project.query.all()

            projects = []
            for project in projects_data:
                token = project.token_ticker

                # Fetch the latest data from the database
                token_data = get_latest_token_data(token)

                if token_data:
                    price = token_data.price or 0
                    circ_supply = token_data.circ_supply or 0
                    timestamp = token_data.timestamp
                    tvl = token_data.tvl or 0

                    time_24h_ago = token_data.timestamp - timedelta(hours=24)
                    token_data_24h_ago = get_token_data_at_time(token, time_24h_ago)

                    if token_data_24h_ago and price != 0:
                        price_24h_ago = token_data_24h_ago.price or 0
                        price_day_delta = (price - price_24h_ago)/price*100
                    else:
                        price_day_delta = 0

                    if token_data_24h_ago and tvl != 0:
                        tvl_24h_ago = token_data_24h_ago.tvl or 0
                        tvl_day_delta = (tvl - tvl_24h_ago)/tvl*100
                    else:
                        tvl_day_delta = 0

                    formatted_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S') if timestamp else "NEW"

                else:
                    price = 0
                    circ_supply = 0
                    price_day_delta = 0
                    tvl = 0
                    tvl_day_delta = 0
                    formatted_timestamp = "NEW"

                marketCap = price * circ_supply

                if price < 1:
                    price = round(price, 6)
                elif price <= 10:
                    price = round(price, 4)
                elif price <= 1000:
                    price = round(price, 2)
                else:
                    price = round(price, 0)

                projects.append({
                    'project': project.protocol_name,
                    'description': project.description,
                    'token': project.token_ticker,
                    'supply_formatted': float(circ_supply),
                    'price': price,
                    'tvl': float(tvl),
                    'tvl_day_delta': float(tvl_day_delta),
                    'price_day_delta': float(price_day_delta),
                    'marketCapSorting': marketCap,
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

            projects.sort(key=lambda x: x['marketCapSorting'], reverse=True)

            # Remove the 'marketCapSorting' field used for sorting
            for project in projects:
                del project['marketCapSorting']

            return jsonify(projects)

        except Exception as e:
            return jsonify({"error": str(e)}), 500
