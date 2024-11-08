from openai import OpenAI
from os import getenv
from autogen import *
from pyexpat.errors import messages


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

agent_kt = ConversableAgent(  # 知识追踪代理
    name="agent_kt",
    llm_config=llm_config,
    system_message="",
)

agent_exeGen_generator = ConversableAgent(  # 习题生成代理
    name="agent_exeGen_generator",
    llm_config=llm_config,
    system_message="",
)

# 5个习题评判专家
agent_exeGen_discriminator_1 = ConversableAgent(
    name="agent_exeGen_discriminator",
    llm_config=llm_config,
    system_message="",
)

agent_exeGen_discriminator_2 = ConversableAgent(
    name="agent_exeGen_discriminator",
    llm_config=llm_config,
    system_message="",
)

agent_exeGen_discriminator_3 = ConversableAgent(
    name="agent_exeGen_discriminator",
    llm_config=llm_config,
    system_message="",
)

agent_exeGen_discriminator_4 = ConversableAgent(
    name="agent_exeGen_discriminator",
    llm_config=llm_config,
    system_message="",
)

agent_exeGen_discriminator_5 = ConversableAgent(
    name="agent_exeGen_discriminator",
    llm_config=llm_config,
    system_message="",
)

discriminators = autogen.Generator(  # 习题评判专家组
    agents=[agent_exeGen_discriminator_1, agent_exeGen_discriminator_2, agent_exeGen_discriminator_3,
            agent_exeGen_discriminator_4, agent_exeGen_discriminator_5], messages=[], max_round=12)

chatManager = GroupChatManager(
    generator=discriminators,
    llm_config=llm_config
)

agent_host = ConversableAgent(
    name="agent_kt",
    llm_config=llm_config,
    system_message="",
)
