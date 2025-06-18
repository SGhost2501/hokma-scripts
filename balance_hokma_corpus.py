import json
import random
import argparse
from collections import defaultdict


def main():
    parser = argparse.ArgumentParser(description="Balance hokma dataset by theme")
    parser.add_argument('--input', default='hokma_corpus_final.jsonl')
    parser.add_argument('--output', default='hokma_corpus_balanced.jsonl')
    parser.add_argument('--max_per_theme', type=int, default=None,
                        help='Maximum examples per theme. Defaults to min theme count')
    args = parser.parse_args()

    buckets = defaultdict(list)
    with open(args.input, encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            obj = json.loads(line)
            theme = obj.get('theme', 'unknown')
            buckets[theme].append(obj)

    if args.max_per_theme is None:
        args.max_per_theme = min(len(v) for v in buckets.values())

    balanced = []
    for theme, items in buckets.items():
        random.shuffle(items)
        balanced.extend(items[:args.max_per_theme])

    random.shuffle(balanced)
    with open(args.output, 'w', encoding='utf-8') as out:
        for obj in balanced:
            json.dump(obj, out, ensure_ascii=False)
            out.write('\n')
    print(f"Wrote {len(balanced)} entries to {args.output}")


if __name__ == '__main__':
    main()
