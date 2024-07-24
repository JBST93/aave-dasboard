import os, sys
from apscheduler.schedulers.background import BlockingScheduler
from app import app
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from aave.fetch_data_aavev3 import fetch_store_rates as aave
from curve.fetch_store_data import fetch_store_data as curve
from gearbox.fetch_data import fetch_store_rates as gearbox
from spark.fetch_rates import fetch_store_rates as maker_dsr
from compound.fetch_rates import fetch_store_rates as compound
from morpho.fetch_data_morpho import fetch_data as morpho
from scripts.stablecoin_fetch import get_stablecoin_data as stablecoin
from yearn.get_yearn_data import fetch_yearn as yearn
from pendle.fetch_data import fetch_data as pendle

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sched = BlockingScheduler()

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
            maker_dsr()
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
            logger.info("Morpho Data fetched")
        except Exception as e:
            logger.error(f"Error fetching yearn data: {e}")

        logger.info("Data fetching completed")

sched.add_job(fetch_store_data, 'interval', minutes=10)

def get_stable_data():
    with app.app_context():
        try:
            logger.info("Fetching Stablecoin Data")
            stablecoin()
            logger.info("Stablecoin Data fetched")
        except Exception as e:
            logger.error(f"Error fetching Stablecoin data: {e}")

sched.add_job(get_stable_data, 'interval', minutes=60)

if __name__ == '__main__':
    sched.start()
