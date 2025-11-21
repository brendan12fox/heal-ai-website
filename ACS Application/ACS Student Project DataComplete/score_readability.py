import pandas as pd
from textstat import flesch_kincaid_grade, smog_index, flesch_reading_ease

# Load your master file (adjust filename/path if needed)
df = pd.read_csv("master_combined_backtranslated.csv")

# Make sure the Reverse-Translated Output column exists
if "Reverse-Translated Output" not in df.columns:
    raise ValueError("Column 'Reverse-Translated Output' not found in the CSV")

# Apply readability formulas to each reverse-translated output
df["FKGL Score"] = df["Reverse-Translated Output"].apply(lambda text: flesch_kincaid_grade(str(text)) if pd.notna(text) else None)
df["SMOG Score"] = df["Reverse-Translated Output"].apply(lambda text: smog_index(str(text)) if pd.notna(text) else None)
df["Flesch Ease"] = df["Reverse-Translated Output"].apply(lambda text: flesch_reading_ease(str(text)) if pd.notna(text) else None)

# Save the new version of the file
df.to_csv("master_scored.csv", index=False)
print("✅ Readability scores added and saved to master_scored.csv")