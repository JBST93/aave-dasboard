import requests
import os, sys
from datetime import datetime

# Ensure the root directory is in the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.append(project_root)

from app import app, db
from instances.TokenData import TokenData as Info
from utils.get_price import get_price
from utils.get_infura import select_infura
from utils.load_abi import load_abi

# Note:
# - Centralised (Coinbase)



tokens = [
    {
        "name":"cbBTC",
        "address":"0xcbB7C0000aB88B473b1f5aFd9ef808440eed33Bf",
        "chain":"ethereum",
        "decimals":8,
        "abi":""
    },
    {
        "name":"cbBTC",
        "address":"0xcbB7C0000aB88B473b1f5aFd9ef808440eed33Bf",
        "chain":"base",
        "decimals":8,
        "abi":""
    }
]

abi = load_abi("Coinbase/cbBTC",'abi.json')


def token_data():
    with app.app_context():
        price = get_price("cbBTC",tokens[0].get("address",{}),tokens[0].get("chain"))
        circ_supply_tot = 0
        for token in tokens:
            web3 = select_infura(token["chain"])
            pool_contract = web3.eth.contract(address=token["address"], abi=abi)
            circ_supply_raw = pool_contract.functions.totalSupply().call()
            circ_supply = circ_supply_raw / 10**token["decimals"]
            circ_supply_tot += circ_supply

        tvl = circ_supply_tot * price

        info = Info(
            token=token,
            price=price,
            price_source="",
            tot_supply=circ_supply_tot,
            circ_supply=circ_supply_tot,
            tvl=tvl,
            revenue=0,
            timestamp=datetime.utcnow()
        )
        db.session.add(info)
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        token_data()
