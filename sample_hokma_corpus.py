import json
import random
import argparse


def main():
    parser = argparse.ArgumentParser(description='Sample entries from hokma corpus')
    parser.add_argument('--input', default='hokma_corpus_final.jsonl')
    parser.add_argument('--output', default='hokma_corpus_sample.jsonl')
    parser.add_argument('--count', type=int, default=100)
    args = parser.parse_args()

    with open(args.input, encoding='utf-8') as f:
        entries = [json.loads(line) for line in f if line.strip()]

    sample = random.sample(entries, min(args.count, len(entries)))

    with open(args.output, 'w', encoding='utf-8') as out:
        for e in sample:
            json.dump(e, out, ensure_ascii=False)
            out.write('\n')
    print(f'Wrote {len(sample)} entries to {args.output}')


if __name__ == '__main__':
    main()
