from openai import OpenAI
from os import getenv
from autogen import ConversableAgent, GroupChat, GroupChatManager
import pandas as pd

stuRec_1000_with_tokens = pd.read_csv("subject_data(1)/stuRec_1000_with_tokens.csv")
examples_with_explanation_with_tokens = pd.read_csv("subject_data(1)/examples_with_explanation_with_tokens.csv")

llm_config = {
    "config_list": [{
        "model": "openai/gpt-4o",
        "base_url": "https://openrouter.ai/api/v1",
        "api_key": "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",
        "price": [0.5, 1.5]
    }]
}

# 根据学生的历史数据定义每种方法的提示模板
def get_prompt(method, student_history):
    if method == "zero_shot":
        return (
            f"You are an expert in generating high-quality single-choice exercises for educational purposes.\n"
            f"Your task is to create 10 single-choice exercises in Chinese based on the student's performance in answering history exercises.\n"
            f"The generated exercises should:\n"
            f"1. Cover knowledge concepts related to the student's historical answer records and match the student's level of knowledge.\n"
            f"2. Provide reasonable and clear options.\n"
            f"3. Avoid repeating exercises or introducing ambiguous options.\n"
            f"Student's historical exercise performance is as follows:\n{student_history}\n"
            f"Please ensure that the format of the generated exercises is consistent with the following example. If the knowledge concept in the new exercise overlaps with one from the historical records, keep the name of the knowledge concept unchanged. \n"
            f"Meanwhile, you only need to output the exercises according to the format, without containing any irrelevant statements\n"
            f"1. **Exercise:** 示例题目\n"
            f"- **Options:** {{'A': '选项1', 'B': '选项2', 'C': '选项3', 'D': '选项4'}}\n"
            f"- **Answer:** ['正确答案']\n"
            f"- **Concept:** 知识点\n"
        )

    elif method == "few_shot":
        example_text = (
            "Example: Student's Answer Record and Generated Exercise:\n"
            "Student's performance in answering history exercises:\n"
            "1. content: 不同 VLAN 间数据通信，需通过（ ）进行转发。\n"
            "   option: {'A': 'HUB', 'B': '二层交换机', 'C': '路由器', 'D': '中继器'}\n"
            "   answer: ['C']\n"
            "   is_correct: 0\n"
            "   concept_id: K_二层交换机_计算机科学与技术\n"
            "2. content: 虚拟局域网 VLAN 可根据以下哪些方式划分（）。\n"
            "   option: {'A': '根据端口划分 VLAN', 'B': '根据 MAC 地址划分 VLAN', 'C': '根据网络层（IP 地址）划分 VLAN', 'D': 'IP 组播作为 VLAN'}\n"
            "   answer: ['A', 'B', 'C', 'D']\n"
            "   is_correct: 0\n"
            "   concept_id: K_IP地址_信息与通信工程\n"
            "3. content: 为保证从分布式存储系统中读取的数据正确，需要采用哪种数据处理方式（ ）。\n"
            "   option: {'A': '压缩', 'B': '多份存储', 'C': 'Erasure coding 编码', 'D': 'Checksum 数据校验'}\n"
            "   answer: ['D']\n"
            "   is_correct: 1\n"
            "   concept_id: K_分布式存储系统_计算机科学与技术\n"
            "Generated Exercise:\n"
            "1. **Exercise:** 以下哪种设备可以用来实现不同 VLAN 间的通信？( )\n"
            "   - **Options:** {'A': 'HUB', 'B': '二层交换机', 'C': '路由器', 'D': '中继器'}\n"
            "   - **Answer:** ['C']\n"
            "   - **Concept:** K_二层交换机_计算机科学与技术\n"
            "2. **Exercise:** VLAN 划分的常见方式有哪些？( )\n"
            "   - **Options:** {'A': '根据端口划分 VLAN', 'B': '根据 MAC 地址划分 VLAN', 'C': '根据网络层（IP 地址）划分 VLAN', 'D': 'IP 组播作为 VLAN'}\n"
            "   - **Answer:** ['A', 'B', 'C']\n"
            "   - **Concept:** K_IP地址_信息与通信工程\n"
            "3. **Exercise:** 分布式存储系统中，为了确保读取数据的正确性，哪种方法是最佳选择？( )\n"
            "   - **Options:** {'A': '压缩', 'B': '多份存储', 'C': 'Erasure coding 编码', 'D': 'Checksum 数据校验'}\n"
            "   - **Answer:** ['D']\n"
            "   - **Concept:** K_分布式存储系统_计算机科学与技术\n"
        )
        return (
            f"You are an expert in generating single-choice exercises for educational purposes.\n"
            f"Your task is to create 10 high-quality single-choice Exercises in Chinese based on the student's performance in answering history exercises and the examples I provide for you.\n"
            f"The generated exercises should meet the following criteria:\n"
            f"1. Cover knowledge concepts related to the student's historical answer records and match the student's level of knowledge.\n"
            f"2. Provide reasonable and clear options.\n"
            f"3. Avoid repeating exercises or introducing ambiguous options.\n"
            f"Example of exercise generation is as follows:\n{example_text}\n"
            f"Student's historical exercise performance is as follows:\n{student_history}\n"
            f"Please ensure that the format of the generated exercises is consistent with the following example. If the knowledge concept in the new exercise overlaps with one from the historical records, keep the name of the knowledge concept unchanged. \n"
            f"Meanwhile, you only need to output the exercises according to the format, without containing any irrelevant statements\n"
            f"1. **Exercise:** {{题目}}\n"
            f"- **Options:** {{'A': '选项1', 'B': '选项2', 'C': '选项3', 'D': '选项4'}}\n"
            f"- **Answer:** ['正确答案']\n"
            f"- **Concept:** 知识点\n"
        )
    elif method == "chain_of_thought":
        return (
            f"You are an expert in generating single-choice exercises for educational purposes.\n"
            f"Your task is to create 10 high-quality single-choice exercises in Chinese by following a thought chain based on the student's performance in answering history exercises.\n"
            f"Please follow these steps to create the exercises:\n"
            f"1. Analyze the student's performance in answering history exercises:\n"
            f"   - Identify weak aspects to reinforce learning by focusing on knowledge concepts the student answered incorrectly.\n"
            f"   - Test the stable mastery of knowledge concepts the student answered correctly.\n"
            f"2. Ensure that the generated exercises cover the following types of knowledge concepts:\n"
            f"   - Weak concepts: Reinforce knowledge concepts the student answered incorrectly.\n"
            f"   - Mastery concepts: Test knowledge concepts the student has already mastered.\n"
            f"3. Validate and optimize the generated exercises:\n"
            f"   - Verify the logical integrity of each exercise to ensure there is no ambiguity between the exercise and the options.\n"
            f"   - Ensure the distractor options are plausible but not misleading.\n"
            f"   - Optimize the language expression to make each exercise clearer and easier to understand.\n"
            f"Student's historical exercise performance is as follows:\n{student_history}\n"
            f"Please ensure that the format of the generated exercises is consistent with the following example. If the knowledge concept in the new exercise overlaps with one from the historical records, keep the name of the knowledge concept unchanged. \n"
            f"Meanwhile, you only need to output the exercises according to the format, without containing any irrelevant statements\n"
            f"1. **Exercise:** {{题目}}\n"
            f"- **Options:** {{'A': '选项1', 'B': '选项2', 'C': '选项3', 'D': '选项4'}}\n"
            f"- **Answer:** ['正确答案']\n"
            f"- **Concept:** 知识点\n"
        )
    elif method == "few_shot_chain_of_thought":
        example_text = (
            "Example: Student's Answer Record and Generated Exercise:\n"
            "Student's performance in answering history exercises:\n"
            "1. content: 不同 VLAN 间数据通信，需通过（ ）进行转发。\n"
            "   option: {'A': 'HUB', 'B': '二层交换机', 'C': '路由器', 'D': '中继器'}\n"
            "   answer: ['C']\n"
            "   is_correct: 0\n"
            "   concept_id: K_二层交换机_计算机科学与技术\n"
            "2. content: 虚拟局域网 VLAN 可根据以下哪些方式划分（）。\n"
            "   option: {'A': '根据端口划分 VLAN', 'B': '根据 MAC 地址划分 VLAN', 'C': '根据网络层（IP 地址）划分 VLAN', 'D': 'IP 组播作为 VLAN'}\n"
            "   answer: ['A', 'B', 'C', 'D']\n"
            "   is_correct: 0\n"
            "   concept_id: K_IP地址_信息与通信工程\n"
            "3. content: 为保证从分布式存储系统中读取的数据正确，需要采用哪种数据处理方式（ ）。\n"
            "   option: {'A': '压缩', 'B': '多份存储', 'C': 'Erasure coding 编码', 'D': 'Checksum 数据校验'}\n"
            "   answer: ['D']\n"
            "   is_correct: 1\n"
            "   concept_id: K_分布式存储系统_计算机科学与技术\n"
            "Analysis based on the thought chain:\n"
            "Step 1: Analyze the student's performance in answering history exercises:\n"
            "   - Knowledge concepts that students answered incorrectly:\n"
            "       - knowledge concept: 不同 VLAN 间通信。\n"
            "       - Reason for mistake: 混淆了二层交换机和路由器的功能。\n"
            "   - Knowledge concepts answered correctly by students:\n"
            "       - knowledge concept: VLAN 划分。\n"
            "       - Reason for correctness: 学生对基本的 VLAN 划分方式掌握良好。\n"
            "   - New knowledge concepts that students have not been exposed to:\n"
            "       - knowledge concept: 分布式存储系统的数据校验机制。\n"
            "Step 2: Set the exercise design goals and requirements:\n"
            "   - For incorrect knowledge concepts (e.g., 不同 VLAN 间通信):\n"
            "       - Goal: 巩固 VLAN 通信相关设备的理解。\n"
            "   - For correct knowledge concepts (e.g., VLAN 划分):\n"
            "       - Goal: 在复杂场景下测试 VLAN 划分的灵活应用。\n"
            "   - For new knowledge concepts (e.g., 分布式存储系统):\n"
            "       - Goal: 引入分布式存储系统的基础知识，拓展学习范围。\n"
            "Step 3: Validate and optimize the generated exercises:\n"
            "   - Ensure logical integrity: Verify that there is no ambiguity between the exercise and the options.\n"
            "   - Check distractor options: Make them plausible but not misleading.\n"
            "   - Optimize language clarity: Ensure the exercises are clear and easy to understand.\n"
            "Generated Exercise:\n"
            "1. **Exercise:** 以下设备中哪种可以用来实现不同 VLAN 间的通信？( )\n"
            "   - **Options:** {'A': 'HUB', 'B': '二层交换机', 'C': '路由器', 'D': '中继器'}\n"
            "   - **Answer:** ['C']\n"
            "   - **Concept:** K_二层交换机_计算机科学与技术\n"
            "2. **Exercise:** VLAN 划分的常见方式有哪些？( )\n"
            "   - **Options:** {'A': '根据端口划分 VLAN', 'B': '根据 MAC 地址划分 VLAN', 'C': '根据网络层（IP 地址）划分 VLAN', 'D': 'IP 组播作为 VLAN'}\n"
            "   - **Answer:** ['A', 'B', 'C']\n"
            "   - **Concept:** K_IP地址_信息与通信工程\n"
            "3. **Exercise:** 分布式存储系统中，为了确保读取数据的正确性，哪种方法是最佳选择？( )\n"
            "   - **Options:** {'A': '压缩', 'B': '多份存储', 'C': 'Erasure coding 编码', 'D': 'Checksum 数据校验'}\n"
            "   - **Answer:** ['D']\n"
            "   - **Concept:** K_分布式存储系统_计算机科学与技术\n"
        )
        return (
            f"You are an expert in generating single-choice exercises for educational purposes.\n"
            f"Your task is to create 10 high-quality single-choice exercises in Chinese by following a thought chain and using the examples provided.\n"
            f"Please follow these steps to create the exercises:\n"
            f"1. Analyze the student's performance in answering history exercises:\n"
            f"   - Identify weak aspects to reinforce learning by focusing on knowledge concepts the student answered incorrectly.\n"
            f"   - Test stable mastery of knowledge concepts the student answered correctly.\n"
            f"   - Introduce appropriate new knowledge concepts to expand the student's learning scope.\n"
            f"2. Ensure that the generated exercises meet the following requirements:\n"
            f"   - Reinforce weak knowledge concepts (those the student answered incorrectly).\n"
            f"   - Test knowledge concepts the student has already mastered.\n"
            f"   - Introduce new knowledge concepts relevant to the field (e.g., computer science).\n"
            f"3. Validate and optimize the generated exercises:\n"
            f"   - Verify the logical integrity of each exercise to ensure clarity and accuracy.\n"
            f"   - Ensure distractor options are plausible but not misleading.\n"
            f"   - Optimize the language to make the exercises clear and easy to understand.\n"
            f"Example of exercise generation is as follows:\n{example_text}\n"
            f"Student's historical exercise performance is as follows:\n{student_history}\n"
            f"Please ensure that the format of the generated exercises is consistent with the following example. If the knowledge concept in the new exercise overlaps with one from the historical records, keep the name of the knowledge concept unchanged. \n"
            f"Meanwhile, you only need to output the exercises according to the format, without containing any irrelevant statements\n"
            f"1. **Exercise:** {{题目}}\n"
            f"- **Options:** {{'A': '选项1', 'B': '选项2', 'C': '选项3', 'D': '选项4'}}\n"
            f"- **Answer:** ['正确答案']\n"
            f"- **Concept:** 知识点\n"
        )

# 创建每种方法的代理
def create_agent(name, prompt):
    return ConversableAgent(
        name=name,
        llm_config=llm_config,
        system_message=prompt
    )

def prepare_student_history():
    # 提取学生的历史作答记录并标准化格式
    student_history_records = stuRec_1000_with_tokens.head(10).to_dict(orient="records")
    student_history = "\n".join([
        f"content: {record['content']}\n"
        f"option: {record['option']}\n"
        f"answer: {record['answer']}\n"
        f"is_correct: {record['is_correct']}\n"
        f"concept_id: {record['concept_id']}\n"
        for record in student_history_records
    ])
    return student_history

# 保存实验结果到文件
def save_results_to_file(method, results):
    file_path = "res_Single_Choice.txt"
    with open(file_path, "a", encoding="utf-8") as file:
        file.write(f"========== {method.upper()} ==========\n")
        file.write(results + "\n\n")
    print(f"Results for {method} saved to {file_path}")

# 运行特定方法的实验
def run_experiment(method, student_history):
    try:
        print("=" * 50)
        print(f"运行方法:{method}")
        print("=" * 50)

        prompt = get_prompt(method, student_history)
        agent = create_agent(f"agent_{method}", prompt)

        print("生成的提示词:\n", prompt)

        response = agent.generate_reply(messages=[{"content": "生成习题", "role": "user"}])

        if not response:
            raise ValueError("API响应为空。请检查配置或网络。")

        print(f"{method} 的响应:\n", response)

        save_results_to_file(method, response)

        return response

    except Exception as e:
        print(f"运行方法 {method} 时出错：{e}")

if __name__ == "__main__":
    student_history = prepare_student_history()

    # 比较的方法
    methods = ["zero_shot", "few_shot", "chain_of_thought", "few_shot_chain_of_thought"]

    for method in methods:
        run_experiment(method, student_history)
