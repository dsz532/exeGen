import pandas as pd
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Evaluate error coverage rate for exercises.")
    parser.add_argument("--exercise_type", type=str, required=True, help="Single_Choice, Multiple_Choice, or TrueorFalse")
    args = parser.parse_args()

    if args.exercise_type not in ["Single_Choice", "Multiple_Choice", "TrueorFalse"]:
        raise ValueError("Invalid exercise type. Choose from Single_Choice, Multiple_Choice, or TrueorFalse.")

    return args.exercise_type

if __name__ == "__main__":
    exercise_type = parse_arguments()

    student_history_path = "student_history.xlsx"
    exercises_path = f"exercises_concepts_{exercise_type}.xlsx"
    output_path = f"ECR_evaluation_results_{exercise_type}.xlsx"

    student_history_df = pd.read_excel(student_history_path, header=None, names=["Concepts", "Is_Correct"])

    # 提取学生历史作答记录中做错的知识点
    error_concepts = student_history_df[student_history_df["Is_Correct"] == 0]["Concepts"].tolist()

    # 读取题目对应的知识点
    exercises_df = pd.read_excel(exercises_path, header=None, names=["Concepts"])

    methods = ["zero_shot", "few_shot", "chain_of_thought", "few_shot_chain_of_thought", "AdaExam"]
    method_results = {}

    for i, method in enumerate(methods):
        # 提取当前方法的知识点（每种方法10行，分别从50行中切片）
        method_concepts = exercises_df.iloc[i * 10:(i + 1) * 10]["Concepts"].tolist()

        # 错误覆盖率 (ECR) 计算
        error_covered_count = sum(1 for concept in method_concepts if concept in error_concepts)
        error_coverage_rate = error_covered_count / len(method_concepts) if method_concepts else 0

        method_results[method] = {
            "Error Coverage Rate (ECR)": round(error_coverage_rate, 2)
        }

    results_df = pd.DataFrame.from_dict(method_results, orient="index")
    results_df.index.name = "Method"
    results_df.reset_index(inplace=True)
    results_df.to_excel(output_path, index=False)

    print(f"评估结果已成功保存至 {output_path}")
