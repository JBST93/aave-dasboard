import requests
import json
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Ensure the root directory is in the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.append(project_root)

load_dotenv(os.path.join(project_root, '.env'))

from app import app, db
from instances.YieldRate import YieldRate as Yield
from instances.TokenData import TokenData as Info
from utils.get_price import get_price
from utils.get_last_price_db import get_latest_price

def fetch_silo_data():
    """
    Fetch Silo Finance data from their API
    """
    try:
        print("🔍 Fetching Silo Finance data...")

        # Silo Finance API endpoint
        api_url = "https://app.silo.finance/api/earn"

        response = requests.post(
            api_url,
            json={"limit": 100, "offset": 0},
            headers={
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (compatible; SiloAPY/1.0)"
            },
            timeout=15
        )

        if response.status_code == 200:
            data = response.json()
            pools = data.get("pools", [])
            print(f"✅ Fetched {len(pools)} pools from Silo Finance API")
            return pools
        else:
            print(f"❌ Silo Finance API returned status {response.status_code}")
            return []

    except Exception as e:
        print(f"❌ Error fetching Silo Finance data: {e}")
        return []

def process_silo_pools(pools):
    """
    Process Silo Finance pools and create yield rate records
    """
    processed_pools = []

    try:
        print(f"📊 Processing {len(pools)} Silo Finance pools...")

        for pool in pools:
            try:
                # Extract pool information
                symbol = pool.get("tokenSymbol", "Unknown")
                name = pool.get("tokenName", "Unknown")
                address = pool.get("tokenAddress", "")
                decimals = int(pool.get("tokenDecimals", 18))
                chain_key = pool.get("chainKey", "ethereum")
                silo_id = pool.get("siloId", "")
                market_id = pool.get("marketId", "")

                # Convert TVL from wei to proper units
                total_supply_usd = pool.get("totalSupplyUsd", "0")
                tvl_usd = float(total_supply_usd) / (10 ** decimals) if total_supply_usd else 0

                # Convert APY from wei to percentage
                supply_apr = pool.get("supplyApr", "0")
                supply_base_apr = pool.get("supplyBaseApr", "0")
                underlying_apy = pool.get("underlyingApy", "0")

                # Convert APR from wei format to percentage
                apy_base = float(supply_apr) / 1e18 * 100 if supply_apr else 0
                apy_base_raw = float(supply_base_apr) / 1e18 * 100 if supply_base_apr else 0
                apy_underlying = float(underlying_apy) / 1e18 * 100 if underlying_apy else 0

                # Use the highest APY value
                final_apy = max(apy_base, apy_base_raw, apy_underlying)

                # Check if pool is borrowable
                is_non_borrowable = pool.get("isNonBorrowable", False)
                pool_type = "Lending" if not is_non_borrowable else "Staking"

                # Determine vault type based on vaultManager
                vault_manager = pool.get("vaultManager", "silo")
                if vault_manager == "silo":
                    vault_type = "Isolated Vault"
                else:
                    vault_type = "Managed Vault"

                # Skip if TVL is too small (less than $1000)
                if tvl_usd < 1000:
                    continue

                # Skip if APY is 0 or negative
                if final_apy <= 0:
                    continue

                # Get token price
                token_price = get_price(symbol) or 1.0

                # Create yield rate record
                yield_record = Yield(
                    market=symbol,
                    project="Silo Finance",
                    information=f"{vault_type} - {name}",
                    yield_rate_base=round(final_apy, 2),
                    yield_rate_reward=0,  # Silo typically doesn't have reward tokens
                    yield_token_reward=None,
                    tvl=tvl_usd,
                    action="Lend" if pool_type == "Lending" else "Stake",
                    chain=chain_key.title(),
                    type=pool_type,
                    smart_contract=address,
                    timestamp=datetime.now()
                )

                processed_pools.append(yield_record)

                print(f"   ✅ {symbol} ({name}) - {vault_type} - TVL: ${tvl_usd:,.2f}, APY: {final_apy:.2f}%, Chain: {chain_key}")

            except Exception as e:
                print(f"   ❌ Error processing pool {symbol}: {e}")
                continue

        return processed_pools

    except Exception as e:
        print(f"❌ Error processing Silo Finance pools: {e}")
        return []

def fetch_store_rates():
    """
    Main function to fetch and store Silo Finance yield rates
    """
    try:
        print("SILO FINANCE - FETCHING YIELD RATES")
        print("=" * 60)

        # Fetch data from API
        pools = fetch_silo_data()
        if not pools:
            print("❌ No pools fetched from Silo Finance API")
            return

        # Process pools
        processed_pools = process_silo_pools(pools)
        if not processed_pools:
            print("❌ No pools processed")
            return

        print(f"✅ Processed {len(processed_pools)} Silo Finance pools")

        # Store in database
        try:
            # Delete existing Silo Finance records
            Yield.query.filter_by(project="Silo Finance").delete()

            # Add new records
            for pool in processed_pools:
                db.session.add(pool)

            db.session.commit()
            print(f"✅ Stored {len(processed_pools)} Silo Finance yield rates in database")

        except Exception as e:
            print(f"❌ Error storing Silo Finance data: {e}")
            db.session.rollback()

        # Summary
        total_tvl = sum(pool.tvl for pool in processed_pools)
        chains = list(set(pool.chain for pool in processed_pools))

        print(f"\n📊 SILO FINANCE SUMMARY:")
        print(f"Total pools: {len(processed_pools)}")
        print(f"Total TVL: ${total_tvl:,.2f}")
        print(f"Chains: {', '.join(chains)}")

    except Exception as e:
        print(f"❌ Error in fetch_store_rates: {e}")

if __name__ == '__main__':
    with app.app_context():
        fetch_store_rates()
