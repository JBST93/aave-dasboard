import requests
from datetime import datetime
import sys, os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from app import app, db
from instances.MoneyMarketRate import MoneyMarketRate

# Documentation: https://docs.yearn.fi/developers/v2/yearn-api#api-schema
api_url = "https://api.yexporter.io/v1/chains/1/vaults/all"

r = requests.get(api_url)
data = r.json()

def fetch_yearn():
    if r.status_code == 200:
        with app.app_context():
            try:

                for vault in data:
                    name = vault["name"]
                    tvl = vault["tvl"]["tvl"]
                    apy = vault["apy"]["net_apy"]*100
                    token_deposit = vault["token"]["symbol"]
                    contract_address=vault["address"]
                    if len(token_deposit) < 6 and tvl and tvl > 0:

                        rate = MoneyMarketRate(
                                                token=token_deposit,
                                                protocol="Yearn",
                                                liquidity_rate=apy,
                                                liquidity_reward_rate=None,
                                                chain="Ethereum",
                                                borrow_rate=0,
                                                collateral= name,
                                                tvl=tvl,
                                                timestamp=datetime.utcnow(),
                                            )

                        db.session.add(rate)
                        db.session.commit()

            except Exception as e:
                    logger.error(f"Error processing market data: {e}")
    else:
        logger.error(f"Query failed to run with a {r.status_code}.")


if __name__ == '__main__':
    fetch_yearn()
