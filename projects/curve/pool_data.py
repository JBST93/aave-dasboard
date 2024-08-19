from flask import jsonify
import sys, os
import requests

import functools
import time

chains = ["ethereum","arbitrum"]

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(project_root)

from app import app

def get_crvusd():
    endpoint_crvusd="https://api.curve.fi/v1/getCrvusdTotalSupply"
    r = requests.get(endpoint_crvusd)
    data = r.json()
    supply_crv_usd = data.get("data",{}).get("crvusdTotalSupply")
    print(supply_crv_usd)



def get_volumes(chain):
    endpoint_volumes = f"https://api.curve.fi/v1/getVolumes/{chain}"
    r = requests.get(endpoint_volumes)
    data = r.json()
    return data.get("data",{}).get("pools",{})


@functools.cache
def get_pools():
    data_list = []

    for chain in chains:

        endpoint = f"https://api.curve.fi/v1/getPools/all/{chain}"
        r = requests.get(endpoint)
        data = r.json()

        pools = data.get("data",{}).get("poolData",{})
        count_pools = len(pools)
        total_tvl = 0

        volumes = get_volumes(chain)

        for pool in pools:
            address = pool.get("address")
            name = pool.get("name")
            symbol = pool.get("symbol")
            tvl_with_basepool = pool.get("totalSupply")
            tvl = pool.get("usdTotalExcludingBasePool")
            total_tvl += tvl
            coins_info = pool.get("coins")
            chain = pool.get("blockchainId")
            type = pool.get("assetTypeName")
            if type == "usd":
                type = "Stable Pool"
            elif type =="eth":
                type="ETH Pool"
            elif type =="btc":
                type ="BTC Pool"
            else:
                type ="Unknown"

            gaugeCrvApy = pool.get("gaugeCrvApy",[]) or []
            if isinstance(gaugeCrvApy, list) and len(gaugeCrvApy) > 0 and gaugeCrvApy[0] is not None:
                reward_apy = round(float(gaugeCrvApy[0]),2)
            else:
                reward_apy = 0

            coins = []
            if tvl > 1:
                for coin in coins_info:
                    token = coin.get("symbol")

                    usd_price = float(coin.get("usdPrice") or 0)
                    balance = float(coin.get("poolBalance", 0))
                    decimals = float(coin.get("decimals", 18))

                    balance_normalised = balance / 10**(decimals)
                    balance_normalised_usd = balance_normalised * usd_price
                    if tvl > 0:
                        percent = round(float(balance_normalised_usd) / float(tvl) * 100, 2)
                    else:
                        percent = 0
                    coins.append([token,balance_normalised_usd, percent])

            if tvl > 1:
                for volume_data in volumes:
                    if volume_data.get("address") == address:
                        volume = volume_data.get("volumeUSD", 0)
                        base_apy = volume_data.get("latestDailyApyPcent",0)
                        break
            apy = round((base_apy + reward_apy),2)

            if tvl > 1 and volume > 1:
                data = {
                    "symbol":symbol,
                    "coins":coins,
                    "tvl":tvl,
                    "apy":apy,
                    "volume":volume,
                    "address":address,
                    "chain":chain.capitalize(),
                    "type":type,
                    "base_apy":base_apy,
                    "reward_apy":reward_apy
                }

                data_list.append(data)

    sorted_data_list = sorted(data_list, key=lambda x: x['tvl'], reverse=True)
    crv_usd_supply = get_crvusd()
    print(crv_usd_supply)

    return jsonify(sorted_data_list)



# Run the Flask app
if __name__ == "__main__":
    with app.app_context():
        print(get_crvusd)
