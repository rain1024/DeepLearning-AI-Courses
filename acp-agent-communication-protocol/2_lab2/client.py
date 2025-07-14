import nest_asyncio
nest_asyncio.apply()

from acp_sdk.client import Client
import asyncio
from colorama import Fore 

async def run_hospital_workflow() -> None:
    # input_text = "Do I need rehabilitation after a shoulder reconstruction?"
    input_text = "tôi có những quyền lợi bảo hiểm nào"
    async with Client(base_url="http://localhost:8001") as insurer, Client(base_url="http://localhost:8000") as hospital:
        run1 = await hospital.run_sync(
            agent="health_agent",
            input=input_text
        )
        content = run1.output[0].parts[0].content
        print(Fore.LIGHTMAGENTA_EX+ content + Fore.RESET)

        run2 = await insurer.run_sync(
            agent="policy_agent", input=f"Context: {content} What is the waiting period for rehabilitation?"
        )
        print(Fore.YELLOW + run2.output[0].parts[0].content + Fore.RESET)

if __name__ == "__main__":
    asyncio.run(run_hospital_workflow())