from langchain_openai import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from operator import itemgetter
import os
from dotenv import load_dotenv
from langfuse import Langfuse


load_dotenv(override=True)
 
prompt1 = ChatPromptTemplate.from_template(
    "What {type} is easiest to learn but hardest to master? Give a step by step approach of your thoughts, ending in your answer"
)
prompt2 = ChatPromptTemplate.from_template(
    "How {type} can be learned in 21 days? respond in {language}"
)
model = AzureChatOpenAI(
    deployment_name=os.getenv("AZURE_DEPLOYMENT_NAME"),
    model_name=os.getenv("AZURE_DEPLOYMENT_NAME"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)
chain1 = prompt1 | model | StrOutputParser()
chain2 = (
    {"type": chain1, "language": itemgetter("language")}
    | prompt2
    | model
    | StrOutputParser()
)

langfuse = Langfuse(
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    host=os.getenv("LANGFUSE_HOST")
)
trace = langfuse.trace(name="chain_of_thought_example", user_id="user-1234")
 
# Create a handler scoped to this trace
langfuse_handler = trace.get_langchain_handler()
 
# First run
answer = chain2.invoke(
    {"type": "business", "language": "german"}, config={"callbacks": [langfuse_handler]}
)
print(answer)
 
# Second run
chain2.invoke(
    {"type": "business", "language": "english"}, config={"callbacks": [langfuse_handler]}
)