import pandas as pd
import openai
import time
import os
from openai import OpenAI
from dotenv import load_dotenv

# ✅ Create the client (reads OPENAI_API_KEY from environment variable)
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable must be set")
client = OpenAI(api_key=api_key)

# 📂 Load the master file
df = pd.read_csv("master_combined_data.csv")

# 🔍 Filter rows to translate
to_translate = df[
    (df["Instruction Type"].str.lower() == "pre-op") &
    (df["Language"].str.lower() != "english") &
    (df["Reverse-Translated Output"].isna() | df["Reverse-Translated Output"].eq(""))
].copy()

print(f"🎯 Rows to back-translate: {len(to_translate)}")

# 🔁 Back-translation function (new syntax)
def back_translate(text, lang):
    prompt = f"Translate this {lang} surgical instruction back into clear English:\n\n{text}"
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ Error: {e}")
        return ""

# 🔄 Process each row
results = []
for idx, row in to_translate.iterrows():
    print(f"🔄 Translating row {idx}: {row['Procedure']} ({row['Language']}, {row['Reading Level']})")
    translation = back_translate(row["GPT Output"], row["Language"])
    results.append((idx, translation))
    time.sleep(1.5)

# ✍️ Update DataFrame
for idx, translation in results:
    df.at[idx, "Reverse-Translated Output"] = translation

# 💾 Save updated file
df.to_csv("master_combined_backtranslated.csv", index=False)
print("✅ Done! Saved to: master_combined_backtranslated.csv")