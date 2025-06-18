import json
import re

def clean_entry(entry):
    def is_valid(line):
        # Remove lines that are just code, section headers, brackets, or JSON keys
        return not (
            re.match(r'^\s*[\[\]\{\}]+\s*$', line) or
            re.match(r'^\s*("|“).*("|”|,)$', line) or
            re.match(r'^\s*("|“).*\s*:\s*("|”|,)?$', line) or
            'random' in line or
            'return f"' in line or
            'import ' in line or
            'GENERATOR LOGIC' in line or
            'advice_list' in line or
            'base =' in line or
            'else:' in line or
            'if name:' in line or
            line.strip() in ('', '],', '])')
        )
    def strip_junk(line):
        # Remove extra quotes and commas
        return line.strip().strip('",').strip('“”').strip()

    entry['inputs'] = [strip_junk(x) for x in entry['inputs'] if is_valid(x)]
    entry['outputs'] = [strip_junk(x) for x in entry['outputs'] if is_valid(x)]
    return entry

with open('hokma_templates_generated.json', encoding='utf-8') as f:
    data = json.load(f)

cleaned = [clean_entry(x) for x in data]

with open('hokma_templates_cleaned.json', 'w', encoding='utf-8') as f:
    json.dump(cleaned, f, ensure_ascii=False, indent=2)