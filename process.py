from agents import *
from dataSet import *

agent_kt.description = "a knowledge tracking expert"
agent_exeGen_generator.description = "an exercise generation expert"
agent_exeGen_discriminator_1.description = "exercise evaluation expert 1"
agent_exeGen_discriminator_2.description = "exercise evaluation expert 2"
agent_exeGen_discriminator_3.description = "exercise evaluation expert 3"
agent_host.description = "the host of this meeting"

out_groupchat = GroupChat(
    agents=[agent_kt, agent_exeGen_generator, agent_exeGen_discriminator_1, agent_exeGen_discriminator_2,
            agent_exeGen_discriminator_3, agent_host],
    messages=[],
    send_introductions=True,
)

out_groupchat_manager = GroupChatManager(
    groupchat=out_groupchat,
    llm_config=llm_config,
)

# chat_res = agent_host.initiate_chats(
#     [
#         {
#             "recipient": agent_kt,
#             "message": text,
#             "max_turns": 2,
#             "summary_method": "last_msg",
#         },
#         {
#             "recipient": agent_exeGen_generator,
#             "message": "",
#             "max_turns": 2,
#             "summary_method": "last_msg",
#         },
#         {
#             "recipient": agent_exeGen_discriminator_1,
#             "message": "",
#             "max_turns": 2,
#             "summary_method": "last_msg",
#         },
#         {
#             "recipient": agent_exeGen_discriminator_2,
#             "message": "",
#             "max_turns": 2,
#             "summary_method": "last_msg",
#         },
#         {
#             "recipient": agent_exeGen_discriminator_3,
#             "message": "",
#             "max_turns": 2,
#             "summary_method": "last_msg",
#         },
#         {
#             "recipient": agent_exeGen_discriminator_4,
#             "message": "",
#             "max_turns": 2,
#             "summary_method": "last_msg",
#         },
#         {
#             "recipient": agent_exeGen_discriminator_5,
#             "message": "",
#             "max_turns": 2,
#             "summary_method": "last_msg",
#         },
#     ]
# )


chat_res = agent_host.initiate_chat(
    out_groupchat_manager,
    message=text,
    summary_method="reflection_with_llm",
)
