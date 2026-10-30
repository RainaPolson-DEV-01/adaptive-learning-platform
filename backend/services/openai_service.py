import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

_client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version="2024-02-01",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)


def get_client():
    return _client


def get_model_name():
    return os.getenv("GPT_DEPLOYMENT")