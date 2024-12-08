from agents import *

agent_kt.description = "a knowledge tracking expert"
agent_exeGen_generator.description = "an exercise generation expert"
agent_exeGen_discriminator.description = "an exercise evaluation expert"
agent_host.description = "moderator of this meeting"

groupchat = GroupChat(
    agents=[agent_kt, agent_exeGen_generator, agent_exeGen_discriminator, agent_host],
    messages=[],
    max_round=6,
    send_introductions=True,
)

groupchat_manager = GroupChatManager(
    groupchat=groupchat,
    llm_config=llm_config,
)

file = open("test.txt", "r")
text = file.read()

chat_res = agent_host.initiate_chat(
    groupchat_manager,
    message=text,
    summary_method="reflection_with_llm",
)

print(chat_res.summary)
