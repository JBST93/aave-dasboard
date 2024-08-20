from flask import Flask
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from app import app

def get_price(token, address, chain):
    with app.app_context():
        logger.info(f"Fetching price for {token}")
        price = get_price_kraken(token) or get_price_bitstamp(token) or get_price_curve(address, chain) or  0
        return price

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
    r = requests.get(endpoint, timeout=10)
    if r.status_code == 200:
        try:
           data = r.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching price from Bitstamp: {e}")
            return None

        return float(data.get("last"))
    else:
        return None


def get_price_curve(address, chain):
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



if __name__ == '__main__':
        get_price()
