import os
import glob
import re
from collections import defaultdict

# Directory containing source text files
SOURCE_DIR = 'abnormalities list'

# Files that contain meta instructions rather than in-universe text
IGNORE_FILES = {
    'Hokma_LLM_Master_Summary.txt',
}

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

# Skip lines containing these phrases or symbols
IGNORE_PHRASES = [
    'training data progress',
    'next steps',
    'created by chatgpt',
    'model:',
    'jsonl',
    'target:',
    'goal:',
    'master summary',
    'project',
    'mistral-7b',
    '🔄',
    '✅',
    '🛠',
]

def categorize(text: str) -> str:
    l = text.lower()
    for theme, words in KEYWORDS.items():
        if any(w in l for w in words):
            return theme
    return 'advice'

# Collect as many unique lines as available
MAX_OUTPUTS = None
MAX_INPUTS = None

# Maximum length of a single sentence to keep
MAX_LEN = 300

def clean_line(text: str) -> str:
    text = re.sub(r"\s+", " ", text.strip())
    return text

def split_sentences(text: str):
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [p.strip() for p in parts if p.strip()]

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
        fname = os.path.basename(path)
        if fname in IGNORE_FILES:
            continue
        with open(path, encoding='utf-8', errors='ignore') as f:
            for raw in f:
                line = clean_line(raw)
                if not line or line.startswith('>'):
                    continue
                lowered = line.lower()
                if any(p in lowered for p in IGNORE_PHRASES):
                    continue
                for sentence in split_sentences(line):
                    if len(sentence) < 3 or len(sentence) > MAX_LEN:
                        continue
                    theme = categorize(sentence)
                    if is_question(sentence):
                        if (
                            (MAX_INPUTS is None or len(data[theme]['inputs']) < MAX_INPUTS)
                            and sentence not in data[theme]['i_set']
                        ):
                            data[theme]['inputs'].append(sentence)
                            data[theme]['i_set'].add(sentence)
                    else:
                        if (
                            (MAX_OUTPUTS is None or len(data[theme]['outputs']) < MAX_OUTPUTS)
                            and sentence not in data[theme]['o_set']
                        ):
                            data[theme]['outputs'].append(sentence)
                            data[theme]['o_set'].add(sentence)
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
            if inputs:
                out.write('\n========================\n')
                out.write(f'{theme.upper()} – AUTO (inputs)\n')
                out.write('========================\n')
                for line in inputs:
                    out.write(line + '\n')
        print(f"{theme}: {len(outputs)} outputs, {len(inputs)} inputs")

def main():
    data = gather_lines()
    write_files(data)

if __name__ == '__main__':
    main()

