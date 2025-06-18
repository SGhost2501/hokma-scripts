import json
import re
from collections import Counter

FILE_PATH = 'hokma_corpus_final.jsonl'

PLACEHOLDER_RE = re.compile(r'^(?:[A-Z][a-z]*\s)?(?:Page|Entry)\s*\d+$')


def main():
    short_entries = []
    placeholder_outputs = []
    missing_fields = []
    inputs = []

    with open(FILE_PATH, encoding='utf-8') as f:
        for lineno, line in enumerate(f, 1):
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as e:
                print(f'Line {lineno}: invalid JSON - {e}')
                continue

            instruction = obj.get('instruction')
            inp = obj.get('input')
            out = obj.get('output')
            theme = obj.get('theme')

            if not all([instruction, inp, out, theme]):
                missing_fields.append(lineno)

            if inp:
                inputs.append(inp)
                if len(inp.split()) < 5:
                    short_entries.append((lineno, 'input', inp))

            if out:
                if len(out.split()) < 5:
                    short_entries.append((lineno, 'output', out))
                if PLACEHOLDER_RE.fullmatch(out.strip()):
                    placeholder_outputs.append((lineno, out))

    dup_inputs = [(text, count) for text, count in Counter(inputs).items() if count > 1]

    print('=== Audit Summary ===')
    print(f'Total entries: {len(inputs)}')
    print(f'Short inputs/outputs (<5 words): {len(short_entries)}')
    for entry in short_entries[:10]:
        ln, kind, text = entry
        print(f'  Line {ln} short {kind}: {text}')

    print(f'Placeholder-like outputs: {len(placeholder_outputs)}')
    for ln, text in placeholder_outputs[:10]:
        print(f'  Line {ln}: {text}')

    print(f'Entries missing fields: {len(missing_fields)}')
    if missing_fields:
        print('  Lines:', missing_fields[:10])

    print(f'Duplicate inputs: {len(dup_inputs)}')
    for text, count in dup_inputs[:10]:
        print(f'  {repr(text)} appears {count} times')


if __name__ == '__main__':
    main()
