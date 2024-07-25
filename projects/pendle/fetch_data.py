import requests
from datetime import datetime
import sys, os
import logging

# Ensure the root directory is in the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(project_root)

from app import app, db
from instances.YieldRate import YieldRate as Data

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Documentation: https://api-v2.pendle.finance/core/docs#/Markets/MarketsController_marketApyHistory

chain_ids = [1,10,42161,56, 5000]

# Dictionary to map chain IDs to names
chain_mapping = {
    1: "Ethereum",
    10: "Optimism",
    42161: "Arbitrum",
    56: "Binance",
    5000: "Mantle"
}

def fetch_data():
    for chain_id in chain_ids:
        try:
            api = f"https://api-v2.pendle.finance/core/v1/{chain_id}/markets?order_by=name%3A1&skip=0&limit=100&is_expired=false&select=all&is_active=true"
            r = requests.get(api)
            r.raise_for_status()
            data = r.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch data for chain {chain_id}: {e}")
            continue

        results = data.get("results", [])

        for result in results:
            address = result["address"]
            yield_api = f"https://api-v2.pendle.finance/core/v2/{chain_id}/markets/{address}/data"

            try:
                r = requests.get(yield_api)
                r.raise_for_status()
                dataset = r.json()
            except requests.exceptions.RequestException as e:
                logger.error(f"Failed to fetch yield data for address {address} on chain {chain_id}: {e}")
                continue

            name = result.get('pt', {}).get('name', 'N/A')
            maturity = result.get("expiry", {})
            datetime_obj = datetime.fromisoformat(maturity.replace("Z", "+00:00"))
            formatted_maturity = datetime_obj.strftime("%Y-%m-%d")

            token = result.get("accountingAsset", {}).get("symbol", 'N/A')
            tvl = result.get('liquidity', {}).get('usd', "0")
            chain = chain_mapping.get(chain_id, "Unknown")

            apy_base = result.get("impliedApy", "0")
            apy_reward = result.get("pendleApy", "0")
            apy_swap = result.get("aggregatedApy", "0")
            apy_lp = float(apy_swap) + float(apy_reward)

            try:
                token_pt = f"{token} (Buy PT) - {formatted_maturity}"
                token_lp = f"{token} (LP) - {formatted_maturity}"


                deposit = Data(
                    market=token,
                    project="Pendle",
                    information=token_pt,
                    yield_rate_base=float(apy_base)*100,
                    yield_rate_reward=None,
                    yield_token_reward=None,
                    tvl=tvl,
                    chain=chain,
                    type="Interest Rate Derivative",
                    smart_contract=address,
                    timestamp=datetime.utcnow()
                )
                db.session.add(deposit)

                lp = Data(
                    market=token,
                    project="Pendle",
                    information=token_lp,
                    yield_rate_base=float(apy_base)*100,
                    yield_rate_reward=apy_lp*100,
                    yield_token_reward=None,
                    tvl=tvl,
                    chain=chain,
                    type="LP - Liquidity Provision",
                    smart_contract=address,
                    timestamp=datetime.utcnow()
                )

                db.session.add(lp)

                db.session.commit()

            except Exception as e:
                logger.error(f"Failed to add data for {token} on chain {chain}: {e}")
                db.session.rollback()

if __name__ == '__main__':
    with app.app_context():
        fetch_data()
