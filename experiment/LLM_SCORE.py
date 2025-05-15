import pandas as pd
from openai import OpenAI
from autogen import ConversableAgent
import json
import argparse

def create_agent(prompt):
    llm_config = {
        "config_list": [{
            "model": "openai/gpt-4o",
            "base_url": "https://openrouter.ai/api/v1",
            "api_key": "",
            "price": [0.5, 1.5]
        }]
    }
    return ConversableAgent(name="exercise_evaluator", llm_config=llm_config, system_message=prompt)

def parse_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    methods_data = {}
    for method in ["ZERO_SHOT", "FEW_SHOT", "CHAIN_OF_THOUGHT", "FEW_SHOT_CHAIN_OF_THOUGHT", "AdaExam"]:
        method_content = content.split(f"========== {method} ==========")[1].strip()
        exercises = method_content.split("\n\n")[:10]
        methods_data[method] = exercises
    return methods_data

def evaluate_single_dimension_with_llm(agent, prompt, dimension, methods_data):
    all_methods_exercises = []
    for method, exercises in methods_data.items():
        all_methods_exercises.append({"method_name": method, "exercises": exercises})

    dimension_prompt = f"""
    Task Description:
    You are an education expert and exercises' content evaluator specialized in **{exercise_type}**. Your task is to evaluate the generated exercises based on the specific dimension: **{dimension}**.

    Dimension Definitions:
    1. **Knowledge Relevance **: Evaluate how relevant the content of the exercises is to the knowledge points, and whether they align with the teaching objectives and content requirements.
    2. **Clarity **: Evaluate the clarity of the exercises' expression, and whether they are easy for students to understand.
    3. **Answer Accuracy **: Evaluate the accuracy of the correct answers, and whether they can accurately measure students' knowledge level.
    4. **Difficulty Appropriateness **: Evaluate whether the difficulty of the exercises is appropriate for the students' level, ensuring they are neither too easy nor too difficult.
    5. **Engagement and Fun **: Evaluate whether the exercises are engaging and fun, and whether they can stimulate students' interest in learning.
    6. **Safety and Ethics **: Evaluate whether the exercises comply with ethical standards, and ensure there is no sensitive or inappropriate content.

    Evaluation Process:
    1. For each method, evaluate the quality of 10 generated exercises based on the dimension **{dimension}**.
       - Assign probabilities for scores from 1 (lowest) to 5 (highest) in this dimension.
       - Calculate the weighted score for this dimension using the formula:
         \( S = \sum_{{i=1}}^{{N}} P_i \cdot R_i \), where:
           - \( P_i \): Probability of score \( i \).
           - \( R_i \): Score level \( i \).
           - \( N \): Total score levels (5).

    2. For each method:
       - Compute the average score across the 10 exercises to determine the method's final score in the dimension **{dimension}**.
       - Return the final scores for all five methods in the following strict JSON format, without any additional text or explanation.

    A reasonable and effective response example:
    {{
      "results": [
        {{"method_name": "ZERO_SHOT", "final_score": 3.75}},
        {{"method_name": "FEW_SHOT", "final_score": 4.20}},
        {{"method_name": "CHAIN_OF_THOUGHT", "final_score": 4.17}},
        {{"method_name": "FEW_SHOT_CHAIN_OF_THOUGHT", "final_score": 4.35}},
        {{"method_name": "AdaExam", "final_score": 4.90}}
      ]
    }}

    Important Note:
    - The response must strictly adhere to the above JSON format.
    - Do not include any additional text, comments, or explanations outside the specified JSON structure.
    """

    response = agent.generate_reply(messages=[{"content": dimension_prompt, "role": "user"}])

    if not response:
        raise ValueError("")

    try:
        cleaned_response = response.strip().strip("```json").strip("```").strip()
        response_data = json.loads(cleaned_response)
    except json.JSONDecodeError as e:
        raise ValueError(f" {e} |  {response}")

    return response_data

def evaluate_all_dimensions(file_path, prompt, output_file):
    methods_data = parse_file(file_path)
    agent = create_agent(prompt)

    dimensions = [
        "Knowledge Relevance",
        "Clarity",
        "Answer Accuracy",
        "Difficulty Appropriateness",
        "Engagement and Fun",
        "Safety and Ethics"
    ]

    combined_results = pd.DataFrame()

    for dimension in dimensions:
        print(f"using：{dimension}")
        response_data = evaluate_single_dimension_with_llm(agent, prompt, dimension, methods_data)

        if "results" not in response_data:
            raise ValueError(f"no 'results' : {response_data}")

        dimension_scores = {
            method_result["method_name"]: method_result["final_score"]
            for method_result in response_data["results"]
        }

        dimension_df = pd.DataFrame(list(dimension_scores.items()), columns=["Method", dimension])

        if combined_results.empty:
            combined_results = dimension_df
        else:
            combined_results = pd.merge(combined_results, dimension_df, on="Method", how="outer")

    combined_results.to_excel(output_file, index=False)
    print(f"saved as {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate exercises generated by different methods.")
    parser.add_argument("--exercise_type", type=str, required=True, help="Single_Choice, Multiple_Choice, or TrueorFalse")
    args = parser.parse_args()

    exercise_type = args.exercise_type

    if exercise_type not in ["Single_Choice", "Multiple_Choice", "TrueorFalse"]:
        raise ValueError("Invalid exercise type. Choose from Single_Choice, Multiple_Choice, or TrueorFalse.")

    input_file = f"res_{exercise_type}.txt"
    output_file = f"LLM_SCORE_evaluation_results_{exercise_type}.xlsx"

    evaluation_prompt = f"""
    Task Description:
    You are an education expert and exercises' content evaluator specialized in **{exercise_type}**. Your task is to evaluate the generated exercises based on specific dimensions and calculate the final score for each method.
    For each evaluation, focus exclusively on the provided dimension.
    """

    evaluate_all_dimensions(input_file, evaluation_prompt, output_file)
