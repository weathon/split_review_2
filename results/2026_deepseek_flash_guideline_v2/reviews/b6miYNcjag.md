## Summary

This paper introduces the problem of "reliability scoring" for datasets where ground truth is unobserved but auxiliary observations are available. The authors formalize ground-truth-based reliability orderings (exact match, Blackwell, Hamming/dist), prove impossibility results showing inherent limitations, and propose the Gram determinant score — a measure of the squared volume spanned by observation distributions conditioned on reported labels. The score is shown to be experiment-agnostic (ranking independent of the observation process) and, under mild conditions, uniquely so. Experiments on synthetic categorical data, CIFAR-10 embeddings, and real employment vintages demonstrate monotonic behavior under increasing corruption.

## Strengths

- **Near-tight feasibility characterization**: The paper first establishes impossibility results (Proposition 3.1) showing that no reliability score can preserve Hamming/dist ordering on the broad class $\mathcal{Q}_{\text{dom}}$ of diagonally dominant misreport matrices. It then proves (Theorem 4.2) that the Gram determinant preserves a close approximation ($\alpha$-dist ordering) under only a slightly more restricted set $\mathcal{Q}_{L,\delta}$. This near-matching of upper and lower bounds on feasibility is rare and valuable.

- **Experiment agnosticism and uniqueness characterization**: Proposition 4.3 proves that the Gram determinant ranking does not depend on which experiment $\mathbf{P}$ generated the observations, via the clean factorization $\Gamma(\mathbf{PQ}) = \det(\mathbf{P}^\top\mathbf{P})\det(\mathbf{Q})^2$. Moreover, under mild continuity and homogeneity conditions, it is the unique (up to scaling) experiment-agnostic score. This is a genuine characterization result, not just a method demonstration.

- **Clean geometric interpretation**: The Gram determinant equals the squared volume of the parallelepiped spanned by the columns of $\mathbf{PQ}$ (Eq. 4). Truthful reporting maximizes volume; misreporting applies column-stochastic transformations that shrink it. This bridges intuitive understanding and rigorous analysis.

- **Real-world validation with known ground-truth ordering**: Experiment 3 on CES employment vintages (initial estimate → one-month revision → final value) shows the Gram determinant score monotonically increasing across revisions, matching the known direction of BLS accuracy improvements. This provides external validation beyond synthetic corruption.

- **Kernelized extension to continuous spaces**: Definition 4.6 extends the score to arbitrary observation spaces via kernels, and the CIFAR-10 experiment (Experiment 2) demonstrates it working on 8-dimensional image embeddings, with ordering-preservation guarantees (deferred to Appendix F).

## Weaknesses

### Fatal
None.

### Major
None that threaten the paper's core claims.

### Minor

- **Missing baseline comparison in the main text**: The paper's closest related methods — determinant mutual information (Kong 2024, which directly inspired the Gram determinant) and Shannon mutual information (Zheng et al. 2025) — are discussed in related work but not empirically compared anywhere in the main text. While the conclusion states that Appendix G tests "additional candidates," this is not specified to include those directly comparable methods, and the main experimental section (Section 5) contains no baselines at all. The experiments only show that the Gram determinant score changes monotonically with corruption level — which any reasonable reliability score should do. Without a baseline comparison, the experiments cannot demonstrate whether the Gram determinant is *better* (more sensitive, more robust) than existing alternatives. This weakens the paper's empirical claims relative to the claims in the abstract ("effectively captures data quality").

- **Gap between theoretical guarantee and experimental regime for dist-ordering**: Theorem 4.2.3 guarantees $\alpha$-dist ordering preservation only under very tight corruption bounds ($\delta = 1/(64 L^2 d^2)$ Hamming distance bound), yet the synthetic experiments use corruption levels up to $p=0.5$ (50% corruption). For $d=5$ and $L\approx 1$, the bound allows roughly $\delta \approx 1/1600$ — far less than 0.5. The paper does not discuss whether the experimental conditions satisfy (or how far they exceed) the theoretical requirements. While the theoretical conditions are sufficient not necessary, the lack of any acknowledgment or analysis of this gap weakens the connection between theory and evidence.

- **Employment data sensitivity**: Experiment 3 discretizes month-to-month differences into four quantile buckets and reports only a single score with no sensitivity analysis. For a dataset of only $N=209$, results could be sensitive to bin boundaries.

### Trivial

- **Self-pair bias in plug-in estimator acknowledged but unquantified**: Definition 4.4's estimator sums over all pairs including $n=n'$, where $\mathbf{1}[y_n=y_n]=1$ deterministically while its estimand $\langle P_{x_n}, P_{x_n}\rangle < 1$. The paper notes this parenthetically ("if $n\neq n'$") but doesn't quantify the impact. For $N=4000$ (synthetic) and $N=10000$ (CIFAR-10), the bias is $\mathcal{O}(d/N) \approx 0.1\%$ of the determinant — negligible for ranking — but a brief note would clarify.

## Nice-to-Haves

- Adding a single baseline comparison (e.g., against Kong 2024's determinant mutual information on the synthetic data) would substantially strengthen the empirical case without requiring extensive new experiments.
- Testing with higher-dimensional CIFAR-10 projections (e.g., 64-d) to probe scaling behavior.
- A brief sensitivity analysis for the employment data discretization.

## Removed Points

**Removed** (partially inaccurate): The harsh critic's blanket claim of "no empirical baselines." The paper states in the conclusion that Appendix G tests additional candidates. However, the concern about missing comparison against the most closely related specific methods (Kong 2024, Zheng 2025) in the main text is valid and kept as a Minor weakness above.

**Removed** (parser artifact): References to garbled figure descriptions — these are PDF-parser artifacts, not author errors.

**Removed** (scope creep): Criticism about $\mathbf{Q}$ needing to be square (non-square $\mathbf{Q}$ breaks the factorization) — the paper explicitly works within the square-$\mathbf{Q}$ regime, which is a natural starting point.

**Removed** (addressed in paper): Scalability concerns — the conclusion explicitly discusses dimensionality reduction and DPP sampling as future work directions.

**Removed** (strawman): Criticism of Blackwell ordering's restriction to $\mathcal{Q}_{\text{reg}}$ — the paper explicitly discusses why this restriction is necessary for the ordering to be a strict partial order.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add a baseline comparison in the main experimental section.** The synthetic data experiment (Experiment 1) is a natural setting for a comparison against Kong (2024)'s determinant mutual information. Even a single figure showing both scores across corruption levels would substantially strengthen the empirical case.
2. **Explicitly discuss the gap between Theorem 4.2's corruption bound and experimental corruption levels.** A brief statement that the bound is sufficient but likely not necessary, or an empirical demonstration that the score works far beyond the bound, would help readers calibrate the theoretical contribution.
3. **Quantify the self-pair bias** in the plug-in estimator (e.g., "for N=4000 the relative bias is <0.2%") or run an ablation excluding self-pairs.
4. **Add a sensitivity analysis** for the employment data discretization.

## Score and Decision

I assign a score of **7** and a decision of **Accept**.

**Reasoning**: The paper makes genuine theoretical contributions — the problem formalization, impossibility results with near-tight bounds, the factorization leading to experiment agnosticism, and the uniqueness characterization are all novel and well-executed. For a theory-heavy paper, the experiments serve as sanity checks rather than rigorous empirical validation, which is acceptable for the theoretical contribution level. The primary weakness is the absence of baseline comparisons, which weakens the empirical claims but does not undermine the theoretical contributions. With the addition of baseline comparisons, this paper would be a solid accept.

**Anchors considered**: The calibration search tool was unavailable (corpus path issue), so I calibrated based on general ICLR reviewing standards: a paper with clean theory, near-tight bounds, and a uniqueness characterization at this score level typically receives between 6 and 8. The experimental limitations prevent an 8; the theoretical depth prevents a 6. A score of 7 appropriately reflects a paper that is above the borderline but has actionable empirical weaknesses.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>