from web3 import Web3
from dotenv import load_dotenv
import os
import sys
from datetime import datetime
# Ensure the root directory is in the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

load_dotenv(os.path.join(project_root, '.env'))

from app import app, db
from instances.YieldRate import YieldRate as Yield
from instances.TokenData import TokenData as Info
from scripts.utils import load_abi, insert_yield_db, get_curve_price
from utils.get_price import get_price
from utils.get_last_price_db import get_latest_price
from utils.get_infura import select_infura

provider_abi = load_abi("aave",'aave_abi.json')

gov_token = "AAVE"
gov_token_price = get_price("AAVE")
tot_supply=118250087,
circ_supply=118250087,

smart_contracts = [
        {
            "chain": "ethereum" ,
            "address": "0x7B4EB56E7CD4b454BA8ff71E4518426369a138a3",
            "version": "v3",
            "instance":"Main"
        },
        {
            "chain": "ethereum" ,
            "address": "0xa3206d66cF94AA1e93B21a9D8d409d6375309F4A",
            "version": "v3",
            "instance":"Lido"
        },
        {
            "chain": "ethereum" ,
            "address": "0x8Cb4b66f7B13F2Ae4D3c91338fC007dbF8C14208",
            "version": "v3",
            "instance": "EtherFi"
        },
        {
            "chain": "arbitrum" ,
            "address": "0x69FA688f1Dc47d4B5d8029D5a35FB7a548310654",
            "version": "v3",
            "instance":"Main"
        },
        {
            "chain": "optimism" ,
            "address": "0x69FA688f1Dc47d4B5d8029D5a35FB7a548310654",
            "version": "v3",
            "instance":"Main"
        },
        {
            "chain": "polygon" ,
            "address": "0x69FA688f1Dc47d4B5d8029D5a35FB7a548310654",
            "version": "v3",
            "instance":"Main"
        },
        {
            "chain": "fantom" ,
            "address": "0x69FA688f1Dc47d4B5d8029D5a35FB7a548310654",
            "version": "v3",
            "instance":"Main"
        },
        {
            "chain": "avalanche" ,
            "address": "0x69FA688f1Dc47d4B5d8029D5a35FB7a548310654",
            "version": "v3",
            "instance":"Main"
        },
        {
            "chain": "base" ,
            "address": "0x2d8A3C5677189723C4cB8873CfC9C8976FDF38Ac",
            "version": "v3",
            "instance":"Main"
        }
]

def token_data(total_lend_usd, total_borrowed_usd):
    tvl_usd = total_lend_usd - total_borrowed_usd

    info = Info(
        token=gov_token,
        price=gov_token_price,
        price_source="",
        tot_supply=tot_supply,
        circ_supply=circ_supply,
        tvl=tvl_usd,
        revenue=0,
        timestamp=datetime.utcnow()
    )
    db.session.add(info)
    db.session.commit()


def fetch_store_rates():
    total_lend_usd = 0
    total_borrowed_usd = 0

    for contract in smart_contracts:
        chain = contract['chain']
        address = contract['address']
        version = contract['version']
        instance = contract['instance']

        web3 = select_infura(chain)
        pool_contract = web3.eth.contract(address=address, abi=provider_abi)
        data = pool_contract.functions.getAllReservesTokens().call()

        information = f"{version} - {instance} instance"

        for item in data:
            try:
                token = item[0]
                contract = item[1]
                price = get_latest_price(token)

                reserve_data = pool_contract.functions.getReserveData(contract).call()

                apy_base = reserve_data[5] / 1e27 * 100  # Convert from Ray to percentage
                apy_base_formatted = round(apy_base, 2)

                lend_amount_raw = reserve_data[2]
                borrowed_amount_raw = reserve_data[3]+reserve_data[4]

                if token in ['USDC', 'pyUSD', 'USDT']:
                    lend_amount = lend_amount_raw / 1e6
                    borrowed_amount = borrowed_amount_raw /1e6
                elif token == "WBTC":
                    lend_amount = lend_amount_raw / 1e8
                    borrowed_amount = borrowed_amount_raw/1e8
                else:
                    lend_amount = lend_amount_raw / 1e18
                    borrowed_amount = borrowed_amount_raw / 1e18

                price = get_latest_price(token) or 0
                supply_amount_usd = lend_amount * price
                borrowed_amount_usd = borrowed_amount * price

                total_lend_usd += supply_amount_usd
                total_borrowed_usd += borrowed_amount_usd

                print(f"{token} - {information} - {supply_amount_usd}")
                contract_type = "Lending"

                data = Yield(
                    market=token,
                    project='Aave',
                    information=information,
                    chain=chain.capitalize(),
                    tvl=supply_amount_usd,
                    yield_rate_base=apy_base_formatted,
                    yield_rate_reward=None,
                    smart_contract=contract,
                    action='Lend',
                    type = contract_type,
                    timestamp=datetime.now()
                )

                db.session.add(data)
                print("ADDED TO DB")

            except Exception as e:
                print(f"Error fetching data for {token}: {e}")

        db.session.commit()
        print("COMMITED")

    token_data(total_lend_usd,total_borrowed_usd)
    print("ADDED TVL")

if __name__ == '__main__':
    with app.app_context():
        fetch_store_rates()
