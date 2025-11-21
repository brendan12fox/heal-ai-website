import openai
import pandas as pd
import textstat
import time
import os
from dotenv import load_dotenv

# Initialize OpenAI client
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable must be set")
client = openai.OpenAI(api_key=api_key)

# Settings
procedures = ["Appendectomy", "Cholecystectomy", "Inguinal Hernia Repair", "Mastectomy", "Cataract Surgery"]
languages = ["English", "Spanish", "Arabic", "Bengali"]
reading_levels = {
    "2nd Grade": "Write at a 2nd grade reading level.",
    "6th Grade": "Write at a 6th grade reading level.",
    "High School": "Write at a high school reading level."
}
replicates = 3

# Prompt builder
def make_prompt(procedure, lang, level, stage):
    instructions = {
        "2nd Grade": """
Write at a 2nd grade reading level.
- Use simple words that a 7–8-year-old can understand.
- Keep sentences very short (less than 10 words).
- Do not use medical terms.
- Use clear headings and short bullet points.
- Avoid abstract or complex ideas.
- Flesch-Kincaid Grade Level should be below 3.0.
""",
        "6th Grade": """
Write at a 6th grade reading level.
- Use common everyday words.
- Keep sentences short and direct.
- Avoid complex medical language unless clearly explained.
- Use bullet points for clarity.
- Flesch-Kincaid Grade Level should be between 5.5 and 6.5.
""",
        "High School": """
Write at a high school reading level (9th–12th grade).
- Use plain English but more detailed explanations are okay.
- You may include limited medical terms if explained.
- Use paragraphs or bullet points as needed.
- Flesch-Kincaid Grade Level should be between 9.0 and 12.0.
"""
    }.get(level, "")

    content_section = """
Write clear and easy-to-understand **{stage}** instructions for: **{procedure}**

Sections to include:
- What the procedure is
- Why it is needed
- Benefits
- Risks and complications
- Alternatives
- Recovery expectations
- Patient rights (e.g., asking questions or refusing)
""" if stage == "pre-op" else """
Write clear and easy-to-understand **{stage}** care instructions for: **{procedure}**

Sections to include:
- Wound care
- Pain management
- Activity restrictions
- Diet
- When to call the doctor
- Red flag symptoms
- Follow-up instructions
"""

    return f"""
You are a medical assistant creating {lang} instructions for a patient.

{instructions}

{content_section.format(stage=stage, procedure=procedure)}
""".strip()

# Back-translation
def backtranslate(text, source_lang):
    prompt = f"Translate the following {source_lang} medical instructions into English:\n\n{text}"
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Backtranslation error: {e}")
        return ""

# Readability scoring
def get_scores(text):
    try:
        return {
            "FKGL": textstat.flesch_kincaid_grade(text),
            "SMOG": textstat.smog_index(text),
            "Flesch-Ease": textstat.flesch_reading_ease(text)
        }
    except Exception as e:
        print(f"Scoring error: {e}")
        return {"FKGL": None, "SMOG": None, "Flesch-Ease": None}

# Run data collection
rows = []

for proc in procedures:
    for lang in languages:
        for level_desc in reading_levels:
            for stage in ["pre-op", "post-op"]:
                for rep in range(1, replicates + 1):
                    print(f"⏳ {proc} | {lang} | {level_desc} | {stage} | Replicate {rep}")
                    prompt = make_prompt(proc, lang, level_desc, stage)

                    try:
                        response = client.chat.completions.create(
                            model="gpt-4o",
                            messages=[{"role": "user", "content": prompt}]
                        )
                        full_text = response.choices[0].message.content.strip()
                    except Exception as e:
                        print(f"GPT error: {e}")
                        full_text = ""

                    if lang != "English":
                        translated_text = backtranslate(full_text, lang)
                        score_target = translated_text
                    else:
                        translated_text = ""
                        score_target = full_text

                    scores = get_scores(score_target)

                    rows.append({
                        "Procedure": proc,
                        "Language": lang,
                        "Reading Level": level_desc,
                        "Stage": stage,
                        "Replicate": rep,
                        "GPT Output": full_text,
                        "Back-Translated English": translated_text,
                        **scores
                    })

                    time.sleep(1)

# Save all outputs
df = pd.DataFrame(rows)
df.to_excel("Multilingual_PostOp_Instructions_Triplicate.xlsx", index=False)
print("✅ Triplicate run complete. Saved to 'Multilingual_PostOp_Instructions_Triplicate.xlsx'")