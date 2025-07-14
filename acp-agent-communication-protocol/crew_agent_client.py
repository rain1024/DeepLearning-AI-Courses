import nest_asyncio
nest_asyncio.apply()

import os
# url = os.environ.get('DLAI_LOCAL_URL').format(port=8888)

from acp_sdk.client import Client
import asyncio
from colorama import Fore 

async def example() -> None:
    async with Client(base_url="http://localhost:8001") as client:
        run = await client.run_sync(
            agent="policy_agent",
            # input="What is the waiting period for rehabilitation?"
            input="Chi phí bảo hiểm là bao nhiêu"
        )
        print(Fore.YELLOW + run.output[0].parts[0].content + Fore.RESET)

if __name__ == "__main__":
    asyncio.run(example())