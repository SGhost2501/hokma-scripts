import json
import os

INPUT_FILE = "hokma_templates_refined.json"
OUTPUT_DIR = "."
PER_THEME = True  # Output per-theme files

def generate_llm_output(prompt):
    # Placeholder: call your favorite LLM API here!
    # For now, just return None so it gets flagged for manual review.
    return None

def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    theme_buckets = {}

    for entry in data:
        input_text = entry.get("inputs", [""])[0].strip()
        outputs = entry.get("outputs", [])
        theme = entry.get("theme", "unknown").strip().lower()

        # Clean up input and outputs
        outputs = [o.strip() for o in outputs if o.strip()]

        if not outputs or any(o.lower().strip() in ["# example usages", ""] for o in outputs):
            # Try to auto-generate output with an LLM (optional)
            # new_output = generate_llm_output(input_text)
            new_output = None
            if new_output:
                outputs = [new_output]
                entry["auto_generated"] = True
                entry["needs_review"] = False
            else:
                entry["needs_review"] = True
                outputs = []
        
        if not outputs:
            entry["outputs"] = []
        else:
            entry["outputs"] = outputs

        if PER_THEME:
            theme_buckets.setdefault(theme, []).append(entry)
    
    # Write per-theme files
    if PER_THEME:
        for theme, blocks in theme_buckets.items():
            path = os.path.join(OUTPUT_DIR, f"hokma_{theme}_templates_1to1.json")
            with open(path, "w", encoding="utf-8") as f:
                json.dump(blocks, f, indent=2, ensure_ascii=False)
            print(f"Wrote {len(blocks)} entries to {path}")

    # Write a full file too
    all_blocks = [e for blocks in theme_buckets.values() for e in blocks]
    with open(os.path.join(OUTPUT_DIR, "hokma_templates_final_1to1.json"), "w", encoding="utf-8") as f:
        json.dump(all_blocks, f, indent=2, ensure_ascii=False)
    print(f"Wrote {len(all_blocks)} entries to hokma_templates_final_1to1.json")

if __name__ == "__main__":
    main()