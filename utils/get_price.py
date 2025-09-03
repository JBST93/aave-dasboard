from flask import Flask
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from app import app

def get_price(token, address=None, chain=None):
    with app.app_context():
        # Debug problematic tokens
        if token in ['LUSD', 'crvUSD', 'USDe']:
            print(f"🔍 Fetching price for {token}...")
            
        price = get_price_kraken(token) or get_price_bitstamp(token) or get_price_okx(token) or get_price_curve(address, chain) or get_gateio_price(token) or get_angle_price(token) or 0
        
        # Debug problematic tokens
        if token in ['LUSD', 'crvUSD', 'USDe']:
            if price > 1000:
                print(f"⚠️  {token} price from external source: ${price:,.2f} (seems too high!)")
            else:
                print(f"✅ {token} price from external source: ${price:,.2f}")
                
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

def get_price_okx(token):
    endpoint = f"https://www.okx.com/api/v5/market/ticker?instId={token}-USDT"
    try:
        r = requests.get(endpoint, timeout=10)
        r.raise_for_status()
        data = r.json()
        price = data.get("data", [])
        if price:
            price = price[0].get("last")
            return float(price)

        else:
            price = None
            return price

    except requests.RequestException as e:
        logger.error(f"Error fetching price from OKX: {e}")
    return None

def get_price_bitstamp(token: str, quote: str = "usd"):
    """
    Robust Bitstamp price fetcher.
    Handles:
    - normal dict response: {"last": "...", ...}
    - list responses: [{"pair": "ETHUSD", "last": "..."} ...]
    - missing/invalid pairs -> returns None (lets the caller fall through)
    """
    pair = f"{token.lower()}{quote.lower()}"           # e.g. "ethusd"
    url = f"https://www.bitstamp.net/api/v2/ticker/{pair}/"  # trailing slash helps avoid redirects

    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()

        # Case 1: Dict response (normal for a valid pair)
        if isinstance(data, dict):
            last = data.get("last") or data.get("last_price")
            return float(last) if last is not None else None

        # Case 2: List response (Bitstamp sometimes returns a list of tickers)
        if isinstance(data, list):
            # Prefer exact pair match if present
            for item in data:
                if isinstance(item, dict) and item.get("pair", "").lower() == pair:
                    if "last" in item:
                        return float(item["last"])
            # Fallback to the first dict that has "last"
            for item in data:
                if isinstance(item, dict) and "last" in item:
                    return float(item["last"])

        # No usable price found
        return None

    except Exception as e:
        logger.warning(f"Bitstamp price fetch failed for {pair}: {e}")
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

def get_gateio_price(token):
    try:
        endpoint = f"https://api.gateio.ws/api/v4/spot/tickers?currency_pair={token}_USDT"
        data = requests.get(endpoint).json()
        price = data[0]["last"]
        return price
    except requests.RequestException as e:
        return None

def get_angle_price(token):
    endpoint = "https://api.angle.money/v1/prices"
    try:
        r = requests.get(endpoint, timeout=10)
        r.raise_for_status()
        data = r.json()

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

    for item in data:
        if item['token'] == token:
            return item['rate']

    return None  # Return None if the token is not found




if __name__ == '__main__':
        get_price()
