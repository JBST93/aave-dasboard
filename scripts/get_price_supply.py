# Script used to fetch price from JSON and circulating supply
from flask import Flask, jsonify
import sys, os, json
import requests

# 1. Check for the currencies in my JSON
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
                        chain =result.get("chain")
                        address = result.get("address")
                        supply = result.get("supply")

                        tokens.append(
                            {
                                "token":token,
                                "chain":chain,
                                "address":address,
                                "supply":supply
                            }
                        )
                return tokens

        except Exception as e:
            print ({"error",str(e)}, 500)

def get_price_supply():
    tokens = open_json()
    for item in tokens:
        token = item["token"]
        address = item["address"]
        chain = item["chain"]
        supply = item.get("supply",{})

        price = get_price_kraken(token) or (address and chain and get_curve_price(address, chain))
        item['price'] = price

        if supply:
            circSupply = get_supply(supply)
            item['circSupply'] = circSupply

        del item["supply"]
        del item["address"]
        del item["chain"]

         # Add to database
        token_data = Data(
            token=token,
            price=price,
            circ_supply=circSupply
            )

        db.session.add(token_data)

        db.session.commit()


    return tokens

def get_price_kraken(token):
        ticker = f"{token}USD"
        endpoint = f"https://api.kraken.com/0/public/Ticker?pair={ticker}"
        r = requests.get(endpoint)
        r.raise_for_status()
        data = r.json()
        result = data.get("result",{})
        if ticker in result:
            price = result[ticker].get("c",0)[0]
            return float(price)


def get_curve_price(address, chain):
    endpoint = f"https://prices.curve.fi/v1/usd_price/{chain}/{address}"
    r = requests.get(endpoint)
    r.raise_for_status()
    data = r.json()
    price = data.get("data",{}).get("usd_price")
    return float(price)

# 5. Fetch through Uniswap Price

def get_supply(token):
    data = token.get("circSupply",{})
    method = data.get("method")
    endpoint = data.get("endpoint")
    path = data.get("path")

    if method == "API":
        r = requests.get(endpoint)
        data = r.json()
        circSupply = get_nested_value(data, path)
    elif method == "hardcoded":
        circSupply = data.get("amount")
    else:
        return None

    return circSupply




if __name__ == '__main__':
    with app.app_context():
        get_price_supply()
