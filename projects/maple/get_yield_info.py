import requests
import json
import os
import sys
from datetime import datetime
from decimal import Decimal, getcontext
from dotenv import load_dotenv

# Ensure the root directory is in the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

load_dotenv(os.path.join(project_root, '.env'))

from app import app, db
from instances.YieldRate import YieldRate as Yield
from instances.TokenData import TokenData as Info
from utils.get_price import get_price
from utils.get_last_price_db import get_latest_price

# Set high precision for calculations
getcontext().prec = 50

MAPLE_GRAPHQL_QUERY = {
    "operationName": "getLendData",
    "variables": {},
    "query": """
    query getLendData {
        poolV2S(where: {syrupRouter_not: null}) {
            id
            name
            assets
            strategiesDeployed
            principalOut
            collateralValue
            weeklyApy
            asset {
                id
                symbol
                decimals
                price
            }
        }
    }
    """
}

gov_token = "MPL"
gov_token_price = get_price("MPL")
tot_supply = 10000000  # 10M MPL tokens
circ_supply = 10000000

def fetch_syrup_apy_data():
    api_url = "https://api.maple.finance/v2/graphql"

    try:
        response = requests.post(
            api_url,
            json=MAPLE_GRAPHQL_QUERY,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (compatible; MapleAPY/1.0)"
            },
            timeout=15
        )

        if response.status_code == 200:
            data = response.json()

            if "errors" in data:
                print("GraphQL errors:")
                for error in data["errors"]:
                    print(f"  - {error}")
                return None

            if "data" in data:
                pools = data["data"].get("poolV2S", [])

                print(f"Found {len(pools)} Syrup pools")

                return {
                    "pools": pools,
                }

        else:

            return None

    except Exception as e:
        print(f"Request failed: {e}")
        return None

def calculate_syrup_metrics(pool_data, drips_yield_boost):

    pool = pool_data

    # Asset info
    asset_decimals = int(pool["asset"]["decimals"])
    price_decimals = 8
    asset_symbol = pool["asset"]["symbol"]

    # Price calculation
    token_price = Decimal(pool["asset"]["price"]) / Decimal(10) ** price_decimals

    # Total assets calculation (sum of all pool components)
    total_assets = (
        Decimal(pool.get("assets", 0)) +
        Decimal(pool.get("strategiesDeployed", 0)) +
        Decimal(pool.get("principalOut", 0)) +
        Decimal(pool.get("collateralValue", 0))
    )

    # TVL in USD
    tvl_usd = float(
        (total_assets * token_price) / (Decimal(10) ** asset_decimals)
    )

    # APY calculations
    weekly_apy_raw = Decimal(pool.get("weeklyApy", 0))
    apy_base = float(weekly_apy_raw / (Decimal(10) ** 28))

    drips_boost_raw = 0
    apy_reward = 0

    return {
        "pool_id": pool["id"],
        "name": pool["name"],
        "asset_symbol": asset_symbol,
        "asset_address": pool["asset"]["id"],
        "tvl_usd": tvl_usd,
        "apy_base": apy_base,
        "apy_reward": apy_reward,
        "apy_total": apy_base + apy_reward,
        "token_price": float(token_price),
        "raw_weekly_apy": str(weekly_apy_raw),
        "raw_drips_boost": str(drips_boost_raw)
    }

def token_data(total_tvl_usd):
    """
    Store Maple token data in the database
    """
    info = Info(
        token=gov_token,
        price=gov_token_price,
        price_source="",
        tot_supply=tot_supply,
        circ_supply=circ_supply,
        tvl=total_tvl_usd,
        revenue=0,
        timestamp=datetime.utcnow()
    )
    db.session.add(info)
    db.session.commit()

def fetch_store_rates():
    """
    Main function to fetch and store Maple Syrup rates in the database
    """
    print("MAPLE SYRUP APY - FETCHING AND STORING RATES")
    print("=" * 50)

    total_tvl_usd = 0
    processed_count = 0
    skipped_count = 0

    # Fetch data using DeFiLlama's method
    syrup_data = fetch_syrup_apy_data()

    if not syrup_data:
        print("Failed to fetch Syrup data")
        return

    pools = syrup_data["pools"]
    syrup_globals = syrup_data["syrup_globals"]
    drips_yield_boost = syrup_globals.get("dripsYieldBoost", 0)

    print(f"\nProcessing {len(pools)} Syrup pools...")
    print(f"Global drips yield boost: {drips_yield_boost}")

    for pool_data in pools:
        try:
            metrics = calculate_syrup_metrics(pool_data, drips_yield_boost)

            # Skip pools with minimal TVL (< $1000)
            if metrics['tvl_usd'] < 1000:
                skipped_count += 1
                continue

            total_tvl_usd += metrics['tvl_usd']

            # Format APY values
            apy_base_formatted = round(metrics['apy_base'], 2)
            apy_reward_formatted = round(metrics['apy_reward'], 2) if metrics['apy_reward'] > 0 else None

            # Information string matching Aave format
            information = f"Syrup - {metrics['name']}"

            # Create yield data entry
            yield_data = Yield(
                market=metrics['asset_symbol'],
                project='Maple',
                information=information,
                chain='Ethereum',  # Maple is primarily on Ethereum
                tvl=metrics['tvl_usd'],
                yield_rate_base=apy_base_formatted,
                yield_rate_reward=apy_reward_formatted,
                smart_contract=metrics['asset_address'],
                action='Lend',
                type='Lending',
                timestamp=datetime.now()
            )

            db.session.add(yield_data)
            processed_count += 1


        except Exception as e:
            print(f"Error processing pool {pool_data.get('name', 'Unknown')}: {e}")
            skipped_count += 1

    try:
        db.session.commit()
        token_data(total_tvl_usd)

    except Exception as e:
        print(f"Error committing to database: {e}")
        db.session.rollback()

    # Summary


    if processed_count > 0:
        print(f"\n🎉 SUCCESS! Stored Maple Syrup yield data:")
        print("  Base APY = weeklyApy ÷ 10^28")
        print("  Reward APY = dripsYieldBoost ÷ 10^4")
        print("  Total APY = Base APY + Reward APY")
    else:
        print("\n❌ No pools processed")

if __name__ == '__main__':
    with app.app_context():
        fetch_store_rates()
