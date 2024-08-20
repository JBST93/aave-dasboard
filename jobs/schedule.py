import os, sys
from apscheduler.schedulers.background import BlockingScheduler
from app import app
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from projects.aave.fetch_data import fetch_store_rates as aave
from projects.compound.fetch_rates import fetch_store_rates as compound
from projects.curve.fetch_store_data import fetch_store_data as curve
from projects.gearbox.fetch_data import fetch_store_data as gearbox
from projects.morpho.fetch_data_morpho import fetch_data_metamorpho as morpho
from projects.pendle.fetch_data import fetch_data as pendle
from projects.spark.fetch_rates import fetch_store_sparklend as spark
from projects.yearn.get_yearn_data import fetch_yearn as yearn
from projects.fx.fetch_data import fetch_store_data as fx
from projects.clearpool.fetch_data import fetch_store_rates as clearpool
from projects.lido.get_rate import get_data_steth as lido
from projects.rocketpool.fetch_data import get_data_reth as rocketpool


from scripts.get_price_supply import get_price_supply


from scripts.stablecoin_fetch import get_stablecoin_data as stablecoin

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

FETCH_INTERVAL_MINUTES = 30
STABLECOIN_INTERVAL_MINUTES = 60

sched = BlockingScheduler()

def log_and_execute(func, func_name):
    """Log execution of the given function with error handling."""
    try:
        logger.info(f"Fetching Data for {func_name}")
        func()
        logger.info(f"{func_name} Data fetched")
    except Exception as e:
        logger.error(f"Error fetching {func_name} data: {e}")


def fetch_store_data():
    """Fetch data for all defined projects."""
    tasks = {
        "Aave": aave,
        "Curve": curve,
        "Gearbox": gearbox,
        "Maker DSR": spark,
        "Compound": compound,
        "Morpho": morpho,
        "Yearn": yearn,
        "Pendle": pendle,
        "FX": fx,
        "Clearpool": clearpool,
        "Lido": lido,
        "RocketPool":rocketpool,
    }

    with app.app_context():
        for name, task in tasks.items():
            log_and_execute(task, name)


def fetch_price_supply():
    with app.app_context():
        log_and_execute(get_price_supply, "Token Info")


sched.add_job(fetch_store_data, 'interval', minutes=FETCH_INTERVAL_MINUTES)
sched.add_job(get_price_supply, 'interval', minutes=30)

if __name__ == '__main__':
    sched.start()
