import pandas
import json
import numpy as np
import ast
import re

from pandas.core.interchange.dataframe_protocol import DataFrame

stuRec_1000_with_tokens = pandas.read_csv("../subject_data(1)/stuRec_1000_with_tokens.csv")
examples_with_explanation_with_tokens = pandas.read_csv("../subject_data(1)/examples_with_explanation_with_tokens.csv")
concept_relation_filtered = pandas.read_csv("../subject_data(1)/concept_relationship_filtered.csv")


def get_chain(concept, chain):
    filtered_df = concept_relation_filtered[concept_relation_filtered['c2'] == concept]
    if not filtered_df.empty:
        first_row = filtered_df.head(1)
        upper_concept = first_row['c1'].iloc[0]
        chain = upper_concept + "-" + chain
        return get_chain(upper_concept, chain)
    else:
        return chain


def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)


def get_examples_by_similarity(example, rec):

    result_rows = []


    for i, rec_row in rec.iterrows():
        rec_tokens = ast.literal_eval(rec_row['tokens'])


        max_similarity = -1
        max_index = -1


        for j, example_row in example.iterrows():
            example_tokens = ast.literal_eval(example_row['tokens'])


            similarity = cosine_similarity(rec_tokens, example_tokens)


            if similarity > max_similarity:
                max_similarity = similarity
                max_index = j


        result_rows.append(example.iloc[max_index])

    result_df = pandas.DataFrame(result_rows)

    return result_df


def get_examples_by_concept(example, rec):
    result_rows = []
    for index, rec_row in rec.iterrows():
        temp = example[example['concept_id'] == rec_row['concept_id']]
        if temp.empty: continue
        if not example[(example['concept_id'] == rec_row['concept_id']) & (example['is_correct'] == 0)].empty:
            result_rows.append(
                example[(example['concept_id'] == rec_row['concept_id']) & (example['is_correct'] == 0)].iloc[0])
        if not example[(example['concept_id'] == rec_row['concept_id']) & (example['is_correct'] == 1)].empty:
            result_rows.append(
                example[(example['concept_id'] == rec_row['concept_id']) & (example['is_correct'] == 1)].iloc[0])
        rec = rec[rec['concept_id'] != rec_row['concept_id']]
    return pandas.DataFrame(result_rows), rec

# print(text)
# print(n_text)
