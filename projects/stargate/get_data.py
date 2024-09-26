# https://stargateprotocol.gitbook.io/stargate/v/v2-developer-docs/technical-reference/mainnet-contracts
import requests, sys, os
from web3 import Web3
from dotenv import load_dotenv
from datetime import datetime
import logging

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

load_dotenv(os.path.join(project_root, '.env'))

from app import app, db
from scripts.utils import load_abi
from utils.get_price import get_price
from instances.TokenData import TokenData as Data
from instances.YieldRate import YieldRate as Yield

provider_abi = load_abi("stargate",'v2_pool_abi.json')
reward_abi = load_abi("stargate",'reward_abi.json')

infura_url = "https://mainnet.infura.io/v3/"

infura_url ={
    "ethereum":"https://mainnet.infura.io/v3/",
    "arbitrum":"https://arbitrum-mainnet.infura.io/v3/",
    "optimism":"https://optimism-mainnet.infura.io/v3/",
    "polygon":"https://polygon-mainnet.infura.io/v3/",
}
infura_key = os.getenv('INFURA_KEY')
if not infura_key:
    raise ValueError("INFURA_KEY not found in environment variables")


contracts = [
    {
        "chain": "ethereum",
        "token": "ETH",
        "address":"0x77b2043768d28E9C9aB44E1aBfC95944bcE57931",
        "decimals": 18,
        "lp":"0xfcb42A0e352a08AbD50b8EE68d01f581B6Dfd80A"

    },
    {
        "chain": "ethereum",
        "token": "USDC",
        "address":"0xc026395860Db2d07ee33e05fE50ed7bD583189C7",
        "decimals": 6,
        "lp":"0x5DaAee9EF143faFF495B581e9863570e83F99d31"
    },
    {
        "chain": "ethereum",
        "token": "USDT",
        "address":"0x933597a323Eb81cAe705C5bC29985172fd5A3973",
        "decimals": 6,
        "lp":"0x17BBC9BD51A52aAf4d2CC6652630DaF4fdB358F7"
    },
    {
        "chain": "arbitrum",
        "token": "ETH",
        "address":"0xA45B5130f36CDcA45667738e2a258AB09f4A5f7F",
        "decimals": 18,
        "lp":"0x993614e1c8c9C5AbE49462Ce5702431978Fd767F"
    },
    {
        "chain": "arbitrum",
        "token": "USDC",
        "address":"0xe8CDF27AcD73a434D661C84887215F7598e7d0d3",
        "decimals": 6,
        "lp":"0x6Ea313859A5D9F6fF2a68f529e6361174bFD2225"
    },
    {
        "chain": "arbitrum",
        "token": "USDT",
        "address":"0xcE8CcA271Ebc0533920C83d39F417ED6A0abB7D0",
        "decimals": 6,
        "lp":"0x8D66Ff1845b1baCC6E87D867CA4680d05A349cA8"
    },
    {
        "chain": "optimism",
        "token": "ETH",
        "address":"0xe8CDF27AcD73a434D661C84887215F7598e7d0d3",
        "decimals": 18,
        "lp":"0x6Ea313859A5D9F6fF2a68f529e6361174bFD2225"
    },
    {
        "chain": "optimism",
        "token": "USDC",
        "address":"0xcE8CcA271Ebc0533920C83d39F417ED6A0abB7D0",
        "decimals": 6,
        "lp":"0x8D66Ff1845b1baCC6E87D867CA4680d05A349cA8"
    },
    {
        "chain": "optimism",
        "token": "USDT",
        "address":"0x19cFCE47eD54a88614648DC3f19A5980097007dD",
        "decimals": 6,
        "lp":"0x9f58A79D81477130C0C6D74b96e1397db9765ab1"
    },
]





def get_token_data():
    with app.app_context():
        token = "STG"
        decimals = 18
        address = "0xAf5191B0De278C7286d6C7CC6ab6BB8A73bA2Cd6"
        chain = "ETH"
        price = get_price(token,address,chain)
        supply_circ = 204338417
        supply_tot = 1000000000

        data = Data (
            token=token,
            price=price,
            price_source= "",
            tot_supply= supply_tot,
            circ_supply= supply_circ ,
            timestamp=datetime.utcnow(),
        )

        db.session.add(data)
        db.session.commit()


reward_contracts = {
    "ethereum":"0x5871A7f88b0f3F5143Bf599Fd45F8C0Dc237E881",
    "arbitrum":"0x957b12606690C7692eF92bb5c34a0E63baED99C7",
    "optimism":"0x146c8e409C113ED87C6183f4d25c50251DFfbb3a"
}

stg_address = {
    "ethereum":"0xAf5191B0De278C7286d6C7CC6ab6BB8A73bA2Cd6",
    "arbitrum":"0x6694340fc020c5E6B96567843da2df01b2CE1eb6",
    "optimism":"0x296F55F8Fb28E498B858d0BcDA06D955B2Cb3f97"

}

def get_yield():
    with app.app_context():
        project = "Stargate"
        total_tvl = 0

        for item in contracts:
            try:
                reward = {
                "reward_token":"STG",
                "reward_decimals":18,
                "reward_address":"0xAf5191B0De278C7286d6C7CC6ab6BB8A73bA2Cd6"
                }

                chain = item.get("chain",{})
                reward_contract = reward_contracts.get(chain)
                reward_address = stg_address.get(chain,{})
                reward_decimal = reward.get("reward_decimals",{})

                web3 = Web3(Web3.HTTPProvider(infura_url[chain] + infura_key))

                reward_contract = web3.eth.contract(address=reward_contract, abi=reward_abi)
                total_reward = sum(reward_contract.functions.allocPointsByReward(reward_address).call()[1])

                stg_reward = reward_contract.functions.rewardDetails(reward_address).call()[0]

                token = item.get("token")
                address = item.get("address")
                chain = item.get("chain")
                decimals = item.get("decimals")
                lp_address = item.get("lp")

                pool_contract = web3.eth.contract(address=address, abi=provider_abi)
                tvl = (pool_contract.functions.tvl().call())
                tvl_standardised = tvl / 10**decimals
                price = get_price(token,address,chain)
                tvl_usd = price*tvl_standardised
                total_tvl += tvl_usd

                share_reward = (reward_contract.functions.allocPointsByStake(lp_address).call())[1][0]
                try:
                    if total_reward != 0:
                        share = float(share_reward) / float(total_reward)
                    else:
                        share = None  # or some default value
                except ZeroDivisionError:
                    share = None  # or some default value if you want to handle it explicitly
                    print("Division by zero occurred when calculating share")


                reward = share * stg_reward / 10**18 * 60*60*24*365 * 0.3119 * 100

                reward_apy = reward/tvl_usd

                data = Yield(
                    market=token,
                    project=project,
                    information="v2",
                    yield_rate_base=0,
                    yield_rate_reward=reward_apy,
                    yield_token_reward="STG",
                    tvl=tvl_usd,
                    chain=chain.capitalize(),
                    type="Bridge",
                    smart_contract=address,
                    timestamp=datetime.utcnow()
                )

                db.session.add(data)
                db.session.commit()

            except Exception as e:
                print(f"Error processing vault data: {e}")

def get_data():
    get_token_data()
    get_yield()

if __name__ == '__main__':
    with app.app_context():
        get_data()
