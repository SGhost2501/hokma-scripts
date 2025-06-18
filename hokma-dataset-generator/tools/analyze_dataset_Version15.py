import sys, json
from collections import Counter

def analyze(path):
    with open(path, "r", encoding="utf-8") as f:
        data = [json.loads(line) for line in f]
    theme_counts = Counter(x.get("theme", "unknown") for x in data)
    print("Theme counts:", dict(theme_counts))
    lens = [len(x["output"].split()) for x in data]
    print("Avg output length:", sum(lens)/len(lens))
    print("Min/Max output length:", min(lens), max(lens))
    # Simple similarity check
    outs = [x["output"] for x in data]
    n_sim = sum(outs[i] == outs[j] for i in range(len(outs)) for j in range(i+1, len(outs)))
    print("Number of exact duplicate outputs:", n_sim)

if __name__ == "__main__":
    analyze(sys.argv[1])