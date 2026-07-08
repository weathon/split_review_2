## Summary

This paper introduces Medix, a median-centric framework for OOD detection that filters potential outliers from unlabeled "in-the-wild" data using element-wise median (EWM) of gradients. The method greedily removes samples whose absence maximally reduces the L₂ distance between the EWM of wild-data gradients and the mean InD gradient. The paper provides two-sided theoretical misclassification bounds (Theorems 4.1 and 4.2) and evaluates against 20 baselines across two InD datasets and five OOD datasets, reporting strong empirical results.

## Strengths

- **Two-sided theoretical guarantees (Theorems 4.1 & 4.2).** The paper bounds both inlier and outlier misclassification rates for the filtering stage, decomposing them into contamination, concentration, and separation effects — a genuine contribution to a literature that is largely empirical. The acknowledgment of a looser bound without sub-Gaussian assumptions (Theorem C.3) shows intellectual honesty. [weight=7.20]

- **Comprehensive empirical evaluation (Tables 1 & 2).** Medix is compared against 20 baselines — including both InD-only methods (MSP, ODIN, Mahalanobis, Energy, KNN+, ASH, etc.) and methods leveraging wild/auxiliary data (OE, WOODS, CONJ, DRL) — across five OOD datasets for both CIFAR-10 and CIFAR-100. Results are consistently strong and reported with standard deviations. [weight=6.81]

- **Well-motivated and clearly explained mechanism.** The core insight — that adding OOD samples shifts the element-wise median gradient away from the InD mean gradient, and that greedily removing samples causing the largest per-sample drop in this distance isolates outliers — is clearly presented, with preliminary experimental support (Figure 1) grounding the optimization objective (Equation 4). [weight=8.60]

- **Two-sided theoretical framing.** Rather than only bounding false positive identification of InD samples as outliers, the paper also bounds false negative retention of OOD samples (Theorem 4.2), giving a balanced characterization of the filter's reliability. [weight=8.73]

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **Computational cost of Algorithm 1 is not analyzed in the main text.** The greedy algorithm requires computing the element-wise median after removing each candidate sample at every iteration. For a wild set of 25,000 samples and penultimate-layer gradients of dimension ≥128, the per-iteration cost is substantial. The paper acknowledges the optimization is "computationally prohibitive" (Section 3.1) and defers to Appendix A.6 for efficiency analysis, but the main body lacks even a big-O complexity statement or wall-clock runtime for the reported dataset sizes. Readers cannot assess whether the method is practical at the claimed scale without consulting deferred appendices. [weight=6.38]

- **The "40.98% improvement" claim is an absolute difference, not a relative improvement.** In Section 1: "outperforming [KNN+] by an average of 40.98% in terms of FPR95." From Table 2, KNN+ averages 46.40% FPR95 and Medix averages 5.42%. The difference is 40.98 percentage points, not 40.98% relative improvement (which would be ~88.3%). This phrasing recurs in the conclusion. While FPR95 improvements are commonly reported as absolute differences in the OOD detection literature, "outperforming by X%" conventionally implies relative improvement, creating ambiguity. [weight=5.89]

- **The theoretical separation condition in Theorem 4.2 is not empirically validated.** The bound requires ‖μ_out − ∇̄_in‖₂ ≥ Δ√d for the OOD mean gradient, but the paper does not measure this separation on any real dataset pair. The sub-Gaussian assumption is validated for InD gradients only (Remark 4.3, Figure 4), leaving the OOD-side assumption and the separation condition unverified. The looser bound (Theorem C.3) relaxes sub-Gaussianity but not the separation condition. [weight=3.70]

- **The motivation experiment (Figure 1) and synthetic example (Figure 2) use unrealistically easy settings.** Figure 1 uses CIFAR-10 vs. SVHN — two highly distinct distributions. Figure 2 places OOD mean at >30 standard deviations from the nearest InD cluster (covariance 0.25I), making the reported 87.5% outlier recall expected rather than impressive. A near-OOD pair (e.g., CIFAR-10 vs. CIFAR-100) would provide a more informative test of the method's sensitivity. [weight=4.49]

### Trivial

- **The while-loop condition in Algorithm 1 uses 'or' logic, making ε a pre-T stopping criterion only.** The loop runs while `t ≤ T or |δ_max| > ε`, meaning it only exits when *both* conditions are false. Convergence before T is triggered by ε, but otherwise the loop runs exactly T iterations. The logic is not incorrect but could be clarified. [weight=4.18]

- **Notation in Section 4 could be stated more explicitly.** The quantities m_in, m_out, and m_min in the bounds are not explicitly defined in the main text (they denote the counts of InD, OOD, and the smaller of the two, respectively). [weight=7.26]

## Nice-to-Haves

- Provide a big-O complexity bound for Algorithm 1 and/or wall-clock runtime for the filtering stage at the reported dataset sizes (25,000 wild samples) in the main text.
- Move the unmatched OOD evaluation (Appendix A.4, where P_out^wild ≠ P_out^test) to the main body, since this setting is more relevant to the open-world claims.
- Measure and report ‖μ_out − ∇̄_in‖₂/√d for the dataset pairs used, to directly validate the separation condition in Theorem 4.2.
- Compare against a simpler baseline that applies a standard OOD scoring function (e.g., energy score, Mahalanobis distance) directly on the wild set with a fixed threshold, to isolate the benefit of the iterative median-based removal.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"Evaluation design uses matched OOD setting (P_out^wild = P_out^test)"** → Removed because this is the standard experimental protocol established by Katz-Samuels et al. (2022a) that all baselines are evaluated under. The unmatched evaluation exists in Appendix A.4. This is not a flaw unique to Medix.
- **"Greedy algorithm complexity is a structural/fatal concern"** → Downgraded from a critical issue to Minor. The paper explicitly acknowledges the computational challenge (Section 3.1) and defers details to Appendix A.6. Without access to the (stripped) appendix, we cannot judge whether the analysis there is adequate.
- **"Batch-level mixing claim in Related Work not substantiated"** → Removed. The paper explains the distinction: "where each batch has a set ratio of InD and OOD samples" (Section 6). The explanation, while brief, is present.
- **"No limitations section / failure case discussion"** → Removed. Not a standard requirement for all papers, and the paper does address some assumptions (e.g., sub-Gaussian validation, looser bounds without it).
- **"Missing comparison to simple percentile-based gradient-norm baseline"** → Moved to Nice-to-Haves. This is a suggestion, not a flaw of the current submission.
- **"Choice of k not justified theoretically"** → Removed. Hyperparameter selection from a candidate set with sensitivity analysis in the appendix is standard practice.
- Strengths removed: None kept that conflicted with verified weaknesses. All kept strengths are specific and evidence-grounded.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Revise the FPR95 improvement claim (Sections 1 and 7) to read "40.98 percentage points lower FPR95" or state the relative improvement explicitly alongside the absolute difference.
2. Add a brief complexity analysis of Algorithm 1 in the main text (e.g., O(d·|S|²) per iteration, or note the incremental median update strategy used).
3. Measure and report the empirical separation ‖μ_out − ∇̄_in‖₂/√d for each InD-OOD pair to validate Theorem 4.2's condition.
4. Clarify the convergence logic of Algorithm 1's while-loop (explain that ε only enables early stopping before T).
5. Consider including a near-OOD pair in the motivation experiment (Figure 1) to demonstrate the method's sensitivity under harder distributional shifts.

## Score and Decision

### Calibration Anchors

| Anchor | Path | Avg Human Score | Round | Itemized | Comparison |
|--------|------|----------------|-------|----------|------------|
| SAL (Du et al. 2024a) | jlEjB8MVGa.md | 6.50 | 1 | Yes | Most directly comparable: same problem setting (wild OOD detection), two-stage pipeline, theory + empirical. Medix has more baselines (20 vs fewer) and no severely negative weakness weights, but similar unvalidated assumptions. |
| HamOS | N6ba2xsmds.md | 6.75 | 2 | Yes | Different approach (synthetic outliers) but same problem area. Accepted at ICLR. Medix has a comparable profile of strengths and weaknesses. |
| Deep NNs Extrapolate Predictably | ljwoQ3cvQh.md | 7.00 | 2 | Yes | Strong empirical + theoretical paper with no major weaknesses. Medix has more actionable weaknesses by comparison. |
| Guaranteed OOD (ProMix) | voVjW1PT2c.md | 6.00 | 1 | Yes | Had novelty concerns (-2.73 weight) and missed theory validation. Medix is stronger than this by comparison. |
| Pathologies of OOD | hlijRgXTDK.md | 4.75 | 1 | No | Critical/analysis paper, not comparable methodology. |
| Double Descent OOD | eN0RyRVbSm.md | 6.50 | 2 | No | Different framing (model complexity). Medix is comparable in score range. |
| ImageNet-OOD | VTYg5ykEGS.md | 6.50 | 2 | No | Benchmarking/analysis paper. |
| Dealing with OOD (tabular) | i28ZjVxl81.md | 2.50 | 1 | No | Weak paper on OOD detection. Medix is clearly stronger. |

### Bracket and Score

**Round 1 bracket:** [6.0, 7.5] — based on comparison with SAL (6.50) and ProMix (6.00) as lower bounds, and HamOS (6.75) and "Deep NNs Extrapolate" (7.00) as upper bounds.

**Round 2 narrowing:** Anchors at 6.50 (SAL) and 6.75 (HamOS) were itemized and compared. Medix's strengths have weights (max 8.73) comparable to SAL's (max 9.45), and Medix's weaknesses have a minimum weight of 3.70 (versus SAL's -1.82). This absence of strongly negative items places Medix slightly above SAL. However, the computational cost concern and unvalidated separation assumption prevent it from reaching the 7.0+ level of the "Deep NNs Extrapolate" paper.

**Final score:** 6.5 / 10 — Medix makes a clear, novel contribution (median-based filtering with theoretical guarantees) backed by a thorough baseline comparison. The weaknesses are presentational and analytical gaps rather than fundamental flaws. The paper would benefit from moving the unmatched OOD evaluation and runtime analysis to the main text and clarifying the performance claims.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>