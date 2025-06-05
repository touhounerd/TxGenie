chain_id_map = {
  "1": "Ethereum",
  "56": "BNB Smart Chain",
  "43114": "Avalanche C-Chain",
  "137": "Polygon",
  "250": "Fantom Opera",
  "42161": "Arbitrum One",
  "10": "Optimism",
  "1101": "Polygon zkEVM",
  "25": "Cronos",
  "80094": "Berachain",
  "8453": "Base",
  "146": "Sonic",
  "999": "HyperEVM",
  "-1": "Solana"
}

cmc_chain_id_map = {
  "1":   "Ethereum",
  "56":  "BNB Smart Chain (BEP20)",
  "43114":"Avalanche C-Chain",
  "137": "Polygon",
  "250": "Fantom (Migrated to Sonic)",
  "42161":"Arbitrum",
  "10":  "Optimism",
  "1101":"Polygon zkEVM",
  "25":  "Cronos",
  "-1":  "Solana",
  "80094": "Berachain",
  "8453": "Base",
  "146": "Sonic",
  "999": "HyperEVM"
}

native_token_map = {
    "1": "ETH",         # Ethereum
    "56": "BNB",        # BNB Smart Chain
    "43114": "AVAX",    # Avalanche C-Chain
    "137": "MATIC",     # Polygon
    "250": "FTM",       # Fantom Opera
    "42161": "ETH",     # Arbitrum One
    "10": "ETH",        # Optimism
    "1101": "ETH",      # Polygon zkEVM
    "25": "CRO",        # Cronos
    "80094": "BERA",    # Berachain
    "8453": "ETH",      # Base
    "146": "SONIC",     # Sonic
    "999": "HYPE",      # HyperEVM
    "-1": "SOL"         # Solana
}


debank_chain_list = [
    {
        "id": "eth",
        "community_id": 1,
        "name": "Ethereum",
        "native_token_id": "eth",
        "logo_url": "https://static.debank.com/image/chain/logo_url/eth/42ba589cd077e7bdd97db6480b0ff61d.png",
        "wrapped_token_id": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
        "is_support_pre_exec": True
    },
    {
        "id": "bsc",
        "community_id": 56,
        "name": "BNB Chain",
        "native_token_id": "bsc",
        "logo_url": "https://static.debank.com/image/chain/logo_url/bsc/bc73fa84b7fc5337905e527dadcbc854.png",
        "wrapped_token_id": "0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c",
        "is_support_pre_exec": True
    },
    {
        "id": "base",
        "community_id": 8453,
        "name": "Base",
        "native_token_id": "base",
        "logo_url": "https://static.debank.com/image/chain/logo_url/base/ccc1513e4f390542c4fb2f4b88ce9579.png",
        "wrapped_token_id": "0x4200000000000000000000000000000000000006",
        "is_support_pre_exec": True
    },
    {
        "id": "arb",
        "community_id": 42161,
        "name": "Arbitrum",
        "native_token_id": "arb",
        "logo_url": "https://static.debank.com/image/chain/logo_url/arb/854f629937ce94bebeb2cd38fb336de7.png",
        "wrapped_token_id": "0x82af49447d8a07e3bd95bd0d56f35241523fbab1",
        "is_support_pre_exec": True
    },
    {
        "id": "matic",
        "community_id": 137,
        "name": "Polygon",
        "native_token_id": "matic",
        "logo_url": "https://static.debank.com/image/chain/logo_url/matic/52ca152c08831e4765506c9bd75767e8.png",
        "wrapped_token_id": "0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270",
        "is_support_pre_exec": True
    },
    {
        "id": "avax",
        "community_id": 43114,
        "name": "Avalanche",
        "native_token_id": "avax",
        "logo_url": "https://static.debank.com/image/chain/logo_url/avax/4d1649e8a0c7dec9de3491b81807d402.png",
        "wrapped_token_id": "0xb31f66aa3c1e785363f0875a1b74e27b85fd66c7",
        "is_support_pre_exec": True
    },
    {
        "id": "op",
        "community_id": 10,
        "name": "OP",
        "native_token_id": "op",
        "logo_url": "https://static.debank.com/image/chain/logo_url/op/01ae734fe781c9c2ae6a4cc7e9244056.png",
        "wrapped_token_id": "0x4200000000000000000000000000000000000006",
        "is_support_pre_exec": True
    },
    {
        "id": "b2",
        "community_id": 223,
        "name": "B²",
        "native_token_id": "b2",
        "logo_url": "https://static.debank.com/image/chain/logo_url/b2/6ca6c8bc33af59c5b9273a2b7efbd236.png",
        "wrapped_token_id": "0x4200000000000000000000000000000000000006",
        "is_support_pre_exec": True
    },
    {
        "id": "mnt",
        "community_id": 5000,
        "name": "Mantle",
        "native_token_id": "mnt",
        "logo_url": "https://static.debank.com/image/chain/logo_url/mnt/0af11a52431d60ded59655c7ca7e1475.png",
        "wrapped_token_id": "0x78c1b0c915c4faa5fffa6cabf0219da63d7f4cb8",
        "is_support_pre_exec": True
    },
    {
        "id": "ftm",
        "community_id": 250,
        "name": "Fantom",
        "native_token_id": "ftm",
        "logo_url": "https://static.debank.com/image/chain/logo_url/ftm/14133435f89637157a4405e954e1b1b2.png",
        "wrapped_token_id": "0x21be370d5312f44cb42ce377bc9b8a0cef1a4c83",
        "is_support_pre_exec": True
    },
    {
        "id": "sonic",
        "community_id": 146,
        "name": "Sonic",
        "native_token_id": "sonic",
        "logo_url": "https://static.debank.com/image/chain/logo_url/sonic/f4e61549f8f73ca5ec3bab454575410c.png",
        "wrapped_token_id": "0x039e2fb66102314ce7b64ce5ce3e5183bc94ad38",
        "is_support_pre_exec": True
    },
    {
        "id": "cro",
        "community_id": 25,
        "name": "Cronos",
        "native_token_id": "cro",
        "logo_url": "https://static.debank.com/image/chain/logo_url/cro/f947000cc879ee8ffa032793808c741c.png",
        "wrapped_token_id": "0x5c7f8a570d578ed84e63fdfa7b1ee72deae1ae23",
        "is_support_pre_exec": True
    },
    {
        "id": "core",
        "community_id": 1116,
        "name": "CORE",
        "native_token_id": "core",
        "logo_url": "https://static.debank.com/image/chain/logo_url/core/ccc02f660e5dd410b23ca3250ae7c060.png",
        "wrapped_token_id": "0x40375c92d9faf44d2f9db9bd9ba41a3317a2404f",
        "is_support_pre_exec": True
    },
    {
        "id": "xdai",
        "community_id": 100,
        "name": "Gnosis Chain",
        "native_token_id": "xdai",
        "logo_url": "https://static.debank.com/image/chain/logo_url/xdai/43c1e09e93e68c9f0f3b132976394529.png",
        "wrapped_token_id": "0xe91d153e0b41518a2ce8dd3d7944fa863463a97d",
        "is_support_pre_exec": True
    },
    {
        "id": "blast",
        "community_id": 81457,
        "name": "Blast",
        "native_token_id": "blast",
        "logo_url": "https://static.debank.com/image/chain/logo_url/blast/15132294afd38ce980639a381ee30149.png",
        "wrapped_token_id": "0x4300000000000000000000000000000000000004",
        "is_support_pre_exec": True
    },
    {
        "id": "merlin",
        "community_id": 4200,
        "name": "Merlin",
        "native_token_id": "merlin",
        "logo_url": "https://static.debank.com/image/chain/logo_url/merlin/458e4686dfb909ba871bd96fe45417a8.png",
        "wrapped_token_id": "0xf6d226f9dc15d9bb51182815b320d3fbe324e1ba",
        "is_support_pre_exec": False
    },
    {
        "id": "mode",
        "community_id": 34443,
        "name": "Mode",
        "native_token_id": "mode",
        "logo_url": "https://static.debank.com/image/chain/logo_url/mode/466e6e12f4fd827f8f497cceb0601a5e.png",
        "wrapped_token_id": "0x4200000000000000000000000000000000000006",
        "is_support_pre_exec": True
    },
    {
        "id": "taiko",
        "community_id": 167000,
        "name": "Taiko",
        "native_token_id": "taiko",
        "logo_url": "https://static.debank.com/image/chain/logo_url/taiko/7723fbdb38ef181cd07a8b8691671e6b.png",
        "wrapped_token_id": "0xa51894664a773981c6c112c43ce576f315d5b1b6",
        "is_support_pre_exec": True
    },
    {
        "id": "linea",
        "community_id": 59144,
        "name": "Linea",
        "native_token_id": "linea",
        "logo_url": "https://static.debank.com/image/chain/logo_url/linea/32d4ff2cf92c766ace975559c232179c.png",
        "wrapped_token_id": "0xe5d7c2a44ffddf6b295a15c148167daaaf5cf34f",
        "is_support_pre_exec": True
    },
    {
        "id": "klay",
        "community_id": 8217,
        "name": "Kaia",
        "native_token_id": "klay",
        "logo_url": "https://static.debank.com/image/chain/logo_url/klay/4182ee077031d843a57e42746c30c072.png",
        "wrapped_token_id": "0xe4f05a66ec68b54a58b17c22107b02e0232cc817",
        "is_support_pre_exec": True
    },
    {
        "id": "era",
        "community_id": 324,
        "name": "zkSync Era",
        "native_token_id": "era",
        "logo_url": "https://static.debank.com/image/chain/logo_url/era/2cfcd0c8436b05d811b03935f6c1d7da.png",
        "wrapped_token_id": "0x5aea5775959fbc2557cc8789bc1bf90a239d9a91",
        "is_support_pre_exec": True
    },
    {
        "id": "scrl",
        "community_id": 534352,
        "name": "Scroll",
        "native_token_id": "scrl",
        "logo_url": "https://static.debank.com/image/chain/logo_url/scrl/1fa5c7e0bfd353ed0a97c1476c9c42d2.png",
        "wrapped_token_id": "0x5300000000000000000000000000000000000004",
        "is_support_pre_exec": True
    },
    {
        "id": "manta",
        "community_id": 169,
        "name": "Manta Pacific",
        "native_token_id": "manta",
        "logo_url": "https://static.debank.com/image/chain/logo_url/manta/0e25a60b96a29d6a5b9e524be7565845.png",
        "wrapped_token_id": "0x0dc808adce2099a9f62aa87d9670745aba741746",
        "is_support_pre_exec": True
    },
    {
        "id": "celo",
        "community_id": 42220,
        "name": "Celo",
        "native_token_id": "celo",
        "logo_url": "https://static.debank.com/image/chain/logo_url/celo/faae2c36714d55db1d7a36aba5868f6a.png",
        "wrapped_token_id": "0x471ece3750da237f93b8e339c536989b8978a438",
        "is_support_pre_exec": True
    },
    {
        "id": "metis",
        "community_id": 1088,
        "name": "Metis",
        "native_token_id": "metis",
        "logo_url": "https://static.debank.com/image/chain/logo_url/metis/7485c0a61c1e05fdf707113b6b6ac917.png",
        "wrapped_token_id": "0x75cb093e4d61d2a2e65d8e0bbb01de8d89b53481",
        "is_support_pre_exec": True
    }
]