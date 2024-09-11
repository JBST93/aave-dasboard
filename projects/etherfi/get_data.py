from dotenv import load_dotenv
import os, sys
from datetime import datetime

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)
load_dotenv(os.path.join(project_root, '.env'))

from app import app, db
from instances.YieldRate import YieldRate
from instances.TokenData import TokenData as Info
from scripts.utils import load_abi
from utils.get_price import get_price
from utils.get_infura import select_infura

provider_abi = load_abi("aave",'aave_abi.json')

tokens = [
  {
    "token": "weETH",
    "contract": "0xCd5fE23C85820F7B72D0926FC9b05b43E359b7ee",
    "chain": "ethereum",
    "decimals": 18,
    "total_supply": None,
    "abi": load_abi("etherfi",'ethfi_abi.json')
  },
  {
    "token": "eETH",
    "contract": "0xCd5fE23C85820F7B72D0926FC9b05b43E359b7ee",
    "chain": "ethereum",
    "decimals": 18,
    "total_supply": None,
    "abi": load_abi("etherfi",'ethfi_abi.json')
  },
  {
    "token": "ETHFI",
    "contract": "0xFe0c30065B384F05761f15d0CC899D4F9F9Cc0eB",
    "chain": "ethereum",
    "decimals": 18,
    "abi": load_abi("etherfi",'ethfi_abi.json')
  }
]

def get_data():
    with app.app_context():
        for token in tokens:
            try:
                web3 = select_infura(token["chain"])
                pool_contract = web3.eth.contract(address=token["contract"], abi=token["abi"])
                supply_raw = pool_contract.functions.totalSupply().call()
                supply = supply_raw / 10 ** token["decimals"]
                price = get_price(token["token"],token["contract"],token["chain"])

                info = Info(
                token=token["token"],
                price=price,
                price_source= "",
                tot_supply= float(supply),
                circ_supply= float(supply),
                timestamp=datetime.utcnow(),
                )
                db.session.add(info)
            except Exception as e:
                print(e)

    db.session.commit()





# Steps
# 3) Create Function to get data
# 4) Create function to upload to DB
