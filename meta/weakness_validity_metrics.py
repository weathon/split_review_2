"""Stage 3 — report the classifier's performance against the deepseek gold labels.

Joins meta/weakness_validity/predictions.jsonl to gold labels and prints accuracy, precision,
recall, F1, Cohen's kappa, and the 2x2 confusion matrix (positive class = invalid), plus label
counts and n, broken down overall and by paper decision (accepted vs rejected).

Numbers only, no interpretation. Run: python meta/weakness_validity_metrics.py
"""
import json
from pathlib import Path

from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    cohen_kappa_score,
    confusion_matrix,
)

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "meta" / "weakness_validity"
POS = "invalid"


def gt_binary_map():
    data = [json.loads(l) for l in open(OUT_DIR / "dataset.jsonl")]
    groups = {}
    for row in data:
        groups.setdefault((row["paper_id"], row["review_idx"]), []).append(row)
    m = {}
    for (pid, ridx), group in groups.items():
        for i, row in enumerate(group):
            m[(pid, ridx, i)] = row["gt_binary"]
    return m


def report(name, gold, pred):
    n = len(gold)
    acc = accuracy_score(gold, pred)
    p, r, f1, _ = precision_recall_fscore_support(gold, pred, labels=[POS], average=None, zero_division=0)
    kappa = cohen_kappa_score(gold, pred)
    cm = confusion_matrix(gold, pred, labels=["invalid", "valid"])
    ng_inv = sum(1 for g in gold if g == "invalid")
    print(f"\n=== {name} (n={n}) ===")
    print(f"gold: invalid={ng_inv} valid={n-ng_inv} | pred: invalid={sum(1 for x in pred if x=='invalid')} valid={sum(1 for x in pred if x=='valid')}")
    print(f"accuracy={acc:.3f}  precision(invalid)={p[0]:.3f}  recall(invalid)={r[0]:.3f}  f1(invalid)={f1[0]:.3f}  kappa={kappa:.3f}")
    print("confusion (rows=gold [invalid,valid], cols=pred [invalid,valid]):")
    print(f"  {cm[0].tolist()}")
    print(f"  {cm[1].tolist()}")


def main():
    preds = [json.loads(l) for l in open(OUT_DIR / "predictions.jsonl")]
    gtb = gt_binary_map()
    gold = [row["gold"] for row in preds]
    pred = [row["pred"] for row in preds]
    report("OVERALL", gold, pred)

    for dec in ["Accept", "Reject"]:
        idx = [k for k, row in enumerate(preds) if gtb[(row["paper_id"], row["review_idx"], row["item_index"])] == dec]
        report(f"{dec} papers", [gold[k] for k in idx], [pred[k] for k in idx])


if __name__ == "__main__":
    main()
