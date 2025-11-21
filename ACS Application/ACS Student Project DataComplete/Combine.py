import pandas as pd
import os

# 📁 Folder path (current directory)
folder_path = "/Users/brendanfox/Desktop/ACS Application/ACS Student Project DataComplete"

# ✔️ Target filenames (simple format)
procedures = [
    "Appendectomy",
    "Hernia Repair",
    "Cholecystectomy",
    "Tonsillectomy",
    "Cataract Surgery"
]

# 📥 Combine all CSVs into one dataframe
dfs = []
for proc in procedures:
    filename = f"{proc}.csv"
    filepath = os.path.join(folder_path, filename)
    if os.path.exists(filepath):
        df = pd.read_csv(filepath)
        df["Procedure"] = proc  # Tag with procedure name
        dfs.append(df)
        print(f"✅ Loaded: {filename}")
    else:
        print(f"⚠️ Missing: {filename}")

# 📊 Combine and export
if dfs:
    combined_df = pd.concat(dfs, ignore_index=True)
    output_path = os.path.join(folder_path, "master_combined_data.csv")
    combined_df.to_csv(output_path, index=False)
    print(f"\n✅ Combined file saved to:\n{output_path}")
else:
    print("🚫 No files were combined. Check filenames or folder path.")