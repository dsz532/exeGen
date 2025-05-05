import json
import re

from autogen import ConversableAgent

llm_config = {
    "cache_seed": None,
    "config_list": [{
        "model": "qwen-plus",
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "api_key": "",
        "price": [0, 0]
    }]
}

examplar_gene = ConversableAgent(
    name='agent',
    llm_config=llm_config,
    system_message="who are you",
)

examplar_gene2 = ConversableAgent(
    name='agent',
    llm_config=llm_config,
    system_message="who are you",
)

chatres = examplar_gene.initiate_chat(examplar_gene2,max_turns=2)

print(chatres)
