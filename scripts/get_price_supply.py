from flask import Flask, jsonify
import sys, os, json
import requests

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
json_file_path = os.path.join(project_root, 'projects', 'projects.json')
from app import app, db
from instances.TokenData import TokenData as Data

def get_nested_value(data, path):
    keys = path.split('.')
    for key in keys:
        if key.isdigit():
            data = data[int(key)]
        else:
            data = data.get(key, {})
        if not data:
            break
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

                        tokens.append(
                            {
                                "token": token,
                                "chain": chain,
                                "address": address,
                                "supply": supply
                            }
                        )
                return tokens
        except Exception as e:
            print(f"Error reading JSON file: {e}")
            return []

def get_price_supply():
    tokens = open_json()
    if not tokens:
        print("No tokens found in JSON file")
        return

    for item in tokens:
        token = item["token"]
        address = item["address"]
        chain = item["chain"]
        supply = item.get("supply", {})

        price = get_price_kraken(token) or (address and chain and get_curve_price(address, chain))
        item['price'] = price

        if supply:
            circ_supply = get_supply(supply)
            item['circ_supply'] = circ_supply

        del item["supply"]
        del item["address"]
        del item["chain"]

        try:
            token_data = Data(
                token=token,
                price=price,
                circ_supply=circ_supply
            )
            db.session.add(token_data)
        except Exception as e:
            print.error(f"Error adding token data to database: {e}")

    try:
        db.session.commit()
        print.info("Token data committed to database")
    except Exception as e:
        print.error(f"Error committing token data to database: {e}")

    return tokens

def get_price_kraken(token):
    ticker = f"{token}USD"
    endpoint = f"https://api.kraken.com/0/public/Ticker?pair={ticker}"
    try:
        r = requests.get(endpoint)
        r.raise_for_status()
        data = r.json()
        result = data.get("result", {})
        if ticker in result:
            price = result[ticker].get("c", [0])[0]
            return float(price)
    except requests.RequestException as e:
        print.error(f"Error fetching price from Kraken: {e}")
    return None

def get_curve_price(address, chain):
    endpoint = f"https://prices.curve.fi/v1/usd_price/{chain}/{address}"
    try:
        r = requests.get(endpoint)
        r.raise_for_status()
        data = r.json()
        price = data.get("data", {}).get("usd_price")
        return float(price)
    except requests.RequestException as e:
        print.error(f"Error fetching price from Curve: {e}")
    return None

def get_supply(supply):
    data = supply.get("circSupply", {})
    method = data.get("method")
    endpoint = data.get("endpoint")
    path = data.get("path")

    try:
        if method == "API":
            r = requests.get(endpoint)
            r.raise_for_status()
            data = r.json()
            circ_supply = get_nested_value(data, path)
        elif method == "hardcoded":
            circ_supply = data.get("amount")
        else:
            circ_supply = None
    except requests.RequestException as e:
        print.error(f"Error fetching supply data: {e}")
        circ_supply = None

    return circ_supply

if __name__ == '__main__':
    with app.app_context():
        get_price_supply()
