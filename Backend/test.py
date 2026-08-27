from analyzer import analyze_cfd_file
from visualization import create_graphs
from ai_assistant import generate_summary


file_path = "../data/results.csv"


# 1. Analyze CFD data

results = analyze_cfd_file(file_path)


# 2. Create graphs

create_graphs(file_path)


# 3. Send CFD results to AI

summary = generate_summary(results)


# 4. Display AI response

print("\n")
print("========== AI CFD ANALYSIS ==========")

print(summary)