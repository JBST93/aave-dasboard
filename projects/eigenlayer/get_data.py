import requests
import os, sys


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

from app import app, db
from scripts.utils import load_abi
from utils.get_price import get_price
from instances.TokenData import TokenData as Data

# API documentation: https://docs.eigenexplorer.com/api-reference/endpoint/historical/retrieve-historical-tvl

endpoint = "https://api.eigenexplorer.com/metrics"

r = requests.get(endpoint)
data = r.json()

# TVL in ETH
tvl_eth = data.get("tvl")
price_ETH = get_price("ETH","NA","NA")
tvl_usd = tvl_eth * price_ETH
