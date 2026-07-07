## Summary
LRACA is a deep multi-view clustering framework that combines three modules: (1) a category-aware anchor generation strategy using hierarchical K-means to produce cross-view consistent prototypes, (2) a dynamic low-rank attention mechanism with entropy regularization to reduce quadratic complexity and improve feature discriminability, and (3) a cluster-level contrastive learning module guided by pseudo-labels. Experiments on six large-scale datasets benchmark LRACA against eight MVC baselines.

## Strengths
- **Scale focus is appropriate**: The paper targets genuinely large-scale settings (up to 126k samples) where standard instance-level contrastive methods fail with OOM errors. The choice to evaluate on TinyImageNet (200 classes) and YouTubeFace50 (50 classes, 126k samples) is commendable.
- **Ablation demonstrates module utility**: Table 3 shows that removing either the Anchor Alignment Constraint (AAC) or Low-Rank Projection (LRP) consistently degrades performance, confirming both components contribute. The drop in CIFAR-10 ACC when removing LRP (−7.0%) is meaningful.
- **Cluster-level contrastive loss is a reasonable design**: Operating on cluster probability vectors instead of raw features reduces memory and avoids noisy sample-level false negatives, which is a sensible choice for large-scale settings.

## Weaknesses

### Fatal
None that outright invalidate the contribution.

### Major

1. **Results table inconsistency with ablation**: In Table 2, LRACA on YouTubeFaceSel reports ACC=33.75 and PUR=41.30. The full model row in Table 3 (LC+AAC+LRP) for the same dataset reports ACC=31.75 and PUR=39.00. These are different numbers for the same model, which undermines result reliability.

2. **Factually incorrect performance claims**: The abstract and Section 4.2 claim LRACA "significantly outperforms state-of-the-art methods," but Table 2 directly contradicts this. GC-CMVC achieves higher ACC on YouTubeFaceSel (34.10 vs. 33.75), FSMSC achieves higher ACC on CIFAR-10 (99.54 vs. 99.24) and on NUSWIDEOBJ (19.03 vs. 17.64). Section 4.2 states "LRACA achieves an average ACC/PUR advantage of 3.8% on NUSWIDEOBJ and YouTubeFaceSel," but LRACA is not even first-place on these datasets by ACC.

3. **Entropy regularization is conceptually inverted**: Eq. 12 maximizes entropy (negative entropy is minimized, so entropy is maximized), and the text correctly says this "prevents attention from focusing on a few dominant anchors"—i.e., it promotes uniform/dense distributions. Yet the same sentence states "This encourages sparsity for discriminative features." Sparsity and maximum entropy are contradictory objectives; one or the description is wrong.

4. **Claimed linear complexity is contradicted by the paper's own formula**: Section 3.3 headlines "linear complexity O(Nk)," yet the total complexity (Eq. 191) includes a term O(n_v²m²K) that is quadratic in batch size m. This makes the linear-complexity claim incorrect as stated.

### Minor

1. **Keys and Values are identical in the attention design (Eq. 10)**: K̃ and Ṽ are computed by the exact same formula, meaning they carry identical information. No justification is given for this design choice, and it degrades attention expressiveness.

2. **Parameter sensitivity is internally inconsistent**: Fig. 2 and its extracted table show that k=32 achieves higher ACC and NMI than k=16 on both evaluated datasets, yet the authors fix k=16 as "optimal." The rationale for not using k=32 (possibly efficiency) is never stated.

3. **Ablation lacks a pure LC baseline**: Table 3 only shows LC+AAC, LC+LRP, and LC+AAC+LRP. The standalone CL-only baseline is absent, making it impossible to quantify the absolute contribution of the contrastive objective itself.

4. **Projection matrix shape inconsistency**: Eq. 9 defines Θ ∈ ℝ^{k×d} via softmax(AW_c), but M (number of anchors) varies while Θ must be k×d; the computation softmax(AW_c) with A ∈ ℝ^{M×d}, W_c ∈ ℝ^{d×k} produces ℝ^{M×k}, not ℝ^{k×d}—transposition or aggregation step is missing from the exposition.

### Trivial
- The paper mentions GC-CMVC as a baseline but does not define the abbreviation in the comparison methods section.

## Nice-to-Haves
- A wall-clock training time comparison against the baselines would strengthen the efficiency claim.
- Reporting variance across multiple runs would help assess statistical significance of improvements.

## Novel Insights
The idea of initializing and dynamically updating the low-rank projection matrix Θ using semantically meaningful anchor cluster centers (rather than random JL projections) is a sensible and underexplored coupling between the clustering objective and the approximation strategy. If the technical inconsistencies were resolved, this synergy could constitute a meaningful insight for the linear attention community. The cluster-level contrastive loss formulation on soft probability vectors also avoids false-negative issues that plague instance-level contrastive MVC methods at scale, though the novelty here is moderate.

## Suggestions
- Reconcile the numbers in Table 2 and Table 3 for YouTubeFaceSel.
- Either fix the entropy minimization/maximization contradiction in Section 3.1.1 or correct the description.
- Revise the complexity claim: either fix the formula in Eq. 191 or acknowledge that linear complexity applies only to the attention module, not the overall pipeline.
- Revise the claim "significantly outperforms" to accurately reflect where LRACA leads vs. is competitive.
- Provide justification (efficiency trade-off) for choosing k=16 over k=32.

## Score and Decision

The paper targets a valid problem and proposes a reasonable combination of ideas. However, three major issues—an internal inconsistency between the main results table and the ablation table, an unjustified "significantly outperforms" narrative contradicted by the authors' own Table 2, and a false complexity claim contradicted by the paper's own formula—significantly weaken the submission's credibility. These are not minor presentation issues; they undermine the core empirical and theoretical claims. The technical novelty is incremental (Linformer-style attention + anchor-based MVC + cluster contrastive learning), and the results are mixed rather than clearly state-of-the-art.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>