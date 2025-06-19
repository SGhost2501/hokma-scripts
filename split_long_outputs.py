import json
import argparse
import re

SENT_RE = re.compile(r"(?<=[.!?])\s+")


def split_output(text: str, max_words: int) -> list[str]:
    sentences = [s.strip() for s in SENT_RE.split(text.strip()) if s.strip()]
    chunks = []
    current = ""
    for sent in sentences:
        if not current:
            current = sent
        elif len((current + " " + sent).split()) <= max_words:
            current += " " + sent
        else:
            chunks.append(current)
            current = sent
    if current:
        chunks.append(current)
    return chunks


def main():
    parser = argparse.ArgumentParser(description="Split long outputs into chunks")
    parser.add_argument("--input", default="hokma_corpus_diversified.jsonl")
    parser.add_argument("--output", default="hokma_corpus_split.jsonl")
    parser.add_argument("--max_words", type=int, default=100)
    args = parser.parse_args()

    new_entries = []
    with open(args.input, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            entry = json.loads(line)
            out_text = entry.get("output", "")
            if len(out_text.split()) <= args.max_words:
                new_entries.append(entry)
                continue
            parts = split_output(out_text, args.max_words)
            for part in parts:
                e = entry.copy()
                e["output"] = part
                new_entries.append(e)

    with open(args.output, "w", encoding="utf-8") as out:
        for e in new_entries:
            json.dump(e, out, ensure_ascii=False)
            out.write("\n")
    print(f"Wrote {len(new_entries)} entries to {args.output}")


if __name__ == "__main__":
    main()
