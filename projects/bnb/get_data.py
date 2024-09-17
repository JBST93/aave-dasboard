import requests, sys, os
from datetime import datetime

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

from app import app, db

from utils.get_price import get_price
from utils.get_infura import select_infura
from utils.load_abi import load_abi
from instances.TokenData import TokenData as Data

token = "BNB"
tokens = [
    {
        "name":"BTCB",
        "chain":"bsc",
        "address":"0x7130d2A12B9BCbFAe4f2634d864A1Ee1Ce3Ead9c",
        "abi":load_abi("bnb","abi_btcb.json"),
        "decimals":18
    },
     {
        "name":"BNB",
        "chain":"bsc",
        "address":"0xb8c77482e45f1f44de1745f52c74426c631bdd52",
        "abi": None,
        "decimals": 18
    }

]

def get_data():
    with app.app_context():
        for token in tokens:
            if token["name"] == "BNB":
                price = get_price(token["name"],token["address"],token["chain"])
                total_supply = 200000000
                circ_supply = 145887575
                tvl = 0
            else:
                price = get_price("BTC",token["address"],token["chain"])
                web3 = select_infura(token["chain"])
                contract = web3.eth.contract(address=token["address"], abi=token["abi"])
                supply_raw = contract.functions.totalSupply().call()
                total_supply = supply_raw / 10 ** token["decimals"]
                circ_supply = total_supply
                tvl = circ_supply*price


            data = Data (
                    token=token["name"],
                    price=price,
                    price_source= "",
                    tvl = tvl,
                    tot_supply= float(total_supply),
                    circ_supply= float(circ_supply),
                    timestamp=datetime.utcnow(),
                )

            db.session.add(data)

        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        get_data()
