
import json
from typing import Union

from autogen import *
from create_prompt import *
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("--type_of_prompt", type=str, help="natural_language_text or json_text")
parser.add_argument("--exercise_type", type=str,
                    help="Single_Choice or Multiple_Choice or True_or_False")
parser.add_argument("--output_type", type=str, help="natural_language or json")
parser.add_argument("--Number_of_Generations", type=int)

stuRec_1000_with_tokens = pandas.read_csv("../subject_data(1)/stuRec_1000_with_tokens.csv")
examples_with_explanation_with_tokens = pandas.read_csv("../subject_data(1)/examples_with_explanation_with_tokens.csv")
concept_relation_filtered = pandas.read_csv("../subject_data(1)/concept_relationship_filtered.csv")

llm_config = {
    "cache_seed": None,
    "config_list": [{
        "model": "gpt-4o",
        "base_url": "https://api.xty.app/v1",
        "api_key": "",
        "price": [0.0004, 0.0012]
    }]
}

# examplar_gene = ConversableAgent(
#     name='examplar',
#     llm_config=llm_config,
#     system_message="",
# )

# agent_kt = ConversableAgent(
#     name="agent_kt",
#     llm_config=llm_config,
#     system_message="""
#     You are a knowledge tracking expert.
#     You will receive a file containing sample exercises and a record of the student’s performance on these exercises. Each record includes the student's response, whether it was correct or incorrect, and the associated knowledge concept. The explanation attribute represents the reasoning behind why the student answered correctly or incorrectly, but some explanations may be missing or incomplete.
#     Your task is as follows:
#     1. **Analyze each exercise in the student's record**:
#        - For correct answers, deduce the reasoning or knowledge that enabled the student to answer correctly.
#        - For incorrect answers, identify potential misunderstandings, gaps in knowledge, or reasoning errors that led to the mistake.
#     2. **Complete the missing or incomplete explanations for each exercise**:
#        - Clearly explain the reasoning behind the student's response or identify any misunderstandings that led to errors.
#        - Break down your explanation into logical steps to accurately reflect the student’s thought process and understanding of the knowledge concept.
#     3. **Summarize the student’s overall knowledge state of the knowledge concepts**:
#        - Identify the knowledge concepts the student has mastered based on consistent correct responses and sound reasoning.
#        - Highlight knowledge concepts where the student struggles, based on patterns of incorrect answers or unclear reasoning.
#        - Suggest aspects for further improvement, including specific prerequisite knowledge or concepts the student should review.
#     4. **Output format**:
#        - Your output should strictly follow the format provided by the host.
#        - Each exercise record should include the following attributes:
#          - **content**: The content of the exercise (e.g., question text).
#          - **option**: The options provided for the exercise (if applicable).
#          - **right_answer**: The correct answer(s) to the exercise (e.g., a list of correct answers).
#          - **knowledge_evidence**: Multiple knowledge triples. This should represent the relationship between the topic, the exercise, and the relevant knowledge concepts.
#          - **is_correct**: A boolean indicating whether the student's answer was correct or not.
#          - **explanation**: A detailed breakdown of the student’s reasoning, or an explanation of why the answer was correct/incorrect.
#     Please ensure that your explanations are precise, clear, and grounded in logical reasoning to provide actionable insights into the student’s knowledge state. The format should be consistent with the example provided and focus on delivering a detailed yet structured response. Ensure that the `knowledge_evidence` includes the necessary knowledge triples for each exercise.
#     """,
# )

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

agent_generator = ConversableAgent(
    name="agent_generator",
    llm_config=llm_config,
    system_message=f"""
    You are an exercise generation expert; 
    you will receive a list containing the knowledge tracking expert's summary of the student's knowledge state of the knowledge concepts, including examples with concept_id to guide you. 
    Based on this information, you will need to generate {exercise_number} new {exercise_type} exercises and their answers in the format provided, ensuring that the knowledge concepts (concepts) in the exercises directly correspond to the provided concept_id values. 
    The exercises must strictly adhere to the specified {exercise_type} format, as outlined below: 
    {exercise_fmt}\n
    Focus on generating exercises related to the student's weak knowledge concepts: 
    - Prioritize designing exercises targeting the student's weak aspects to strengthen their understanding and improve performance. 
    - Create multiple exercises related to these weak knowledge concepts to reinforce the student's practice of these concepts. 
    Ensure the knowledge concepts in the exercises meet the following criteria: 
    - The knowledge concepts must be written in Chinese. 
    - Each knowledge concept in the generated exercises must directly match a concept_id from the student's historical records. 
    - Do not create new knowledge concept names or concept_ids. 
    While focusing on weak knowledge concepts, ensure the generated exercises possess the following characteristics: 
    - **Clarity**: Use precise language to avoid ambiguity. 
    - **Relevance**: Directly test the knowledge concepts mentioned in the summary. 
    - **Logicality**: For choice-based exercises, ensure that distractors (incorrect options) are relevant and reasonable, reducing the likelihood of random guessing. 
    The generation process is as follows: 
    1. Allocate most of the exercises to the weak knowledge concepts while including a few exercises to reinforce the mastered concepts. 
    2. Ensure diversity in wording, difficulty levels, and scenarios to maintain the student’s engagement and provide an appropriate level of challenge. 
    3. You need to edit the final version of the exercise list strictly in the format {o_fmt} and return it.
    The generated exercises must strictly follow the {exercise_type} format, and all knowledge concepts must directly match those provided with concept_id. Your output should reflect a deep analysis of the student's learning needs and a targeted design approach.
    """,
)

# agent_discriminator_1 = ConversableAgent(
#     name="Linguistic_Fluency_discriminator",
#     llm_config=llm_config,
#     system_message="""
#     You are an exercise evaluation expert specializing in assessing linguistic fluency.
#     You will receive a list of newly generated exercises and their answers created by the exercise generation expert. Your task is to determine whether the language used in these exercises is fluent and appropriate for effective communication.
#     **Evaluation Process**:
#     1. **Evaluate Sentence Structure**:
#        - Analyze the grammatical structure of each exercise to ensure it adheres to standard language conventions.
#        - Check for any grammatical errors, awkward phrasing, or incomplete sentences.
#     2. **Assess Word Choice**:
#        - Ensure the vocabulary used is suitable for the target audience.
#        - Identify and flag any ambiguous, overly complex, or contextually inappropriate words.
#     3. **Check Coherence and Clarity**:
#        - Confirm that the language in the exercises clearly conveys the intended meaning.
#        - Ensure the exercises and answers are logically structured and easy to understand.
#     4. **Provide Suggestions for Improvement**:
#        - Highlight specific aspects where linguistic fluency can be enhanced.
#        - Offer recommendations for rephrasing or simplifying content without altering its meaning.
#     Your evaluation should focus on ensuring that the exercises are free of language errors and effectively communicate the intended concepts.
#     """,
# # )
#
# agent_discriminator_2 = ConversableAgent(
#     name="Knowledge_Concept_Coverage_discriminator",
#     llm_config=llm_config,
#     system_message="""
#     You are an exercise evaluation expert specializing in assessing the coverage of knowledge concepts.
#     You will receive:
#     1. A summary of the student’s knowledge state of knowledge concepts provided by the knowledge tracking expert.
#     2. A list of newly generated exercises and their answers created by the exercise generation expert.
#     Your task is to determine whether the newly generated exercises adequately address the student's weak knowledge concepts.
#     **Evaluation Process**:
#     1. **Analyze the Knowledge Concept Summary**:
#        - Identify the key knowledge concepts that the exercises should address.
#        - Pay special attention to the student’s weak aspects and error records.
#     2. **Match Exercises to Weak Knowledge concepts**:
#        - Review each exercise to determine if it targets the relevant weak knowledge concepts.
#        - Ensure all weak knowledge concepts are sufficiently practiced.
#     3. **Identify Missing or Repeated Knowledge Concepts**:
#        - Point out any weak knowledge concepts that are not addressed in the exercises.
#        - Mark exercises that repeat the same concepts unnecessarily, without providing additional learning value.
#     4. **Provide Feedback**:
#        - Summarize the strengths and weaknesses in covering weak knowledge concepts.
#        - Recommend adjustments to better target the student's learning needs.
#     Your evaluation should ensure that the exercises primarily focus on the student’s weak knowledge concepts, helping them improve understanding and performance.
#     """,
# )
#
# agent_discriminator_3 = ConversableAgent(
#     name="Correctness_and_Reasonableness_discriminator",
#     llm_config=llm_config,
#     system_message="""
#     You are an exercise evaluation expert specializing in assessing the correctness and reasonableness of exercises.
#     You will receive a list of newly generated exercises and their answers created by the exercise generation expert. Your task is to evaluate whether the exercises and their answers are accurate, logical, and reasonable.
#     **Evaluation Process**:
#     1. **Check the Accuracy of Answers**:
#        - Verify whether the answers provided are correct and align with the knowledge concepts being tested.
#        - Flag any incorrect or incomplete answers.
#     2. **Evaluate the Logic of Exercises**:
#        - Ensure each exercise has a clear and logical structure.
#        - Confirm that the exercise aligns with the provided answer and the intended knowledge concept.
#     3. **Assess the Reasonableness of Exercises**:
#        - Determine whether the exercises are appropriate for the student's current learning level.
#        - Ensure the difficulty level is neither too high nor too low, making it suitable for practice or assessment.
#     4. **Provide Feedback**:
#        - Highlight specific issues with incorrect or unreasonable exercises.
#        - Recommend improvements to enhance clarity, accuracy, or alignment with learning goals.
#     Your evaluation should ensure that the exercises are accurate, logical, and effectively designed to meet the student’s learning needs.
#     """,
# )


# RecommendationManager = ConversableAgent(
#     name="RecommendationManager",
#     llm_config=llm_config,
#     system_message=f"""
#     You are the moderator of this workflow, responsible for overseeing the collaborative process between multiple agents to create and evaluate high-quality exercises tailored to a student’s learning needs.
#     Each time you speak you need to specify the next agent to speak.
#     Your responsibilities include the following:
#     1. **Track Knowledge State**:
#        - Instruct **agent_kt** to generate a comprehensive summary of the student’s knowledge state, including both mastered concepts and weak aspects. Specifically, **agent_kt** should:
#          - Analyze each exercise in the student's record, deducing reasoning for correct answers and identifying misunderstandings for incorrect answers.
#          - Complete any missing or incomplete explanations, providing a breakdown of the student’s thought process.
#          - Ensure the output follows the exact format provided below, where each exercise record includes:
#            - **content**: The content of the exercise (e.g., question text).
#            - **option**: The options provided for the exercise (if applicable).
#            - **right_answer**: A list of the correct answers to the exercise.
#            - **knowledge_evidence**: Multiple knowledge triples, which should represent relationships.
#            - **is_correct**: A boolean indicating whether the student answered correctly.
#            - **explanation**: A detailed explanation of why the student’s answer was correct or incorrect, including the reasoning behind their answer.
#          - Ensure that all **knowledge_evidence** entries are clearly formatted and correspond to the relevant knowledge concepts in the exercise, as exemplified in the provided template.
#          - Return  the summary of student’s knowledge states in the exact format, ensuring consistency with the example, so that it is actionable and precise for future steps.
#          - **Important**: Do not provide redundant or unnecessary information in your responses. Directly analyze and return the output as per the required format without elaborating excessively on the process.
#     2. **Generate New Exercises**:
#        - Provide the knowledge state from agent_kt to the **exercise generation expert (agent_generator)**.
#        - Instruct agent_generator to create ten new exercises, ensuring these exercises are specifically designed around the student’s weak knowledge concepts and adhere to the specified exercise type format.
#        - **Important**: Ensure that the instructions to agent_generator are clear and to the point. Avoid excessive introductory or redundant statements.
#     3. **Evaluate the Linguistic Fluency**:
#        - Submit the newly generated exercises to **Linguistic Fluency Discriminator**: Verifies whether the exercises are linguistically accurate, fluent, and clear.
#     4. **Evaluate the Knowledge Concept Coverage**:
#        - Submit the newly generated exercises to **Knowledge Concept Coverage discriminator**: Ensures that the exercises adequately cover the student’s weak knowledge concepts.
#     5. **Evaluate the Correctness and Reasonableness**:
#        - Submit the newly generated exercises to **Correctness and Reasonableness discriminator**: Confirms whether the exercises and their answers are accurate, logical, and suitable for the student’s current learning level.
#     6. **Iterative Regeneration**:
#        - If any agent_discriminator finds the exercises unsatisfactory:
#          - Return to agent_generator and instruct them to regenerate the exercises based on the feedback provided.
#          - Repeat this iterative process until all three agents agree that the exercises meet the required standards.
#     7. **Final Output**:
#        - Once all agents have approved the exercise, you need to edit the final version of the exercise list strictly in the format {o_fmt} and return it, and say 'stopChat' to let the chat end.
#     **Key Guidelines**:
#     - Prioritize the student’s weak knowledge concepts throughout the process to ensure targeted learning.
#     - Ensure that all steps are completed efficiently and logically, with clear communication between agents.
#     - Manage the iterative refinement process to guarantee that the final exercises are of high quality and effectively address the student’s learning needs.
#     - **Important**: Ensure that all agents focus on their specific task without unnecessary repetition. Any redundant remarks should be minimized to avoid clutter and ensure an efficient workflow.
#     Your ultimate goal is to manage collaboration between agents and produce a final list of exercises that are accurate, relevant, and highly tailored to the student’s learning requirements.
#     """,
# )


# def custom_speaker_selection_func(
#         last_speaker: Agent, groupchat: GroupChat
# ) -> Union[Agent, str, None]:
#     if "stopChat" in groupchat.messages[-1]["content"]:
#         return None
#     if last_speaker is RecommendationManager:
#         return "auto"
#     else:
#         return RecommendationManager


out_groupchat = GroupChat(
    agents=[agent_generator],
    select_speaker_message_template="""
    Selects the next speaking agent based on what RecommendationManager has said.
    End the chat when RecommendationManager returns the final list of exercises.
    The following roles are available:
    {roles}.
    Select the next role from {agentlist} to speak. Only return the role.
    """,
    messages=[],
    max_round=20,
)

out_groupchat_manager = GroupChatManager(
    groupchat=out_groupchat,
    llm_config=llm_config,
)

agent_generator.description = "an exercise generation expert"


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
            print(f"error：{e}")
    return None


# for i in range(3, 14):


text = {
    # "round": i,
    "examples": [],
    "tasks": []
}

stuRec_1000_with_tokens = pandas.read_csv("../subject_data(1)/stuRec_1000_with_tokens.csv")
stuRec_1000_with_tokens = stuRec_1000_with_tokens.iloc[35:45]
selected_columns1 = ['content', 'option', 'right_answer', 'knowledge_evidence', 'is_correct', 'explanation']

hard_example, stuRec_1000_with_tokens = get_examples_by_concept(examples_with_explanation_with_tokens,
                                                                stuRec_1000_with_tokens)
hard_example = hard_example[selected_columns1]

text['examples'] += hard_example.to_dict(orient='records')

if not stuRec_1000_with_tokens.empty:
    res = get_examples_by_similarity(examples_with_explanation_with_tokens, stuRec_1000_with_tokens)[
        selected_columns1].to_dict(orient='records')

    text["examples"] += res

stuRec_1000_with_tokens = pandas.read_csv("../subject_data(1)/stuRec_1000_with_tokens.csv")
stuRec_1000_with_tokens = stuRec_1000_with_tokens.iloc[35:45]
selected_columns2 = ['content', 'option', 'right_answer', 'knowledge_evidence', 'is_correct']
stuRec_1000_with_tokens = stuRec_1000_with_tokens[selected_columns2]

# stuRec_1000_with_tokens["knowledge_chain"] = ""
# for index, row in stuRec_1000_with_tokens.iterrows():
#     chain = get_chain(row['concept_id'], row['concept_id'])
#     stuRec_1000_with_tokens.at[index, 'knowledge_chain'] = chain

stuRec_1000_with_tokens["explanation"] = ""
stuRec_1000_with_tokens = stuRec_1000_with_tokens.to_dict(orient='records')
text["tasks"] = stuRec_1000_with_tokens

text = json.dumps(text, ensure_ascii=False, indent=4)

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
