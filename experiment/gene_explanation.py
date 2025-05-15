import pandas
from autogen import *
import json

examples_with_explanation = pandas.read_csv("../subject_data/examples_with_explanation_with_tokens.csv")

llm_config = {
    "cache_seed": None,
    "config_list": [{
        "model": "openai/gpt-4o",
        "base_url": "https://openrouter.ai/api/v1",
        "api_key": "",
        "price": [0, 0]
    }]

}

agent_explanation = ConversableAgent(
    name="agent_explanation",
    llm_config=llm_config,
    system_message="You are an interpreter, and you will receive a record of a student's work in json format that contains the content of the exercise, the answer, and whether it was correct or not. "
                   "You need to provide a short explanation for each record based on this information, explaining why the student answered the question incorrectly or correctly."
                   "The only thing you return is the json text containing the explanation, don't use snippet markup.",
    human_input_mode="NEVER",
)

# examples_with_explanation["explanation"] = "No explanation provided."
examples_with_explanation = examples_with_explanation[
    ["problem_id", "user_id", "content", "option", "right_answer", "concept_id", "course_name", "knowledge_chain",
     "is_correct", "explanation", "tokens", "knowledge_evidence"]]
examples_with_explanation = examples_with_explanation.drop_duplicates()

for index, row in examples_with_explanation[
    examples_with_explanation["explanation"] == "No explanation provided."].iterrows():
    row = row.to_dict()
    row = json.dumps(row, ensure_ascii=False, indent=4)
    res = agent_explanation.generate_reply(
        messages=[{"content": row, "role": "user"}],
    )
    print(res)
    res = json.loads(res)
    examples_with_explanation.at[index, "explanation"] = res["explanation"]
    examples_with_explanation.to_csv("subject_data/examples_with_explanation_with_tokens.csv", index=False)
