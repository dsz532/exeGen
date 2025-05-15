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

    current_section = None
    for line in lines:
        line = line.strip()
        if line.startswith("==========") and any(section in line for section in sections):
            current_section = line.split()[-1]
        elif line.startswith("- **Concept:**") and current_section:
            concept_name = line.split(":")[-1].strip().replace("**", "").strip()

            concept_name = concept_name.lstrip("!@#$%^&*()-+=~`<>,./?;:'\"|\\[]{} ")
            concept_data.append(concept_name)

    concept_df = pd.DataFrame(concept_data, columns=["Knowledge Concepts"])

    concept_df.to_excel(output_path, index=False, header=False)

    print(f"saved as：{output_path}")
