import pandas as pd
import numpy as np
from scipy import stats
from sklearn.metrics import roc_auc_score
from itertools import combinations

ADMIN_BLACKLIST = {"rzGEfYr2ZC", "1CR1MTIgmq", "RlMCc0JTu4", "HwyYpLxY0G"}
N_BOOT = 2000
SEED = 0

def load(path):
    df = pd.read_csv(path)
    df = df[df["pred_score"] >= 0]
    df = df[~df["paper_id"].isin(ADMIN_BLACKLIST)]
    return df.reset_index(drop=True)

ours = load("final_results/ours_cmp3_ours_v2/scores.csv")

others = {
    "baseline": "final_results/baseline_cmp3_baseline_v2/scores.csv",
    "nocal": "final_results/nocal_cmp3_nocal_v3/scores.csv",
    "DeepReviewer-v2": "final_results/DeepReviewer-v2-openai/scores.csv",
    "DeepReviewer-14B": "final_results/DeepReviewer_14B/scores.csv",
}

def pval(deltas):
    deltas = np.asarray(deltas, dtype=float)
    return float(min(1.0, 2 * min(np.mean(deltas <= 0), np.mean(deltas >= 0))))

def metrics_pointwise(pred, gt_avg, labels):
    return {
        "spearman": float(stats.spearmanr(pred, gt_avg).statistic),
        "pearson": float(stats.pearsonr(pred, gt_avg).statistic),
        "mae": float(np.mean(np.abs(pred - gt_avg))),
        "auroc": float(roc_auc_score(labels, pred)),
    }

rng = np.random.default_rng(SEED)
print(f"paired paper bootstrap, n_boot={N_BOOT}, seed={SEED}")

for name, path in others.items():
    other = load(path)
    m = ours.merge(other[["paper_id", "pred_score"]], on="paper_id", suffixes=("_ours", "_other"))
    po = m["pred_score_ours"].values
    px = m["pred_score_other"].values
    gt = m["gt_avg_score"].values
    lab = (m["gt_binary"].str.strip().str.lower() == "accept").astype(int).values
    mo = metrics_pointwise(po, gt, lab)
    mx = metrics_pointwise(px, gt, lab)
    deltas = {k: [] for k in mo}
    n = len(m)
    for _ in range(N_BOOT):
        idx = rng.integers(0, n, n)
        bo = metrics_pointwise(po[idx], gt[idx], lab[idx])
        bx = metrics_pointwise(px[idx], gt[idx], lab[idx])
        for k in deltas:
            deltas[k].append(bo[k] - bx[k])
    print(f"\nours vs {name} (n={n}):")
    for k in mo:
        print(f"  {k:<9} ours={mo[k]:.4f}  {name}={mx[k]:.4f}  diff={mo[k]-mx[k]:+.4f}  p={pval(deltas[k]):.4f}")

# human baselines on ours' papers
gt_score_cols = [c for c in ours.columns if c.startswith("gt_score_")]
pred, gt_avg, labels = [], [], []
loo_by_paper, pairs_by_paper, indiv_by_paper = [], [], []
for _, row in ours.iterrows():
    human = [float(row[c]) for c in gt_score_cols if pd.notna(row[c])]
    if len(human) < 2:
        continue
    pred.append(float(row["pred_score"]))
    gt_avg.append(float(row["gt_avg_score"]))
    labels.append(int(row["gt_binary"].strip().lower() == "accept"))
    loo = [((sum(human) - h) / (len(human) - 1), h) for h in human]
    loo_by_paper.append(loo)
    pairs_by_paper.append([(human[i], human[j]) for i, j in combinations(range(len(human)), 2)])
    indiv_by_paper.append(human)

pred = np.asarray(pred)
gt_avg = np.asarray(gt_avg)
labels = np.asarray(labels)
n = len(pred)

def human_metrics(idx):
    ai = metrics_pointwise(pred[idx], gt_avg[idx], labels[idx])
    loo = [p for i in idx for p in loo_by_paper[i]]
    loo_a = np.asarray([p[0] for p in loo])
    loo_b = np.asarray([p[1] for p in loo])
    ovo = [p for i in idx for p in pairs_by_paper[i]]
    ovo_a = np.asarray([p[0] for p in ovo])
    ovo_b = np.asarray([p[1] for p in ovo])
    indiv_scores = np.asarray([s for i in idx for s in indiv_by_paper[i]])
    indiv_labels = np.asarray([labels[i] for i in idx for _ in indiv_by_paper[i]])
    human_auroc = float(roc_auc_score(indiv_labels, indiv_scores))
    loo_m = {
        "spearman": float(stats.spearmanr(loo_a, loo_b).statistic),
        "pearson": float(stats.pearsonr(loo_a, loo_b).statistic),
        "mae": float(np.mean(np.abs(loo_a - loo_b))),
        "auroc": human_auroc,
    }
    ovo_m = {
        "spearman": float(stats.spearmanr(ovo_a, ovo_b).statistic),
        "pearson": float(stats.pearsonr(ovo_a, ovo_b).statistic),
        "mae": float(np.mean(np.abs(ovo_a - ovo_b))),
        "auroc": human_auroc,
    }
    return ai, loo_m, ovo_m

full_idx = np.arange(n)
ai0, loo0, ovo0 = human_metrics(full_idx)
deltas_loo = {k: [] for k in ai0}
deltas_ovo = {k: [] for k in ai0}
for _ in range(N_BOOT):
    idx = rng.integers(0, n, n)
    ai, loo, ovo = human_metrics(idx)
    for k in ai:
        deltas_loo[k].append(ai[k] - loo[k])
        deltas_ovo[k].append(ai[k] - ovo[k])

print(f"\nours vs human leave-one-out (n={n} papers):")
for k in ai0:
    print(f"  {k:<9} ours={ai0[k]:.4f}  human={loo0[k]:.4f}  diff={ai0[k]-loo0[k]:+.4f}  p={pval(deltas_loo[k]):.4f}")
print(f"\nours vs human one-vs-one (n={n} papers):")
for k in ai0:
    print(f"  {k:<9} ours={ai0[k]:.4f}  human={ovo0[k]:.4f}  diff={ai0[k]-ovo0[k]:+.4f}  p={pval(deltas_ovo[k]):.4f}")
