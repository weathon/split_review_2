## Summary

This paper introduces CrowdFM, a bipartite GNN that pre-trains on domain-randomized synthetic crowdsourcing data (generated via a 3PL IRT model) to perform zero-shot label aggregation across heterogeneous datasets without any dataset-specific retraining. The model uses size-invariant node initialization (shared learnable vectors for all workers/tasks) and attention-based message passing to learn transferable representations. Experiments on 22 real-world crowdsourcing datasets show CrowdFM (83.41% avg. accuracy) is competitive with the best dataset-specific methods such as EBCC (84.08%) while running orders of magnitude faster at inference time, and its learned embeddings can be adapted to worker assessment and task assignment.

## Strengths

1. **Well-motivated, precisely framed problem.** The paper clearly identifies the gap between Majority Voting (fast but inaccurate) and dataset-specific methods (accurate but non-transferable), and formalizes the cross-dataset generalization objective (Eq. 2) versus per-dataset estimation (Eq. 1) — a clean setup that situates the contribution exactly.

2. **Size-invariant initialization is a principled and non-trivial design choice.** Sharing a single learnable vector across all workers and another across all tasks (Section 3.2), rather than using dataset-specific IDs, directly addresses the structural heterogeneity challenge. This is a simple but key insight that enables the model to process datasets of arbitrary size with the same fixed parameters.

3. **Thoughtfully constructed synthetic data generator.** The generator uses the 3PL IRT model, heavy-tailed participation distributions, and domain randomization over generator parameters (Section 3.1). The ablation study confirms its importance (w/o SG drops from ~83% to ~78.5% accuracy). This goes well beyond the uniform random generation used by HyperLM.

4. **Thorough evaluation across 22 real-world datasets.** The breadth of benchmarks is a genuine strength, and the use of the Wilcoxon signed-ranks test is appropriate for this paired comparison setting. The ablation studies (Figure 6) isolate the contributions of the synthetic generator and the attention mechanism.

5. **Demonstrated transfer to multiple downstream tasks.** The worker/task assessment (Section 4.3.1) and task assignment (Section 4.3.2) experiments show that CrowdFM's learned embeddings carry information beyond the primary aggregation objective, supporting the claim of transferable representations.

## Weaknesses

### Fatal
None. The core contribution — a zero-shot GNN for label aggregation that is competitive with dataset-specific methods — is sound and supported by the evidence.

### Major

1. **Task assignment compatibility predictor is trained using ground-truth labels for data filtering, creating a significant confound.** Section 4.3.2 states: "we perform data filtering: for each task $t_j$, we sample an equal number of correct and incorrect responses based on agreement with the ground truth $y_j$" (lines 266–267). This means the compatibility head's training data is constructed using knowledge of the true labels — information unavailable in any real deployment scenario. The comparison between "Predictor" and "Random" strategies (Figure 5) therefore partly measures how well the model exploits privileged information (ground-truth-based filtering) rather than true predictive compatibility from learned embeddings alone. This does not invalidate the experiment entirely — the Predictor strategy still outperforms Random, which indicates the embeddings carry useful signal — but it sharply limits the practical conclusions one can draw about CrowdFM's usefulness for real task assignment. The authors should either: (a) train the compatibility head without ground-truth filtering, (b) use the model's own predicted labels as a proxy for correctness, or (c) clearly discuss this confound as a limitation.

### Minor

2. **Runtime comparison is asymmetric.** Table 1 reports CrowdFM's runtime as 0.53s per dataset — this is inference-only, excluding the substantial pretraining cost. Baseline methods (DS, EBCC, GLAD, etc.) include both training and inference time, since they must be fit from scratch per dataset. The paper weakly acknowledges this ("efficient inference" in line 206) but presents the times as directly comparable in the table without meaningful caveat. While the asymmetry is inherent in the paradigm being compared (amortized cost is the point of a foundation model), the paper should state explicitly what is measured for each method and separately report CrowdFM's pretraining cost for full transparency.

3. **Real-world worker/task assessment uses confounded proxy measures and overstates correlations.** On the Web dataset (Figure 4), the paper uses "individual worker accuracy" and "task error rate" as proxies for ability and difficulty. Worker accuracy is confounded with task difficulty (workers assigned easy tasks appear more skilled), and task error rate is confounded with worker ability (easy tasks assigned to skilled workers appear even easier). The reported Pearson correlations (0.449 for worker ability, 0.606 for task difficulty) are moderate, not "strong" as claimed in the text ("the predictions from CrowdFM … exhibit **strong correlation**" — line 246). These are respectable results for a zero-shot model, but the characterization should be more measured.

4. **The "foundation model" label overreaches relative to what CrowdFM actually does.** CrowdFM is pre-trained on synthetic data from a single parametric model family (3PL IRT) and adapted to three downstream tasks that all involve reading out different aspects of the same learned representations from the same encoder. This is a far narrower scope than what "foundation model" typically implies in the literature (large-scale pre-training on diverse, real data with adaptation to qualitatively different tasks). The paper's contribution — a transferable GNN for aggregation — stands on its own merits without this label, which sets expectations the model does not meet.

### Trivial
None.

## Nice-to-Haves

- **Head-to-head win/loss comparisons against each baseline**, supplementing the #Win-over-MV metric. The current "#Win" column (number of datasets where each method beats MV) is informative but doesn't directly show how CrowdFM compares to EBCC, BWA, or DS dataset-by-dataset.
- **A real-to-real transfer experiment** (e.g., train on a subset of the 22 real datasets and evaluate on held-out real datasets) would further substantiate the cross-dataset generalization claim beyond synthetic-to-real transfer.
- **Standard deviations or confidence intervals** on the average accuracy results in Table 1, particularly for baselines with optimization variance.

## Removed Points

These points from the input review were removed with justification:

- **"#Win metric is misleading"** — Removed because the paper transparently defines "#Win" in the table caption as "the number of datasets where each method outperforms MV." The claims made (e.g., "our method achieves the highest number of wins over MV") are factually accurate given this definition.
- **"Synthetic data generator lacks distributional validation"** — Removed because the paper explicitly references Appendix F ("includes a quantitative analysis comparing synthetic and real-world datasets"), which was stripped by the parser. Per policy, weaknesses about missing appendix content are not valid.
- **"Attention mechanism is not conventional pairwise attention"** — Removed because this is an architectural observation, not a weakness. The mechanism works as described (self-attention over annotations normalized per node) and is clearly specified in Equations 5–8.
- **"Hyperparameter ablations show no saturation"** — Removed because the input critic themselves notes "this is not a flaw per se." Monotonic improvement with scale is a positive scaling property.
- **"Missing cross-dataset generalization (real-to-real)"** — Demoted to Nice-to-Have because synthetic-to-real transfer is a valid form of cross-dataset generalization. A real-to-real experiment would be additive, not required to support the paper's claim.
- **"Variance/error bars missing"** — Demoted to Nice-to-Have because CrowdFM's inference is deterministic given fixed weights, making variance less critical than for baselines with optimization randomness.

## Novel Insights

None beyond the paper's own contributions. The reviews identify presentation and methodological confounds but do not surface a fundamentally new interpretation of the results.

## Suggestions

1. **Fix or clearly discuss the task assignment confound.** The ground-truth-based filtering in Section 4.3.2 is the paper's most significant methodological issue. The simplest fix is to retrain the compatibility head without filtering, or use the model's own predicted labels as a proxy for correctness.
2. **Report inference-only runtime for all methods** alongside a separate statement of CrowdFM's pretraining cost, so readers can make an informed comparison.
3. **Tone down the "foundation model" framing** to something like "transferable aggregation model" or "general-purpose aggregation network" to better match the scope of the contribution.
4. **Add head-to-head win/loss counts** (CrowdFM vs. each baseline, dataset-by-dataset) so the "#Win" metric directly supports the comparison readers care about most.

## Score and Decision

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>