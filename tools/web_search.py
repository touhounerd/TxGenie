import os
import time
import json
import asyncio
import aiohttp
from dotenv import load_dotenv
import log

logging = log.Logger("web_search").get_logger()
load_dotenv()

COUNT = 20

async def web_search_handler(query: str) -> str:
    t0 = time.time()
    url = "https://api.bochaai.com/v1/web-search"

    payload = {
        "query": query,
        "summary": True,
        "count": COUNT,
        "page": 1
    }

    headers = {
        "Authorization": "Bearer " + os.getenv("BOCHA_API_KEY", ""),
        "Content-Type": "application/json"
    }

    ret = ""
    result_num = 0

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as response:
                response.raise_for_status()
                data = await response.json()
                items = data.get("data", {}).get("webPages", {}).get("value", [])

                unwanted = {
                    "snippet",
                    "siteIcon",
                    "cachedPageUrl",
                    "language",
                    "isFamilyFriendly",
                    "isNavigational",
                }
                filtered = [
                    {k: v for k, v in entry.items() if k not in unwanted}
                    for entry in items
                ]
                result_num = len(filtered)
                ret = json.dumps(filtered, ensure_ascii=False)

    except Exception as e:
        logging.error(f"Web search error: {e}")
        ret = ""
        result_num = 0

    elapsed = time.time() - t0
    logging.info(f"query={query} ｜result_num={result_num} ｜use time={elapsed:.2f} seconds")
    return ret


if __name__ == "__main__":
    async def main():
        query = "Who is Nakamoto?"
        result = await web_search_handler(query)
        print(result)

    asyncio.run(main())
