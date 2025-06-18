import sys, json
from collections import Counter

def load_templates(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    templates = load_templates(sys.argv[1])
    errors = []
    all_inputs = []
    for i, tpl in enumerate(templates):
        if not tpl.get("inputs") or not tpl.get("outputs"):
            errors.append(f"Template {i} missing input or output.")
        for field in ["inputs", "outputs"]:
            if any(not x.strip() for x in tpl[field]):
                errors.append(f"Template {i} has empty {field}.")
        all_inputs += tpl["inputs"]
    ctr = Counter(all_inputs)
    dups = [k for k, v in ctr.items() if v > 1]
    if dups:
        errors.append(f"Duplicate inputs found: {dups}")
    if errors:
        print("[ERROR]")
        for e in errors: print(e)
        sys.exit(1)
    print("Validation passed.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_templates.py templates.json")
        sys.exit(1)
    main()