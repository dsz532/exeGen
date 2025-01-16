import pandas as pd
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Extract knowledge concepts from exercise files.")
    parser.add_argument("--exercise_type", type=str, required=True, help="Single_Choice, Multiple_Choice, or TrueorFalse")
    args = parser.parse_args()

    if args.exercise_type not in ["Single_Choice", "Multiple_Choice", "TrueorFalse"]:
        raise ValueError("Invalid exercise type. Choose from Single_Choice, Multiple_Choice, or TrueorFalse.")

    return args.exercise_type

if __name__ == "__main__":
    exercise_type = parse_arguments()

    input_path = f"res_{exercise_type}.txt"
    output_path = f"exercises_concepts_{exercise_type}.xlsx"

    concept_data = []

    sections = ["ZERO_SHOT", "FEW_SHOT", "CHAIN_OF_THOUGHT", "FEW_SHOT_CHAIN_OF_THOUGHT", "AdaExam"]

    with open(input_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # 提取知识点信息
    current_section = None
    for line in lines:
        line = line.strip()
        # 检测当前段落
        if line.startswith("==========") and any(section in line for section in sections):
            current_section = line.split()[-1]  # 获取当前方法名称（如 ZERO_SHOT）
        elif line.startswith("- **Concept:**") and current_section:
            # 提取 Concept，从第一个字母开始读取，不包含 "**"
            concept_name = line.split(":")[-1].strip().replace("**", "").strip()

            # 确保知识点从字母开始（去除可能的非字母开头字符）
            concept_name = concept_name.lstrip("!@#$%^&*()-+=~`<>,./?;:'\"|\\[]{} ")  # 去除前缀非字母字符
            concept_data.append(concept_name)

    concept_df = pd.DataFrame(concept_data, columns=["Knowledge Concepts"])

    # 保存到 Excel 文件
    concept_df.to_excel(output_path, index=False, header=False)

    print(f"知识点已成功提取并保存为 Excel 文件：{output_path}")
