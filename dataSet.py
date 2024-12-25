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


# 构造example
# top3_problems = problem_concept.groupby('concept_id').head(1).reset_index(drop=True)
# result_df = pandas.merge(problem_concept, problem, on='problem_id', how='left')
# result_df = pandas.merge(user_problem, result_df, on='problem_id', how='left')
# result_df = result_df.dropna(subset=['title'])
# result_df.to_csv("subject_data(1)/example.csv", index=False)

# 添加课程信息
# stuRec = pandas.merge(stuRec, course_problem, on="problem_id", how="left")
# selected_columns = ["course_id", "name"]
# course_profile = course_profile[selected_columns]
# stuRec = pandas.merge(stuRec, course_profile, on="course_id", how="left")
# stuRec.to_csv("subject_data(1)/stuRec.csv", index=False)

# 获取一个用户的作答记录
# result_df = pandas.merge(problem_concept, problem, on='problem_id', how='left')
# result_df = result_df.dropna(subset=['title'])
#
# user_problem = user_problem.query("user_id == 'U_29040364'")  # 样例用户对应的做题条目
# result_df = pandas.merge(user_problem, result_df, on='problem_id', how='left')
#
# result_df = result_df.dropna(subset=['concept_id'])

# result_df.to_csv("subject_data(1)/example.csv", index=False)

# 添加带有explanation属性的example表
# example["explanation"] = "No explanation provided."
# selected_columns = ['content', 'option', 'answer', 'is_correct', 'concept_id','course_name', 'knowledge_chain', 'explanation']
# df_selected = example[selected_columns]
# df_selected.to_csv('subject_data(1)/examples_with_explanation.csv', index=False)

# 删除所有无效行
# df_filtered = concept_relation[concept_relation['ground_truth'] != 0]  # 删除值为0的行
# df_filtered = df_filtered[df_filtered['ground_truth'] != -1]  # 删除值为-1的行
#
# df_filtered.to_csv('subject_data(1)/concept_relationship_filtered.csv', index=False)

# 递归计算知识链
# example["knowledge_chain"] = ""


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


# for index, row in example.iterrows():
#     chain = get_chain(row['concept_id'], row['concept_id'])
#     example.at[index, 'knowledge_chain'] = chain
#
# example.to_csv("subject_data(1)/example.csv", index=False)

# 构造提示词
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
print(n_text)

# 排查循环错误
# a = 0
# for index1, row1 in concept_relation_filtered.iterrows():
#     for index2, row2 in concept_relation_filtered.iterrows():
#         if row1['c1'] == row2['c2'] and row1['c2'] == row2['c1']:
#             print(row1['c1'], row1['c2'])
#             a = a + 1
#
# print(a)
