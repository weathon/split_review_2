Now I will produce the final consolidated review.

## Summary

The paper studies offline change point localization and inference in dynamic multilayer random dot product graphs (D-MRDPGs). It proposes a two-stage algorithm combining seeded binary segmentation with low-rank tensor estimation (TH-PCA), establishes consistency for estimating the number and locations of change points, derives limiting distributions for the refined estimators (a novel result in network change-point analysis), and constructs data-driven confidence intervals. Experiments on simulations and a real-world agricultural trade network are presented.

## Strengths

1. **Novel problem formulation.** The paper formalizes offline change point detection in dynamic multilayer random dot product graphs, a setting not previously treated in the offline regime. The modeling choice of keeping latent positions fixed while allowing layer-specific weight matrices to change over time (Model 1) is well-motivated.

2. **Limiting distribution results.** Theorem 2 (vanishing-jump regime) and the associated confidence interval construction represent the paper's deepest theoretical contribution. Deriving the limiting distribution of change point estimators in a network setting, with the two-sided Brownian motion structure, is a non-trivial and genuinely significant statistical result that goes beyond existing single-layer and online-multilayer network literature.

3. **Two-stage algorithmic design.** Combining seeded binary segmentation (Stage I) with tensor-based low-rank refinement via TH-PCA (Stage II) is a sensible architecture, and the overall theoretical complexity analysis is provided.

## Weaknesses

### Fatal
None.

### Major

1. **Real-data confidence intervals are inconsistently centered.** In Table 4, for two of the four change points the reported 95% CI does not contain the detected point estimate: the 2005 change point (detected time index 20) has CI (17.97, 18.05) and the 2013 change point (detected time index 28) has CI (25.99, 26.06). While the CI formula [η̂_k − q_{1−α/2}/κ̂_k², η̂_k − q_{α/2}/κ̂_k²] can in principle produce intervals not centered at η̂_k (if both simulated arg-min quantiles lie on the same side of zero), this is a non-standard and potentially confusing property that is not acknowledged or explained in the paper. Together with the very narrow average CI lengths in Scenario 1 (0.003 on T=200, Table 2), these results raise questions about whether the variance estimation (Step 2 of Section 3.1) is properly calibrated. Since confidence interval construction is advertised as a core contribution, this warrants explanation or diagnostic evidence.

2. **Gap between theory and implementation on the independence assumption.** The theory (Theorems 1 and 2) and Algorithm 1 require *four mutually independent* adjacency tensor sequences {A(t)}, {A'(t)}, {B(t)}, {B'(t)}. The paper acknowledges (end of Section 2.2) that in practice—and in all experiments—it uses "the same two split tensor sequences via the odd-even splitting approach." No argument or evidence is provided that the theoretical guarantees (consistency rates, limiting distributions) survive this substitution. The independence structure is integral to the proofs (it enables Stage I CUSUM scanning and Stage II TH-PCA refinement to operate on independent data), so the gap is non-trivial.

### Minor

1. **Heuristic threshold selection with no data-driven procedure.** Theorem 1 requires the threshold τ to satisfy c_{τ,1} n√L log^{3/2}(T) < τ < c_{τ,2} κ²Δ, where κ is unknown. The paper sets τ = 0.1 n√L log^{3/2}(T) heuristically (Section 4.1) and reports a sensitivity analysis only in a deferred appendix. No practical guidance is given for choosing τ on new data, and no diagnostic is provided for whether the chosen value falls in the admissible range.

2. **The paired CUSUM operation used in Algorithm 1 is not formally defined.** Stage I (line 125) computes |(Ã^{α,β}(t), B̃^{α,β}(t))|—an inner product between two CUSUM tensors—but this operation is not explicitly defined in the paper (the notation section defines ⟨M, Q⟩ but not |(·,·)| with parentheses). While the intended meaning can be inferred, the connection between this paired statistic and the theoretical guarantees (which are stated for single-sequence CUSUM statistics) is unclear.

3. **Scenario 3 robustness claim is overstated.** In Scenario 3 (n=50), where Model 1 is violated, CPDmrdpg achieves |K̂−K| = 0.19 and d(Ĉ, C) = 9.64. The Hausdorff distance is an order of magnitude worse than kerSeg (nets.), which scores 0.18. The paper's claim of "remaining robust even when Model 1 is violated" overstates the evidence for this particular setting.

### Trivial
None.

## Nice-to-Haves
- Provide a formal or heuristic justification, or simulation evidence, that the odd-even split preserves the approximate independence needed for the theoretical guarantees.
- Develop a data-driven threshold selection procedure (e.g., permutation-based or simulation-based calibration), or demonstrate that results are robust across a wide range of τ values in the main text.
- Report actual runtimes in addition to theoretical complexity.
- For the real-data analysis, explain why the CIs for the 2005 and 2013 change points are centered away from the detected time points.

## Removed Points
These points are flagged to be removed; treat them with caution:

- **Main experimental comparison is staged / relevant competitors hidden in appendix.** The paper states comparisons with Wang et al. (2025) and Li et al. (2024) are in Appendix G.1. The parser strips appendices from all papers; these exist in the original submission. Removed per parser-artifact rule.
- **Non-vanishing jump regime deferred to Appendix A.** The paper explicitly scopes its main theoretical contribution to the vanishing regime. This is a deliberate scope choice, not a flaw.
- **Δ=Θ(T) assumption bounds K to a constant.** The paper acknowledges this can be relaxed (Section 5). Removed as the paper already addresses it.
- **"First of its kind" claims repeated.** Presentation nitpick without substance.
- **Typo in CUSUM weight function notation.** Parser/formatting artifact per rules.
- **T=200 is a modest time horizon.** The paper allows all parameters to diverge with T; T=200 is a reasonable simulation budget for the proposed experiments.
- **Malformed formula for C(G, G').** Likely parser artifact from PDF extraction.
- **"Inf" entries in Table 1 are uninformative.** They show gSeg frequently fails to detect any change points, which is itself informative.
- **Missing related works.** Per rules, do not mention missing related works without external sources to verify.
- **Reproducibility concerns about hyperparameters or training logs.** Per rules, disconnect unless essential details are missing.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Investigate and explain the behavior of the confidence interval procedure, particularly why CIs can be centered away from the detected change points and whether the variance estimates in Step 2 of Section 3.1 may be biased downward.
2. Bridge the four-sequence gap: provide a heuristic justification, simulation evidence, or a modified algorithm that operates with a single pair of sequences while preserving the theoretical guarantees.
3. Provide practical guidance for threshold selection in the main text, or demonstrate that performance is robust across a wide range of τ values.
4. Formally define the paired CUSUM statistic used in Algorithm 1 and clarify how it connects to the theoretical analysis.

Score round to .5 or .0.

Let me now assign the final score based on calibration.

**Round 1 bracket**: After comparing with the calibration anchors, I identified that papers with similar methodology (change point detection with theory + experiments, e.g., I5MquO1g7R at avg 4.75) and similar application domains (multilayer networks, e.g., vjHCyOWc7h at avg 4.40) cluster around 4.0–5.5. The current paper has stronger theoretical novelty than these anchors but also has more significant concerns about its CI calibration claim (a core contribution). The most similar paper in terms of theoretical ambition—deriving limiting distributions for change point estimators—does not have a direct analogue in the calibration set, but the paper with the closest statistical-theory profile (QtJiPhnsqV, avg 5.00, Reject) was rated 5.0. I bracket the paper at 3.5–5.5.

Based on the calibration search, I anchor the final score by comparing against:

| Anchor Paper | Avg Score | Round | Comparison |
|---|---|---|---|
| I5MquO1g7R (Change Point Detection via TV-HMM) | 4.75 | R1 | Similar structure (algorithm + theory + experiments), but weaker theory and less serious CI concerns; rejected. Current paper has stronger theory but a more significant calibration issue in its core CI contribution. |
| vjHCyOWc7h (Mixture SBM for Multiplex Graphs) | 4.40 | R1 | Multilayer network paper with theoretical guarantees; rejected mainly for insufficient baselines and limited experiments. Current paper has stronger theoretical novelty. |
| Frok9AItud (Node Similarities under Random Projections) | 5.80 | R1 | Strong theoretical paper on graph embeddings; accepted. Current paper has comparable theoretical depth but the CI calibration issue is a concern that the anchor did not face. |
| QtJiPhnsqV (Inferences on Covariance Matrix) | 5.00 | R2 | Statistical inference paper with asymptotic normality results; rejected. Similar profile of theory + CIs, but the anchor's weaknesses were about presentation and limited scope rather than calibration validity. |

The paper's theoretical results (limiting distributions for network change points) are genuinely novel and represent a meaningful contribution. However, the CI calibration concerns and the theory-practice gap are significant issues that affect the core claimed contributions. The paper is stronger in theory than the typical 4.5 reject, but the CI implausibility (a claimed contribution, not a secondary feature) prevents it from reaching the 6.0 accept threshold. A score of 4.5 reflects this: the paper has real contributions but needs substantive revisions before acceptance.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>