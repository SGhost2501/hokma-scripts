# Hokma Template Dataset Refinement Toolkit

This toolkit processes, cleans, audits, and refines LLM prompt/response template datasets (e.g., for a Hokma-themed assistant) from raw `.txt` files into highly structured, deduplicated, and metadata-rich JSONs suitable for LLM fine-tuning.

---

## Workflow Overview

### 1. Merge Raw Text Files

- **Script:** `merge_hokmaballs_to_json.py`
- **Purpose:** Reads all `hokmaballs*.txt` files, parses input/output pairs, assigns a theme, and outputs `hokma_templates_generated.json`.

```sh
python merge_hokmaballs_to_json.py
```

---

### 2. Clean and Sanitize Merged Dataset

- **Script:** `clean_hokma_templates.py`
- **Purpose:** Removes stray characters, code, and non-natural-language entries.
- **Output:** `hokma_templates_cleaned.json`

```sh
python clean_hokma_templates.py
```

---

### 3. Audit Inputs/Outputs

- **Script:** `audit_inputs_outputs.py`
- **Purpose:** Flags potential misaligned items (e.g., outputs in input fields) for review.
- **Action:** Review printed output and manually correct `hokma_templates_cleaned.json` as needed.

```sh
python audit_inputs_outputs.py
```

---

### 4. Refine, Split, Deduplicate, and Add Metadata

- **Script:** `refine_and_split_templates.py`
- **Purpose:** Moves misplaced lines, splits multi-input/output blocks into granular 1-to-1 examples, deduplicates, adds metadata.
- **Output:** `hokma_templates_refined.json`

```sh
python refine_and_split_templates.py
```

---

### 5. Advanced Refinement & Per-Theme/1-to-1 Outputs

- **Script:** `refine_hokma_templates_advanced.py`
- **Purpose:** 
  - Further cleans and normalizes the data,
  - Enforces strict 1-to-1 input/output mapping,
  - Separates data into per-theme and 1to1 files (e.g. `hokma_advice_templates_1to1.json`, `hokma_meme_templates_1to1.json`, etc),
  - Fills in missing outputs with placeholders if needed,
  - Adds richer metadata if applicable.
- **Output:** Multiple files, such as:
    - `hokma_advice_templates_1to1.json`
    - `hokma_edge_templates_1to1.json`
    - `hokma_meme_templates_1to1.json`
    - `hokma_philosophy_templates_1to1.json`
    - `hokma_refusal_templates_1to1.json`
    - `hokma_templates_final_1to1.json`

```sh
python refine_hokma_templates_advanced.py
```

---

### 6. Final Manual Review (Strongly Recommended)

- Open the generated *_1to1.json files in a JSON-aware editor.
- Double-check random samples for logical consistency and output quality.
- Optionally update metadata fields (e.g., `"reviewed": true`).

---

## Example Full Workflow

```sh
python merge_hokmaballs_to_json.py
python clean_hokma_templates.py
python audit_inputs_outputs.py  # Manual corrections if needed
python refine_and_split_templates.py
python refine_hokma_templates_advanced.py
# Final review in a text editor
```

---

## Output Files

- `hokma_templates_generated.json` – Raw merged dataset.
- `hokma_templates_cleaned.json` – Cleaned and filtered dataset.
- `hokma_templates_refined.json` – Deduplicated, split, and metadata-rich dataset.
- `hokma_advice_templates_1to1.json` and similar – Strict 1-to-1, per-theme datasets (final).
- `hokma_templates_final_1to1.json` – Full final, 1-to-1 dataset.

---

## Requirements

- Python 3.x
- All scripts and data files in the same directory.

---

## Support

For questions or feature requests, open an issue or contact the maintainer.
