import openai
import pandas as pd
import textstat
import time
import os
from dotenv import load_dotenv

# --- SETUP ---
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("OPENAI_API_KEY environment variable must be set")

procedures = [
    "Appendectomy",
    "Inguinal Hernia Repair",
    "Cholecystectomy",
    "Tonsillectomy",
    "Colonoscopy"
]

languages = ["English", "Spanish", "Arabic", "Bengali"]
reading_levels = ["2nd Grade", "6th Grade", "High School"]

# --- HELPER FUNCTIONS ---

def build_prompt(procedure, language, level):
    return f"""
You are a medical assistant. Write clear and easy-to-read patient instructions in {language} for a {level} reading level.

Include the following **PRE-OPERATIVE** sections for {procedure}:
1. What the procedure is
2. Why it is needed
3. Risks and complications
4. Benefits
5. Alternatives
6. Recovery expectations
7. Patient rights to ask questions or refuse

Then include the following **POST-OPERATIVE** sections:
1. Wound care
2. Pain management
3. Activity restrictions
4. Diet
5. When to call the doctor
6. Red flag symptoms
7. Follow-up instructions
"""

def call_gpt(prompt, model="gpt-4o"):
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"GPT Error: {e}")
        return ""

def back_translate(text, lang):
    prompt = f"Translate the following medical instructions from {lang} back into English. Keep formatting:\n\n{text}"
    return call_gpt(prompt)

def score_readability(text):
    return {
        "FKGL Score": round(textstat.flesch_kincaid_grade(text), 2),
        "SMOG Score": round(textstat.smog_index(text), 2),
        "Flesch Ease": round(textstat.flesch_reading_ease(text), 2)
    }

# --- MAIN SCRIPT ---

results = []

for procedure in procedures:
    for lang in languages:
        for level in reading_levels:
            print(f"⏳ Generating: {procedure} | {lang} | {level}")
            prompt = build_prompt(procedure, lang, level)
            output = call_gpt(prompt)
            time.sleep(2)

            if not output:
                continue

            if lang == "English":
                backtranslated = ""
                scores = score_readability(output)
            else:
                backtranslated = back_translate(output, lang)
                time.sleep(2)
                scores = score_readability(backtranslated)

            results.append({
                "Procedure": procedure,
                "Language": lang,
                "Reading Level": level,
                "GPT Output": output,
                "Backtranslated English": backtranslated,
                **scores
            })

# --- EXPORT ---
df = pd.DataFrame(results)
df.to_excel("gpt_procedure_instructions.xlsx", index=False)
print("✅ All instructions saved to gpt_procedure_instructions.xlsx")	