# file: extract_flagged_entries.py

import json

INPUT_PATH = "hokma_templates_final_1to1.json"
OUTPUT_PATH = "flagged_entries_for_chatgpt.txt"

def load_dataset(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_flagged_entries(data):
    lines = []
    for entry in data:
        if entry.get("needs_review") and (not entry.get("outputs")):
            input_text = " ".join(entry.get("inputs", []))
            theme = entry.get("theme", "unknown")
            lines.append(f"Input: \"{input_text}\"\nTheme: \"{theme}\"\n---")
    return lines

def save_lines(lines, path):
    with open(path, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
    print(f"✅ Flagged entries saved to {path}")

def main():
    data = load_dataset(INPUT_PATH)
    lines = extract_flagged_entries(data)
    save_lines(lines, OUTPUT_PATH)

if __name__ == "__main__":
    main()
