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
    skipped_bad_scores = 0
    skipped_no_items = 0
    for ex in tqdm.tqdm(ds):
        pid = ex["id"]
        if pid in seen:  # each paper appears 3x (mode fast/standard/best)
            continue
        seen.add(pid)

        # strict rating parse: any unparseable entry -> skip the whole paper
        raw = ex["rating"]
        try:
            if isinstance(raw, str):
                raw = json.loads(raw)
            scores = [int(s.split(":", 1)[0].strip()) if isinstance(s, str) else int(s)
                      for s in raw]
        except (ValueError, TypeError):
            print(f"skip {pid}: unparseable rating {ex['rating']!r}")
            skipped_bad_scores += 1
            continue
        if not scores:
            print(f"skip {pid}: empty rating list")
            skipped_bad_scores += 1
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
    val, train_pool = samples[:n_val], samples[n_val:]  # val keeps natural distribution

    # uniform-ish train: bin by rounded gt, cap each bin at 400 (user decision)
    bins = {}
    for s in train_pool:
        bins.setdefault(round(s["gt"]), []).append(s)
    train = []
    for b in sorted(bins):
        train.extend(bins[b][:400])
    rng.shuffle(train)
    print("train bin counts after cap:",
          {b: min(len(v), 400) for b, v in sorted(bins.items())})

    with open(TRAIN_OUT, "w") as f:
        for s in train:
            f.write(json.dumps(s) + "\n")
    with open(VAL_OUT, "w") as f:
        for s in val:
            f.write(json.dumps(s) + "\n")

    n_items = [len(s["items"]) for s in samples]
    gts = [s["gt"] for s in samples]
    print(f"papers: {len(samples)} (train {len(train)}, val {len(val)})")
    print(f"skipped: bad_scores={skipped_bad_scores}, no_items={skipped_no_items}")
    print(f"items/paper: min={min(n_items)} mean={sum(n_items)/len(n_items):.2f} max={max(n_items)}")
    print(f"gt: min={min(gts):.2f} mean={sum(gts)/len(gts):.2f} max={max(gts):.2f}")
    import collections
    hist = collections.Counter(round(g) for g in gts)
    print("gt hist (rounded):", dict(sorted(hist.items())))


if __name__ == "__main__":
    main()
