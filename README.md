# uma-extractor-merge

Merge two (or more) [UmaExtractor](https://github.com/xancia/UmaExtractor) `data.json` dumps into one file, so tools that read a single dump see every veteran from all accounts as if they were one account.

## Usage

Python 3.8+, no dependencies.

```bash
python merge_umas.py data.json data_alt.json -o data_merged.json
```

Any number of inputs works. Output defaults to `data_merged.json`.

## What it does

`trained_chara_id` is a per-account counter, so two accounts can use the same id for different characters, and parent links (`succession_trained_chara_id_1/2`) would then point at the wrong horse.

- The first file keeps its ids unchanged.
- In each later file, any id already taken (by a character or a parent reference) is remapped to a fresh id above every existing one.
- `trained_chara_id`, `succession_trained_chara_id_1/2` and `owner_trained_chara_id` are rewritten together, so every parent link still points inside its own account.
- Every other field is copied as-is; the output keeps the same format as a normal `data.json`.

Dumps are gitignored (`*.json`) so account data never gets committed.
