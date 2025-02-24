from dotenv import dotenv_values
from langchain.schema import HumanMessage
from langchain_openai import AzureChatOpenAI
from pydantic import SecretStr

env = dotenv_values(".env")
api_version = "2024-12-01-preview"
base_url = env["AZURE_AI_FOUNDRY_ENDPOINT"]
api_key = SecretStr(env["AZURE_AI_FOUNDRY_API_KEY"] or "")

o1 = AzureChatOpenAI(
    azure_deployment="o1-crew",
    model="o1",
    api_version=api_version,
    api_key=api_key,
    azure_endpoint=base_url,
)

gpt4o = AzureChatOpenAI(
    azure_deployment="gpt-4o-3",
    model="gpt-4o",
    api_version=api_version,
    api_key=api_key,
    azure_endpoint=base_url,
)

if __name__ == "__main__":
    response = gpt4o([HumanMessage(content="Hello, world!")])
    print(response.content) # type: ignore