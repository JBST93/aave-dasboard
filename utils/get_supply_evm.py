import sys, os

from web3 import Web3
from dotenv import load_dotenv

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

load_dotenv(os.path.join(project_root, '.env'))

from app import app, db
from scripts.utils import load_abi

provider_abi = load_abi("paypal",'pyusd_abi.json')

infura_url = "https://mainnet.infura.io/v3/"

infura_key = os.getenv('INFURA_KEY')
if not infura_key:
    raise ValueError("INFURA_KEY not found in environment variables")

token = "pyUSD"
ETH_contract = "0x6c3ea9036406852006290770BEdFcAbA0e23A0e8"
SOL_contract = "2b1kV6DkPAnxd5ixfnxCpjxmKwqjjaYmCZfHsFu24GXo"
decimals = 6


def get_evm_supply(contract):
    infura_url = "https://mainnet.infura.io/v3/"
    web3 = Web3(Web3.HTTPProvider(infura_url + infura_key))
    contract = web3.eth.contract(address=ETH_contract, abi=provider_abi)
    supply = contract.functions.totalSupply().call()
    supply = supply / 10 ** decimals
    return supply
