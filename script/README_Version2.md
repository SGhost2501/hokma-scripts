# Hokma Dataset Generator

Generate large, diverse, and lore-faithful prompt/response datasets for training large language models to roleplay as Hokma (or other Lobotomy Corp/LCB characters).

## Features

- **Weighted template sampling** for realistic topic distribution
- **Multiple inputs/outputs** per template for natural variation
- **Support for long, monologue-style responses** for output diversity
- **Per-theme output grouping** (optional)
- **Progress bar** with `tqdm` (optional)
- **Theme distribution logging**
- **CLI with extensive options**

## Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/YOUR_USERNAME/hokma-dataset-generator.git
   cd hokma-dataset-generator
   ```

2. (Optional) Install tqdm for progress bars:
   ```bash
   pip install tqdm
   ```

3. (Optional) Create and activate a virtual environment.

## Usage

```bash
python hokma_dataset_generator.py [options]
```

### Most common options

- `-n`, `--num-entries`: Number of prompt/response entries to generate (default: 1000)
- `-o`, `--output`: Output file name (default: `hokma_dataset.jsonl`)
- `-s`, `--seed`: Random seed (default: 42)
- `--shuffle`: Shuffle dataset before saving
- `--theme-log THEME_LOG.json`: Save theme distribution log and per-theme samples
- `--verbose`: Print each generated entry to console (for debugging/small runs)
- `--group-by-theme`: Write separate output files per theme (e.g., `hokma_theme_lore.jsonl`)

### Example

```bash
python hokma_dataset_generator.py -n 1500 --shuffle --output hokma_1500.jsonl --theme-log stats.json
```

### Example: Grouped by theme

```bash
python hokma_dataset_generator.py -n 1500 --group-by-theme
```

### Example: Verbose (print every entry)

```bash
python hokma_dataset_generator.py -n 5 --verbose
```

## Template Customization

- Edit the `templates` array in `hokma_dataset_generator.py` to add more themes, input variations, and output styles.
- Each template supports:
    - `theme` (string): category for stats and grouping
    - `weight` (int): relative likelihood to sample this template
    - `instruction` (string): what the user is asking
    - `inputs` (list): ways the user might phrase the question
    - `outputs` (list): possible model responses

## Output

- **Default:** JSONL file with one prompt/response per line.
- **Theme log:** JSON file with counts and detailed per-theme samples.
- **Grouped by theme:** One JSONL file per theme.

## License

MIT

---

**Contributions welcome!**  
Open an issue or PR to suggest more Hokma lore, templates, or features.