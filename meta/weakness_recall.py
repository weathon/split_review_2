"""STAGE 3B — per-method recall of valid / invalid weaknesses.

Replaces the SDK classifier. For each paper and each method's generated review, a matching judge
(deepseek-v4-flash, blind to the valid/invalid label) decides which of the paper's gold weakness
items that method's review ALSO raised. Then, pooling items across papers (micro), for each method:
    recall_valid   = matched valid items   / total valid items
    recall_invalid = matched invalid items / total invalid items

Gold weaknesses come from the stage-2 dataset (paper_id, review_item, label).
Method reviews come from final_results/ (6 methods, heterogeneous formats).
DeepReviewer_14B: the method output is its META REVIEW (results[0].meta_review.content).

Output: meta/weakness_validity_out/recall/<method>/<pid>.json holding the matched gold indices.
Resume: skip a (method, paper) whose file exists. A paper with no review for a method is skipped whole.
Run: python meta/weakness_recall.py
"""
import json
import os
import re
import time
from collections import defaultdict
from pathlib import Path

import dotenv
from datasets import load_from_disk
from openai import OpenAI
from pydantic import BaseModel

ROOT = Path(__file__).resolve().parent.parent
dotenv.load_dotenv(ROOT / ".env")

FINAL = ROOT / "final_results"
DS_PATH = Path(__file__).parent / "weakness_validity_out" / "dataset_strict"
OUT = Path(__file__).parent / "weakness_validity_out" / "recall_strict"

client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.environ["OPENROUTER_API_KEY"])
MODEL = "deepseek/deepseek-v4-flash"
MAX_RETRIES = 5
RETRY_DELAY = 5

METHODS = {
    "ours_cmp3_ours_v2": {"dir": FINAL / "ours_cmp3_ours_v2" / "reviews", "kind": "single_md"},
    "nocal_cmp3_nocal_v3": {"dir": FINAL / "nocal_cmp3_nocal_v3" / "reviews", "kind": "single_md"},
    "baseline_cmp3_baseline_v2": {"dir": FINAL / "baseline_cmp3_baseline_v2" / "reviews", "kind": "single_md"},
    "cspaper": {"dir": FINAL / "cspaper", "kind": "cspaper_md"},
    "DeepReviewer_14B": {"dir": FINAL / "DeepReviewer_14B", "kind": "deepreviewer_meta"},
    "DeepReviewer-v2-openai": {"dir": FINAL / "DeepReviewer-v2-openai", "kind": "single_md"},
}


class Match(BaseModel):
    raised_indices: list[int]


PROMPT = """Below is an automatically generated peer review of a paper, followed by a numbered list of specific weakness items that OTHER reviewers raised about the SAME paper.

Decide, for each numbered weakness item, whether the generated review ALSO raises that SAME specific weakness. A match requires the same specific concern about the same aspect of the paper (e.g. both complain about a missing ablation on component X, or both question the same unsupported claim). Do NOT match merely because both mention the same general topic, and do NOT match generic overlap.

Return the list of item numbers (integers) that the generated review raises. Return an empty list if none.

=== GENERATED REVIEW ===
{review}

=== NUMBERED WEAKNESS ITEMS ===
{items}
"""


def load_review(method, pid):
    cfg = METHODS[method]
    d = cfg["dir"]
    if cfg["kind"] == "single_md":
        p = d / f"{pid}.md"
        return p.read_text() if p.exists() else None
    if cfg["kind"] == "cspaper_md":
        p = d / f"{pid}__ICLR_main_2026_2.md"
        return p.read_text() if p.exists() else None
    if cfg["kind"] == "deepreviewer_meta":
        p = d / f"{pid}.txt.json"
        if not p.exists():
            return None
        return json.load(open(p))["results"][0]["meta_review"]["content"]
    raise ValueError(cfg["kind"])


def match(review_text, gold_items):
    numbered = "\n".join(f"{i + 1}. {it['review_item']}" for i, it in enumerate(gold_items))
    prompt = PROMPT.format(review=review_text, items=numbered)
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = client.chat.completions.parse(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
                response_format=Match,
                extra_body={"reasoning": {"enabled": True}},
            )
            return resp.choices[0].message.parsed.raised_indices
        except Exception as e:
            if attempt == MAX_RETRIES:
                raise
            print(f"  retry {attempt}/{MAX_RETRIES}: {type(e).__name__}: {e}")
            time.sleep(RETRY_DELAY * attempt)


ds = load_from_disk(str(DS_PATH))
gold = defaultdict(list)
for r in ds:
    gold[r["paper_id"]].append({"review_item": r["review_item"], "label": r["label"]})

for method in METHODS:
    (OUT / method).mkdir(parents=True, exist_ok=True)
    for pid, items in gold.items():
        out_path = OUT / method / f"{pid}.json"
        if out_path.exists():
            continue
        review_text = load_review(method, pid)
        if review_text is None:
            print(f"{method}/{pid}: no review, skip")
            continue
        raised = match(review_text, items)
        raised_set = set(raised)
        result = {
            "paper_id": pid,
            "method": method,
            "n_items": len(items),
            "matched": [
                {"index": i + 1, "label": it["label"], "raised": (i + 1) in raised_set}
                for i, it in enumerate(items)
            ],
        }
        json.dump(result, open(out_path, "w"), indent=1)
        print(f"{method}/{pid}: {len(raised_set)}/{len(items)} raised")

print("\n=== MICRO RECALL (pooled items) ===")
for method in METHODS:
    tot = {"valid": 0, "invalid": 0}
    hit = {"valid": 0, "invalid": 0}
    papers = 0
    for f in (OUT / method).glob("*.json"):
        papers += 1
        for m in json.load(open(f))["matched"]:
            tot[m["label"]] += 1
            if m["raised"]:
                hit[m["label"]] += 1
    rv = hit["valid"] / tot["valid"] if tot["valid"] else float("nan")
    ri = hit["invalid"] / tot["invalid"] if tot["invalid"] else float("nan")
    print(f"{method}: papers={papers}  recall_valid={rv:.4f} ({hit['valid']}/{tot['valid']})  "
          f"recall_invalid={ri:.4f} ({hit['invalid']}/{tot['invalid']})")
