import requests
import time
from datetime import datetime
import os, sys
from dotenv import load_dotenv


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

load_dotenv(os.path.join(project_root, '.env'))

from app import app, db
from instances.Stablecoin import Stablecoin

etherscan_key = os.getenv('ETHERSCAN_KEY')


tether_info = {
        "company": "Tether",
        "token": "USDC",
        "url": "https://app.tether.to/transparency.json",
        "query":"[data_formatted][name] &total_liabilities"
        }

circle_info = {
        "company": "Circle",
        "token":"USDC",
        "url": "https://api.circle.com/v1/stablecoins",
        "query":"api"
        }

list_chain = [
    {
        "entity": "Aave",
        "token":"GHO",
        "contract": "0x40d16fc0246ad3160ccc09b8d0d3a2cd28ae6c2f",
        "decimals": 18,
        "info":"decentralised",
        "chain":"ethereum",
        "pegged_against":"USD"
    },
     {
        "entity":"Maker",
        "token":"DAI",
        "contract": "0x6b175474e89094c44da98b954eedeac495271d0f",
        "decimals": 18,
        "info":"decentralised",
        "chain":"ethereum",
        "pegged_against":"USD"

    },
    {
        "entity":"Frax Finance",
        "token":"FRAX",
        "contract":"0xa0d69e286b938e21cbf7e51d71f6a4c8918f482f",
        "decimals": 18,
        "info":"decentralised",
        "chain":"ethereum",
        "pegged_against":"USD"
    },
    {
        "entity":"Frax Finance",
        "token":"FRAX",
        "contract": "0x853d955acef822db058eb8505911ed77f175b99e",
        "decimals": 18,
        "info":"decentralised",
        "chain":"ethereum",
        "pegged_against":"USD"
    },
    {
        "entity":"Synthetix",
        "token":"sUSD",
        "contract":"0x57ab1ec28d129707052df4df418d58a2d46d5f51",
        "info":"decentralised",
        "decimals":18,
        "chain":"ethereum",
        "pegged_against":"USD",

    },
    {
        "entity":"Montain Protocol",
        "token":"USDM",
        "contract":"0x59D9356E565Ab3A36dD77763Fc0d87fEaf85508C",
        "info":"decentralised",
        "decimals":18,
        "chain":"ethereum",
        "pegged_against":"USD",

    },
     {
        "entity":"Abracadabra",
        "token":"MIM",
        "contract":"0x99d8a9c45b2eca8864373a26d1459e3dff1e17f3",
        "info":"decentralised",
        "decimals":18,
        "chain":"ethereum",
        "pegged_against":"USD",

    },

    {
        "entity":"Ethena",
        "token":"USDe",
        "contract": "0x4c9edd5852cd905f086c759e8383e09bff1e68b3",
        "decimals": 18,
        "info":"decentralised",
        "chain":"ethereum",
        "query": "chain",
        "pegged_against":"USD"

    },
    {
        "entity":"Inverse Finance",
        "token":"DOLA",
        "contract": "0x865377367054516e17014ccded1e7d814edc9ce4",
        "decimals": 18,
        "info":"decentralised",
        "chain":"ethereum",
        "query": "chain",
        "pegged_against":"USD"
    },
    {
        "entity":"Alchemix",
        "token":"alUSD",
        "contract": "0xbc6da0fe9ad5f3b0d58160288917aa56653660e9",
        "decimals": 18,
        "info":"decentralised",
        "chain":"ethereum",
        "query": "chain",
        "pegged_against":"USD"
    },
    {
        "entity":"Prisma Finance",
        "token":"mkUSD",
        "contract": "0x4591DBfF62656E7859Afe5e45f6f47D3669fBB28",
        "decimals": 18,
        "info":"decentralised",
        "chain":"ethereum",
        "pegged_against":"USD"
    },
    {
        "entity":"Liquity",
        "token":"LUSD",
        "contract": "0x5f98805a4e8be255a32880fdec7f6728c6568ba0",
        "decimals": 18,
        "info":"decentralised",
        "chain":"ethereum",
        "pegged_against":"USD"
    },
    {
        "entity":"Paypal",
        "token":"pyUSD",
        "contract": "0x6c3ea9036406852006290770bedfcaba0e23a0e8",
        "decimals":6,
        "info":"centralised",
        "chain":"ethereum",
        "pegged_against":"USD"
    },
    {
        "entity":"Paxos",
        "token":"USDP",
        "contract":"0x8E870D67F660D95d5be530380D0eC0bd388289E1",
        "decimals":18,
        "info":"centralised",
        "chain":"ethereum",
        "pegged_against":"USD"
    }
]

def get_curve_price(contract_address):
    curve_api = "https://prices.curve.fi/v1/usd_price/ethereum"
    r = requests.get(curve_api)
    data = r.json()
    data = data["data"] ## Gives a lits
    ## iterate through the list to match the contract address
    for pool in data:
        if pool.get("address").lower() == contract_address.lower():  # Ensure case-insensitive comparison
            return round(float(pool.get("usd_price")),4)


def create_instance(token, entity, supply_transformed, chain, pegged_against, price, info):
    with app.app_context():
        info = Stablecoin(
                    token=token,
                    entity=entity,
                    price=price,
                    supply=supply_transformed,
                    chain=chain,
                    pegged_against=pegged_against,
                    info=info,
                    timestamp=datetime.utcnow(),
                )
        db.session.add(info)
        db.session.commit()

def chain():
    for stable in list_chain:
        time.sleep(1)
        api_url = f"https://api.etherscan.io/api?module=stats&action=tokensupply&contractaddress={stable['contract']}&apikey={etherscan_key}"
        r = requests.get(api_url)
        data = r.json()
        decimal = float(f"1e{stable['decimals']}")
        token = stable["token"]
        entity = stable["entity"]
        chain = stable["chain"]
        pegged_against = stable["pegged_against"]
        supply = round(float(data.get("result")))
        supply_transformed = supply / decimal
        price = get_curve_price(stable["contract"])
        info = stable["info"]
        print(f"Added {token}")


        create_instance(token, entity, supply_transformed, chain, pegged_against, price, info)

def tether():
    api_url = tether_info["url"]
    r = requests.get(api_url)
    data = r.json()
    data = data.get("data")

    for key, stable in data.items():
        token = stable["currency_iso"]
        entity = "Tether"
        chain = "All"
        info = "centralised"
        supply_transformed = round(float(stable["total_liabilities"]))
        if token == "usdt":
            contract="0xdac17f958d2ee523a2206206994597c13d831ec7"
            price = get_curve_price(contract)
            pegged_against = "USD"
            print(f"Added {token}")
            create_instance(token, entity, supply_transformed, chain, pegged_against, price, info)

def circle():
    api_url = circle_info["url"]
    r = requests.get(api_url)
    data = r.json()
    data = data["data"]
    for stable in data:
        token = stable["symbol"]
        entity = "Circle"
        chain = "ALL"
        pegged_against= "USD"
        supply_transformed = round(float(stable["totalAmount"]))
        info = "centralised"
        if token == 'USDC':
            contract="0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
            price = get_curve_price(contract)
            print(f"Added {token}")
            create_instance(token, entity, supply_transformed, chain, pegged_against, price, info)

def curve():
    api_url = "https://api.curve.fi/v1/getCrvusdTotalSupply"
    r = requests.get(api_url)
    data = r.json()
    supply = data["data"]["crvusdTotalSupply"]
    supply_transformed = round(float(supply))
    contract = "0xf939E0A03FB07F59A73314E73794Be0E57ac1b4E"
    price = get_curve_price(contract)
    info = "decentralised"
    print("Added crvUSD")
    create_instance("crvUSD", "Curve Finance", supply_transformed, "", "USD", price, info)


if __name__ == '__main__':
    circle()
    tether()
    chain()
    curve()
