import json
import argparse


def convert_entry(entry, platform):
    if platform == 'openai':
        prompt = f"{entry['instruction']}\n{entry['input']}"
        completion = ' ' + entry['output']
        return {'prompt': prompt, 'completion': completion}
    elif platform == 'huggingface':
        text = f"Instruction: {entry['instruction']}\nInput: {entry['input']}\nOutput: {entry['output']}"
        return {'text': text}
    elif platform == 'replicate':
        return {'prompt': f"{entry['instruction']} {entry['input']}", 'response': entry['output']}
    else:
        raise ValueError('Unknown platform')


def main():
    parser = argparse.ArgumentParser(description='Convert hokma corpus to other formats')
    parser.add_argument('platform', choices=['openai', 'huggingface', 'replicate'])
    parser.add_argument('--input', default='hokma_corpus_final.jsonl')
    parser.add_argument('--output', default=None)
    args = parser.parse_args()

    out_path = args.output or f'hokma_corpus_{args.platform}.jsonl'
    with open(args.input, encoding='utf-8') as f:
        entries = [json.loads(line) for line in f if line.strip()]

    with open(out_path, 'w', encoding='utf-8') as out:
        for e in entries:
            conv = convert_entry(e, args.platform)
            json.dump(conv, out, ensure_ascii=False)
            out.write('\n')

    print(f'Wrote {len(entries)} entries to {out_path}')


if __name__ == '__main__':
    main()
