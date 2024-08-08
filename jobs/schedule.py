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

from scripts.get_price_supply import get_price_supply


from scripts.stablecoin_fetch import get_stablecoin_data as stablecoin

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sched = BlockingScheduler()

def log_and_execute(func, func_name):
    try:
        logger.info(f"Fetching Data for {func_name}")
        func()
        logger.info(f"{func_name} Data fetched")
    except Exception as e:
        logger.error(f"Error fetching {func_name} data: {e}")

def fetch_store_data():
    with app.app_context():
        try:
            logger.info("Fetching Data for Aave")
            aave()
            logger.info("Aave Data fetched")
        except Exception as e:
            logger.error(f"Error fetching Aave data: {e}")

        try:
            logger.info("Fetching Data for Curve")
            curve()
            logger.info("Curve Data fetched")
        except Exception as e:
            logger.error(f"Error fetching Curve data: {e}")

        try:
            logger.info("Fetching Data for Gearbox")
            gearbox()
            logger.info("Gearbox Data fetched")
        except Exception as e:
            logger.error(f"Error fetching Gearbox data: {e}")

        try:
            logger.info("Fetching Data for Maker DSR")
            spark()
            logger.info("Maker DSR Data fetched")
        except Exception as e:
            logger.error(f"Error fetching Maker DSR data: {e}")

        try:
            logger.info("Fetching Data for Compound")
            compound()
            logger.info("Compound Data fetched")
        except Exception as e:
            logger.error(f"Error fetching Compound data: {e}")

        try:
            logger.info("Fetching Data for Morpho")
            morpho()
            logger.info("Morpho Data fetched")
        except Exception as e:
            logger.error(f"Error fetching Morpho data: {e}")

        try:
            logger.info("Fetching Data for Yearn")
            yearn()
            logger.info("Morpho Data fetched")
        except Exception as e:
            logger.error(f"Error fetching yearn data: {e}")

        try:
            logger.info("Fetching Data for Pendle")
            pendle()
            logger.info("Pendle Data fetched")
        except Exception as e:
            logger.error(f"Error fetching yearn data: {e}")

        try:
            logger.info("Fetching Data for FX")
            fx()
            logger.info("FX Data fetched")
        except Exception as e:
            logger.error(f"Error fetching yearn data: {e}")

        logger.info("Data fetching completed")

sched.add_job(fetch_store_data, 'interval', minutes=30)

# def get_stable_data():
#     with app.app_context():
#         try:
#             logger.info("Fetching Stablecoin Data")
#             stablecoin()
#             logger.info("Stablecoin Data fetched")
#         except Exception as e:
#             logger.error(f"Error fetching Stablecoin data: {e}")

# sched.add_job(get_stable_data, 'interval', minutes=60)

def fetch_price_supply():
    with app.app_context():
        log_and_execute(get_price_supply, "Token Info")
        print("DONE")

sched.add_job(get_price_supply, 'interval', minutes=2)

if __name__ == '__main__':
    sched.start()
