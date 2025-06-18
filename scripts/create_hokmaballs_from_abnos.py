import os
import re

INPUT_FILE = os.path.join('abnormalities list', 'hokma balls.txt')
OUTPUT_TEMPLATE = 'hokmaballs{}.txt'

# Base ignore phrases
IGNORE_PHRASES = [
    'episode', 'omitted', 'http', 'tvtropes'
]


def clean_line(line: str) -> str | None:
    """Return cleaned line or None if it should be skipped."""
    text = line.strip()
    if not text:
        return None
    lower = text.lower()
    if any(p in lower for p in IGNORE_PHRASES):
        return None
    # Skip lines with unmatched quotes
    if text.count('"') % 2 == 1 or text.count("'") % 2 == 1:
        return None
    if text.count('“') != text.count('”'):
        return None
    # Skip obvious truncations (ellipses or trailing dashes)
    if re.search(r'(\.\.\.|…)$', text) or text.endswith('-') or text.endswith('—'):
        return None
    return text


def main():
    with open(INPUT_FILE, encoding='utf-8') as f:
        lines = [clean_line(l) for l in f]
    lines = [l for l in lines if l]
    chunk_size = (len(lines) + 4) // 5  # split into 5 nearly equal files
    for i in range(5):
        chunk = lines[i*chunk_size:(i+1)*chunk_size]
        with open(OUTPUT_TEMPLATE.format(i+1), 'w', encoding='utf-8') as out:
            out.write('\n'.join(chunk))


if __name__ == '__main__':
    main()
