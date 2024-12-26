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
user_profile = pandas.read_csv("subject_data(1)/user_profile.csv")

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

# 采样1000个用户的答题数据
user_profile = user_profile[["user_id"]]
stuRec_1000 = pandas.merge(user_problem, user_profile, on="user_id")
print(len(stuRec_1000))
stuRec_1000 = pandas.merge(stuRec_1000, problem[["problem_id", "content", "option", "answer"]], on="problem_id")
print(len(stuRec_1000))
stuRec_1000 = pandas.merge(stuRec_1000, problem_concept.drop_duplicates(subset="problem_id"), on="problem_id")
print(len(stuRec_1000))
stuRec_1000 = pandas.merge(stuRec_1000, course_problem[["course_id", "problem_id"]], on="problem_id")
print(len(stuRec_1000))
stuRec_1000 = pandas.merge(stuRec_1000, course_profile[["course_id", "name"]], on="course_id")
print(len(stuRec_1000))
stuRec_1000.to_csv("subject_data(1)/stuRec_1000.csv", index=False)

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

# for index, row in example.iterrows():
#     chain = get_chain(row['concept_id'], row['concept_id'])
#     example.at[index, 'knowledge_chain'] = chain
#
# example.to_csv("subject_data(1)/example.csv", index=False)

# 构造提示词


# 排查循环错误
# a = 0
# for index1, row1 in concept_relation_filtered.iterrows():
#     for index2, row2 in concept_relation_filtered.iterrows():
#         if row1['c1'] == row2['c2'] and row1['c2'] == row2['c1']:
#             print(row1['c1'], row1['c2'])
#             a = a + 1
#
# print(a)
