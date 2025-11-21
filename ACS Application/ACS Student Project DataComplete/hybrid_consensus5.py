import os
import time
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv

# 🔑 Load API key from environment variable
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable must be set")
client = OpenAI(api_key=api_key)

# === File Paths ===
input_path = "/Users/brendanfox/Desktop/Research/TraumaTriageLLM/CombinedData/final_trauma_prompt_script_input.xlsx"
output_path = "/Users/brendanfox/Desktop/Research/TraumaTriageLLM/CombinedData/hybrid_consensus_output5.xlsx"

# === Load Data ===
df = pd.read_excel(input_path)

# === Prompt A: Conservative (L2-biased) ===
def build_prompt_conservative(transcript):
    return [
        {
            "role": "system",
            "content": (
                "You are part of a **layered trauma triage system**. Your task is to take a conservative approach: only assign **Level 1 trauma activation** if the case clearly meets major criteria. This is Step 1 in a multi-prompt funnel.\n\n"
                "== DECISION RULE ==\n"
                "- If ANY Level 1 criteria are clearly met, return 1.\n"
                "- If not, default to Level 2 (return 2).\n\n"
                "== OUTPUT FORMAT ==\n"
                "Line 1: 1 or 2 only\n"
                "Line 2: L[1 or 2], [age] y/o, Vitals(BP, HR, RR), GCS: , MOI (), ETA:\n\n"
                "== STRATEGY ==\n"
                "- Do not guess. Only activate Level 1 if the criteria are explicit.\n"
                "- Be mindful of resource use — avoid unnecessary overtriage.\n"
                "- If the case is uncertain or ambiguous, default to Level 2.\n"
                "- Consider the patient as a whole: vitals, GCS, and MOI together.\n"
            )
        },
        {
            "role": "user",
            "content": f"""TRANSCRIPT:\n{transcript}\n\n== LEVEL 1 TRAUMA ACTIVATION CRITERIA ==\n\n1A. Respiratory compromise or urgent airway management\n1B. Intubation at the scene\n2A. Open skull fracture\n2B. ≥2 proximal long bone fractures\n2C. Unstable pelvic fracture\n3A. BP < 90 mmHg (age ≥10)\n3B. BP < 70 + 2×age (if <9 y/o)\n4A. GCS < 10\n4B. Intracranial hemorrhage + midline shift\n4C. Suspected spinal cord injury\n5A. GSW to head/neck/torso/limbs (proximal)\n5B. Penetrating injury w/ bleeding risk\n6A. Ongoing respiratory support\n6B. Requires blood products\n7A. Multisystem trauma\n8A. Physician discretion
"""
        }
    ]

# === Prompt B: Aggressive (L1-biased) ===
def build_prompt_aggressive(transcript):
    return [
        {
            "role": "system",
            "content": (
                "You are a pediatric trauma triage expert reviewing an EMS field report. Your goal is to **err on the side of patient safety**. If there is any plausible indication of high acuity, activate **Level 1**.\n\n"
                "== CLASSIFICATION ==\n"
                "1 = Level 1 Trauma Activation (high risk or concern)\n"
                "2 = Level 2 Trauma Activation (stable, low-risk)\n\n"
                "== WHEN TO RETURN LEVEL 1 ==\n"
                "- Any clear OR implied Level 1 criteria\n"
                "- Any suggestion of instability, e.g., altered mental status, airway compromise, abnormal vitals\n"
                "- High-risk MOI (ejection, rollover, fall >10ft, penetrating injury)\n"
                "- Combination of moderate factors: e.g., borderline vitals + MOI + unknown GCS\n"
                "- Vague concerning language (e.g., 'not responsive', 'pretty banged up', 'unconscious')\n\n"
                "== STRATEGY ==\n"
                "- DO NOT wait for exact matches; use clinical judgment.\n"
                "- Assume that undertriage can cause harm — if in doubt, lean toward Level 1.\n"
                "- Consider trauma burden (e.g., multiple injuries) even if no single criterion is met.\n\n"
                "== OUTPUT FORMAT ==\n"
                "Line 1: 1 or 2\n"
                "Line 2: L[1 or 2], [age] y/o, Vitals(BP, HR, RR), GCS: , MOI (), ETA:"
            )
        },
        {
            "role": "user",
            "content": f"TRANSCRIPT:\n{transcript}"
        }
    ]


# === Prompt C: ACS Enforcer ===
def build_prompt_tiebreaker(transcript):
    return [
        {
            "role": "system",
            "content": (
                "You are the final authority in a pediatric trauma triage system. Prior reviewers have disagreed.\n\n"
                "== TASK ==\n"
                "Make the final call: Level 1 or Level 2 trauma activation?\n\n"
                "== INSTRUCTIONS ==\n"
                "- If **any signs suggest instability**, **altered GCS**, **high-risk mechanism**, or **multiple injuries**, return 1.\n"
                "- If key info is **missing** (GCS, vitals) and the patient appears altered or there's concerning EMS tone, return 1.\n"
                "- If the transcript is sparse, vague, or ambiguous but there's any doubt of serious injury, return 1.\n"
                "- Only return 2 if **all information points to stability** with no high-risk concern.\n\n"
                "== OUTPUT FORMAT ==\n"
                "Line 1: 1 or 2\n"
                "Line 2: L[1 or 2], [age] y/o, Vitals (BP, HR, RR), GCS: __, MOI (summary), ETA: __"
            )
        },
        {
            "role": "user",
            "content": f"TRANSCRIPT:\n{transcript}"
        }
    ]
    
# === Inference Loop ===
for i, row in df.iterrows():
    if pd.notna(row.get("hybrid_level")):
        continue  # Skip already-processed rows

    transcript = row.get("whisper_transcript", "")
    if not isinstance(transcript, str) or not transcript.strip():
        continue  # Skip empty or invalid transcripts

    try:
        # === Prompt A: Conservative ===
        resp_a = client.chat.completions.create(
            model="gpt-4o",
            messages=build_prompt_conservative(transcript),
            temperature=0.1
        )
        out_a = resp_a.choices[0].message.content.strip().split("\n")
        level_a = out_a[0].strip()
        summary_a = " ".join(out_a[1:]).strip()

        # === Prompt B: Aggressive ===
        resp_b = client.chat.completions.create(
            model="gpt-4o",
            messages=build_prompt_aggressive(transcript),
            temperature=0.1
        )
        out_b = resp_b.choices[0].message.content.strip().split("\n")
        level_b = out_b[0].strip()
        summary_b = " ".join(out_b[1:]).strip()

        # === Hybrid Logic ===
        if level_a == "1" or level_b == "1":
            hybrid_level = "1"
            summary_c = ""  # No Prompt C used
            level_c = ""
        elif level_a == level_b:
            hybrid_level = level_a
            summary_c = ""
            level_c = ""
        else:
            # True disagreement not involving Level 1 → run Prompt C
            resp_c = client.chat.completions.create(
                model="gpt-4o",
                messages=build_prompt_tiebreaker(transcript),
                temperature=0.1
            )
            out_c = resp_c.choices[0].message.content.strip().split("\n")
            level_c = out_c[0].strip()
            summary_c = " ".join(out_c[1:]).strip()
            hybrid_level = level_c

        # === Store Results ===
        df.at[i, "gpt4o_level_conservative"] = level_a
        df.at[i, "gpt4o_page_conservative"] = summary_a
        df.at[i, "gpt4o_level_aggressive"] = level_b
        df.at[i, "gpt4o_page_aggressive"] = summary_b
        df.at[i, "hybrid_level"] = hybrid_level

        if summary_c:
            df.at[i, "gpt4o_level_tiebreaker"] = level_c
            df.at[i, "gpt4o_page_tiebreaker"] = summary_c

        print(f"[{i+1}/{len(df)}] ✅ Success — Hybrid: L{hybrid_level}")
        time.sleep(1.2)

    except Exception as e:
        print(f"[{i+1}/{len(df)}] ❌ ERROR: {str(e)}")
        continue
        
# === Save Results ===
df.to_excel(output_path, index=False)
print(f"\n✅ Done! Saved output to:\n{output_path}")