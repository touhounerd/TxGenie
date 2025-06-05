import os
import inspect
from decimal import Decimal
from typing import Dict, Any, List, Optional, Annotated
from mcp.server import FastMCP
from eth_utils import is_address, to_checksum_address
from dotenv import load_dotenv
from datetime import datetime
from tools.web_search import web_search_handler
from pydantic import Field
import aiohttp
from tools.etherscan import native_token_balance_processor

load_dotenv()

app = FastMCP('mcp-proxy', log_level="INFO")
PROXY = os.getenv("HTTP_PROXY", None)

API_CONFIG = {
    "search": {
        "web_search":{
            "required_params": ["query"],
            "param_descriptions": {
                "query": "search query",
            },
            "description": "Execute internet search, such as news, data, technical documents, market analysis, etc. Do not use internet search to get token exchange prices. query is the search query.",
            "handler": web_search_handler
        }
    },
    "account": {
        "balance": {
            "required_params": ["address", "chainid"],
            "optional_params": {},
            "param_descriptions": {
                "address": "blockchain address",
                "chainid": "blockchain ID"
            },
            "description": "Query the native token balance of the address. address is a strict address; chainid is the blockchain ID, type is string.",
            "result_processor": native_token_balance_processor
        },
        "txlist": {
            "required_params": ["address", "chainid"],
            "param_descriptions": {
                "address": "blockchain address",
                "chainid": "blockchain ID",
            },
            "optional_params": {
                "startblock": None,
                "endblock": None,
                "page": 1,
                "offset": 10,
                "sort": "asc"
            },
            "description": "Get normal transaction records, address is the address, chainid is the blockchain ID, type is string.",
            "result_processor": lambda r: [{
                **tx,
                "value": str(Decimal(tx["value"]) / 10**18),
                "timeStamp": datetime.fromtimestamp(int(tx["timeStamp"]))
            } for tx in r]
        },
        "balancemulti": {
            "required_params": ["addresses", "chainid"],
            "optional_params": {"tag": "latest"},
            "param_descriptions": {
                "addresses": "blockchain address list",
                "chainid": "blockchain ID",
                "tag": "Specifies the block number or state at which to retrieve data."
            },
            "description": "Batch query ETH balance, addresses is the address list",
            "result_processor": lambda r: {acc["account"]: f"{Decimal(acc['balance']) / 10**18:.6f} ETH" for acc in r}
        },
        "txtoken": {
            "required_params": ["address", "chainid"],
            "optional_params": {
                "contractAddress": None,
                "page": 1,
                "offset": 10,
                "sort": "asc"
            },
            "param_descriptions": {
                "address": "blockchain address",
                "contractAddress": "token contract address",
                "chainid": "blockchain ID",
            },
            "description": "Get ERC20 token transfer records, address is the address, chainid is the blockchain ID, type is string.",
            "result_processor": lambda r: [{
                **tx,
                "value": str(Decimal(tx["value"]) / 10**int(tx["tokenDecimal"]))
            } for tx in r]
        }
    },
    "contract": {
        "getabi": {
            "required_params": ["address", "chainid"],
            "optional_params": {},
            "param_descriptions": {
                "address": "contract address",
                "chainid": "blockchain ID",
            },
            "description": "Get contract ABI, address is the contract address, chainid is the blockchain ID, type is string.",
            "result_processor": lambda r: r if r != "Contract source code not verified" else None
        },
        "getsourcecode": {
            "required_params": ["address", "chainid"],
            "optional_params": {},
            "param_descriptions": {
                "address": "contract address",
                "chainid": "blockchain ID",
            },
            "description": "Get contract source code, address is the contract address, chainid is the blockchain ID, type is string.",
            "result_processor": lambda r: r[0] if r else None
        }
    },
    "transaction": {
        "getstatus": {
            "required_params": ["txhash", "chainid"],
            "optional_params": {},
            "param_descriptions": {
                "txhash": "transaction hash",
                "chainid": "blockchain ID",
            },
            "description": "Get transaction execution status, txhash is the transaction hash, if it shows failure, it may be in pending state, tell the user that the transaction failed or is executing, the user needs to check the transaction status themselves, chainid is the blockchain ID, type is string.",
            "result_processor": lambda r: "success" if r == "1" else "failed or executing"
        },
        "gettxreceiptstatus": {
            "required_params": ["txhash", "chainid"],
            "optional_params": {},
            "param_descriptions": {
                "txhash": "transaction hash",
                "chainid": "blockchain ID",
            },
            "description": "Get transaction receipt status, txhash is the transaction hash, if it shows failure, it may be in pending state, tell the user that the transaction failed or is executing, the user needs to check the transaction status themselves, chainid is the blockchain ID, type is string.",
            "result_processor": lambda r: "success" if r == "1" else "failed or executing"
        }
    },
    "block": {
        "getblockreward": {
            "required_params": ["blockno", "chainid"],
            "optional_params": {},
            "description": "Get block reward information, blockno is the block number, chainid is the blockchain ID, type is string.",
            "param_descriptions": {
                "blockno": "block number",
                "chainid": "blockchain ID",
            },
            "result_processor": lambda r: {
                "blockReward": str(Decimal(r["blockReward"]) / 10**18),
                "timeStamp": datetime.fromtimestamp(int(r["timeStamp"]))
            }
        },
        "getblockcountdown": {
            "required_params": ["blockno", "chainid"],
            "optional_params": {},
            "description": "Get block countdown, blockno is the block number, chainid is the blockchain ID, type is string.",
            "param_descriptions": {
                "blockno": "block number",
                "chainid": "blockchain ID",
            },
            "result_processor": lambda r: f"{r['EstimateTimeInSec']}秒"
        }
    },
    "logs": {
        "getLogs": {
            "required_params": ["fromBlock", "toBlock", "address", "chainid"],
            "optional_params": {
                "topic0": None,
                "topic1": None,
                "topic0_1_opr": None,
                "page": 1,
                "offset": 10
            },
            "param_descriptions": {
                "fromBlock": "start block number",
                "toBlock": "end block number",
                "address": "contract address",
                "chainid": "blockchain ID",
            },
            "description": "Query event logs, fromBlock is the start block number, toBlock is the end block number, address is the contract address, chainid is the blockchain ID, type is string.",
            "result_processor": lambda r: [{
                **log,
                "timeStamp": datetime.fromtimestamp(int(log["timeStamp"]))
            } for log in r]
        }
    },
    "proxy": {
        "eth_blockNumber": {
            "required_params": ["chainid"],
            "optional_params": {},
            "description": "Get the latest block number, chainid is the blockchain ID, type is string.",
            "param_descriptions": {
                "chainid": "blockchain ID",
            },
            "result_processor": lambda r: int(r, 16)
        },
        "eth_getTransactionByHash": {
            "required_params": ["txhash", "chainid"],
            "optional_params": {},
            "description": "Get transaction details by hash, txhash is the transaction hash, chainid is the blockchain ID, type is string.",
            "param_descriptions": {
                "txhash": "transaction hash",
                "chainid": "blockchain ID",
            },
            "result_processor": lambda r: {
                **r,
                "value": str(Decimal(r["value"]) / 10**18) if r else None
            }
        }
    },
    "stats": {
        "ethsupply": {
            "required_params": ["chainid"],
            "optional_params": {},
            "description": "Get ETH total supply, chainid is the blockchain ID, type is string, and chainid must be '1' for this function.",
            "result_processor": lambda r: f"{Decimal(r) / 10**18:.2f} ETH"
        }
    },
    "gastracker": {
        "gasoracle": {
            "required_params": ["chainid"],
            "optional_params": {},
            "description": "Get Gas price oracle data, chainid is the blockchain ID, type is string.",
            "result_processor": lambda r: {
                "SafeGasPrice": int(r["SafeGasPrice"]),
                "ProposeGasPrice": int(r["ProposeGasPrice"]),
                "FastGasPrice": int(r["FastGasPrice"])
            }
        }
    }
}


class McpProxy:
    def __init__(self):
        self.api_key = os.getenv("ETHERSCAN_API_KEY")
        self.base_url = "https://api.etherscan.io/v2/api/"

    async def _make_request(self, module: str, action: str, **params):
        """main request entry"""
        params.update({
            "module": module,
            "action": action,
            "chainid":params["chainid"],
            "apikey": self.api_key
        })
        
        # use async with to ensure client aclose() is triggered
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url, params=params, proxy=PROXY) as response:
                response.raise_for_status()
                result = await response.json()

        if result.get("status") == "1" or result.get("result"):
            return result
        raise ValueError(result.get("message", "Unknown error"))
    

import inspect
from inspect import Signature, Parameter

def create_tool_function(module: str, action: str, config: Dict):
    # get parameter description configuration
    param_descriptions = config.get("param_descriptions", {})
    # generate enhanced parameter signature
    params = []
    # merge required and optional parameters
    required_params = config.get("required_params", [])
    optional_params = config.get("optional_params", {})

    # generate parameter signature with default values
    params = []
    for p in required_params:
        # create Field metadata for each parameter
        field_info = Field(..., 
                         title=p.capitalize(),
                         description=param_descriptions.get(p, ""))
        params.append(
            Parameter(p, Parameter.POSITIONAL_OR_KEYWORD,
                     annotation=Annotated[str, field_info])
        )
    for p, default in optional_params.items():
        # create Field metadata for each parameter
        field_info = Field(..., 
                         title=p.capitalize(),
                         description=param_descriptions.get(p, ""))
        params.append(Parameter(p, Parameter.KEYWORD_ONLY, default=default, annotation=Optional[str]))

    # define actual execution logic
    async def generated_function(**raw_kwargs):
        # check required parameters
        for p in required_params:
            if p not in raw_kwargs:
                raise ValueError(f"Missing required parameter: {p}")

        proxy = McpProxy()
        # handle address checksum
        processed = {}
        for k, v in raw_kwargs.items():
            if k.endswith("address") and is_address(v):
                processed[k] = to_checksum_address(v)
            else:
                processed[k] = v

        # if onChain module, just return method+Args format
        # only keep allowed fields
        allowed = set(required_params) | set(optional_params.keys())
        filtered_args = {k: processed[k] for k in processed if k in allowed}
        # handle on-chain module
        if module == "onChain":
            return {
                "method": action,
                "args": processed
            }
        
        result = await proxy._make_request(module, action, **processed)

        if module != "onChain" and "result_processor" in config:
            processor = config["result_processor"]
            sig = inspect.signature(processor)
            if inspect.iscoroutinefunction(processor):
                if len(sig.parameters) == 1:
                    return await processor(result["result"])
                else:
                    return await processor(result["result"], raw_kwargs)
            else:
                # normal synchronous function
                if len(sig.parameters) == 1:
                    return processor(result["result"])
                else:
                    return processor(result["result"], raw_kwargs)
                
        # if no result_processor, just return result["result"]
        return result.get("result", None)

    # set function signature
    generated_function.__signature__ = Signature(params)
    generated_function.__annotations__ = {p: str for p in required_params}
    generated_function.__annotations__.update({p: Optional[str] for p in optional_params})
    # set function name
    generated_function.__name__ = f"{module}_{action}_input"
    return generated_function


registered_tools = {}

# register tools
for module, actions in API_CONFIG.items():
    for action, config in actions.items():
        tool_name = f"{module}_{action}"
        tool_description = config.get("description", "")
        func = create_tool_function(module, action, config)
        app.tool(name=tool_name, description=tool_description)(func)
        registered_tools[tool_name] = func


if __name__ == "__main__":
    app.run(transport='stdio')
    