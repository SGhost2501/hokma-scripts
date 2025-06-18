import json

with open("hokma_templates_cleaned.json", encoding="utf-8") as f:
    data = json.load(f)

for entry in data:
    print(f"\nTheme: {entry['theme']}")
    print("  Suspect Inputs (may be outputs):")
    for i in entry['inputs']:
        if not i.strip().endswith("?") and not i.lower().startswith(
            ("how", "why", "what", "can", "is", "do", "should", "who", "where", "when", "will")
        ):
            print("   >", i)
    print("  Suspect Outputs (may be inputs):")
    for o in entry['outputs']:
        if o.strip().endswith("?"):
            print("   >", o)