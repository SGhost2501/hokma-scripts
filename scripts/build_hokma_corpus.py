import os
import glob
import json
import re

IGNORE_PHRASES = [
    'episode', 'omitted', 'http', 'tvtropes'
]


def clean_line(line: str) -> str | None:
    text = line.strip()
    if not text:
        return None
    lower = text.lower()
    if any(p in lower for p in IGNORE_PHRASES):
        return None
    if text.count('"') % 2 == 1 or text.count("'") % 2 == 1:
        return None
    if text.count('“') != text.count('”'):
        return None
    if re.search(r'(\.\.\.|…)$', text) or text.endswith('-') or text.endswith('—'):
        return None
    if re.match(r'^[(*]|^[\-*•]', text):
        return None
    if text.startswith('`'):
        return None
    # Strip surrounding quotes and trailing commas
    text = text.strip('"').strip("'").rstrip(',').strip('“”')
    return text.strip()


def gather_from_json(path: str) -> list[str]:
    lines = []
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    for entry in data:
        for key in ('inputs', 'outputs'):
            for line in entry.get(key, []):
                cleaned = clean_line(line)
                if cleaned:
                    lines.append(cleaned)
    return lines


def gather_from_abno_folder(folder: str) -> list[str]:
    lines = []
    for fname in glob.glob(os.path.join(folder, '*.txt')):
        with open(fname, encoding='utf-8') as f:
            for line in f:
                cleaned = clean_line(line)
                if cleaned:
                    lines.append(cleaned)
    return lines


def gather_from_hokmaballs(pattern: str = 'hokmaballs*.txt') -> list[str]:
    lines = []
    for fname in glob.glob(pattern):
        with open(fname, encoding='utf-8') as f:
            for line in f:
                if line.startswith('=') or 'input' in line.lower() or 'output' in line.lower():
                    continue
                cleaned = clean_line(line)
                if cleaned:
                    lines.append(cleaned)
    return lines


def main():
    lines = []
    lines.extend(gather_from_json('hokma_templates_final_1to1_filled.json'))
    lines.extend(gather_from_abno_folder('abnormalities list'))
    lines.extend(gather_from_hokmaballs())
    unique = sorted(set(lines))
    with open('hokma_corpus.txt', 'w', encoding='utf-8') as out:
        out.write('\n'.join(unique))
    print(f'Wrote {len(unique)} unique lines to hokma_corpus.txt')


if __name__ == '__main__':
    main()
