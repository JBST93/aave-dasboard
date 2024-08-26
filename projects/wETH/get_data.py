from web3 import Web3
from dotenv import load_dotenv
import os
import sys
from datetime import datetime

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

load_dotenv(os.path.join(project_root, '.env'))

from app import app, db
from utils.get_infura import select_infura
from instances.TokenData import TokenData as Info
from utils.get_price import get_price
from scripts.utils import load_abi

token = "wETH"
contract_address = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
chain = "ethereum"
decimals = 18
provider_abi = load_abi("wETH",'weth_abi.json')
price = get_price(token,contract_address,chain)

def token_data():
    with app.app_context():
        web3 = select_infura(chain)
        pool_contract = web3.eth.contract(address=contract_address, abi=provider_abi)
        totalSupply_raw = pool_contract.functions.totalSupply().call()
        totalSupply = totalSupply_raw / 10**decimals
        totalSupply_usd = totalSupply * price
        print(totalSupply)
        print(totalSupply_usd)


        info = Info(
            token=token,
            price=price,
            price_source="",
            tot_supply=totalSupply,
            circ_supply=totalSupply,
            tvl=0,
            revenue=0,
            timestamp=datetime.utcnow()
        )
        db.session.add(info)
        db.session.commit()
