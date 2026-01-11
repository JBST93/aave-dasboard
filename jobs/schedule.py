"""
Background job scheduler for fetching DeFi yield data.

Runs periodic jobs to fetch yield rates from various protocols
and update token price/supply data.
"""
import os
import sys
import logging

from apscheduler.schedulers.background import BlockingScheduler

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

# Protocol fetchers - only import what's actively used
from projects.aave.fetch_data import fetch_store_rates as aave
from projects.compound.fetch_rates import fetch_store_rates as compound
from projects.curve.fetch_store_data import fetch_store_data as curve
from projects.curve.fetch_store_data import get_crvusd as crv_usd
from projects.curve.pool_data import get_pools as curve_pools
from projects.gearbox.fetch_data import fetch_store_data as gearbox
from projects.morpho.fetch_data_morpho import fetch_data_metamorpho as morpho
from projects.pendle.fetch_data import fetch_data as pendle
from projects.spark.fetch_rates import get_all_data as spark
from projects.maker.get_data import get_data as maker
from projects.fx.fetch_data import fetch_store_data as fx
from projects.clearpool.fetch_data import fetch_store_rates as clearpool
from projects.lido.get_rate import get_data_steth as lido
from projects.rocketpool.fetch_data import get_data_reth as rocketpool
from projects.ethena.get_data import get_data as ethena
from projects.silo.fetch_data import fetch_store_rates as silo
from projects.stargate.get_data import get_data as stargate
from projects.paypal.get_data import get_supply as paypal
from projects.avax.get_data import get_data as avax
from projects.liquity.get_data import get_token as liquity
from projects.abracadabra.get_data import get_token as abra
from projects.ripple.get_data import token_data as ripple
from projects.uniswap.get_data import get_uniswap_pools as uniswap
from projects.venus.get_data import get_store_data as venus
from projects.maple.get_yield_info import fetch_store_rates as maple

from scripts.get_price_supply import get_price_supply

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

FETCH_INTERVAL_MINUTES = 30
STABLECOIN_INTERVAL_MINUTES = 60

sched = BlockingScheduler()

def log_and_execute(func, func_name):
    """Log execution of the given function with error handling."""
    try:
        func()  # Execute the function
        print(f"executed {func_name}")
    except Exception as e:
        logger.error(f"Error fetching {func_name} data: {e}")


def fetch_store_data():
    """Fetch data for all defined projects."""
    tasks = {
        "Aave": aave,
        "Compound": compound,
        "Curve": curve,
        "Curve Pools": curve_pools,
        "CurveUSD": crv_usd,
        "Gearbox": gearbox,
        "Morpho": morpho,
        "Pendle": pendle,
        "Spark": spark,
        "Maker": maker,
        "FX": fx,
        "Clearpool": clearpool,
        "Lido": lido,
        "RocketPool": rocketpool,
        "Ethena": ethena,
        "Silo": silo,
        "Stargate": stargate,
        "Paypal": paypal,
        "Avax": avax,
        "Liquity": liquity,
        "Abracadabra": abra,
        "Ripple": ripple,
        "Uniswap": uniswap,
        "Venus": venus,
        "Maple": maple,
    }

    with app.app_context():
        logger.info(f"Fetching Yields Data")
        for name, task in tasks.items():
            try:
                log_and_execute(task, name)
                print(f"executed {name}")
            except Exception as e:
                print(e)



def fetch_price_supply():
    with app.app_context():
        log_and_execute(get_price_supply, "Token Info")


sched.add_job(fetch_store_data, 'interval', minutes=FETCH_INTERVAL_MINUTES)
sched.add_job(get_price_supply, 'interval', minutes=30)

if __name__ == '__main__':

    fetch_store_data()
    fetch_price_supply()

    sched.start()
