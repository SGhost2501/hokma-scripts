import json
import random
import argparse

ALTERNATIVES = [
    "What is your perspective on this?",
    "Reflect on this for me.",
    "What do you see in this?",
    "Provide your insight.",
    "How would you interpret this?",
]


def main():
    parser = argparse.ArgumentParser(description="Diversify repeated input prompts")
    parser.add_argument("--input", default="hokma_corpus_cleaned.jsonl")
    parser.add_argument("--output", default="hokma_corpus_diversified.jsonl")
    args = parser.parse_args()

    with open(args.input, encoding="utf-8") as f:
        entries = [json.loads(line) for line in f if line.strip()]

    replaced = 0
    for entry in entries:
        if entry.get("input") == "Share your thoughts.":
            entry["input"] = random.choice(ALTERNATIVES)
            replaced += 1

    with open(args.output, "w", encoding="utf-8") as out:
        for e in entries:
            json.dump(e, out, ensure_ascii=False)
            out.write("\n")

    print(f"Replaced {replaced} inputs. Wrote {len(entries)} entries to {args.output}")


if __name__ == "__main__":
    main()
