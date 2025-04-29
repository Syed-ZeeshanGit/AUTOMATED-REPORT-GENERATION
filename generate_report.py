import pandas as pd
from fpdf import FPDF
from datetime import datetime

# Load CSV data
df = pd.read_csv("sample_data.csv")

# Analyze the data
total_students = len(df)
completed_count = df[df["Completed"] == "Yes"].shape[0]
average_score = df["Score"].mean()

# Group by department
department_summary = df.groupby("Department")["Score"].mean().reset_index()

# Generate the report using FPDF
class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Internship Completion Report", ln=True, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 10)
        self.cell(0, 10, f"Generated on {datetime.now().strftime('%Y-%m-%d')}", align="C")

pdf = PDFReport()
pdf.add_page()
pdf.set_font("Arial", "", 12)

# Summary
pdf.cell(0, 10, f"Total Students: {total_students}", ln=True)
pdf.cell(0, 10, f"Completed Internship: {completed_count}", ln=True)
pdf.cell(0, 10, f"Average Score: {average_score:.2f}", ln=True)

pdf.ln(10)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Average Score by Department:", ln=True)
pdf.set_font("Arial", "", 12)

for _, row in department_summary.iterrows():
    pdf.cell(0, 10, f"{row['Department']}: {row['Score']:.2f}", ln=True)

pdf.ln(20)
pdf.set_font("Arial", "I", 11)
pdf.multi_cell(0, 10, "CODTECH certifies that the above data represents internship completions as of the end date.")

# Output PDF
pdf.output("output_report.pdf")

print("✅ Report generated: output_report.pdf")
