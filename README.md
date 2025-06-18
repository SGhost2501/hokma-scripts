# Hokma Template Dataset Refinement Toolkit

This toolkit helps you process, clean, audit, and refine LLM template datasets (e.g., for a Hokma-themed assistant) from raw `.txt` files to a highly structured, deduplicated, and metadata-rich JSON.
Follow these steps in order:

---

## 1. Merge Raw Text Files

**Script:** `merge_hokmaballs_to_json.py`  
**Purpose:**  
- Reads `hokmaballs*.txt` files.
- Parses input/output pairs.
- Assigns a theme based on file.
- Outputs `hokma_templates_generated.json`.

**How to use:**
```sh
python merge_hokmaballs_to_json.py
```
- Ensure all `hokmaballs*.txt` files and the script are in the same folder.

---

## 2. Clean and Sanitize the Merged Dataset

**Script:** `clean_hokma_templates.py`  
**Purpose:**  
- Removes stray quotes, commas, code fragments, and non-natural-language entries from inputs/outputs.
- Outputs a cleaned file: `hokma_templates_cleaned.json`.

**How to use:**
```sh
python clean_hokma_templates.py
```
- Place `hokma_templates_generated.json` and the script in the same folder.

---

## 3. Audit and Flag Misplaced Inputs/Outputs

**Script:** `audit_inputs_outputs.py`  
**Purpose:**  
- Scans `hokma_templates_cleaned.json` for potential misaligned items (e.g., outputs in the input list and vice versa).
- Prints suspicious lines for manual review.

**How to use:**
```sh
python audit_inputs_outputs.py
```
- Review the output and manually correct `hokma_templates_cleaned.json` if desired.

---

## 4. Refine, Split, Deduplicate, and Add Metadata

**Script:** `refine_and_split_templates.py`  
**Purpose:**  
- Automatically moves misplaced lines.
- Splits blocks into granular, input-aligned mini blocks (each input with related outputs).
- Deduplicates entries.
- Optionally adds metadata such as source theme and review status.
- Outputs `hokma_templates_refined.json`.

**How to use:**
```sh
python refine_and_split_templates.py
```
- Place your (optionally reviewed) `hokma_templates_cleaned.json` and the script in the same folder.

---

## 5. Final Manual Review (Optional and Recommended)

- Open `hokma_templates_refined.json` in a JSON-aware editor.
- Double-check sample blocks for logical consistency and coherence.
- Optionally fill metadata fields (e.g., set `"reviewed": true` after manual approval).

---

## Example Workflow

```sh
python merge_hokmaballs_to_json.py
python clean_hokma_templates.py
python audit_inputs_outputs.py  # Read output and edit cleaned JSON if needed
python refine_and_split_templates.py
# Final review in a text editor
```

---

## Notes

- You can adjust theme mappings, block sizes, or metadata fields by editing the scripts.
- For any script, use `python scriptname.py --help` if CLI options are present.

---

## Requirements

- Python 3.x
- All scripts and data files in the same directory.

---

## File Outputs

- `hokma_templates_generated.json` – Raw merged dataset.
- `hokma_templates_cleaned.json` – Cleaned and filtered dataset.
- `hokma_templates_refined.json` – Final, audit-passed, deduplicated, split, and metadata-rich dataset, ready for LLM ingestion.

---

## Support

For questions or feature requests, open an issue or contact the maintainer.
