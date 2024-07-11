import os, sys
from apscheduler.schedulers.background import BlockingScheduler
from app import app


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from aave.fetch_data_aavev3 import fetch_store_rates as aave
from curve.fetch_store_data import fetch_store_data as curve
from gearbox.fetch_data import fetch_store_rates as gearbox
from spark.fetch_rates import fetch_store_rates as maker_dsr =

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=5)
def fetch_store_data():
    print("Fetching Data")
    aave()
    curve()
    gearbox()
    maker_dsr()
    print ("Data fetched")

sched.start()
