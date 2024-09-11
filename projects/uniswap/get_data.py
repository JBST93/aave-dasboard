import requests
import os, sys
from dotenv import load_dotenv
import logging
import json
from datetime import datetime

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(project_root)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


load_dotenv(os.path.join(project_root, '.env'))
load_dotenv()


from app import app, db
from instances.YieldRate import YieldRate


def get_uniswap_pools_v3():

    base_url = "https://gateway.thegraph.com"
    api_key = os.getenv("THEGRAPH_API_KEY")
    subgraph_id = "5zvR82QoaXYFyDEKLZ9t6v9adgnptxYpKpSbxtgVENFV"

    if not api_key:
        logger.error("Error: API key not found. Please set the THEGRAPH_API_KEY environment variable.")
        return None

    url = f"{base_url}/api/{api_key}/subgraphs/id/{subgraph_id}"

    pools_query = """
    {
      pools(first: 1000, orderBy: totalValueLockedUSD, orderDirection: desc) {
        id
        token0 {
          symbol
          decimals
        }
        token1 {
          symbol
          decimals
        }
        totalValueLockedToken0
        totalValueLockedToken1
        totalValueLockedUSD
        feeTier
        sqrtPrice
        tick
        liquidity
      }
    }
    """

    try:
        response = requests.post(url, json={'query': pools_query})
        response.raise_for_status()
        pools_data = response.json()

        if 'data' not in pools_data or 'pools' not in pools_data['data']:
            logger.error("Unexpected API response structure for pools data")
            return None

        pools = pools_data['data']['pools']
        pool_ids = [pool['id'] for pool in pools]

        # Query for poolDayData with a 7-day lookback
        pool_day_data_query = f"""
        {{
          poolDayDatas(first: 1000, orderBy: date, orderDirection: desc, where: {{ pool_in: {json.dumps(pool_ids)} }}) {{
            pool {{
              id
            }}
            volumeUSD
            date
          }}
        }}
        """

        response = requests.post(url, json={'query': pool_day_data_query})
        response.raise_for_status()
        pool_day_data = response.json()

        if 'data' not in pool_day_data or 'poolDayDatas' not in pool_day_data['data']:
            logger.error("Unexpected API response structure for poolDayData")
            return None

        # Create a dictionary to store the latest volumeUSD for each pool
        volume_dict = {}
        for data in pool_day_data['data']['poolDayDatas']:
            pool_id = data['pool']['id']
            if pool_id not in volume_dict:
                volume_dict[pool_id] = 0
            volume_dict[pool_id] += float(data['volumeUSD'])

        # Process pools data
        results = []
        for pool in pools:
            pool_id = pool['id']
            volume = volume_dict.get(pool_id, 0)
            tvl = float(pool['totalValueLockedUSD'])

            if tvl > 100000 and tvl < 1e12:  # Apply TVL filters
                fee_tier = int(pool['feeTier']) / 10000  # Convert fee tier to basis points
                fees_24h = volume * (fee_tier / 10000) / 7  # Adjust for 7-day volume
                yield_rate_base = (fees_24h / tvl) * 365 * 100 if tvl > 0 else 0

                results.append({
                    'pair': f"{pool['token0']['symbol']} / {pool['token1']['symbol']}",
                    'tvl': tvl,
                    'volume': volume / 7,  # Adjust for daily average
                    'apy': yield_rate_base,
                    'fee_tier': fee_tier / 100  # Convert basis points to percentage
                })

        # Sort results by TVL in descending order
        results.sort(key=lambda x: x['tvl'], reverse=True)

        # Print results
        print("\nToken0/Token1 - TVL - Volume - APY - Fee Tier")
        print("-----------------------------------------------")
        for result in results[:100]:  # Limit to top 100 pools
            print(f"{result['pair']} -- ${result['tvl']:,.2f} - ${result['volume']:,.2f} - {result['apy']:.2f}% - {result['fee_tier']:.2f}%")

        return results

    except requests.exceptions.RequestException as e:
        logger.error(f"Error making request: {e}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON: {e}")
        logger.error(f"Raw response content: {response.text}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return None

def get_uniswap_pools():
    base_url = "https://gateway.thegraph.com"
    api_key = os.getenv("THEGRAPH_API_KEY")
    subgraph_id = "EYCKATKGBKLWvSfwvBjzfCBmGwYNdVkduYXVivCsLRFu"

    if not api_key:
        logger.error("Error: API key not found. Please set the THEGRAPH_API_KEY environment variable.")
        return None

    url = f"{base_url}/api/{api_key}/subgraphs/id/{subgraph_id}"

    pairs_query = """
    {
      pairs(first: 1000, orderBy: reserveUSD, orderDirection: desc) {
        id
        token0 {
          symbol
        }
        token1 {
          symbol
        }
        reserve0
        reserve1
        reserveUSD
        txCount
      }
    }
    """

    try:
        response = requests.post(url, json={'query': pairs_query})
        response.raise_for_status()
        pairs_data = response.json()

        if 'data' not in pairs_data or 'pairs' not in pairs_data['data']:
            logger.error("Unexpected API response structure for pairs data")
            return None

        pairs = pairs_data['data']['pairs']
        pair_ids = [pair['id'] for pair in pairs]

        # Query for pairDayData
        pair_day_data_query = f"""
        {{
          pairDayDatas(first: 1000, orderBy: date, orderDirection: desc, where: {{ pairAddress_in: {json.dumps(pair_ids)} }}) {{
            pairAddress
            dailyVolumeUSD
            date
          }}
        }}
        """

        response = requests.post(url, json={'query': pair_day_data_query})
        response.raise_for_status()
        pair_day_data = response.json()

        if 'data' not in pair_day_data or 'pairDayDatas' not in pair_day_data['data']:
            logger.error("Unexpected API response structure for pairDayData")
            return None

        # Create a dictionary to store the latest dailyVolumeUSD for each pair
        volume_dict = {}
        for data in pair_day_data['data']['pairDayDatas']:
            if data['pairAddress'] not in volume_dict:
                volume_dict[data['pairAddress']] = float(data['dailyVolumeUSD'])

        # Process pairs data
        processed_pairs = []
        for pair in pairs:
            pair_id = pair['id']
            volume = volume_dict.get(pair_id, 0)  # Get volume from the volume_dict, default to 0 if not found
            reserve_usd = float(pair['reserveUSD'])

            if reserve_usd < 1e12 and volume > 1000:  # Apply filters
                fees_24h = volume * 0.003  # 0.3% fee
                yield_rate_base = (fees_24h / reserve_usd) * 365 * 100 if reserve_usd > 0 else 0

                yield_rate_reward = 0
                total_yield = yield_rate_base + yield_rate_reward

                data = YieldRate(
                    market=f"{pair['token0']['symbol']} / {pair['token1']['symbol']}",
                    project='Uniswap v2',
                    chain='Ethereum',
                    tvl=reserve_usd,
                    yield_rate_base=yield_rate_base,
                    yield_rate_reward=yield_rate_reward,
                    smart_contract=pair_id,
                    type='LP',
                    timestamp=datetime.now()
                )

                db.session.add(data)

        db.session.commit()

    except requests.exceptions.RequestException as e:
        logger.error(f"Error making request: {e}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON: {e}")
        logger.error(f"Raw response content: {response.text}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return None

if __name__ == "__main__":
    with app.app_context():
        get_uniswap_pools_v3()

with app.app_context():
    get_uniswap_pools_v3()
