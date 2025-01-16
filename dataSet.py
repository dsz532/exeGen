import pandas

# problem = pandas.read_csv("subject_data(1)/problem.csv")
# problem_concept = pandas.read_csv("subject_data(1)/problem_concept.csv")
# concept = pandas.read_csv("subject_data(1)/concept.csv")
# concept_relation = pandas.read_csv("subject_data(1)/concept_relationship.csv")
# user_problem = pandas.read_csv("subject_data(1)/user_problem.csv")
stuRec_1000_with_tokens = pandas.read_csv("subject_data(1)/stuRec_1000_with_tokens.csv")
# example = pandas.read_csv("subject_data(1)/example.csv")
# examples_with_explanation = pandas.read_csv("subject_data(1)/examples_with_explanation.csv")
concept_relation_filtered = pandas.read_csv("subject_data(1)/concept_relationship_filtered.csv")

# course_profile = pandas.read_csv("subject_data(1)/course_profile.csv")
# course_problem = pandas.read_csv("subject_data(1)/course_problem.csv")
# user_profile = pandas.read_csv("subject_data(1)/user_profile.csv")
examples_with_explanation_with_tokens = pandas.read_csv("subject_data(1)/examples_with_explanation_with_tokens.csv")

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
# user_profile = user_profile[["user_id"]]
# stuRec_1000 = pandas.merge(user_problem, user_profile, on="user_id")
# print(len(stuRec_1000))
# stuRec_1000 = pandas.merge(stuRec_1000, problem[["problem_id", "content", "option", "answer"]], on="problem_id")
# print(len(stuRec_1000))
# stuRec_1000 = pandas.merge(stuRec_1000, problem_concept.drop_duplicates(subset="problem_id"), on="problem_id")
# print(len(stuRec_1000))
# stuRec_1000 = pandas.merge(stuRec_1000, course_problem[["course_id", "problem_id"]], on="problem_id")
# print(len(stuRec_1000))
# stuRec_1000 = pandas.merge(stuRec_1000, course_profile[["course_id", "name"]], on="course_id")
# print(len(stuRec_1000))
# stuRec_1000.to_csv("subject_data(1)/stuRec_1000.csv", index=False)

# 添加带有explanation属性的example表
# example["explanation"] = "No explanation provided."
# selected_columns = ['content', 'option', 'answer', 'is_correct', 'concept_id','course_name', 'knowledge_chain', 'explanation']
# df_selected = example[selected_columns]
# df_selected.to_csv('subject_data(1)/examples_with_explanation(short).csv', index=False)

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

# 用bert生成句向量
# vocab_file = 'bert/vocab.txt'
# tokenizer = BertTokenizer(vocab_file)
# bert = BertModel.from_pretrained('bert/bert-base-chinese')
# examples_with_explanation["tokens"] = ""
#
# for index, row in examples_with_explanation.iterrows():
#     sentence = ""
#     sentence += row['content']
#     sentence += str(row['option'])
#     sentence += row['right_answer']
#     sentence += str(row['is_correct'])
#     sentence += row['concept_id']
#     sentence += row['course_name']
#     sentence += row['knowledge_chain']
#     # sentence += row['explanation']
#
#     text_dict = tokenizer.encode_plus(sentence, add_special_tokens=True, return_attention_mask=True)
#     input_ids = torch.tensor(text_dict['input_ids']).unsqueeze(0)
#     token_type_ids = torch.tensor(text_dict['token_type_ids']).unsqueeze(0)
#     attention_mask = torch.tensor(text_dict['attention_mask']).unsqueeze(0)
#
#     res = bert(input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids)
#     tokens = res[0].detach().squeeze(0)
#     tokens = torch.sum(tokens, dim=0).tolist()
#     print(len(tokens))
#     examples_with_explanation.at[index, 'tokens'] = tokens
#
# examples_with_explanation.to_csv("subject_data(1)/examples_with_explanation_with_tokens.csv", index=False)

# 获取知识链
# chain = ""
#
#
# def get_chain(concept):
#     global chain
#     filtered_df = concept_relation_filtered[concept_relation_filtered['c2'] == concept]
#     if not filtered_df.empty:
#         # 若还存在上级知识点，则链接新链后进行递归
#         for index, row in filtered_df.iterrows():
#             upper_concept = row['c1']
#             under_concept = row['c2']
#             temp = under_concept + "的先修为" + upper_concept + ", "
#             if chain.find(temp) != -1:
#                 continue
#             chain += temp
#             get_chain(upper_concept)
#         return
#     else:
#         return
#
#
# examples_with_explanation_with_tokens['knowledge_chain'] = ""
# for index, row in examples_with_explanation_with_tokens.iterrows():
#     chain = ""
#     get_chain(row['concept_id'])
#     examples_with_explanation_with_tokens.at[index, 'knowledge_chain'] = chain
#
# examples_with_explanation_with_tokens.to_csv("subject_data(1)/examples_with_explanation_with_tokens.csv", index=False)

examples_with_explanation_with_tokens["knowledge_evidence"] = ""
for index, row in examples_with_explanation_with_tokens.iterrows():
    examples_with_explanation_with_tokens.at[index, 'knowledge_evidence'] += "题目对应知识点为" + row[
        'concept_id'] + ", "
    examples_with_explanation_with_tokens.at[index, 'knowledge_evidence'] += row['concept_id'] + "对应的课程为" + row[
        'course_name'] + ", "
    # if not str(row['knowledge_chain']) == "nan":
    #     examples_with_explanation_with_tokens.at[index, 'knowledge_evidence'] += row['knowledge_chain']

examples_with_explanation_with_tokens.to_csv("subject_data(1)/examples_with_explanation_with_tokens.csv")
