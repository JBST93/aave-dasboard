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
        "pegged_against":"USD"
    },
    {
        "entity":"Angle",
        "token":"EURA",
        "contract":"0x1a7e4e63778b4f12a199c062f3efdd288afcbce8",
        "decimals":18,
        "info":"decentralised",
        "chain":"ethereum",
        "pegged_against":"EUR"
    },
    {
        "entity":"Angle",
        "token":"USDA",
        "contract":"0x0000206329b97db379d5e1bf586bbdb969c63274",
        "decimals":18,
        "info":"decentralised",
        "chain":"ethereum",
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
    },
    {
        "entity":"Statis",
        "token":"EURs",
        "contract":"0xdb25f211ab05b1c97d595516f45794528a807ad8",
        "decimals":2,
        "info":"centralised",
        "chain":"ethereum",
        "pegged_against":"EUR"
    },
    {   "entity":"Gemini",
        "token":"GUSD",
        "contract":"0x056fd409e1d7a124bd7017459dfea2f387b6d5cd",
        "decimals":2,
        "info":"centralised",
        "chain":"ethereum",
        "pegged_against":"USD"
    },
    {
        "entity":"Tether",
        "token":"XAUt",
        "contract":"0x68749665ff8d2d112fa859aa293f07a622782f38",
        "decimals":6,
        "info":"centralised",
        "chain":"ethereum",
        "pegged_against":"GOLD"
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

def get_one_price(contract_address):
    one_url = f"https://api.1inch.dev/price/v1.1/1/{contract_address}"

    requestOptions = {
        "headers": {
        "Authorization": "Bearer Qzw77er7P6FNv2vtQWsyKb2X1gEPBo3Q"
    },
        "body": "",
        "params": {
        "currency": "USD"
        }
    }

    # Prepare request components
    headers = requestOptions.get("headers", {})
    body = requestOptions.get("body", {})
    params = requestOptions.get("params", {})

    r = requests.get(one_url, headers=headers, params=params)
    data = r.json()
    return round(float(data[f"{contract_address}"]),4)

def get_angle_price(token):
    angle_url = "https://api.angle.money/v1/prices"
    r = requests.get(angle_url)
    data = r.json()
    for stable in data:
        if stable["token"].upper() == token.upper():
            price = stable["rate"]
            print(f"{token} - {price}")

def create_instance(token, entity, supply_transformed, chain, pegged_against, price, info):
    with app.app_context():
        info = Stablecoin(
                    token=token,
                    entity=entity,
                    price=price,
                    supply=supply_transformed,
                    chain=chain,
                    pegged_against=pegged_against,
                    info=info.capitalize(),
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
        if not price:  # This checks for None, empty string, empty list, 0, etc.
            price = get_one_price(stable["contract"])
        info = stable["info"]
        print(f"Added {token} - {price}")


        create_instance(token, entity, supply_transformed, chain, pegged_against, price, info)

def tether():
    api_url = tether_info["url"]
    r = requests.get(api_url)
    data = r.json()
    data = data.get("data")

    for key, stable in data.items():
        token = stable["currency_iso"].upper()
        entity = "Tether"
        chain = "All"
        info = "centralised"
        supply_transformed = round(float(stable["total_liabilities"]))
        if token == "USDT":
            contract="0xdac17f958d2ee523a2206206994597c13d831ec7"
            pegged_against = "USD"

        elif token == "EURT":
            contract="0xc581b735a1688071a1746c968e0798d642ede491"
            pegged_against = "EUR"

        else:
            continue

        price = get_curve_price(contract)
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
            pegged_against = "USD"
        elif token =='EUROC':
            contract="0x1abaea1f7c830bd89acc67ec4af516284b1bc33c"
            pegged_against = "EUR"

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

def euroe():
    api_url = "https://www.membrane.fi/api/totalsupply/euroe/all"
    r = requests.get(api_url)
    data = r.json()
    token="EUROe"
    entity="Membrane.Fi"
    contract="0x820802fa8a99901f52e39acd21177b0be6ee2974"
    chain = "ethereum"
    supply = data
    supply_transformed = round(float(supply))
    info = "centralised"
    pegged_against = "EUR"
    price = get_curve_price(contract)
    if not price:  # This checks for None, empty string, empty list, 0, etc.
        price = get_one_price(contract)

    create_instance(token, entity, supply_transformed, chain, pegged_against, price, info)


def get_stablecoin_data():
    try:
        print("Starting euroe()")
        euroe()
    except Exception as e:
        print(f"euroe() failed: {e}")

    try:
        print("Finished euroe(), starting circle()")
        circle()
    except Exception as e:
        print(f"circle() failed: {e}")

    try:
        print("Finished circle(), starting tether()")
        tether()
    except Exception as e:
        print(f"tether() failed: {e}")

    try:
        print("Finished tether(), starting chain()")
        chain()
    except Exception as e:
        print(f"chain() failed: {e}")

    try:
        print("Finished chain(), starting curve()")
        curve()
    except Exception as e:
        print(f"curve() failed: {e}")

    print("Finished all functions")

if __name__ == '__main__':
    get_stablecoin_data()
