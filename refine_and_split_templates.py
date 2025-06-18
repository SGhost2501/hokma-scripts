import json
import re

# Configuration
INPUT_FILE = "hokma_templates_cleaned.json"
OUTPUT_FILE = "hokma_templates_refined.json"
ADD_METADATA = True  # Set to False if you don't want metadata

def is_input_candidate(line):
    line = line.strip()
    return (line.endswith("?") or
            line.lower().startswith(("how", "why", "what", "can", "is", "do", "should", "who", "where", "when", "will")))

def is_output_candidate(line):
    # Anything that doesn't look like a user prompt is likely an output
    return not is_input_candidate(line)

def dedupe_keep_order(seq):
    seen = set()
    return [x for x in seq if not (x in seen or seen.add(x))]

def generate_blocks(theme, instruction, inputs, outputs, meta):
    # Create a block for each input with all relevant outputs
    blocks = []
    for inp in inputs:
        block = {
            "theme": theme,
            "instruction": instruction,
            "inputs": [inp],
            "outputs": outputs
        }
        if ADD_METADATA:
            block.update(meta)
        blocks.append(block)
    return blocks

def main():
    with open(INPUT_FILE, encoding="utf-8") as f:
        data = json.load(f)

    refined_blocks = []
    for entry in data:
        theme = entry.get("theme", "unknown")
        instruction = entry.get("instruction", "")
        src_weight = entry.get("weight", None)

        # Audit and move misplaced items
        raw_inputs = entry.get("inputs", [])
        raw_outputs = entry.get("outputs", [])

        # Move any misaligned items
        true_inputs = []
        true_outputs = list(raw_outputs)
        for i in raw_inputs:
            if is_input_candidate(i):
                true_inputs.append(i)
            else:
                true_outputs.append(i)
        # Also move any output that looks like an input
        cleaned_outputs = []
        for o in true_outputs:
            if is_input_candidate(o):
                true_inputs.append(o)
            else:
                cleaned_outputs.append(o)

        # Deduplicate
        true_inputs = dedupe_keep_order(true_inputs)
        cleaned_outputs = dedupe_keep_order(cleaned_outputs)

        # Optionally add metadata
        meta = {}
        if ADD_METADATA:
            meta = {
                "source_theme": theme,
                "notes": "",
                "reviewed": False
            }
            if src_weight is not None:
                meta["weight"] = src_weight

        # Split into mini-blocks (one input, all outputs)
        blocks = generate_blocks(theme, instruction, true_inputs, cleaned_outputs, meta)
        refined_blocks.extend(blocks)

    # Save
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(refined_blocks, f, indent=2, ensure_ascii=False)
    print(f"Refined templates written to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()