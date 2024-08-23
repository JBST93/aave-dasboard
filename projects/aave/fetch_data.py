from web3 import Web3
from dotenv import load_dotenv
import os
import sys
# Ensure the root directory is in the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

load_dotenv(os.path.join(project_root, '.env'))

from app import app, db
from instances.YieldRate import YieldRate
from scripts.utils import load_abi, insert_yield_db, get_curve_price


treasury_wallets = {
    "ethereum":"0x464C71f6c2F760DdA6093dCB91C24c39e5d6e18c"

}







provider_abi = load_abi("aave",'aave_abi.json')

smart_contracts = {
    "Ethereum":"0x7B4EB56E7CD4b454BA8ff71E4518426369a138a3",
    "Arbitrum":"0x69FA688f1Dc47d4B5d8029D5a35FB7a548310654",
    "Optimism":"0x69FA688f1Dc47d4B5d8029D5a35FB7a548310654",
    "Polygon":"0x69FA688f1Dc47d4B5d8029D5a35FB7a548310654",
}

infura_url ={
    "Ethereum":"https://mainnet.infura.io/v3/",
    "Arbitrum":"https://arbitrum-mainnet.infura.io/v3/",
    "Optimism":"https://optimism-mainnet.infura.io/v3/",
    "Polygon":"https://polygon-mainnet.infura.io/v3/",
}

infura_key = os.getenv('INFURA_KEY')
if not infura_key:
    raise ValueError("INFURA_KEY not found in environment variables")

def fetch_store_rates():

    print("Starting Fetching Data for AaveV3")
    for chain, contract_address in smart_contracts.items():
        print(f"Fetching Aave v3 data for {chain}...")

        web3 = Web3(Web3.HTTPProvider(infura_url[chain] + infura_key))
        pool_contract = web3.eth.contract(address=contract_address, abi=provider_abi)

        data = pool_contract.functions.getAllReservesTokens().call()
        for item in data:
            try:
                token = item[0]
                contract = item[1]

                reserve_data = pool_contract.functions.getReserveData(contract).call()
                apy_base = reserve_data[5] / 1e27 * 100  # Convert from Ray to percentage
                apy_base_formatted = round(apy_base, 2)

                raw_tvl = pool_contract.functions.getATokenTotalSupply(contract).call()

                if token in ['USDC', 'pyUSD', 'USDT']:  # TVL in LCY - need to find USD
                    tvl = raw_tvl / 1e6  # These tokens have 6 decimal places
                else:
                    tvl = raw_tvl / 1e18  # Default to 18 decimal places for other tokens

                # Need to find TVL_USD
                tvl_usd = tvl
                information = None
                type = "Lending market"

                insert_yield_db(token, "Aave v3", information, apy_base_formatted,None,None,tvl_usd,chain, type, contract)

            except Exception as e:
                print(f"Error fetching data for {token}: {e}")

    db.session.commit()

    print("Aave v3 data fetched and committed")


if __name__ == '__main__':
    with app.app_context():
        fetch_store_rates()
