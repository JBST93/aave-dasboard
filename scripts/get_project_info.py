from flask import Flask, jsonify
import sys, os, json
import requests
from sqlalchemy import desc
from app import app

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
json_file_path = os.path.join(project_root, 'projects', 'projects.json')

from app import db
from instances.TokenData import TokenData


def get_latest_token_data(token):
    """Fetch the latest token data from the database based on timestamp."""
    return TokenData.query.filter_by(token=token).order_by(desc(TokenData.timestamp)).first()

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
                        price = token_data.price
                        circ_supply = token_data.circ_supply or 0
                    else:
                        price = 0
                        circ_supply = 0

                    circ_supply = float(result.get("circ_supply", 0))
                    marketCap = price * circ_supply

                    projects.append({
                        'project': result["project"],
                        'description': result["description"],
                        'token': result["token"],
                        'supply_formatted': circ_supply,
                        'price': price,
                        'marketCap': f"{marketCap:,.0f}",
                        'website': result["website"],
                        'forum': result["forum"],
                        'type': result["business"]
                    })

                return jsonify(projects)

        except Exception as e:
            return jsonify({"error": str(e)}), 500
