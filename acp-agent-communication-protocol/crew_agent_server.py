from collections.abc import AsyncGenerator
from acp_sdk.models import Message, MessagePart
from acp_sdk.server import RunYield, RunYieldResume, Server
from dotenv import load_dotenv

from crewai import Crew, Task, Agent, LLM
from crewai_tools import RagTool
from langfuse import Langfuse
from openinference.instrumentation.crewai import CrewAIInstrumentor
from openinference.instrumentation.litellm import LiteLLMInstrumentor
 
CrewAIInstrumentor().instrument(skip_dep_check=True)
LiteLLMInstrumentor().instrument()

load_dotenv(override=True)
langfuse = Langfuse()

if langfuse.auth_check():
    print("Langfuse client is authenticated and ready!")
else:
    print("Authentication failed. Please check your credentials and host.")

import nest_asyncio
nest_asyncio.apply()

server = Server()

llm = LLM(model="azure/gpt-4.1", max_tokens=1024)

config = {
    "llm": {
        "provider": "azure_openai",
        "config": {
            "model": "gpt-4.1-mini",
        }
    },
    "embedding_model": {
        "provider": "azure_openai",
        "config": {
            "model": "text-embedding-ada-002"
        }
    }
}

rag_tool = RagTool(config=config,  
    chunk_size=1200,       
    chunk_overlap=200,     
)

rag_tool.add("./data/gold-hospital-and-premium-extras.pdf", data_type="pdf_file")


@server.agent()
async def policy_agent(input: list[Message]) -> AsyncGenerator[RunYield, RunYieldResume]:
    "This is an agent for questions around policy coverage, it uses a RAG pattern to find answers based on policy documentation. Use it to help answer questions on coverage and waiting periods."

    insurance_agent = Agent(
        role="Senior Insurance Coverage Assistant", 
        goal="Determine whether something is covered or not",
        backstory="You are an expert insurance agent designed to assist with coverage queries",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[rag_tool], 
        max_retry_limit=5)
    
    task1 = Task(
         description=input[0].parts[0].content,
         expected_output = "A comprehensive response as to the users question",
         agent=insurance_agent
    )
    crew = Crew(agents=[insurance_agent], tasks=[task1], verbose=True)
    with langfuse.start_as_current_span(name="crewai-insurance-service-trace"):
        result = crew.kickoff()
        task_output = await crew.kickoff_async()
        print(result)
        yield Message(parts=[MessagePart(content=str(task_output))])
    langfuse.flush()    

if __name__ == "__main__":
    server.run(port=8001)