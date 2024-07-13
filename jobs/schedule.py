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


# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def fetch_store_data():
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

    logger.info("Data fetching completed")

sched.start()
