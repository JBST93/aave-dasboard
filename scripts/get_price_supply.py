from flask import Flask
import sys, os, json
import requests

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

json_file_path = os.path.join(project_root, 'projects', 'projects.json')

from app import app, db
from utils.get_price import get_price
from instances.TokenData import TokenData as Data
from instances.Projects import Project

def get_nested_value(data, path):
    keys = path.split('.')
    for key in keys:
        if isinstance(data, list) and key.isdigit():
            index = int(key)
            if 0 <= index < len(data):
                data = data[index]
            else:
                return None  # Index out of range
        elif isinstance(data, dict):
            data = data.get(key, None)
        else:
            return None  # Invalid access path
    return data


def get_projects():
    with app.app_context():
        try:
            results = Project.query.all()
            tokens = []
            for result in results:
                if result.token_ticker:
                    tokens.append({
                        "token": result.token_ticker,
                        "chain": result.chain_main or None,
                        "address": result.contract_main or None,
                        "supply": result.supply or 0,
                    })
            return tokens
        except Exception as e:
            logger.error(f"Error reading API data: {e}")
            return []

def get_price_supply():
    with app.app_context():
        print("Fetching data for token without dedicated function")
        tokens = get_projects()
        if not tokens:
            logger.error("No tokens found in database")
            return

        for item in tokens:
            try:
                token = item["token"]
                address = item["address"] or None
                chain = item["chain"] or None
                supply_data = item.get("supply") or 0

                # Check for existing data in the database
                if supply_data:
                    print(f"Fetching data for {token} as supply daya in JSON")

                    circ_supply = get_supply(supply_data) if supply_data else 0
                    price = get_price(token, address, chain) or None

                    if circ_supply is not None and price is not None:
                        item['price'] = price
                        item['circ_supply'] = circ_supply

                        try:
                            token_data = Data(
                                token=token,
                                price=price,
                                circ_supply=circ_supply,
                                tvl = 0,
                            )

                            db.session.add(token_data)

                        except Exception as e:
                            logger.error(f"Error adding token data to database: {e}")
                    else:
                        logger.warning(f"Skipping token {token} due to missing price or supply data")

            except Exception as e:
                print(f"error for f{item["token"]}: {e}")

        try:
            db.session.commit()
        except Exception as e:
            logger.error(f"Error committing token data to database: {e}")

        return tokens


def get_supply(supply):
    data = supply.get("circSupply", {})
    method = data.get("method")
    endpoint = data.get("endpoint")
    path = data.get("path")

    try:
        if method == "API":
            r = requests.get(endpoint, timeout=10)  # Timeout added here
            r.raise_for_status()
            data = r.json()
            circ_supply = get_nested_value(data, path)
        elif method == "hardcoded":
            circ_supply = data.get("amount")
        else:
            circ_supply = None
    except requests.RequestException as e:
        logger.error(f"Error fetching supply data: {e}")
        circ_supply = None

    return circ_supply

if __name__ == '__main__':
        get_price_supply()
