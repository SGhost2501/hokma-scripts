import os
import glob
import re
from collections import defaultdict

# Directory containing source text files
SOURCE_DIR = 'abnormalities list'

# Themes and simple keywords for rough categorization
THEMES = ['advice', 'edge', 'meme', 'refusal', 'philosophy']
KEYWORDS = {
    'edge': [
        'kill', 'death', 'blood', 'murder', 'die', 'violence',
        'destroy', 'slaughter', 'dead'
    ],
    'meme': [
        'joke', 'meme', 'lol', 'haha', 'funny', 'lmao',
        'sarcasm', 'meme'
    ],
    'refusal': [
        'cannot', "can't", 'won\'t', 'refuse', 'denied', 'refused',
        'reject', 'decline', 'no way'
    ],
    'philosophy': [
        'meaning', 'purpose', 'exist', 'truth', 'life', 'destiny',
        'free will', 'why', 'reason'
    ],
    # advice is default
}

def categorize(text: str) -> str:
    l = text.lower()
    for theme, words in KEYWORDS.items():
        if any(w in l for w in words):
            return theme
    return 'advice'

MAX_OUTPUTS = 100
MAX_INPUTS = 50

def clean_line(text: str) -> str:
    text = re.sub(r"\s+", " ", text.strip())
    return text

def is_question(text: str) -> bool:
    if text.endswith("?"):
        return True
    return bool(re.match(r"(?i)^(who|what|when|where|why|how)\b", text))

def gather_lines():
    data = {
        theme: {
            'inputs': [],
            'outputs': [],
            'i_set': set(),
            'o_set': set(),
        }
        for theme in THEMES
    }
    for path in sorted(glob.glob(os.path.join(SOURCE_DIR, '*.txt'))):
        with open(path, encoding='utf-8', errors='ignore') as f:
            for raw in f:
                line = clean_line(raw)
                if not line or line.startswith('>'):
                    continue
                if len(line) < 3 or len(line) > 200:
                    continue
                theme = categorize(line)
                if is_question(line):
                    if (
                        len(data[theme]['inputs']) < MAX_INPUTS
                        and line not in data[theme]['i_set']
                    ):
                        data[theme]['inputs'].append(line)
                        data[theme]['i_set'].add(line)
                else:
                    if (
                        len(data[theme]['outputs']) < MAX_OUTPUTS
                        and line not in data[theme]['o_set']
                    ):
                        data[theme]['outputs'].append(line)
                        data[theme]['o_set'].add(line)
    # Remove helper sets
    for theme in THEMES:
        data[theme].pop('i_set')
        data[theme].pop('o_set')
    return data

def write_files(data):
    os.makedirs('.', exist_ok=True)
    for idx, theme in enumerate(THEMES, 1):
        outputs = sorted(data[theme]['outputs'])
        inputs = sorted(data[theme]['inputs'])
        with open(f'hokmaballs{idx}.txt', 'w', encoding='utf-8') as out:
            out.write('========================\n')
            out.write(f'{theme.upper()} – AUTO (outputs)\n')
            out.write('========================\n')
            for line in outputs:
                out.write(line + '\n')
            out.write('\n========================\n')
            out.write(f'{theme.upper()} – AUTO (inputs)\n')
            out.write('========================\n')
            for line in inputs:
                out.write(line + '\n')

def main():
    data = gather_lines()
    write_files(data)

if __name__ == '__main__':
    main()
