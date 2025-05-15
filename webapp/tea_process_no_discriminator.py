from typing import Union

from autogen import *
from numpy.f2py.symbolic import Language

from experiment.create_prompt import *
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("--type_of_prompt", type=str, help="natural_language_text or json_text")
parser.add_argument("--exercise_type", type=str,
                    help="Single_Choice or Multiple_Choice or True_or_False")
parser.add_argument("--output_type", type=str, help="natural_language or json")
parser.add_argument("--Number_of_Generations", type=int)
parser.add_argument("--Knowledge_Concept", type=str)
parser.add_argument("--Language", type=str)
parser.add_argument("--Difficulty", type=str)

stuRec_1000_with_tokens = pandas.read_csv("../subject_data(1)/stuRec_1000_with_tokens.csv")
examples_with_explanation_with_tokens = pandas.read_csv("../subject_data(1)/examples_with_explanation_with_tokens.csv")
concept_relation_filtered = pandas.read_csv("../subject_data(1)/concept_relationship_filtered.csv")

llm_config = {
    "cache_seed": None,
    "config_list": [{
        "model": "qwen-plus",
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "api_key": "",
        "price": [0.0004, 0.0012]
    }]
}

exercise_type = parser.parse_args().exercise_type
exercise_number = parser.parse_args().Number_of_Generations
exercise_fmt = ""

if exercise_type == "Single_Choice":
    exercise_fmt = """- **Single-Choice Exercises**: 
                   **Exercise:** Example exercise text 
                    - **Options:** {'A': 'Option 1', 'B': 'Option 2', 'C': 'Option 3', 'D': 'Option 4'} 
                    - **Answer:** ['Correct Answer'] (There can only be one right answer.)
                    - **Concept:** Related Knowledge Concept (in Chinese, from historical records, matching concept_id) """
elif exercise_type == "Multiple_Choice":
    exercise_fmt = """- **Multiple-Choice Exercises**: 
                   **Exercise:** Example exercise text 
                    - **Options:** {'A': 'Option 1', 'B': 'Option 2', 'C': 'Option 3', 'D': 'Option 4'} 
                    - **Answer:** ['Correct Answer 1', 'Correct Answer 2'] (More than one correct answer must be present)
                    - **Concept:** Related Knowledge Concept (in Chinese, from historical records, matching concept_id) """
elif exercise_type == "True_or_False":
    exercise_fmt = """- **True/False Exercises**: 
                   **Exercise:** {Statement} 
                    - **Answer:** ['True' or 'False'] 
                    - **Concept:** Related Knowledge Concept (in Chinese, from historical records, matching concept_id) """

language = parser.parse_args().Language
difficulty = parser.parse_args().Difficulty
agent_generator = ConversableAgent(  # 习题生成代理
    name="agent_generator",
    llm_config=llm_config,
    system_message=f"""
    You are an exercise generation expert; 
    you will receive a list of tasks in ONE subject and ONE knowledge concept. 
    Based on this information, you will need to generate {exercise_number} new {exercise_type} exercises and their answers in the format provided, ensuring that the knowledge concepts (concepts) in the exercises directly correspond to the provided concept_id values. 
    The exercises must strictly adhere to the specified {exercise_type} format, as outlined below: 
    {exercise_fmt}\n
    Ensure the knowledge concepts in the exercises meet the following criteria: 
    - The knowledge concepts must be written in {Language}. 
    - Each knowledge concept in the generated exercises must directly match the concept_id given.
    - Do not create new knowledge concept names or concept_ids. 
    While focusing on weak knowledge concepts, ensure the generated exercises possess the following characteristics: 
    - **Clarity**: Use precise language to avoid ambiguity. 
    - **Logicality**: For choice-based exercises, ensure that distractors (incorrect options) are relevant and reasonable, reducing the likelihood of random guessing. 
    - **Difficulty**: The difficulty of the exercises you generate must be {difficulty}
    The generated exercises must strictly follow the {exercise_type} format, and all knowledge concepts must directly match those provided with concept_id. Your output should reflect a deep analysis of the student's learning needs and a targeted design approach.
    """,
)

o_format = parser.parse_args().output_type
if o_format == "natural_language":
    f = open("../txtfile/n_output.txt", "r")
    o_fmt = f.read()
elif o_format == "json":
    f = open("../txtfile/j_output.txt", "r")
    o_fmt = f.read()
else:
    f = open("../txtfile/j_output.txt", "r")
    o_fmt = f.read()

agent_host = ConversableAgent(
    name="RecommendationManager",
    llm_config=llm_config,
    system_message=f"""
    You are the moderator of this workflow, responsible for overseeing the collaborative process between multiple agents to create and evaluate high-quality exercises tailored to a student’s learning needs.
    Each time you speak you need to specify the next agent to speak.
    Your responsibilities include the following: 
    1. **Generate New Exercises**:
       - Instruct agent_generator to create ten new exercises, ensuring these exercises are specifically designed around knowledge concepts and adhere to the specified exercise type format.
       - **Important**: Ensure that the instructions to agent_generator are clear and to the point. Avoid excessive introductory or redundant statements.
    2. **Output**:
       - You need to edit the final version of the exercise list strictly in the format {o_fmt} and return it, and say 'stopChat' to let the chat end.
    - **Important**: Ensure that all agents focus on their specific task without unnecessary repetition. Any redundant remarks should be minimized to avoid clutter and ensure an efficient workflow.
    Your ultimate goal is to manage collaboration between agents and produce a final list of exercises that are accurate, relevant, and highly tailored to the student’s learning requirements.
    """,
)


def custom_speaker_selection_func(
        last_speaker: Agent, groupchat: GroupChat
) -> Union[Agent, str, None]:
    if "stopChat" in groupchat.messages[-1]["content"]:
        return None
    if last_speaker is agent_host:
        return "auto"
    else:
        return agent_host


out_groupchat = GroupChat(
    agents=[agent_generator, agent_host],
    select_speaker_message_template="""
    Selects the next speaking agent based on what RecommendationManager has said.
    End the chat when RecommendationManager returns the final list of exercises.
    The following roles are available:
    {roles}.
    Select the next role from {agentlist} to speak. Only return the role.
    """,
    speaker_selection_method=custom_speaker_selection_func,
    messages=[],
    max_round=20,
)

out_groupchat_manager = GroupChatManager(
    groupchat=out_groupchat,
    llm_config=llm_config,
)

agent_generator.description = "an exercise generation expert"
agent_host.description = "host of the chat"


def convert_to_natural_language(text):
    natural_language_text = ""

    # 处理examples
    natural_language_text += "examples:\n"
    flag = 0
    for example in text['examples']:
        content = example['content']
        options = example['option']
        right_answer = example['right_answer']
        knowledge_evidence = example['knowledge_evidence']
        is_correct = example['is_correct']
        explanation = example['explanation']

        flag += 1
        natural_language_text += str(flag) + ",\n"

        natural_language_text += "content:" + content + "\n"
        natural_language_text += "option:" + options + "\n"
        natural_language_text += "right_answer:" + right_answer + "\n"
        natural_language_text += "knowledge_evidence:" + knowledge_evidence + "\n"
        natural_language_text += "is_correct:" + str(is_correct) + "\n"
        natural_language_text += "explanation:" + explanation + "\n"

    # 处理tasks，逻辑与examples相同
    natural_language_text += "tasks:\n"
    flag = 0
    for task in text['tasks']:
        content = task['content']
        options = task['option']
        right_answer = task['right_answer']
        knowledge_evidence = task['knowledge_evidence']
        is_correct = task['is_correct']
        explanation = task['explanation']

        flag += 1
        natural_language_text += str(flag) + ",\n"
        natural_language_text += "content:" + content + "\n"
        natural_language_text += "option:" + options + "\n"
        natural_language_text += "right_answer:" + right_answer + "\n"
        natural_language_text += "knowledge_evidence:" + knowledge_evidence + "\n"
        natural_language_text += "is_correct:" + str(is_correct) + "\n"
        natural_language_text += "explanation:" + explanation + "\n"

    return natural_language_text


def extract_last_json(s):
    pattern = r'```json(.*?)```'
    matches = re.findall(pattern, s, re.DOTALL)
    if matches:
        json_str = matches[-1]
        try:
            json_obj = json.loads(json_str, strict=False)
            return json_obj
        except json.JSONDecodeError as e:
            print(f"解析错误：{e}")
    return None


# for i in range(3, 14):


text = {
    # "round": i,
    "examples": [],
    "tasks": []
}

# 获取task数组
knowledge_concept = parser.parse_args().Knowledge_Concept
stuRec_1000_with_tokens = pandas.read_csv("../subject_data(1)/stuRec_1000_with_tokens.csv")
stuRec_1000_with_tokens = stuRec_1000_with_tokens.loc[
    stuRec_1000_with_tokens['concept_id'] == knowledge_concept].head(10)
selected_columns1 = ['content', 'option', 'right_answer', 'knowledge_evidence', 'is_correct', 'explanation']

# 硬匹配
hard_example, stuRec_1000_with_tokens = get_examples_by_concept(examples_with_explanation_with_tokens,
                                                                stuRec_1000_with_tokens)
hard_example = hard_example[selected_columns1]

text['examples'] += hard_example.to_dict(orient='records')

# 软匹配
if not stuRec_1000_with_tokens.empty:
    res = get_examples_by_similarity(examples_with_explanation_with_tokens, stuRec_1000_with_tokens)[
        selected_columns1].to_dict(orient='records')

    text["examples"] += res

# 匹配完成后重新读取习题记录信息
stuRec_1000_with_tokens = pandas.read_csv("../subject_data(1)/stuRec_1000_with_tokens.csv")
stuRec_1000_with_tokens = stuRec_1000_with_tokens.loc[
    stuRec_1000_with_tokens['concept_id'] == knowledge_concept].head(10)
selected_columns2 = ['content', 'option', 'right_answer', 'knowledge_evidence', 'is_correct']
stuRec_1000_with_tokens = stuRec_1000_with_tokens[selected_columns2]

# 计算习题记录的知识链
# stuRec_1000_with_tokens["knowledge_chain"] = ""
# for index, row in stuRec_1000_with_tokens.iterrows():
#     chain = get_chain(row['concept_id'], row['concept_id'])
#     stuRec_1000_with_tokens.at[index, 'knowledge_chain'] = chain

# 将新题目explanation置空
stuRec_1000_with_tokens["explanation"] = ""
stuRec_1000_with_tokens = stuRec_1000_with_tokens.to_dict(orient='records')
text["tasks"] = stuRec_1000_with_tokens

text = json.dumps(text, ensure_ascii=False, indent=4)

# 将提示词文本转换为自然语言形式
n_text = json.loads(text)

# n_text = convert_to_natural_language(n_text)

type = parser.parse_args().type_of_prompt
if type == "natural_language_text":
    prompt = n_text
elif type == "json_text":
    prompt = text
else:
    prompt = text

chat_res = out_groupchat_manager.initiate_chat(
    agent_generator,
    message=prompt,
    summary_method="reflection_with_llm",
    max_turns=20
)

# 获取生成的新题目
chat_cost = chat_res.cost
chat_his = chat_res.chat_history
chat_his_str = chat_his[-1]['content']
res_exe = extract_last_json(chat_his_str)
text = json.loads(text)
text["result"] = res_exe
text["cost"] = chat_cost
text["chat_history"] = chat_his
text = json.dumps(text, ensure_ascii=False, indent=4)
chat_his = json.dumps(chat_his, ensure_ascii=False, indent=4)
with open(f'output/output{os.getpid()}.txt', 'w', encoding='utf-8') as f:
    f.write(text)
