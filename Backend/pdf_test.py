from analyzer import analyze_cfd_file
from report_generator import generate_pdf
from ai_assistant import generate_summary


file_path = "../Data/results.csv"

# Analyze CFD data
results = analyze_cfd_file(file_path)

# Generate AI analysis
summary = generate_summary(results)

# Generate PDF
output = "../generated/CFD_Report.pdf"

generate_pdf(
    results,
    summary,
    output
)

print("PDF generated successfully!")
print("Location:", output)