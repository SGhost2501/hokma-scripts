import os
import glob
import json
import re
from datetime import datetime

IGNORE_PHRASES = [
    'episode', 'omitted', 'http', 'tvtropes'
]

THEME_MAP = {
    'lore': ("User asks about Abnormalities.", "Tell me about Abnormalities."),
    'management': ("User inquires about agent management.", "How should we handle our agents?"),
    'philosophy': ("User seeks philosophical insight.", "Share your wisdom."),
    'advice': ("User requests advice.", "Do you have any advice?"),
    'reflection': ("User asks Hokma to reflect.", "Share your thoughts."),
}


def clean_line(line: str) -> str | None:
    text = line.strip().replace('\t', ' ')
    if not text:
        return None
    lower = text.lower()
    if any(p in lower for p in IGNORE_PHRASES):
        return None
    # remove parentheticals
    text = re.sub(r"\([^)]*\)", "", text)
    text = re.sub(r"\[[^\]]*\]", "", text)
    # remove section headers or enumerations
    if re.match(r"^\d+[.:]?\s*$", text):
        return None
    if re.match(r"^[a-zA-Z ]+:$", text):
        return None
    if re.match(r"^\d+%", text):
        return None
    if re.match(r"^\d+", text) and ":" in text[:5]:
        return None
    if re.match(r"^\d+(\.\d+)?\s+", text):
        return None
    text = re.sub(r"^\d+\s*", "", text)
    if len(text.split()) < 3:
        return None
    if text.startswith(('-','*')):
        return None
    if 'damage' in lower or 'e.g.o' in lower or 'ego' in lower:
        return None
    if '<' in text or '>' in text:
        return None
    text = text.strip("\"'“”`., ")
    return text.strip()


def gather_from_abno(folder: str) -> list[tuple[str, str]]:
    lines = []
    for fname in glob.glob(os.path.join(folder, '*.txt')):
        with open(fname, encoding='utf-8') as f:
            for line in f:
                cleaned = clean_line(line)
                if cleaned:
                    lines.append((cleaned, fname))
    return lines


def gather_from_hokmaballs(pattern: str = 'hokmaballs*.txt') -> list[tuple[str, str]]:
    lines = []
    for fname in glob.glob(pattern):
        with open(fname, encoding='utf-8') as f:
            for line in f:
                if line.startswith('=') or 'input' in line.lower() or 'output' in line.lower():
                    continue
                cleaned = clean_line(line)
                if cleaned:
                    lines.append((cleaned, fname))
    return lines


def gather_from_json(path: str) -> list[tuple[str, str]]:
    lines = []
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    for entry in data:
        for key in ('inputs', 'outputs'):
            for line in entry.get(key, []):
                cleaned = clean_line(line)
                if cleaned:
                    lines.append((cleaned, path))
    return lines

def gather_pairs_from_json(path: str, created_at: str) -> list[dict]:
    pairs = []
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    for entry in data:
        for inp in entry.get('inputs', []):
            inp_clean = clean_line(inp)
            if not inp_clean:
                continue
            for out in entry.get('outputs', []):
                out_clean = clean_line(out)
                if not out_clean:
                    continue
                theme = classify_theme(out_clean)
                instruction, _ = THEME_MAP[theme]
                pairs.append({
                    'instruction': instruction,
                    'input': inp_clean,
                    'output': out_clean,
                    'theme': theme,
                    'reviewed': False,
                    'source_file': path,
                    'created_at': created_at
                })
    return pairs


def classify_theme(line: str) -> str:
    l = line.lower()
    if 'abnormal' in l:
        return 'lore'
    if 'agent' in l or 'employee' in l or 'manager' in l:
        return 'management'
    if any(w in l for w in ['truth', 'mind', 'soul', 'spirit', 'regret', 'wisdom']):
        return 'philosophy'
    if any(w in l for w in ['should', 'could', 'would', 'advice']):
        return 'advice'
    return 'reflection'


def build_entries(items: list[tuple[str, str]], created_at: str) -> list[dict]:
    entries = []
    for line, source in items:
        theme = classify_theme(line)
        instruction, prompt = THEME_MAP[theme]
        entries.append({
            'instruction': instruction,
            'input': prompt,
            'output': line,
            'theme': theme,
            'reviewed': False,
            'source_file': source,
            'created_at': created_at
        })
    return entries


def main():
    timestamp = datetime.utcnow().isoformat() + 'Z'
    lines = []
    lines.extend(gather_from_abno('abnormalities list'))
    lines.extend(gather_from_hokmaballs())
    lines.extend(gather_from_json('hokma_templates_cleaned.json'))
    # deduplicate text while keeping source; prefer first occurrence
    seen_text = {}
    for text, src in lines:
        if text not in seen_text:
            seen_text[text] = src
    unique = [(text, src) for text, src in seen_text.items()]

    entries = build_entries(unique, timestamp)
    # Add explicit prompt/response pairs from the cleaned templates
    entries.extend(gather_pairs_from_json('hokma_templates_cleaned.json', timestamp))
    dedup = []
    seen = set()
    for e in entries:
        key = (e['instruction'], e['input'], e['output'])
        if key in seen:
            continue
        seen.add(key)
        dedup.append(e)
    with open('hokma_corpus_final.jsonl', 'w', encoding='utf-8') as out:
        for e in dedup:
            json.dump(e, out, ensure_ascii=False)
            out.write('\n')
    print(f'Wrote {len(dedup)} entries to hokma_corpus_final.jsonl')
    for e in dedup[:10]:
        print(e)


if __name__ == '__main__':
    main()
