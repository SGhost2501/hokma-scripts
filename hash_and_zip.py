import argparse
import hashlib
import os
import zipfile
import json
from collections import Counter
from datetime import datetime


def summarize(path: str):
    with open(path, 'rb') as f:
        data = f.read()
    sha = hashlib.sha256(data).hexdigest()
    entries = []
    with open(path, encoding='utf-8') as f:
        for line in f:
            if line.strip():
                entries.append(json.loads(line))
    themes = Counter(e.get('theme', 'unknown') for e in entries)
    return sha, len(entries), themes


def write_readme(sha: str, total: int, themes: Counter, date: str):
    lines = ["# Hokma Cleaned Corpus", "", f"- Total entries: {total}", f"- Generated on: {date}", f"- SHA256: {sha}", "", "## Theme Counts"]
    for theme, count in themes.items():
        lines.append(f"- {theme}: {count}")
    with open('README_CLEANED.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


def main():
    parser = argparse.ArgumentParser(description='Hash and zip hokma corpus')
    parser.add_argument('--input', default='hokma_corpus_balanced.jsonl', help='File to zip')
    parser.add_argument('--cleaned', default='hokma_corpus_cleaned.jsonl', help='Cleaned dataset for README stats')
    args = parser.parse_args()

    with open(args.input, 'rb') as f:
        data = f.read()
    sha_input = hashlib.sha256(data).hexdigest()
    base = os.path.splitext(os.path.basename(args.input))[0]
    zip_name = f"{base}_{sha_input[:8]}.zip"

    with zipfile.ZipFile(zip_name, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr(os.path.basename(args.input), data)

    sha_clean, total, themes = summarize(args.cleaned)
    date = datetime.utcnow().isoformat() + 'Z'
    write_readme(sha_clean, total, themes, date)

    print(f"SHA256 (cleaned): {sha_clean}")
    print(f"Created {zip_name} and README_CLEANED.md")


if __name__ == '__main__':
    main()
