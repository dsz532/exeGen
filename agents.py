from openai import OpenAI
from os import getenv
from autogen import *

# gets API Key from environment variable OPENAI_API_KEY
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
)

llm_config = {
    "config_list": [{
        "model": "openai/gpt-3.5-turbo",
        "base_url": "https://openrouter.ai/api/v1",
        "api_key": "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"
    }]
}

conversable_agent = ConversableAgent(
    name="111",
    llm_config=llm_config,
    system_message="I'm an openai assistant running in autogen",
)


