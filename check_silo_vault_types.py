import requests
import json

def check_silo_vault_types():
    """
    Check Silo Finance API to understand vault types
    """
    print("SILO FINANCE - CHECKING VAULT TYPES")
    print("=" * 60)

    api_url = "https://app.silo.finance/api/earn"

    try:
        response = requests.post(
            api_url,
            json={"limit": 5, "offset": 0},
            headers={
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (compatible; SiloAPY/1.0)"
            },
            timeout=15
        )

        if response.status_code == 200:
            data = response.json()
            pools = data.get('pools', [])

            print(f"Found {len(pools)} pools")
            print("\n📊 ANALYZING POOL STRUCTURE:")
            print("-" * 60)

            for i, pool in enumerate(pools):
                print(f"\nPool {i+1}: {pool.get('tokenSymbol', 'Unknown')}")
                print("Available fields:")
                for key, value in pool.items():
                    print(f"  {key}: {type(value).__name__} = {str(value)[:100]}{'...' if len(str(value)) > 100 else ''}")
                print("-" * 40)

            # Look for vault type indicators
            print("\n🔍 LOOKING FOR VAULT TYPE INDICATORS:")
            print("-" * 60)

            # Check if there are any fields that might indicate vault type
            possible_vault_type_fields = [
                'vaultType', 'type', 'poolType', 'earnPoolType',
                'isIsolated', 'isManaged', 'vaultCategory', 'category'
            ]

            for field in possible_vault_type_fields:
                if field in pools[0] if pools else {}:
                    print(f"✅ Found field '{field}': {pools[0][field]}")
                else:
                    print(f"❌ Field '{field}' not found")

            # Check the _tag field which might indicate type
            if '_tag' in pools[0] if pools else {}:
                print(f"\n🏷️  '_tag' field values across pools:")
                for i, pool in enumerate(pools):
                    print(f"  Pool {i+1}: {pool.get('_tag', 'N/A')}")

            # Check if there are any other indicators
            print(f"\n📋 OTHER POTENTIAL INDICATORS:")
            for i, pool in enumerate(pools):
                print(f"Pool {i+1} ({pool.get('tokenSymbol', 'Unknown')}):")
                print(f"  siloSymbol0: {pool.get('siloSymbol0', 'N/A')}")
                print(f"  siloSymbol1: {pool.get('siloSymbol1', 'N/A')}")
                print(f"  isNonBorrowable: {pool.get('isNonBorrowable', 'N/A')}")
                print(f"  programs: {len(pool.get('programs', []))} programs")
                print(f"  points: {len(pool.get('points', []))} points")

        else:
            print(f"❌ API Error: {response.status_code}")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    check_silo_vault_types()
