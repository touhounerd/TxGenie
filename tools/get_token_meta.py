from typing import Dict
from dotenv import load_dotenv  
from decimal import Decimal
from txgenie_data_api import TxGenieDataAPI
import asyncio
load_dotenv()


async def tokenbalance_processor(raw_result: str, params: dict) -> str:
    """
    raw_result: e.g. "19694417350"
    params:  {"address": "...", "contractAddress": "...", "chainid": "..."}
    """
    bn_api = TxGenieDataAPI()
    meta = await bn_api.get_token_metadata(params["contractAddress"], params["chainid"])
    await bn_api.close()
    
    token_data = meta.get("data").get("tokenAddresses", [])

    decimals = 18
    for i in token_data:
        chainid = i.get("chainId")
        if chainid == int(params["chainid"]):
            decimals = i.get("decimals")
            break

    symbol = meta.get("data", {}).get("symbol", {})
    amount = float(Decimal(raw_result) / 10**decimals)
    return {"address": params["address"], "amount": amount, "symbol": symbol}


if __name__ == "__main__":
    ret = asyncio.run(tokenbalance_processor("1623160", {"address": "", "contractAddress": "", "chainid": "1"}))
    print(ret)
