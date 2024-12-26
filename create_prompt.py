import pandas
import json

problem = pandas.read_csv("subject_data(1)/problem.csv")
problem_concept = pandas.read_csv("subject_data(1)/problem_concept.csv")
concept = pandas.read_csv("subject_data(1)/concept.csv")
concept_relation = pandas.read_csv("subject_data(1)/concept_relationship.csv")
user_problem = pandas.read_csv("subject_data(1)/user_problem.csv")
stuRec = pandas.read_csv("subject_data(1)/stuRec.csv")
example = pandas.read_csv("subject_data(1)/example.csv")
examples_with_explanation = pandas.read_csv("subject_data(1)/examples_with_explanation.csv")
concept_relation_filtered = pandas.read_csv("subject_data(1)/concept_relationship_filtered.csv")
course_profile = pandas.read_csv("subject_data(1)/course_profile.csv")
course_problem = pandas.read_csv("subject_data(1)/course_problem.csv")


def get_chain(concept, chain):
    filtered_df = concept_relation_filtered[concept_relation_filtered['c2'] == concept]
    if not filtered_df.empty:
        # 若还存在上级知识点，则链接新链后进行递归
        first_row = filtered_df.head(1)
        upper_concept = first_row['c1'].iloc[0]
        chain = upper_concept + "-" + chain
        return get_chain(upper_concept, chain)
    else:
        return chain


text = {
    "examples": [],
    "tasks": []
}

examples_with_explanation = examples_with_explanation.groupby('concept_id').head(1)
examples_with_explanation = pandas.merge(stuRec[['concept_id']].head(10), examples_with_explanation, on='concept_id',
                                         how='left')
example_data = examples_with_explanation.to_dict(orient='records')
text["examples"] = example_data

selected_columns = ['content', 'option', 'answer', 'course_name', 'concept_id', 'is_correct']
stuRec = stuRec[selected_columns]

stuRec["knowledge_chain"] = ""
for index, row in stuRec.iterrows():
    chain = get_chain(row['concept_id'], row['concept_id'])
    stuRec.at[index, 'knowledge_chain'] = chain

stuRec = stuRec.head(10)
stuRec["explanation"] = ""
stuRec = stuRec.to_dict(orient='records')
text["tasks"] = stuRec

text = json.dumps(text, ensure_ascii=False, indent=4)

# 将提示词文本转换为自然语言形式
n_text = json.loads(text)


def convert_to_natural_language(n_text):
    natural_language_text = ""

    # 处理examples
    natural_language_text += "examples:\n"
    flag = 0
    for example in n_text['examples']:
        content = example['content']
        options = example['option']
        answer = example['answer']
        is_correct = example['is_correct']
        concept_id = example['concept_id']
        course_name = example['course_name']
        knowledge_chain = example['knowledge_chain']
        explanation = example['explanation']

        flag += 1
        natural_language_text += str(flag) + ",\n"

        natural_language_text += "content:" + content + "\n"
        natural_language_text += "option:" + options + "\n"
        natural_language_text += "answer:" + answer + "\n"
        natural_language_text += "is_correct:" + str(is_correct) + "\n"
        natural_language_text += "concept_id:" + concept_id + "\n"
        natural_language_text += "course_name:" + course_name + "\n"
        natural_language_text += "knowledge_chain:" + knowledge_chain + "\n"
        natural_language_text += "explanation:" + explanation + "\n"

    # 处理tasks，逻辑与examples相同
    natural_language_text += "tasks:\n"
    flag = 0
    for task in n_text['tasks']:
        content = task['content']
        options = task['option']
        answer = task['answer']
        is_correct = task['is_correct']
        concept_id = task['concept_id']
        course_name = task['course_name']
        knowledge_chain = task['knowledge_chain']
        explanation = task['explanation']

        flag += 1
        natural_language_text += str(flag) + ",\n"
        natural_language_text += "content:" + content + "\n"
        natural_language_text += "option:" + options + "\n"
        natural_language_text += "answer:" + answer + "\n"
        natural_language_text += "is_correct:" + str(is_correct) + "\n"
        natural_language_text += "concept_id:" + concept_id + "\n"
        natural_language_text += "course_name:" + course_name + "\n"
        natural_language_text += "knowledge_chain:" + knowledge_chain + "\n"
        natural_language_text += "explanation:" + explanation + "\n"

    return natural_language_text


n_text = convert_to_natural_language(n_text)
