import argparse
import os
import subprocess


STEPS = [
    ("clean", "python clean_hokma_corpus.py"),
    ("diversify", "python diversify_inputs.py"),
    ("split", "python split_long_outputs.py"),
    ("balance", "python balance_hokma_corpus.py --input hokma_corpus_split.jsonl"),
    ("package", "python hash_and_zip.py --input hokma_corpus_balanced.jsonl --cleaned hokma_corpus_cleaned.jsonl"),
]


def run(cmd: str):
    print(f"\n==> {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def main():
    parser = argparse.ArgumentParser(description="Run Hokma dataset pipeline")
    parser.add_argument("--force", action="store_true", help="Force rerun even if outputs exist")
    parser.add_argument("--skip-clean", action="store_true")
    parser.add_argument("--skip-diversify", action="store_true")
    parser.add_argument("--skip-split", action="store_true")
    parser.add_argument("--skip-balance", action="store_true")
    parser.add_argument("--skip-package", action="store_true")
    args = parser.parse_args()

    outputs = {
        "clean": "hokma_corpus_cleaned.jsonl",
        "diversify": "hokma_corpus_diversified.jsonl",
        "split": "hokma_corpus_split.jsonl",
        "balance": "hokma_corpus_balanced.jsonl",
    }

    for name, cmd in STEPS:
        skip_flag = getattr(args, f"skip_{name}", False)
        if skip_flag:
            continue
        out_file = outputs.get(name)
        if not args.force and out_file and os.path.exists(out_file):
            print(f"Skipping {name}, {out_file} exists")
            continue
        run(cmd)


if __name__ == "__main__":
    main()
