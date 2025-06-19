import json
import argparse
import re

PLACEHOLDER_PATTERNS = [
    re.compile(r"Icon\.png", re.IGNORECASE),
    re.compile(r"Page is currently undergoing realization", re.IGNORECASE),
    re.compile(r"Dear Guests", re.IGNORECASE),
]


def is_placeholder(text: str) -> bool:
    return any(p.search(text) for p in PLACEHOLDER_PATTERNS)


def main():
    parser = argparse.ArgumentParser(description="Clean Hokma corpus of placeholder outputs")
    parser.add_argument("--input", default="hokma_corpus_final.jsonl")
    parser.add_argument("--output", default="hokma_corpus_cleaned.jsonl")
    parser.add_argument("--removed", default="hokma_corpus_removed.jsonl")
    args = parser.parse_args()

    kept = []
    removed = []
    with open(args.input, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            obj = json.loads(line)
            out = obj.get("output", "")
            if is_placeholder(out):
                removed.append(obj)
            else:
                kept.append(obj)

    with open(args.output, "w", encoding="utf-8") as out_f:
        for obj in kept:
            json.dump(obj, out_f, ensure_ascii=False)
            out_f.write("\n")

    with open(args.removed, "w", encoding="utf-8") as rem_f:
        for obj in removed:
            json.dump(obj, rem_f, ensure_ascii=False)
            rem_f.write("\n")

    print(f"Removed {len(removed)} entries")
    print(f"Wrote {len(kept)} entries to {args.output}")


if __name__ == "__main__":
    main()
