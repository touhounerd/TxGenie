# TxGenie

[**TxGenie**](https://txgenie.ai/) is a modular Python-based assistant designed to explore the world of cryptocurrencies and decentralized finance (DeFi). It provides tools for transaction analysis, data extraction, and intelligent prompt generation to help users better understand and interact with blockchain ecosystems. By open-sourcing the core of MCP, we aim to foster deeper synergy between AI and blockchain — empowering the emergence of truly crypto-native, intelligent agents.

---

## ✨ Features

- **Multi-chain Compatibility**: TxGenie supports most mainstream blockchains. To query across different networks, just modify the chainid parameter in your API request.
- **Multi-functional Integration**: Combines transaction analysis, natural language generation, and prompt templating.
- **Modular Architecture**: Well-structured and easy to extend or maintain.
- **Developer-Friendly**: Ideal for building DeFi dashboards, analytics tools, or AI-powered blockchain assistants.

---

## 📁 Project Structure

```
TxGenie/
├── data/             # Blockchain meta data
├── tools/            # MCP tools
├── client.py         # Main MCP client
├── mcp_proxy.py      # MCP servers
├── prompt.py         # Prompt generation and management
├── log.py            # log module
├── requirements.txt  # Python dependencies
├── .env              # API keys and environment variables
└── README.md         # Project documentation
```

---

## 🚀 Getting Started

1. **Clone the Repository**

   ```bash
   git clone https://github.com/touhounerd/TxGenie.git
   cd TxGenie
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**

   Create `.env` file with your API keys:
   ```bash
   LLM_API_KEY=
   LLM_BASE_URL=
   LLM_MODEL=
   
   ETHERSCAN_API_KEY=
   BOCHA_API_KEY=
   HTTP_PROXY=
   ```

5. **Run the Client**

   ```bash
   python client.py
   ```

---

## 🧠 Use Cases

- Ask about the latest trends in blockchain or AI.
- Query wallet balances on supported blockchains.
- Retrieve and understand smart contract ABIs.
- Generate natural language explanations for blockchain activity.
- Power dashboards or bots for DeFi analytics and education.

---

## 🔧 Example Usage

### Run the client:

```bash
python client.py
```

### Access via Postman (HTTP POST)

**Endpoint:**
```
http://0.0.0.0:8861/query_stream
```

**Request Payload:** (Query Vitalik's ETH balance)

```json
{
  "address": "0xd8da6bf26964af9d7eed9e03e53415d37aa96045",
  "msg": [
    {
      "role": "user",
      "content": "How much ETH do I have"
    }
  ],
  "chainid": "1"
}
```

**Response Example:**

```json
{
    "type": "final",
    "data": {
        "status": 0,
        "msg": "You currently have **0.1545 ETH** in your Ethereum wallet.",
        "onChainCalls": []
    },
    "timestamp": 1749139999.9931355
}
```

---

## 🧪 Coming Soon
The following features will be open-sourced soon：
- Web3 wallet integration for on-chain execution
- Social media sentiment analysis tool
- On-chain address profiling toolkit
- Liquidity pool analysis module
- DeFi protocol insight tool

---

## 🤝 Contributing

We welcome contributions! To get involved:

1. **Fork the repository**
2. **Create a feature branch**:

   ```bash
   git checkout -b feature/your-feature
   ```

3. **Commit your changes**:

   ```bash
   git commit -m "Add feature"
   ```

4. **Push to your fork**:

   ```bash
   git push origin feature/your-feature
   ```

5. **Create a Pull Request**

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
