import numpy as np
import pandas as pd

target = pd.read_csv("datasets/iclr2026_new/ratings.csv")
baseline = pd.read_csv("results/deepreview_baseline/scores.csv")

target_bin = np.floor(target["avg_score"]).astype(int)
baseline_bin = np.floor(baseline["gt_avg_score"]).astype(int)

target_prop = target_bin.value_counts(normalize=True)

# largest N such that for every bin, round(N * target_prop[bin]) <= available rows in baseline
avail = baseline_bin.value_counts()
bins = sorted(target_prop.index)

def feasible(n):
    counts = {b: int(round(n * target_prop[b])) for b in bins}
    return all(counts[b] <= avail.get(b, 0) for b in bins)

n = len(baseline)
while n > 0 and not feasible(n):
    n -= 1

counts = {b: int(round(n * target_prop[b])) for b in bins}

rng = np.random.RandomState(0)
picked = []
for b in bins:
    pool = baseline.index[baseline_bin == b].to_numpy()
    k = counts[b]
    if k > 0:
        picked.extend(rng.choice(pool, size=k, replace=False))

out = baseline.loc[picked].reset_index(drop=True)
out.to_csv("results/deepreview_baseline/scores_resampled.csv", index=False)

print("target_prop (floor bin):")
print(target_prop.sort_index())
print()
print("baseline available per bin:")
print(avail.sort_index())
print()
print("chosen N:", n)
print("per-bin counts:", {b: counts[b] for b in bins})
print("output rows:", len(out))
print("output bin dist:")
print(np.floor(out["gt_avg_score"]).astype(int).value_counts(normalize=True).sort_index())
