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
from instances.TokenData import TokenData as Data

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


def open_json():
    with app.app_context():
        try:
            with open(json_file_path, 'r') as file:
                results = json.load(file)
                tokens = []
                for result in results:
                    if result.get("token"):
                        token = result.get("token")
                        chain = result.get("chain")
                        address = result.get("address")
                        supply = result.get("supply")
                        tvl = result.get("tvl")


                        tokens.append(
                            {
                                "token": token,
                                "chain": chain,
                                "address": address,
                                "supply": supply,
                                "tvl": tvl,
                            }
                        )
                return tokens
        except Exception as e:
            logger.error(f"Error reading JSON file: {e}")
            return []

def get_price_supply():
    with app.app_context():
        tokens = open_json()
        if not tokens:
            logger.error("No tokens found in JSON file")
            return

        for item in tokens:
            token = item["token"]
            address = item["address"]
            chain = item["chain"]
            supply = item.get("supply", {})
            supply = item.get("tvl", "-")


            logger.info(f"Fetching price for {token}")
            price = get_price_kraken(token) or get_price_bitstamp(token) or (address and chain and get_curve_price(address, chain) or 0)
            item['price'] = price

            if supply:
                circ_supply = get_supply(supply)
                if isinstance(circ_supply, float):
                    item['circ_supply'] = circ_supply
                else:
                    item['circ_supply'] = 0

            logger.info(f"Processed token {token} with price {price} and supply {circ_supply}")

            del item["supply"]
            del item["address"]
            del item["chain"]

            if token != "stETH":

                try:
                    token_data = Data(
                        token=token,
                        price=price,
                        circ_supply=circ_supply
                    )

                    db.session.add(token_data)

                except Exception as e:
                    logger.error(f"Error adding token data to database: {e}")

        try:
            db.session.commit()
            logger.info("Token data committed to database")
        except Exception as e:
            logger.error(f"Error committing token data to database: {e}")

        return tokens

def get_price_kraken(token):
    ticker = f"{token}USD"
    endpoint = f"https://api.kraken.com/0/public/Ticker?pair={ticker}"
    try:
        r = requests.get(endpoint, timeout=10)  # Timeout added here
        r.raise_for_status()
        data = r.json()
        result = data.get("result", {})
        if ticker in result:
            price = result[ticker].get("c", [0])[0]
            return float(price)
    except requests.RequestException as e:
        logger.error(f"Error fetching price from Kraken: {e}")
    return None

def get_price_bitstamp(token):
    pair = f"{token.lower()}usd"

    endpoint = f"https://www.bitstamp.net/api/v2/ticker/{pair}"
    r = requests.get(endpoint)
    if r.status_code == 200:
        try:
           data = r.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching price from Kraken: {e}")
            return None
        return data.get("last")
    else:
        return None




def get_curve_price(address, chain):
    endpoint = f"https://prices.curve.fi/v1/usd_price/{chain}/{address}"
    try:
        r = requests.get(endpoint, timeout=10)  # Timeout added here
        r.raise_for_status()
        data = r.json()
        price = data.get("data", {}).get("usd_price")
        return float(price)
    except requests.RequestException as e:
        logger.error(f"Error fetching price from Curve: {e}")
    return None

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
        print("This script is intended to be run as a scheduled task.")
