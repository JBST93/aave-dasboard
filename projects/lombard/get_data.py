import os, sys
from datetime import datetime

# Ensure the root directory is in the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

from app import app, db
from instances.TokenData import TokenData as Info
from utils.get_price import get_price
from utils.get_infura import select_infura
from utils.load_abi import load_abi


tokens = [
    {
        "name":"LBTC",
        "decimals":8,
        "chain":"ethereum",
        "address":"0x8236a87084f8B84306f72007F36F2618A5634494",
        "abi":load_abi("lombard",'abi.json')
    },
]


def get_token_data():
    with app.app_context():
        for token in tokens:
            price = get_price(token["name"],token["address"],token["chain"])
            web3 = select_infura(token["chain"])
            pool_contract = web3.eth.contract(address=token["address"], abi=token["abi"])
            circ_supply_raw = pool_contract.functions.totalSupply().call()
            circ_supply = circ_supply_raw / 10**token["decimals"]
            tvl = circ_supply*price

            info = Info(
                token=token["name"],
                price=price,
                price_source="",
                tot_supply=circ_supply,
                circ_supply=circ_supply,
                tvl=tvl,
                revenue=0,
                timestamp=datetime.utcnow()
            )
        db.session.add(info)
        db.session.commit()


if __name__ == '__main__':
    with app.app_context():
        get_token_data()
