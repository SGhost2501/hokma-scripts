import json

def is_question(text):
    text = text.strip()
    return text.endswith("?") or text.lower().startswith((
        "how", "why", "what", "can", "is", "do", "should", "who", "where", "when", "will"
    ))

with open("hokma_templates_refined.json", encoding="utf-8") as f:
    data = json.load(f)

new_blocks = []
for block in data:
    theme = block.get("theme", "")
    instruction = block.get("instruction", "")
    inputs = block.get("inputs", [])
    outputs = block.get("outputs", [])
    # Realign statement-like inputs
    real_inputs = []
    real_outputs = list(outputs)
    for i in inputs:
        if is_question(i):
            real_inputs.append(i)
        else:
            real_outputs.append(i)
    # Deduplicate outputs
    real_outputs = list(dict.fromkeys(real_outputs))
    # Split into one input per block for better relevance
    for inp in real_inputs:
        new_blocks.append({
            "theme": theme,
            "instruction": instruction,
            "inputs": [inp],
            "outputs": real_outputs
        })

with open("hokma_templates_realigned.json", "w", encoding="utf-8") as f:
    json.dump(new_blocks, f, indent=2, ensure_ascii=False)
print("Wrote realigned blocks to hokma_templates_realigned.json")