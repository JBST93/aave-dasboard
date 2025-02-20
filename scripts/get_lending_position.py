from web3 import Web3
from web3.contract import Contract
from typing import List, Dict, Any
import os
import sys
from dotenv import load_dotenv
from eth_abi import decode

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

load_dotenv(os.path.join(project_root, '.env'))

# Updated contract addresses based on AAVE V3 architecture


smart_contracts = [
        {
            "chain": "ethereum" ,
            "address": "0x7B4EB56E7CD4b454BA8ff71E4518426369a138a3",
            "version": "v3",
            "instance":"Main"
        },
        {
            "chain": "ethereum" ,
            "address": "0x7B4EB56E7CD4b454BA8ff71E4518426369a138a3",
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
        }
]

def select_infura(chain):
    infura_key = os.getenv('INFURA_KEY')
    if not infura_key:
        raise ValueError("INFURA_KEY not found in environment variables")

    infura_urls = {
        "ethereum": f"https://mainnet.infura.io/v3/{infura_key}",
        "arbitrum": f"https://arbitrum-mainnet.infura.io/v3/{infura_key}",
        "optimism": f"https://optimism-mainnet.infura.io/v3/{infura_key}",
        "polygon": f"https://polygon-mainnet.infura.io/v3/{infura_key}",
        "base": f"https://base-mainnet.infura.io/v3/{infura_key}",
        "avalanche": f"https://avalanche-mainnet.infura.io/v3/{infura_key}",
        "fantom": "https://rpc.ftm.tools"  # Using public RPC for Fantom
    }

    if chain not in infura_urls:
        raise ValueError(f"Unsupported chain: {chain}")
    return infura_urls[chain]


def get_multicall_contract(web3: Web3) -> Contract:
    # Multicall3 contract on Ethereum mainnet
    MULTICALL_ADDRESS = "0xcA11bde05977b3631167028862bE2a173976CA11"

    MULTICALL_ABI = [
        {
            "inputs": [
                {
                    "components": [
                        {"name": "target", "type": "address"},
                        {"name": "allowFailure", "type": "bool"},
                        {"name": "callData", "type": "bytes"}
                    ],
                    "name": "calls",
                    "type": "tuple[]"
                }
            ],
            "name": "aggregate3",
            "outputs": [
                {
                    "components": [
                        {"name": "success", "type": "bool"},
                        {"name": "returnData", "type": "bytes"}
                    ],
                    "name": "returnData",
                    "type": "tuple[]"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        }
    ]

    return web3.eth.contract(address=MULTICALL_ADDRESS, abi=MULTICALL_ABI)

def get_user_balances(web3: Web3, pool_address: str, data_provider_address: str, user_address: str) -> Dict[str, Any]:
    # Initialize contracts with ABIs
    pool_abi = [{"inputs":[{"name":"user","type":"address"}],"name":"getUserAccountData","outputs":[{"name":"totalCollateralBase","type":"uint256"},{"name":"totalDebtBase","type":"uint256"},{"name":"availableBorrowsBase","type":"uint256"},{"name":"currentLiquidationThreshold","type":"uint256"},{"name":"ltv","type":"uint256"},{"name":"healthFactor","type":"uint256"}],"stateMutability":"view","type":"function"}]
    data_provider_abi = [
        {"inputs":[],"name":"getAllReservesTokens","outputs":[{"components":[{"name":"symbol","type":"string"},{"name":"tokenAddress","type":"address"}],"type":"tuple[]"}],"stateMutability":"view","type":"function"},
        {"inputs":[{"name":"asset","type":"address"},{"name":"user","type":"address"}],"name":"getUserReserveData","outputs":[{"name":"currentATokenBalance","type":"uint256"},{"name":"currentStableDebt","type":"uint256"},{"name":"currentVariableDebt","type":"uint256"},{"name":"principalStableDebt","type":"uint256"},{"name":"scaledVariableDebt","type":"uint256"},{"name":"stableBorrowRate","type":"uint256"},{"name":"liquidityRate","type":"uint256"},{"name":"stableRateLastUpdated","type":"uint40"},{"name":"usageAsCollateralEnabled","type":"bool"}],"stateMutability":"view","type":"function"}
    ]

    pool = web3.eth.contract(address=pool_address, abi=pool_abi)
    data_provider = web3.eth.contract(address=data_provider_address, abi=data_provider_abi)
    multicall = get_multicall_contract(web3)

    # First, get all reserves (1 call)
    reserves = data_provider.functions.getAllReservesTokens().call()

    # Prepare multicall for user data
    calls = []

    # Add getUserAccountData call
    calls.append({
        'target': pool_address,
        'allowFailure': False,
        'callData': pool.encodeABI('getUserAccountData', [user_address])
    })

    # Add getUserReserveData calls for each token
    for _, token_address in reserves:
        calls.append({
            'target': data_provider_address,
            'allowFailure': False,
            'callData': data_provider.encodeABI('getUserReserveData', [token_address, user_address])
        })

    # Make multicall (1 call for all data)
    multicall_results = multicall.functions.aggregate3(calls).call()

    # Decode account data
    account_data = decode(
        ['uint256', 'uint256', 'uint256', 'uint256', 'uint256', 'uint256'],
        multicall_results[0][1]
    )

    user_balances = []
    for i, (symbol, token_address) in enumerate(reserves):
        reserve_data = decode(
            ['uint256', 'uint256', 'uint256', 'uint256', 'uint256', 'uint256', 'uint256', 'uint40', 'bool'],
            multicall_results[i + 1][1]
        )

        if reserve_data[0] > 0 or reserve_data[2] > 0:  # if aToken balance or variable debt > 0
            user_balances.append({
                'symbol': symbol,
                'token_address': token_address,
                'supply_balance': reserve_data[0],
                'variable_debt': reserve_data[2],
                'collateral_enabled': reserve_data[8]
            })

    return {
        'positions': user_balances,
        'account_data': {
            'total_collateral_base': account_data[0],
            'total_debt_base': account_data[1],
            'available_borrows_base': account_data[2],
            'current_liquidation_threshold': account_data[3],
            'ltv': account_data[4],
            'health_factor': account_data[5]
        }
    }

# Add pool addresses mapping with instance-specific addresses
POOL_ADDRESSES = {
    "ethereum": {
        "Main": "0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2",
        "Lido": "0x764594F8e9757edE877B75716f8077162B251460",
        "EtherFi": "0x8Cb4b66f7B13F2Ae4D3c91338fC007dbF8C14208",
    },
    "arbitrum": {
        "Main": "0x794a61358D6845594F94dc1DB02A252b5b4814aD"
    },
    "optimism": {
        "Main": "0x794a61358D6845594F94dc1DB02A252b5b4814aD"
    },
    "polygon": {
        "Main": "0x794a61358D6845594F94dc1DB02A252b5b4814aD"
    },
    "base": {
        "Main": "0x794a61358D6845594F94dc1DB02A252b5b4814aD"
    },
    "avalanche": {
        "Main": "0x794a61358D6845594F94dc1DB02A252b5b4814aD"
    },
    "fantom": {
        "Main": "0x794a61358D6845594F94dc1DB02A252b5b4814aD"
    }
    # Add other chains as needed
}

# Main execution block changes
for contract in smart_contracts:
    chain = contract['chain']
    data_provider_address = contract['address']
    instance = contract['instance']

    try:
        # Connect to appropriate network
        try:
            infura_url = select_infura(chain)
            web3 = Web3(Web3.HTTPProvider(infura_url))
            if not web3.is_connected():
                print(f"Failed to connect to {chain}")
                continue
        except ValueError as e:
            print(f"Error with chain {chain}: {str(e)}")
            continue

        # Get pool address based on chain and instance
        AAVE_V3_POOL = POOL_ADDRESSES.get(chain, {}).get(instance)
        if not AAVE_V3_POOL:
            print(f"No pool address found for {chain} - {instance}")
            continue

        # Ensure addresses are checksummed
        AAVE_V3_POOL = Web3.to_checksum_address(AAVE_V3_POOL)
        data_provider_address = Web3.to_checksum_address(data_provider_address)
        USER_ADDRESS = Web3.to_checksum_address('0x13dd4C65252274A442428039Ae815F3a13e84Ff3')

        print(f"\n=== {chain.upper()} - {instance} Instance ===")

        # Get user balances
        result = get_user_balances(web3, AAVE_V3_POOL, data_provider_address, USER_ADDRESS)

        # Print results
        print("\nAccount Overview:")
        print(f"Total Collateral: {result['account_data']['total_collateral_base']}")
        print(f"Total Debt: {result['account_data']['total_debt_base']}")
        print(f"Health Factor: {result['account_data']['health_factor']}")

        print("\nPositions:")
        for position in result['positions']:
            print(f"\nToken: {position['symbol']}")
            print(f"Supply Balance: {position['supply_balance']}")
            print(f"Variable Debt: {position['variable_debt']}")
            print(f"Used as Collateral: {position['collateral_enabled']}")

    except Exception as e:
        print(f"Error processing {chain} - {instance}: {str(e)}")
        continue
