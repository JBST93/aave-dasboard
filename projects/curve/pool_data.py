from flask import jsonify
import sys, os
import requests

import functools
import time
from sqlalchemy import desc, and_
from datetime import datetime


chains = ["ethereum","arbitrum","optimism","base","fraxtal"]

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(project_root)

from app import app, db

token = "CRV"
from instances.TokenData import TokenData
from instances.YieldRate import YieldRate

def get_supply():
    endpoint = "https://api.curve.fi/api/getCrvCircSupply"
    r = requests.get(endpoint)
    data = r.json()
    supply = data.get("data").get("crvCirculatingSupply")
    return float(supply)

def get_crvusd():
    endpoint_crvusd="https://api.curve.fi/v1/getCrvusdTotalSupply"
    r = requests.get(endpoint_crvusd)
    data = r.json()
    supply_crv_usd = data.get("data",{}).get("crvusdTotalSupply")
    print(supply_crv_usd)

def get_latest_token_data(token):
    """Fetch the latest token data from the database based on timestamp."""
    result = TokenData.query.filter_by(token=token).order_by(desc(TokenData.timestamp)).first()
    return float(result.price)

def get_volumes(chain):
    endpoint_volumes = f"https://api.curve.fi/v1/getVolumes/{chain}"
    r = requests.get(endpoint_volumes)
    data = r.json()
    return data.get("data",{}).get("pools",{})


@functools.cache
def get_pools():
    try:
        price = get_latest_token_data("CRV")
        supply_raw = get_supply()
        supply_usd = supply_raw * price
        data_list = []
        processed_count = 0
        skipped_count = 0

        for chain in chains:
            endpoint = f"https://api.curve.fi/v1/getPools/all/{chain}"
            try:
                r = requests.get(endpoint, timeout=30)
                r.raise_for_status()
                data = r.json()

                if "data" not in data or "poolData" not in data["data"]:
                    print(f"No pool data for {chain}")
                    continue

                pools = data["data"]["poolData"]
                print(f"Processing {len(pools)} pools for {chain}")

                volumes = get_volumes(chain)

                for pool in pools:
                    try:
                        address = pool.get("address")
                        tvl = pool.get("usdTotalExcludingBasePool", 0)
                        coins_info = pool.get("coins", [])
                        chain_name = pool.get("blockchainId", chain)
                        type_name = pool.get("assetTypeName", "Unknown")

                        # Normalize type names
                        if type_name == "usd":
                            type_name = "Stable Pool"
                        elif type_name == "eth":
                            type_name = "ETH Pool"
                        elif type_name == "btc":
                            type_name = "BTC Pool"
                        else:
                            type_name = "Other Pool"

                        # Handle gauge CRV APY
                        gaugeCrvApy = pool.get("gaugeCrvApy", [])
                        if isinstance(gaugeCrvApy, list) and len(gaugeCrvApy) > 0 and gaugeCrvApy[0] is not None:
                            reward_apy = round(float(gaugeCrvApy[0]), 2)
                        else:
                            reward_apy = 0

                        # Process coins
                        coins = []
                        if tvl > 1 and coins_info:
                            for coin in coins_info:
                                token = coin.get("symbol", "Unknown")
                                usd_price = float(coin.get("usdPrice", 0))
                                balance = float(coin.get("poolBalance", 0))
                                decimals = float(coin.get("decimals", 18))

                                balance_normalised = balance / 10**(decimals)
                                balance_normalised_usd = balance_normalised * usd_price
                                if tvl > 0:
                                    percent = round(float(balance_normalised_usd) / float(tvl) * 100, 2)
                                else:
                                    percent = 0
                                coins.append([token, balance_normalised_usd, percent])

                        # Get volume and base APY
                        volume = 0
                        base_apy = 0
                        if tvl > 1 and volumes:
                            for volume_data in volumes:
                                if volume_data.get("address") == address:
                                    volume = volume_data.get("volumeUSD", 0)
                                    base_apy = volume_data.get("latestDailyApyPcent", 0)
                                    break

                        apy = round((base_apy + reward_apy), 2)

                        # Only process pools with meaningful TVL and volume
                        if tvl > 1000 and volume > 100:  # Increased thresholds for better data quality
                            symbol = " / ".join([coin[0] for coin in coins]) if coins else "Unknown"

                            pool_data = {
                                "symbol": symbol,
                                "coins": coins,
                                "tvl": tvl,
                                "apy": apy,
                                "volume": volume,
                                "address": address,
                                "chain": chain_name.capitalize(),
                                "type": type_name,
                                "base_apy": base_apy,
                                "reward_apy": reward_apy
                            }

                            data_list.append(pool_data)

                            info = YieldRate(
                                market=symbol,
                                project="Curve",
                                information="Curve Finance Pool",
                                yield_rate_base=base_apy,
                                yield_rate_reward=reward_apy,
                                yield_token_reward="CRV",
                                tvl=tvl,
                                chain=chain_name.capitalize(),
                                type=type_name,
                                smart_contract=address,
                                timestamp=datetime.utcnow()
                            )
                            db.session.add(info)
                            processed_count += 1
                        else:
                            skipped_count += 1

                    except Exception as e:
                        print(f"Error processing pool {address}: {e}")
                        skipped_count += 1

                db.session.commit()
                print(f"Curve {chain}: {processed_count} pools processed, {skipped_count} skipped")

            except Exception as e:
                print(f"Error fetching pools for {chain}: {e}")

        sorted_data_list = sorted(data_list, key=lambda x: x['tvl'], reverse=True)

        result = {
            "name": "Curve Finance",
            "price": price,
            "supply": supply_usd,
            "pools": sorted_data_list,
            "total_processed": processed_count
        }

        return jsonify(result)

    except Exception as e:
        print(f"Error in get_pools: {e}")
        return jsonify({"error": str(e)})
# Run the Flask app
if __name__ == "__main__":
    with app.app_context():
        get_pools()
