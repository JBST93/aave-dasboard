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
            with open(json_file_path, 'r') as file:
                results = json.load(file)

                projects = []
                for result in results:
                    token = result.get("token")

                    # Fetch the latest data from the database
                    token_data = get_latest_token_data(token)

                    if token_data:
                        price = token_data.price or 0
                        circ_supply = token_data.circ_supply or 0

                        time_24h_ago = token_data.timestamp - timedelta(hours=24)
                        token_data_24h_ago = get_token_data_at_time(token, time_24h_ago)

                        if token_data_24h_ago and price != 0:
                            price_24h_ago = token_data_24h_ago.price or 0
                            price_day_delta = (price - price_24h_ago)/price*100
                        else:
                            price_day_delta = 0

                    else:
                        price = 0
                        circ_supply = 0
                        price_day_delta = 0


                    marketCap = price * circ_supply

                    if price < 1:
                        price = round(price,6)

                    elif price <= 10:
                        price = round(price,4)

                    else:
                        price = round(price,2)


                    projects.append({
                        'project': result["project"],
                        'description': result["description"],
                        'token': result["token"],
                        'supply_formatted': circ_supply,
                        'price': price,
                        'price_day_delta': f"{price_day_delta:,.2f}",
                        'marketCapSorting': marketCap,
                        'marketCap': f"{marketCap:,.0f}",
                        'website': result["website"],
                        'forum': result["forum"],
                        'type': result["business"],
                        'logo': result.get("logoUrl","")

                    })

                projects.sort(key=lambda x: x['marketCapSorting'], reverse=True)

                # Remove the 'marketCap' field used for sorting
                for project in projects:
                    del project['marketCapSorting']


                return jsonify(projects)

        except Exception as e:
            return jsonify({"error": str(e)}), 500
