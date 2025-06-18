import json

# File paths
INPUT_PATH = "hokma_templates_final_1to1.json"
FILLED_OUTPUTS_PATH = "filled_outputs_hokma_advice_2025.json"
OUTPUT_PATH = "hokma_templates_final_1to1_filled.json"

# Load ChatGPT-filled outputs
with open(FILLED_OUTPUTS_PATH, "r", encoding="utf-8") as f:
    filled_outputs = json.load(f)

# Build a lookup from input to outputs
filled_outputs_map = {item["input"]: item["outputs"] for item in filled_outputs}

# Load the main dataset
with open(INPUT_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

updated = 0
for entry in data:
    input_text = entry.get("inputs", [""])[0]
    if input_text in filled_outputs_map:
        entry["outputs"] = filled_outputs_map[input_text]
        entry["auto_generated"] = True
        entry.pop("needs_review", None)
        updated += 1

# Save the updated dataset
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Inserted outputs for {updated} entries from {FILLED_OUTPUTS_PATH}. Saved as {OUTPUT_PATH}")