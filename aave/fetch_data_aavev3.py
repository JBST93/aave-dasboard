from web3 import Web3
from dotenv import load_dotenv
import os
import sys
import json
from datetime import datetime

# Ensure the root directory is in the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

# Load environment variables
load_dotenv(os.path.join(project_root, '.env'))

# Import app and db from the root directory
from app import app, db
from instances.MoneyMarketRate import MoneyMarketRate

# Connect to an Ethereum node
infura_url = os.getenv('INFURA_URL')
web3 = Web3(Web3.HTTPProvider(infura_url))

script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path to the aave_abi.json file
abi_path = os.path.join(script_dir, 'aave_abi.json')

with open(abi_path) as f:
    try:
        provider_abi = json.load(f)
    except FileNotFoundError:
        exit(1)

token_addresses = {
    "USDC": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
    "USDT": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
    "DAI": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
    "USDe": "0x4c9EDD5852cd905f086C759E8383e09bff1E68B3",
    "pyUSD": "0x6c3ea9036406852006290770BEdFcAbA0e23A0e8",
    "LUSD": "0x5f98805A4E8be255a32880FDeC7F6728C6568bA0",
    "crvUSD": "0xf939E0A03FB07F59A73314E73794Be0E57ac1b4E",
    "FRAX": "0x853d955aCEf822Db058eb8505911ED77F175b99e",
    "sDai": "0x83F20F44975D03b1b09e64809B757c47f942BEeA",
    "sUSDe": "0x9D39A5DE30e57443BfF2A8307A4256c8797A3497",
}

token_addresses_ARB = {
    "UDSDCe": "0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8",
    "USDT": "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9",
    "DAI":"0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1",
    "MAI": "0x3F56e0c36d275367b8C502090EDF38289b3dEa0d",
    "LUSD": "0x93b346b6BC2548dA6A1E7d98E9a421B42541425b",
    "USDC": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
    "FRAX":"0x17FC002b466eEc40DaE837Fc4bE5c67993ddBd6F",
    "GHO" : "0x7dfF72693f6A4149b17e7C6314655f6A9F7c8B33",
}


contract_addresses = "0x7B4EB56E7CD4b454BA8ff71E4518426369a138a3"  # AaveProtocolDataProvider


pool_contract = web3.eth.contract(address=contract_addresses, abi=provider_abi)

def fetch_store_rates():
    print("Starting Fetching Data for AaveV3")
    with app.app_context():
        for token in token_addresses:
            try:
                reserve_data = pool_contract.functions.getReserveData(token_addresses[token]).call()
                liquidity_rate = reserve_data[5] / 1e27 * 100  # Convert from Ray to percentage
                borrow_rate = reserve_data[6] / 1e27 * 100  # Convert from Ray to percentage

                transformed_liquidity_rate = round(liquidity_rate, 2)
                transformed_borrow_rate = round(borrow_rate, 2)

                raw_tvl = pool_contract.functions.getATokenTotalSupply(token_addresses[token]).call()

                if token in ['USDC', 'pyUSD', 'USDT']:
                    tvl = raw_tvl / 1e6  # These tokens have 6 decimal places
                else:
                    tvl = raw_tvl / 1e18  # Default to 18 decimal places for other tokens

                rate = MoneyMarketRate(
                    token=token,
                    protocol="Aave V3",
                    liquidity_rate=float(transformed_liquidity_rate),
                    borrow_rate=float(transformed_borrow_rate),
                    chain='Ethereum',
                    tvl=tvl,
                    timestamp=datetime.utcnow()
                )

                db.session.add(rate)
            except Exception as e:
                print(f"Error fetching data for {token}: {e}")

        db.session.commit()
        print("Fetched")

if __name__ == '__main__':
    fetch_store_rates()
