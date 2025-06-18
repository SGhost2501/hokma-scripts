import glob
import json
import re

# Map each file index to its theme
THEME_MAP = {
    1: "advice",
    2: "edge",
    3: "meme",
    4: "refusal",
    5: "philosophy"
}

def extract_blocks(lines):
    """Extracts inputs and outputs between delimiters or headings."""
    blocks = {'inputs': [], 'outputs': []}
    mode = None
    for line in lines:
        line = line.strip()
        if not line or line.startswith('='):
            continue
        if 'input' in line.lower():
            mode = 'inputs'
        elif 'output' in line.lower():
            mode = 'outputs'
        elif mode and not line.startswith('===='):
            if line and not line.startswith('['):
                blocks[mode].append(line)
    return blocks

def process_file(fname):
    idx = int(re.search(r'hokmaballs(\d+)\.txt', fname).group(1))
    theme = THEME_MAP.get(idx, "unknown")
    with open(fname, encoding='utf-8') as f:
        lines = f.readlines()
    blocks = extract_blocks(lines)
    return {
        "theme": theme,
        "weight": 2,
        "instruction": f"User asks about {theme}.",
        "inputs": list(set(blocks['inputs'])),
        "outputs": list(set(blocks['outputs']))
    }

def main():
    all_templates = []
    for fname in sorted(glob.glob('hokmaballs*.txt')):
        template = process_file(fname)
        all_templates.append(template)
    # Optionally: append to your pool or theme log
    with open('hokma_templates_generated.json', 'w', encoding='utf-8') as out:
        json.dump(all_templates, out, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()