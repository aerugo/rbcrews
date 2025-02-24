import os

from crewai import LLM
from dotenv import load_dotenv
from langchain.schema import HumanMessage
from langchain_openai import AzureChatOpenAI

load_dotenv()
api_version = "2024-12-01-preview"
base_url = os.environ.get("AZURE_AI_FOUNDRY_ENDPOINT")
api_key = os.environ.get("AZURE_AI_FOUNDRY_API_KEY", default="")

_o1 = AzureChatOpenAI(
    azure_deployment="o1-crew",
    api_version=api_version,
    model="o1",
)

o1 = LLM(
    model="azure/o1-crew",  # Use the full deployment name
    api_key=os.environ.get("AZURE_AI_FOUNDRY_API_KEY"),
    base_url=os.environ.get("AZURE_AI_FOUNDRY_ENDPOINT"),
    api_version="2024-12-01-preview"
)

_gpt4o = AzureChatOpenAI(
    azure_deployment="gpt-4o-3",
    api_version=api_version,
    model="gpt-4o",
    temperature=0.9,
)

gpt4o = LLM(
    model="azure/o1-crew",  # Use the full deployment name
    api_key=os.environ.get("AZURE_AI_FOUNDRY_API_KEY"),
    base_url=os.environ.get("AZURE_AI_FOUNDRY_ENDPOINT"),
    api_version="2024-12-01-preview"
)

def get_azure_llm(llm_name: str) -> LLM:
    if llm_name == "o1":
        return o1
    elif llm_name == "gpt4o":
        return gpt4o
    else:
        raise ValueError(f"Unknown LLM name: {llm_name}")

if __name__ == "__main__":
    response = get_azure_llm("gpt4o")([HumanMessage(content="Hello, world!")])
    print(response.content) # type: ignore