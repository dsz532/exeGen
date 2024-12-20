
import pandas
import agents
import json

problem = pandas.read_csv("subject_data(1)/problem.csv")
problem_concept = pandas.read_csv("subject_data(1)/problem_concept.csv")
concept = pandas.read_csv("subject_data(1)/concept.csv")
concept_relation = pandas.read_csv("subject_data(1)/concept_relationship.csv")
user_problem = pandas.read_csv("subject_data(1)/user_problem.csv")
stuRec = pandas.read_csv("subject_data(1)/stuRec.csv")
example = pandas.read_csv("subject_data(1)/example.csv")
examples_with_explanation = pandas.read_csv("subject_data(1)/examples_with_explanation.csv")

# 构造example
# top3_problems = problem_concept.groupby('concept_id').head(1).reset_index(drop=True)
# result_df = pandas.merge(problem_concept, problem, on='problem_id', how='left')
# result_df = pandas.merge(user_problem, result_df, on='problem_id', how='left')
# result_df = result_df.dropna(subset=['title'])

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
# selected_columns = ['content', 'option', 'answer', 'is_correct', 'explanation']
# df_selected = example[selected_columns]
# df_selected = df_selected.head(20)
# df_selected.to_csv('subject_data(1)/examples_with_explanation.csv', index=False)

# 递归计算知识链
# example["knowledge_chain"] = ""
#
#
# def get_chain(concept, chain):
#     filtered_df = concept_relation[concept_relation['c1'] == concept]
#     if not filtered_df.empty:
#         # 若还存在上级知识点，则链接新链后进行递归
#         first_row = filtered_df.head(1)
#         upper_concept = first_row['c2'].iloc[0]
#         chain = upper_concept + "-" + chain
#         return get_chain(upper_concept, chain)
#     else:
#         return chain
#
#
# for index, row in example.iterrows():
#     chain = get_chain(row['concept_id'], row['concept_id'])
#     example.at[index, 'knowledge_chain'] = chain
#
# example.to_csv("subject_data(1)/example.csv", index=False)

# text = {
#     "examples": [],
#     "tasks": []
# }
#
# example_data = examples_with_explanation.to_dict(orient='records')
# example_json = json.dumps(example_data, ensure_ascii=False, indent=4)
#
# text["examples"] = example_data
# text = json.dumps(text, ensure_ascii=False, indent=4)
# print(text)

a = 0
for index1, row1 in concept_relation.iterrows():
    for index2, row2 in concept_relation.iterrows():
        if row1['c1'] == row2['c2'] and row1['c2'] == row2['c1']:
            print(row1['c1'], row1['c2'])
            a = a + 1

print(a)
