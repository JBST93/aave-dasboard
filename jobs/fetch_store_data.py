import os, sys
from apscheduler.schedulers.background import BackgroundScheduler


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))


from aave.fetch_data_aavev3 import fetch_store_rates as aave
from curve.fetch_store_data import fetch_store_data as curve
from gearbox.fetch_data import fetch_store_rates as gearbox

def fetch_store_data():
    print("Fetching Data")
    aave()
    curve()
    gearbox()
    print ("Data fetched")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_store_data, 'interval', minutes=30, misfire_grace_time=3600)
    scheduler.start()
