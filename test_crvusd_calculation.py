#!/usr/bin/env python3

import os
import sys
from datetime import datetime

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
sys.path.append(project_root)

from utils.get_infura import select_infura
from scripts.utils import load_abi

def test_crvusd_calculation():
    """Test crvUSD calculation to find the issue"""
    
    print("Testing crvUSD Calculation on Aave")
    print("=" * 60)
    
    # Main Aave instance
    main_address = "0x7B4EB56E7CD4b454BA8ff71E4518426369a138a3"
    
    try:
        web3 = select_infura("ethereum")
        provider_abi = load_abi("aave", 'aave_abi.json')
        pool_contract = web3.eth.contract(address=main_address, abi=provider_abi)
        
        # Get crvUSD data
        data = pool_contract.functions.getAllReservesTokens().call()
        
        for token, contract_addr in data:
            if token == "crvUSD":
                print(f"crvUSD Contract: {contract_addr}")
                print("-" * 40)
                
                reserve_data = pool_contract.functions.getReserveData(contract_addr).call()
                
                lend_amount_raw = reserve_data[2]
                borrowed_amount_raw = reserve_data[3] + reserve_data[4]
                
                # Calculate with 18 decimals (current)
                lend_amount_18 = lend_amount_raw / 1e18
                borrowed_amount_18 = borrowed_amount_raw / 1e18
                
                # Calculate with 6 decimals (test)
                lend_amount_6 = lend_amount_raw / 1e6
                borrowed_amount_6 = borrowed_amount_raw / 1e6
                
                print(f"Raw supply amount: {lend_amount_raw}")
                print(f"Supply amount (18 decimals): {lend_amount_18:,.2f} crvUSD")
                print(f"Supply amount (6 decimals): {lend_amount_6:,.2f} crvUSD")
                
                # Test different prices with 18 decimals
                test_prices = [1.0, 0.99, 1.01, 100.0, 1000.0, 10000.0]
                
                print(f"\nTVL calculations with 18 decimals:")
                for price in test_prices:
                    tvl = lend_amount_18 * price
                    print(f"  Price ${price:,.2f}: TVL = ${tvl:,.2f}")
                
                # Test different prices with 6 decimals
                print(f"\nTVL calculations with 6 decimals:")
                for price in test_prices:
                    tvl = lend_amount_6 * price
                    print(f"  Price ${price:,.2f}: TVL = ${tvl:,.2f}")
                
                # Check if the issue is with the raw amount
                if lend_amount_18 > 1e6:  # More than 1 million crvUSD
                    print(f"\n⚠️  WARNING: {lend_amount_18:,.2f} crvUSD seems too high with 18 decimals!")
                if lend_amount_6 > 1e6:  # More than 1 million crvUSD
                    print(f"⚠️  WARNING: {lend_amount_6:,.2f} crvUSD seems too high with 6 decimals!")
                
                # Show what price would give reasonable TVL
                if lend_amount_18 > 1e6:
                    reasonable_tvl = 1e6  # $1M
                    required_price = reasonable_tvl / lend_amount_18
                    print(f"\nTo get $1M TVL with 18 decimals, crvUSD price should be: ${required_price:,.6f}")
                
                break
        else:
            print("crvUSD not found in Aave reserves")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_crvusd_calculation()
