import requests
import os, sys
from dotenv import load_dotenv
import logging
import json

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(project_root)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


load_dotenv(os.path.join(project_root, '.env'))

from instances.YieldRate import YieldRate
from app import app, db

load_dotenv()

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
        logger.info("Sending request for pairs data")
        response = requests.post(url, json={'query': pairs_query})
        logger.info(f"Received response with status code: {response.status_code}")
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

        logger.info("Sending request for pairDayData")
        response = requests.post(url, json={'query': pair_day_data_query})
        logger.info(f"Received response with status code: {response.status_code}")
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
                    chain='Ethereum',  # Uniswap V2 is on Ethereum
                    tvl=reserve_usd,
                    yield_rate_base=yield_rate_base,
                    yield_rate_reward=yield_rate_reward,
                    total_yield=total_yield,
                    volume=volume,
                    smart_contract=pair_id,
                )

                db.session.add(data)

        db.session.commit()
        logger.info(f"Successfully processed and stored {len(pairs)} Uniswap pool data entries")

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
        get_uniswap_pools()
    print("Uniswap data fetching process completed")
