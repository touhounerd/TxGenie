import json
import asyncio

import aiohttp
import log

logging = log.Logger("txgenie_data_api").get_logger()


class TxGenieDataAPI:
    def __init__(self):
        self.base_url = "opensource-soon"
        # aiohttp ClientSession can be reused concurrently
        self._session: aiohttp.ClientSession = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30)
        )

    async def close(self):
        """
        Close aiohttp session
        """
        try:
            await self._session.close()
        except Exception:
            pass

    async def _make_request(self, endpoint: str, params: dict = None) -> dict | None:
        """
        Make async HTTP request
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            # Make async request
            async with self._session.get(url, params=params) as response:
                response.raise_for_status()
                text_body = await response.text()        # Read body as text first
                data = json.loads(text_body)             # Parse text as JSON
                return data

        except aiohttp.ClientError as e:
            logging.error(f"Request failed: {e}")
            return None

    async def get_token_metadata(self, contract_address: str, chain_id: int) -> dict | None:
        """
        Get token metadata for given contract address and chain ID
        """
        endpoint = "opensource-soon"
        params = {"contractAddress": contract_address, "chainId": chain_id}
        data = await self._make_request(endpoint, params)
        return data

if __name__ == "__main__":
    async def main():
        api = TxGenieDataAPI()
        try:
            tasks = [
                api.get_token_metadata(contract_address="", chain_id=56)
            ]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for res in results:
                print(json.dumps(res, ensure_ascii=False, indent=2))
        finally:
            await api.close()

    asyncio.run(main())