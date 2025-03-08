import argparse
import json
import sys
from autogen import *
from create_prompt import *


def exeGen(exercise_type, number_of_generations):
    exercise_type = exercise_type
    Number_of_Generations = number_of_generations
    output_type = "natural_language"
    type_of_prompt = "natural_language_text"

    stuRec_1000_with_tokens = pandas.read_csv("subject_data(1)/stuRec_1000_with_tokens.csv")
    examples_with_explanation_with_tokens = pandas.read_csv("subject_data(1)/examples_with_explanation_with_tokens.csv")
    concept_relation_filtered = pandas.read_csv("subject_data(1)/concept_relationship_filtered.csv")

    llm_config = {
        "cache_seed": None,
        "config_list": [{
            "model": "qwen-max-latest",
            "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
            "api_key": "sk-af4e8bebee384301952d8e3ba8df6906",
            "price": [0.0016, 0.0064]
        }]
    }

    examplar_gene = ConversableAgent(
        name='examplar',
        llm_config=llm_config,
        system_message="",
    )

    exercise_type = exercise_type
    exercise_number = Number_of_Generations

    agent_exeGen_generator = ConversableAgent(  # 习题生成代理
        name="agent_exeGen_generator",
        llm_config=llm_config,
        system_message="You are an exercise generation expert; "
                       "you will receive a list containing information about exercises and the student’s answer statuses, including examples with concept_id to guide you. "
                       f"Based on this information, you will need to generate {exercise_number} new {exercise_type} exercises and their answers in the format provided, ensuring that the knowledge concepts (concepts) in the exercises directly correspond to the provided concept_id values. "
                       f"The exercises must strictly adhere to the specified {exercise_type} format, as outlined below: "
                       "- **Single-Choice Exercises**: "
                       "**Exercise:** Example exercise text "
                       "- **Options:** {'A': 'Option 1', 'B': 'Option 2', 'C': 'Option 3', 'D': 'Option 4'} "
                       "- **Answer:** ['Correct Answer'] "
                       "- **Concept:** Related Knowledge Concept (in Chinese, from historical records, matching concept_id) "
                       "- **Multiple-Choice Exercises**: "
                       "**Exercise:** Example exercise text "
                       "- **Options:** {'A': 'Option 1', 'B': 'Option 2', 'C': 'Option 3', 'D': 'Option 4'} "
                       "- **Answer:** ['Correct Answer 1', 'Correct Answer 2'] "
                       "- **Concept:** Related Knowledge Concept (in Chinese, from historical records, matching concept_id) "
                       "- **True/False Exercises**: "
                       "**Exercise:** {Statement} "
                       "- **Answer:** ['True' or 'False'] "
                       "- **Concept:** Related Knowledge Concept (in Chinese, from historical records, matching concept_id) "
                       "Focus on generating exercises related to the student's weak knowledge concepts: "
                       "- Prioritize designing exercises targeting the student's weak aspects to strengthen their understanding and improve performance. "
                       "- Create multiple exercises related to these weak knowledge concepts to reinforce the student's practice of these concepts. "
                       "Ensure the knowledge concepts in the exercises meet the following criteria: "
                       "- The knowledge concepts must be written in Chinese. "
                       "- Each knowledge concept in the generated exercises must directly match a concept_id from the student's historical records. "
                       "- Do not create new knowledge concept names or concept_ids. "
                       "While focusing on weak knowledge concepts, ensure the generated exercises possess the following characteristics: "
                       "- **Clarity**: Use precise language to avoid ambiguity. "
                       "- **Relevance**: Directly test the knowledge concepts mentioned in the summary. "
                       "- **Logicality**: For choice-based exercises, ensure that distractors (incorrect options) are relevant and reasonable, reducing the likelihood of random guessing. "
                       "The generation process is as follows: "
                       "1. Analyze the summary of knowledge states, including concept_id, to identify the student's weak knowledge concepts and make these the primary focus of the exercise design. "
                       "2. Allocate most of the exercises to the weak knowledge concepts while including a few exercises to reinforce the mastered concepts. "
                       "3. Ensure diversity in wording, difficulty levels, and scenarios to maintain the student’s engagement and provide an appropriate level of challenge. "
                       f"The generated exercises must strictly follow the {exercise_type} format, and all knowledge concepts must directly match those provided with concept_id. Your output should reflect a deep analysis of the student's learning needs and a targeted design approach. For example, if exercise_type = Multiple_Choice, you must generate ten multiple-choice exercises in the required format as outlined above."
        ,
    )

    # 3个习题评判专家
    agent_exeGen_discriminator_1 = ConversableAgent(
        name="agent_exeGen_discriminator_1",
        llm_config=llm_config,
        system_message="""
        You are an exercise evaluation expert specializing in assessing linguistic fluency.
        You will receive a list of newly generated exercises and their answers created by the exercise generation expert. Your task is to determine whether the language used in these exercises is fluent and appropriate for effective communication.
        **Evaluation Process**:
        1. **Evaluate Sentence Structure**:
        - Analyze the grammatical structure of each exercise to ensure it adheres to standard language conventions.
        - Check for any grammatical errors, awkward phrasing, or incomplete sentences.
        2. **Assess Word Choice**:
        - Ensure the vocabulary used is suitable for the target audience.
        - Identify and flag any ambiguous, overly complex, or contextually inappropriate words.
        3. **Check Coherence and Clarity**:
        - Confirm that the language in the exercises clearly conveys the intended meaning.
        - Ensure the exercises and answers are logically structured and easy to understand.
        4. **Provide Suggestions for Improvement**:
        - Highlight specific aspects where linguistic fluency can be enhanced.
        - Offer recommendations for rephrasing or simplifying content without altering its meaning.
        Your evaluation should focus on ensuring that the exercises are free of language errors and effectively communicate the intended concepts.
        """,
    )

    agent_exeGen_discriminator_2 = ConversableAgent(
        name="agent_exeGen_discriminator_2",
        llm_config=llm_config,
        system_message="""
        You are an exercise evaluation expert specializing in assessing the coverage of knowledge concepts.
        You will receive:
        1. A summary of the student’s mastery of knowledge concepts provided by the knowledge tracking expert.
        2. A list of newly generated exercises and their answers created by the exercise generation expert.
        Your task is to determine whether the newly generated exercises adequately address the student's weak knowledge concepts.
        **Evaluation Process**:
        1. **Analyze the Knowledge Concept Summary**:
        - Identify the key knowledge concepts that the exercises should address.
        - Pay special attention to the student’s weak aspects and error records.
        2. **Match Exercises to Weak Knowledge concepts**:
        - Review each exercise to determine if it targets the relevant weak knowledge concepts.
        - Ensure all weak knowledge concepts are sufficiently practiced.
        3. **Identify Missing or Repeated Knowledge Concepts**:
        - Point out any weak knowledge concepts that are not addressed in the exercises.
        - Mark exercises that repeat the same concepts unnecessarily, without providing additional learning value.
        4. **Provide Feedback**:
        - Summarize the strengths and weaknesses in covering weak knowledge concepts.
        - Recommend adjustments to better target the student's learning needs.
        Your evaluation should ensure that the exercises primarily focus on the student’s weak knowledge concepts, helping them improve understanding and performance.
        """,
    )

    agent_exeGen_discriminator_3 = ConversableAgent(
        name="agent_exeGen_discriminator_3",
        llm_config=llm_config,
        system_message="""
        You are an exercise evaluation expert specializing in assessing the correctness and reasonableness of exercises.
        You will receive a list of newly generated exercises and their answers created by the exercise generation expert. Your task is to evaluate whether the exercises and their answers are accurate, logical, and reasonable.
        **Evaluation Process**:
        1. **Check the Accuracy of Answers**:
        - Verify whether the answers provided are correct and align with the knowledge concepts being tested.
        - Flag any incorrect or incomplete answers.
        2. **Evaluate the Logic of Exercises**:
        - Ensure each exercise has a clear and logical structure.
        - Confirm that the exercise aligns with the provided answer and the intended knowledge concept.
        3. **Assess the Reasonableness of Exercises**:
        - Determine whether the exercises are appropriate for the student's current learning level.
        - Ensure the difficulty level is neither too high nor too low, making it suitable for practice or assessment.
        4. **Provide Feedback**:
        - Highlight specific issues with incorrect or unreasonable exercises.
        - Recommend improvements to enhance clarity, accuracy, or alignment with learning goals.
        Your evaluation should ensure that the exercises are accurate, logical, and effectively designed to meet the student’s learning needs.
        """,
    )

    o_format = output_type
    if o_format == "natural_language":
        f = open("txtfile/n_output.txt", "r")
        o_fmt = f.read()
    elif o_format == "json":
        f = open("txtfile/j_output.txt", "r")
        o_fmt = f.read()
    else:
        f = open("txtfile/j_output.txt", "r")
        o_fmt = f.read()

    agent_host = ConversableAgent(
        name="agent_host",
        llm_config=llm_config,
        system_message=f"""
        You are the moderator of this workflow, responsible for overseeing the collaborative process between multiple agents to create and evaluate high-quality exercises tailored to a student’s learning needs.
        Your responsibilities include the following: 
        1. **Obtain Initial Input**:
        - Receive a list containing information about exercises and the student’s answer statuses.
        2. **Generate New Exercises**:
        - Provide the exercise record to the **exercise generation expert (agent_exeGen_generator)**.
        - Instruct agent_exeGen_generator to create ten new exercises, ensuring these exercises are specifically designed around the student’s weak knowledge concepts and adhere to the specified exercise type format.
        - **Important**: Ensure that the instructions to agent_exeGen_generator are clear and to the point. Avoid excessive introductory or redundant statements.
        3. **Evaluate the Exercises**:
        - Submit the newly generated exercises to the three **exercise evaluation experts (agent_exeGen_discriminators)** for review. Each expert evaluates a specific aspect of the exercises:
            - **Linguistic Fluency (agent_exeGen_discriminator_1)**: Verifies whether the exercises are linguistically accurate, fluent, and clear.
            - **Knowledge Concept Coverage (agent_exeGen_discriminator_2)**: Ensures that the exercises adequately cover the student’s weak knowledge concepts.
            - **Correctness and Reasonableness (agent_exeGen_discriminator_3)**: Confirms whether the exercises and their answers are accurate, logical, and suitable for the student’s current learning level.
            - **Important**: Instruct each evaluation expert to directly evaluate the exercises without unnecessary preambles or redundant statements. They should focus on the specific task assigned and provide concise feedback.
        4. **Iterative Regeneration**:
        - If any agent_exeGen_discriminator finds the exercises unsatisfactory:
            - Return to agent_exeGen_generator and instruct them to regenerate the exercises based on the feedback provided.
            - Repeat this iterative process until all three agents agree that the exercises meet the required standards.
        5. **Final Output**:
        - Once all agents have approved the exercise, you need to edit the final version of the exercise list strictly in the format {o_fmt} and return it, then let the chat end.
        **Key Guidelines**:
        - Prioritize the student’s weak knowledge concepts throughout the process to ensure targeted learning.
        - Ensure that all steps are completed efficiently and logically, with clear communication between agents.
        - Manage the iterative refinement process to guarantee that the final exercises are of high quality and effectively address the student’s learning needs.
        - **Important**: Ensure that all agents focus on their specific task without unnecessary repetition. Any redundant remarks should be minimized to avoid clutter and ensure an efficient workflow.
        Your ultimate goal is to manage collaboration between agents and produce a final list of exercises that are accurate, relevant, and highly tailored to the student’s learning requirements.
        """,
    )

    out_groupchat = GroupChat(
        agents=[agent_exeGen_generator, agent_exeGen_discriminator_1, agent_exeGen_discriminator_2,
                agent_exeGen_discriminator_3, agent_host],
        messages=[],
        send_introductions=True,
    )

    out_groupchat_manager = GroupChatManager(
        groupchat=out_groupchat,
        llm_config=llm_config,
    )

    # agent_kt.description = "a knowledge tracking expert"
    agent_exeGen_generator.description = "an exercise generation expert"
    agent_exeGen_discriminator_1.description = "exercise evaluation expert 1"
    agent_exeGen_discriminator_2.description = "exercise evaluation expert 2"
    agent_exeGen_discriminator_3.description = "exercise evaluation expert 3"
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
                json_obj = json.loads(json_str)
                return json_obj
            except json.JSONDecodeError as e:
                print(f"解析错误：{e}")
        return None

    i = 33

    text = {
        "examples": [],
        "tasks": []
    }

    # 获取task数组
    stuRec_1000_with_tokens = pandas.read_csv("subject_data(1)/stuRec_1000_with_tokens.csv")
    stuRec_1000_with_tokens = stuRec_1000_with_tokens.iloc[(i * 10):((i + 1) * 10)]
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
    stuRec_1000_with_tokens = pandas.read_csv("subject_data(1)/stuRec_1000_with_tokens.csv")
    stuRec_1000_with_tokens = stuRec_1000_with_tokens.iloc[(i * 10):((i + 1) * 10)]
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

    type = type_of_prompt
    if type == "natural_language_text":
        prompt = n_text
    elif type == "json_text":
        prompt = text
    else:
        prompt = text

    chat_res = out_groupchat_manager.initiate_chat(
        agent_host,
        message=prompt,
        summary_method="reflection_with_llm",
    )
    # 提取并返回结果
    chat_his_str = "\n".join([str(sentence['content']) for sentence in chat_res.chat_history])
    res_exe = extract_last_json(chat_his_str)

    return {
        "exercise_type": exercise_type,
        "count": number_of_generations,
        "exercises": res_exe,
        "history": chat_his_str,
    }


if __name__ == "__main__":
    # 命令行参数解析
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", type=str, required=True)
    parser.add_argument("--count", type=int, required=True)

    args = parser.parse_args()

    result = exeGen(
        exercise_type=args.type,
        number_of_generations=args.count,
    )
    print(json.dumps(result, ensure_ascii=False))  # 输出到stdout
