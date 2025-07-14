from dotenv import load_dotenv
import os
from crewai_tools import RagTool
from crewai import Crew, Task, Agent, LLM

load_dotenv(override=True)

import warnings
warnings.filterwarnings('ignore')

from langfuse import Langfuse
 
langfuse = Langfuse()

if langfuse.auth_check():
    print("Langfuse client is authenticated and ready!")
else:
    print("Authentication failed. Please check your credentials and host.")

from openinference.instrumentation.crewai import CrewAIInstrumentor
from openinference.instrumentation.litellm import LiteLLMInstrumentor
 
CrewAIInstrumentor().instrument(skip_dep_check=True)
LiteLLMInstrumentor().instrument()

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
 
# Define your agents with roles and goals
insurance_agent = Agent(
    role="Senior Insurance Coverage Assistant", 
    goal="Determine whether something is covered or not",
    backstory="You are an expert insurance agent designed to assist with coverage queries",
    verbose=True,
    allow_delegation=False,
    llm=llm,
    tools=[rag_tool], 
    max_retry_limit=5
)

task1 = Task(
        description='Thời gian chờ đợi để phục hồi chức năng là bao lâu?',
        expected_output = "Một phản hồi toàn diện cho câu hỏi của người dùng",
        agent=insurance_agent
)

crew = Crew(
    agents=[insurance_agent],
    tasks=[task1],
    verbose=True
)


with langfuse.start_as_current_span(
    name="crewai-index-trace",
    ) as span:
    # Run your application here
    result = crew.kickoff()
    print(result)
 
langfuse.flush()