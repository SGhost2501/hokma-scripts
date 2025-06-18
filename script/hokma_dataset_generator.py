#!/usr/bin/env python3
"""
Hokma Dataset Generator
-----------------------
Generate diverse, lore-faithful prompt/response pairs for Hokma-style LLM roleplay fine-tuning.

Features:
- Weighted template selection for realistic topic distribution
- Rich template support (multiple inputs/outputs, long/monologue responses)
- CLI with argparse: output file, entry count, random seed, shuffle, theme log, verbose, group by theme
- Optional progress bar (tqdm)
- Optional per-theme output files

Author: YourNameHere
License: MIT
"""

import json
import random
import argparse
from collections import Counter, defaultdict

try:
    from tqdm import tqdm
    USE_TQDM = True
except ImportError:
    USE_TQDM = False

# -------------------------- TEMPLATES EXAMPLE --------------------------
# Replace below with your full set for production use!
templates = [
    {
        "theme": "lore",
        "weight": 4,
        "instruction": "User asks about the Seed of Light.",
        "inputs": [
            "What is the Seed of Light?",
            "Can you explain the purpose of the Seed of Light?"
        ],
        "outputs": [
            "The Seed of Light is both beacon and burden. It embodies our desperate hope to redeem this City or reveal its inevitable decline."
        ]
    },
    {
        "theme": "suppression",
        "weight": 2,
        "instruction": "User seeks insight into suppression.",
        "inputs": [
            "Describe Malkuth’s suppression.",
            "What does suppression mean for the Sephirah?"
        ],
        "outputs": [
            "Suppression is both shield and prison, binding purpose and self. Each Sephirah faces their own undoing within its grasp."
        ]
    },
    {
        "theme": "meme",
        "weight": 1,
        "instruction": "User asks a frivolous question.",
        "inputs": [
            "Is water wet, Hokma?",
            "Can you dab?"
        ],
        "outputs": [
            "Such trivial matters bear no relevance in the face of entropy. Let us return to questions worthy of reflection."
        ]
    },
    {
        "theme": "philosophy",
        "weight": 2,
        "instruction": "User requests a deep reflection on memory.",
        "inputs": [
            "What is the nature of memory?"
        ],
        "outputs": [
            "Memory is the river upon which all souls drift. It shapes the land through which it flows, carving valleys of longing and mountains of regret. To remember is to carry both joy and sorrow—a burden that is also a blessing."
        ]
    }
]
# ----------------------------------------------------------------------

def weighted_template_choice(templates):
    weights = [tpl["weight"] for tpl in templates]
    return random.choices(templates, weights=weights, k=1)[0]

def generate_dataset(templates, num_entries=1000, seed=42, with_theme_log=False, verbose=False):
    random.seed(seed)
    dataset = []
    theme_counter = Counter()
    detailed_theme_counter = defaultdict(list) if with_theme_log else None
    progress = tqdm(range(num_entries), desc="Generating", unit="entry") if USE_TQDM and num_entries > 50 else range(num_entries)
    for _ in progress:
        tpl = weighted_template_choice(templates)
        chosen_input = random.choice(tpl["inputs"])
        chosen_output = random.choice(tpl["outputs"])
        entry = {
            "instruction": tpl["instruction"],
            "input": chosen_input,
            "output": chosen_output
        }
        dataset.append(entry)
        theme_counter[tpl["theme"]] += 1
        if with_theme_log:
            detailed_theme_counter[tpl["theme"]].append(entry)
        if verbose:
            print(json.dumps(entry, ensure_ascii=False, indent=2))
    return dataset, theme_counter, detailed_theme_counter

def save_jsonl(dataset, filename):
    with open(filename, "w", encoding="utf-8") as f:
        for item in dataset:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

def save_theme_log(theme_counter, detailed_theme_counter, filename):
    log_data = {
        "theme_counts": theme_counter,
        "detailed": detailed_theme_counter
    }
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)

def save_grouped_by_theme(dataset, out_prefix="hokma_theme_"):
    grouped = defaultdict(list)
    for entry in dataset:
        theme = entry.get("theme", None)
        if not theme:
            # Fallback: extract from instruction string (not perfect)
            theme = entry["instruction"].split()[2].lower()
        grouped[theme].append(entry)
    for theme, items in grouped.items():
        fname = f"{out_prefix}{theme}.jsonl"
        save_jsonl(items, fname)

def main():
    parser = argparse.ArgumentParser(description="Generate Hokma chatbot dataset.")
    parser.add_argument("--num-entries", "-n", type=int, default=1000, help="Number of entries to generate.")
    parser.add_argument("--output", "-o", type=str, default="hokma_dataset.jsonl", help="Output file name.")
    parser.add_argument("--seed", "-s", type=int, default=42, help="Random seed for reproducibility.")
    parser.add_argument("--shuffle", action="store_true", help="Shuffle dataset before saving.")
    parser.add_argument("--theme-log", type=str, default="", help="If given, save theme distribution log to this file.")
    parser.add_argument("--verbose", action="store_true", help="Print each generated entry to console.")
    parser.add_argument("--group-by-theme", action="store_true", help="Group output into separate files per theme (prefix hokma_theme_).")
    args = parser.parse_args()

    dataset, theme_counter, detailed_theme_counter = generate_dataset(
        templates,
        num_entries=args.num_entries,
        seed=args.seed,
        with_theme_log=bool(args.theme_log),
        verbose=args.verbose
    )

    if args.shuffle:
        random.shuffle(dataset)

    if args.group_by_theme:
        save_grouped_by_theme(dataset)
        print(f"Grouped files written by theme with prefix hokma_theme_*.jsonl")
    else:
        save_jsonl(dataset, args.output)
        print(f"Generated {args.num_entries} entries and saved to {args.output}")

    print("\nTheme distribution summary:")
    for theme, count in theme_counter.items():
        print(f"  {theme:12}: {count}")

    if args.theme_log:
        save_theme_log(dict(theme_counter), detailed_theme_counter, args.theme_log)
        print(f"\nTheme distribution log saved to {args.theme_log}")

if __name__ == "__main__":
    main()