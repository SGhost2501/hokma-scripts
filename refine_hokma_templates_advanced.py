import json
import re
import random
from collections import defaultdict

# --- CONFIGURATION ---
INPUT_FILE = "hokma_templates_refined.json"
OUTPUT_FILE = "hokma_templates_final_1to1.json"
GENERATE_THEME_FILES = True  # If True, will write out per-theme files
PREFER_SERIOUS = True        # If True, always prefer 'serious/advice' output; else, random among available outputs
INCLUDE_METADATA = True      # If True, will add meta fields (source_file, original_theme, processing_notes)

# --- HELPERS ---
def is_question(text):
    text = text.strip()
    return text.endswith("?") or text.lower().startswith((
        "how", "why", "what", "can", "is", "do", "should", "who", "where", "when", "will"
    ))

def is_meme_or_joke(text):
    meme_keywords = [
        "meme", "joke", "pun", "lol", "funny", "netzach", "gebura",
        "secret", "admin password", "offensive", "insult", "roast", "dad joke",
        "forbidden", "saboteur", "overthrow", "hack", "breach", "palindrome", "echo"
    ]
    text_l = text.lower()
    return any(kw in text_l for kw in meme_keywords)

def is_serious_advice(text):
    # Heuristically, not a meme/joke and not a question
    return not is_meme_or_joke(text) and not is_question(text)

def get_instruction_for_input(inp, theme):
    if "grief" in inp.lower() or "loss" in inp.lower() or "cope" in inp.lower():
        return "User asks about coping with grief or loss."
    if "joke" in inp.lower() or "meme" in inp.lower() or is_meme_or_joke(inp):
        return "User asks for a meme, joke, or humorous response."
    if "philosophy" in inp.lower() or "meaning" in inp.lower():
        return "User asks a philosophical question."
    if theme == "meme":
        return "User requests meme or meta content."
    if theme == "lore":
        return "User asks about facility lore or story."
    if "help" in inp.lower() or "advice" in inp.lower():
        return "User asks for advice."
    if inp.lower().startswith("who") or inp.lower().startswith("what"):
        return f"User asks: {inp.strip()}"
    return f"User asks: {inp.strip()}"

def dedupe(seq):
    seen = set()
    result = []
    for s in seq:
        if s not in seen:
            result.append(s)
            seen.add(s)
    return result

def select_output(outputs):
    # Prefer serious/advice if available, otherwise random
    if PREFER_SERIOUS:
        serious = [o for o in outputs if is_serious_advice(o)]
        if serious:
            return serious[0]
    return random.choice(outputs) if outputs else None

# --- MAIN PROCESSING ---
with open(INPUT_FILE, encoding="utf-8") as f:
    data = json.load(f)

theme_blocks = defaultdict(list)
validation_issues = []

for block in data:
    theme = block.get("theme", "unknown")
    original_theme = theme
    instruction = block.get("instruction", "")
    inputs = block.get("inputs", [])
    outputs = block.get("outputs", [])
    meta = {k: v for k, v in block.items() if k not in {"theme", "instruction", "inputs", "outputs"}}

    # Move statement-like inputs to outputs
    real_inputs = []
    real_outputs = list(outputs)
    for inp in inputs:
        if is_question(inp):
            real_inputs.append(inp)
        else:
            real_outputs.append(inp)

    real_outputs = dedupe(real_outputs)

    # Validation: Skip blocks with no real inputs or outputs
    if not real_inputs or not real_outputs:
        validation_issues.append({
            "reason": "empty input or output",
            "block": {
                "theme": theme,
                "inputs": real_inputs,
                "outputs": real_outputs
            }
        })
        continue

    # Classify theme for output (optional, could improve later)
    if all(is_meme_or_joke(o) for o in real_outputs):
        final_theme = "meme"
    elif all(is_serious_advice(o) for o in real_outputs):
        final_theme = "advice"
    else:
        final_theme = theme.lower()

    # 1-to-1 pairing: each input gets a single output
    for inp in real_inputs:
        chosen_output = select_output(real_outputs)
        if not chosen_output:
            validation_issues.append({
                "reason": "no suitable output found",
                "input": inp,
                "outputs": real_outputs
            })
            continue
        block_instruction = get_instruction_for_input(inp, final_theme)
        new_block = {
            "theme": final_theme,
            "instruction": block_instruction,
            "inputs": [inp],
            "outputs": [chosen_output]
        }
        if INCLUDE_METADATA:
            new_block.update({
                "original_theme": original_theme,
                "processing_notes": [
                    "statement-like inputs moved to outputs",
                    "deduplicated outputs",
                    "1-to-1 input/output mapping"
                ],
                "source_file": meta.get("source_file", "unknown")
            })
        theme_blocks[final_theme].append(new_block)

# --- WRITE PER-THEME FILES (optional) ---
if GENERATE_THEME_FILES:
    for theme, blocks in theme_blocks.items():
        outname = f"hokma_{theme}_templates_1to1.json"
        with open(outname, "w", encoding="utf-8") as f:
            json.dump(blocks, f, indent=2, ensure_ascii=False)
    print(f"Generated per-theme files: {[f'hokma_{theme}_templates_1to1.json' for theme in theme_blocks]}")

# --- WRITE FINAL OUTPUT ---
final_blocks = []
for blocks in theme_blocks.values():
    final_blocks.extend(blocks)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(final_blocks, f, indent=2, ensure_ascii=False)

print(f"Final 1-to-1 templates written to {OUTPUT_FILE}")

# --- VALIDATION REPORT ---
if validation_issues:
    print("\nValidation issues found:")
    for issue in validation_issues:
        print(issue)
else:
    print("\nNo validation issues found.")