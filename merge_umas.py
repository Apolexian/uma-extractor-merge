#!/usr/bin/env python3
"""Merge several UmaExtractor data.json dumps into one file that behaves like a single account.

trained_chara_id values are per-account counters, so two accounts can hand out the same
id. Ids from later files that clash with ids already taken are remapped to fresh ones, and
every reference to them (succession_trained_chara_id_1/2, owner_trained_chara_id) is
rewritten so parent links stay inside the right account.
"""
import argparse
import json
import sys

ID_FIELDS = ("trained_chara_id", "succession_trained_chara_id_1",
             "succession_trained_chara_id_2", "owner_trained_chara_id")


def load(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        sys.exit(f"{path}: expected a JSON array of characters")
    return data


def ids_in(charas):
    return {c[k] for c in charas for k in ID_FIELDS if c.get(k)}


def merge(dumps):
    """Return (merged list, number of remapped ids per dump)."""
    merged, taken, stats = [], set(), []
    next_id = max((i for d in dumps for i in ids_in(d)), default=0) + 1
    for charas in dumps:
        own = ids_in(charas)
        remap = {}
        for i in sorted(own & taken):
            remap[i] = next_id
            next_id += 1
        for c in charas:
            c = dict(c)
            for k in ID_FIELDS:
                if c.get(k) in remap:
                    c[k] = remap[c[k]]
            merged.append(c)
        taken |= (own - remap.keys()) | set(remap.values())
        stats.append(len(remap))
    return merged, stats


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("inputs", nargs="+", help="data.json files to merge (first one keeps its ids)")
    p.add_argument("-o", "--output", default="data_merged.json")
    args = p.parse_args()
    if len(args.inputs) < 2:
        p.error("need at least two files")

    dumps = [load(path) for path in args.inputs]
    merged, stats = merge(dumps)
    for path, charas, remapped in zip(args.inputs, dumps, stats):
        print(f"{path}: {len(charas)} characters, {remapped} ids remapped")

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)
    print(f"wrote {len(merged)} characters to {args.output}")


if __name__ == "__main__":
    main()
