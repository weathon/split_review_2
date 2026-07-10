The favorability scores are informative. Let me now produce the final consolidated review.

Key observations from the scoring feedback:
- All four strengths are rated highly (0.91–1.00), confirming the core contributions are solid
- The DRL/CONJ issue (0.24) and matched-OOD issue (0.29) are the most impactful weaknesses  
- The synthetic experiment point (0.00) and algorithm loop point (0.03) are flagged as very negative but are minor/trivial — I'll keep them at their appropriate severity
- Overall, strengths strongly outweigh weaknesses, and no weakness is fatal

## Summary

This paper introduces Medix, a median-centric framework for OOD detection that uses unlabeled wild data. The core idea is to filter outliers from a mixed wild dataset by finding a subset whose element-wise median (EWM) of gradients most closely matches the InD mean gradient, leveraging the median's robustness to contamination. The identified outliers are then used to train a binary OOD detector. The paper provides theoretical misclassification bounds for both inliers and outliers and demonstrates strong empirical results across CIFAR-10 and CIFAR-100 against 20 baselines.

## Strengths

- **Novel and well-motivated method:** The median-based filtering approach (Medix) is conceptually clean and well-articulated. The key insight—that the element-wise median of gradients is robust to outlier contamination, and that finding a wild-data subset whose median gradient matches the InD mean gradient recovers inliers—is supported by the preliminary experiment in Figure 1 showing monotonic deviation as OOD is added.

- **Rigorous theoretical analysis:** The paper provides formal misclassification bounds for both inliers (Theorem 4.1) and outliers (Theorem 4.2), decomposed into contamination, concentration, and separation effects. This is rare in the OOD detection literature for the in-the-wild setting. The paper also acknowledges a looser bound without sub-Gaussian assumptions (Theorem C.3, Appendix C.3), showing care.

- **Strong empirical results:** On CIFAR-10, Medix achieves average FPR95 of 0.80% vs. WOODS at 3.40% — a substantial improvement. On CIFAR-100, it achieves 5.42% vs. WOODS at 6.74%. Improvement is consistent across all five OOD test sets on both InD datasets.

- **Comprehensive evaluation:** The paper benchmarks against 20 baselines across multiple OOD datasets with variance reported over five runs for Medix.

## Weaknesses

### Fatal
None.

### Major

- **DRL and CONJ results absent from main tables despite explicit comparative claim:** The baselines section (page 6) lists DRL (Zhang et al., 2024) and CONJ (Peng et al., 2024) among methods compared, and the conclusion states Medix "outperformed state-of-the-art methods such as WOODS and DRL." However, neither DRL nor CONJ appears in the main results tables (Tables 1 and 2). The main paper's evidence does not directly support this specific comparative claim. [Verified: line 174 lists DRL/CONJ as baselines; line 262 claims outperformance over DRL; Tables 1 and 2 do not include DRL or CONJ entries.]

### Minor

- **Matched-OOD evaluation protocol limits the generality implied by "open-world" framing:** The main experimental protocol evaluates a matched-OOD setting where the OOD distribution in the wild data is the same as the test OOD distribution (e.g., wild data = CIFAR + SVHN, test OOD = SVHN). While this follows the established protocol of Katz-Samuels et al. (2022a), the abstract and introduction frame Medix's capability in terms of "open-world settings," which implies generalization to unseen OOD. The paper does address unseen OOD in Appendix A.4, but the main paper's claims are primarily supported by the matched-protocol results. [Verified: Section 5.1 describes the matched construction; Appendix A.4 is referenced for unseen OOD.]

- **Computational cost not discussed in the main paper:** Algorithm 1's greedy leave-one-out procedure as written requires recomputing the EWM gradient for each S\{i} at each iteration, which could be O(d·|S|²) per iteration. While the paper references efficiency evaluation in Appendix A.6, the main text provides no description of incremental median updates, wall-clock time, or whether the procedure is practical for larger wild-dataset sizes (e.g., 100K+ samples). [Verified: Algorithm 1 lines 5–7; Appendix A.6 reference at line 238.]

- **Percentage improvement reporting is ambiguous:** The paper states Medix "outperforming [KNN+] by an average of 40.98%" (abstract) and "reduces the FPR95 by 52.31% on PLACES365" (Section 5.3). From Table 2: KNN+ avg FPR95 = 46.40%, Medix = 5.42% → difference is 40.98 percentage points; KNN+ PLACES365 = 68.30%, Medix = 15.99% → difference is 52.31 percentage points. These are absolute differences, not relative percentages. "40.98%" without qualification is ambiguous. [Verified: Table 2 values; lines 27, 182, 262.]

- **Error bars missing for baselines:** Standard deviations are reported for Medix but not for any baseline method. For CIFAR-100, the gap between Medix (5.42% ± 0.37) and WOODS (6.74%) is 1.32 percentage points; on individual datasets gaps are very small (e.g., SVHN: 0.16% ± 0.02 vs. 0.17%). Without variance for the most relevant competitor, statistical significance is difficult to assess. [Verified: Tables 1 and 2 — Medix with ± values, baselines without.]

- **Synthetic experiment raises questions about error rate composition:** The synthetic data (Figure 2) places OOD data ~20 standard deviations away from InD clusters, making the problem extremely easy. Yet Medix achieves only 87.5% OOD recall (12.5% error rate). The paper acknowledges the experiment is "simple to facilitate better understanding," but does not explain what the 12.5% error rate consists of (false positives vs. false negatives) or contextualize the difficulty level. [Verified: Section 5.3 describes synthetic data with means separated by ~20 units with variance 0.25·I.]

### Trivial

- **Algorithm 1 loop condition ambiguity:** The condition "while t ≤ T or |δ_max| > ε" (line 2) is semantically ambiguous — "or" is unconventional for a convergence criterion (standard interpretation would be "and"). Additionally, δ_max is initialized to ∞ and updated at line 10 but checked at the beginning of the loop, making the first iteration's check trivial. [Verified: Algorithm 1 lines 2, 10.]

## Nice-to-Haves

- Ablation with extreme contamination ratios (π = 0 or π = 1) to test theoretical predictions.
- Sensitivity analysis of Medix's performance with respect to the quality of the initial InD classifier.
- Discussion of whether incremental median updates are used to make Algorithm 1 practical, and wall-clock time for a typical run.

## Removed Points
These points from the input review are flagged to be removed; treat them with caution:

- **Speculation about EWM greedy algorithm behavior (δ_i values being zero for many samples):** This is a plausible analytical observation but is speculative without empirical evidence and does not constitute a verified weakness of the paper as written.
- **Theory bound tightness criticism:** The reviewer acknowledges the paper does not claim tightness. The bounds are conservative by design, and the paper's theoretical contribution lies in the formal structure and relative behavior, not numeric tightness.
- **Missing Figure 4 in main paper:** This criticism concerns an appendix figure that is stripped by the parser; it exists in the original submission.
- **WOODS using 25K vs 50K training samples:** The paper explicitly acknowledges and explains this difference (Section 5.3, line 182).
- **Generic "evaluation lacks rigor" / "claims not fully supported" without specific anchor points:** Removed as insufficiently specific.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions

1. Add DRL and CONJ results to the main tables; if space is truly prohibitive, at minimum cross-reference the appendix clearly and temper the conclusion's claim about outperforming DRL unless supported in the main paper.
2. Clarify percentage reporting throughout: use "percentage points" or explicitly state "relative improvement" when reporting FPR95 reductions.
3. Include a brief computational cost discussion in the main paper — e.g., whether incremental median updates are used, typical wall-clock time, and how the method scales.
4. Add standard deviations for key baselines (particularly WOODS) to enable proper statistical significance assessment.
5. Explain the composition of the 12.5% error rate in the synthetic experiment (false positives vs. false negatives) and acknowledge the separation difficulty.
6. Make the unseen-OOD results more prominent, or qualify the "open-world" claims to accurately reflect that the primary evaluation uses the matched protocol.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>