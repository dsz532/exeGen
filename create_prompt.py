import pandas
import json
import numpy as np
import ast

from pandas.core.interchange.dataframe_protocol import DataFrame

stuRec_1000_with_tokens = pandas.read_csv("subject_data(1)/stuRec_1000_with_tokens.csv")
examples_with_explanation_with_tokens = pandas.read_csv("subject_data(1)/examples_with_explanation_with_tokens.csv")
concept_relation_filtered = pandas.read_csv("subject_data(1)/concept_relationship_filtered.csv")


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


def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)  # 确保vec1是numpy数组
    vec2 = np.array(vec2)  # 确保vec2是numpy数组
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)


def get_examples_by_similarity(example, rec):
    # 初始化一个空列表来存储结果行
    result_rows = []

    # 遍历rec的每一行
    for i, rec_row in rec.iterrows():
        rec_tokens = ast.literal_eval(rec_row['tokens'])

        # 初始化最大相似度和对应的索引
        max_similarity = -1
        max_index = -1

        # 遍历example的每一行
        for j, example_row in example.iterrows():
            example_tokens = ast.literal_eval(example_row['tokens'])

            # 计算余弦相似度
            similarity = cosine_similarity(rec_tokens, example_tokens)

            # 更新最大相似度和索引
            if similarity > max_similarity:
                max_similarity = similarity
                max_index = j

        # 将相似度最高的行添加到结果列表中
        result_rows.append(example.iloc[max_index])

    # 将结果列表转换为DataFrame
    result_df = pandas.DataFrame(result_rows)

    return result_df


text = {
    "examples": [],
    "tasks": []
}

stuRec_1000_with_tokens = stuRec_1000_with_tokens.head(10)
selected_columns1 = ['content', 'option', 'answer', 'course_name', 'concept_id', 'is_correct', 'explanation',
                     'knowledge_chain']

# 获取examples

# examples_with_explanation_with_tokens = examples_with_explanation_with_tokens.groupby('concept_id').head(1)
# examples_with_explanation_with_tokens = pandas.merge(stuRec_1000_with_tokens[['concept_id']].head(10),
#                                                      examples_with_explanation_with_tokens, on='concept_id',
#                                                      how='left')
# examples_with_explanation_with_tokens = examples_with_explanation_with_tokens[selected_columns]
# example_data = examples_with_explanation_with_tokens.to_dict(orient='records')

res = get_examples_by_similarity(examples_with_explanation_with_tokens, stuRec_1000_with_tokens)[
    selected_columns1].to_dict(orient='records')

text["examples"] = res

selected_columns2 = ['content', 'option', 'answer', 'course_name', 'concept_id', 'is_correct']
stuRec_1000_with_tokens = stuRec_1000_with_tokens[selected_columns2]

stuRec_1000_with_tokens["knowledge_chain"] = ""
for index, row in stuRec_1000_with_tokens.iterrows():
    chain = get_chain(row['concept_id'], row['concept_id'])
    stuRec_1000_with_tokens.at[index, 'knowledge_chain'] = chain

stuRec_1000_with_tokens["explanation"] = ""
stuRec_1000_with_tokens = stuRec_1000_with_tokens.to_dict(orient='records')
text["tasks"] = stuRec_1000_with_tokens

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

# print(text)
# print(n_text)
