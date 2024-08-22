from solana.rpc.api import Client
import base58
from solders.pubkey import Pubkey


def get_sol_supply(contract):
    solana_client = Client("https://api.mainnet-beta.solana.com")
    SOL_contract_bytes = base58.b58decode(contract)
    SOL_contract_pubkey = Pubkey.from_bytes(SOL_contract_bytes)
    response = solana_client.get_token_supply(SOL_contract_pubkey)
    supply = float(response.value.amount) / 10**decimals
    return supply
