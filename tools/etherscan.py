from decimal import Decimal
from data.meta_data import native_token_map

def native_token_balance_processor(raw_result: str, raw_kwargs: dict) -> str:
    """
    raw_result: The balance returned by the node (a string in wei format)
    raw_kwargs: {"address": "...", "chainid": "..."}
    """
    chainid = raw_kwargs.get("chainid", "")
    amount_in_eth = Decimal(raw_result) / 10**18
    symbol = native_token_map.get(str(chainid), "ETH")
    return f"{amount_in_eth:.6f} {symbol}"
