"""Build the weakness/strength scoring training set from DeepReview-13K.

One sample per paper: all reviewers' strengths/weaknesses parsed into a flat
item list ("strength: ..." / "weakness: ..."), GT = mean reviewer rating.
Output:
  datasets/weakness_score_train.jsonl
  datasets/weakness_score_val.jsonl   (deterministic 5% split, seed 0)
"""

import json
import os
import random
import re

import dotenv
import tqdm

dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

from datasets import load_dataset

from paths import DATASETS_DIR
from build_deepreview import coerce_scores

TRAIN_OUT = DATASETS_DIR / "weakness_score_train.jsonl"
VAL_OUT = DATASETS_DIR / "weakness_score_val.jsonl"

ITEM_MARKER = re.compile(r"^\s*(?:\d+[.)]|[-*+•])\s+")


def split_items(text: str) -> list[str]:
    """Deterministic list parsing: split on bullet/numbered lines.

    Lines starting with a list marker begin a new item; continuation lines
    attach to the current item. Text before the first marker (or a field with
    no markers at all) is one item.
    """
    items: list[str] = []
    current: list[str] = []
    for line in text.split("\n"):
        if ITEM_MARKER.match(line):
            if current and "".join(current).strip():
                items.append("\n".join(current).strip())
            current = [ITEM_MARKER.sub("", line, count=1)]
        else:
            current.append(line)
    if current and "".join(current).strip():
        items.append("\n".join(current).strip())
    return items


def main():
    ds = load_dataset("WestlakeNLP/DeepReview-13K", token=os.environ["HF_TOKEN"])["train"]

    samples = []
    seen = set()
    skipped_no_scores = 0
    skipped_no_items = 0
    for ex in tqdm.tqdm(ds):
        pid = ex["id"]
        if pid in seen:  # each paper appears 3x (mode fast/standard/best)
            continue
        seen.add(pid)

        scores = coerce_scores(ex["rating"])
        if not scores:
            skipped_no_scores += 1
            continue
        gt = sum(scores) / len(scores)

        reviewer_comments = json.loads(ex["reviewer_comments"])
        items = []
        for rc in reviewer_comments:
            content = rc["content"]
            for field, prefix in (("strengths", "strength"), ("weaknesses", "weakness")):
                text = content[field]
                if not text:
                    continue
                for item in split_items(text):
                    items.append(f"{prefix}: {item}")
        if not items:
            skipped_no_items += 1
            continue

        samples.append({"paper_id": pid, "items": items, "gt": gt})

    rng = random.Random(0)
    rng.shuffle(samples)
    n_val = round(len(samples) * 0.05)
    val, train = samples[:n_val], samples[n_val:]

    with open(TRAIN_OUT, "w") as f:
        for s in train:
            f.write(json.dumps(s) + "\n")
    with open(VAL_OUT, "w") as f:
        for s in val:
            f.write(json.dumps(s) + "\n")

    n_items = [len(s["items"]) for s in samples]
    gts = [s["gt"] for s in samples]
    print(f"papers: {len(samples)} (train {len(train)}, val {len(val)})")
    print(f"skipped: no_scores={skipped_no_scores}, no_items={skipped_no_items}")
    print(f"items/paper: min={min(n_items)} mean={sum(n_items)/len(n_items):.2f} max={max(n_items)}")
    print(f"gt: min={min(gts):.2f} mean={sum(gts)/len(gts):.2f} max={max(gts):.2f}")
    import collections
    hist = collections.Counter(round(g) for g in gts)
    print("gt hist (rounded):", dict(sorted(hist.items())))


if __name__ == "__main__":
    main()
