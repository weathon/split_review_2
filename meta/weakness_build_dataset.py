"""STAGE 2 — build the HF dataset from stage-1 extraction.

Reads every meta/weakness_validity_out/stage1/<id>.json and maps each raw model item to a label:
  resolved   & not needs_editing -> invalid   (resolved, no paper edit needed)
  resolved   & needs_editing     -> DROPPED    (resolved but required editing; excluded per spec)
  unresolved                     -> valid      (AC says the concern remains)
  not_mentioned                  -> DROPPED    (AC never spoke to it; cannot label)

Columns: paper_id, decision, reviewer_index, review_item, ac_status, needs_editing, ac_evidence, label.
Saves to disk at meta/weakness_validity_out/dataset (datasets.Dataset.save_to_disk).
Run: python meta/weakness_build_dataset.py
"""
import json
from collections import Counter
from pathlib import Path

from datasets import Dataset

STAGE1 = Path(__file__).parent / "weakness_validity_out" / "stage1_strict"
OUT = Path(__file__).parent / "weakness_validity_out" / "dataset_strict"

rows = []
n_papers = 0
n_gated = 0
for f in sorted(STAGE1.glob("*.json")):
    d = json.load(open(f))
    n_papers += 1
    if not d["ac_lists_specific_concerns"]:
        n_gated += 1
        continue
    for it in d["items"]:
        status = it["ac_status"]
        if status == "not_mentioned":
            continue
        if status == "resolved":
            if it["needs_editing"]:
                continue
            label = "invalid"
        elif status == "unresolved":
            label = "valid"
        else:
            raise ValueError(f"unexpected ac_status {status!r} in {f.name}")
        rows.append({
            "paper_id": d["paper_id"],
            "decision": d["decision"],
            "reviewer_index": it["reviewer_index"],
            "review_item": it["weakness_text"],
            "ac_status": status,
            "needs_editing": it["needs_editing"],
            "ac_evidence": it["ac_evidence"],
            "label": label,
        })

ds = Dataset.from_list(rows)
ds.save_to_disk(str(OUT))

print(f"papers: {n_papers}  gated_out (generic AC): {n_gated}  kept: {n_papers - n_gated}  rows: {len(rows)}")
print("label distribution:", Counter(r["label"] for r in rows))
print(f"saved to {OUT}")
