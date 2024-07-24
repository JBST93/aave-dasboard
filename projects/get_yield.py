import os, sys
from apscheduler.schedulers.background import BlockingScheduler
from app import app

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from projects.aave.fetch_data import fetch_store_rates as aave
from projects.compound.fetch_rates import fetch_store_rates as compound
from projects.curve.fetch_store_data import fetch_store_data as curve
from projects.gearbox.fetch_data import fetch_store_data as gearbox
from projects.morpho.fetch_data_morpho import fetch_data_metamorpho as morpho
from projects.pendle.fetch_data import fetch_data as gearbox
from projects.spark.fetch_rates import fetch_store_sparklend as spark
from projects.yearn.get_yearn_data import fetch_yearn as yearn
