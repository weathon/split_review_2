Now I have all the calibration information I need. Let me produce the final consolidated review.

## Summary

This paper introduces Medix, a framework that uses the element-wise median (EWM) of gradients to filter candidate OOD samples from unlabeled wild data, then trains a binary OOD detector on the identified outliers plus labeled InD data. The paper provides two-sided theoretical bounds on inlier and outlier misclassification rates and reports strong empirical results across 5 OOD test sets on CIFAR-10 and CIFAR-100 against 20 baselines.

## Strengths

1. **Two-sided theoretical bounds with interpretable structure (Theorems 4.1, 4.2).** The paper derives clean upper bounds on both inlier and outlier misclassification for median-based filtering, decomposed into contamination effects (π/[2(1−π)] and (1−π)/(2π)), concentration effects decaying as O(1/√m), and an exponential separation term for outliers. The π < 0.5 robustness threshold is analytically derived. These are among the few theoretical treatments of the wild-OOD setting (alongside Du et al., 2024a).

2. **Consistent and substantial empirical gains across all OOD test sets (Tables 1, 2).** Medix achieves the best FPR95 and AUROC among all 20 baselines on every InD-OOD pair. On CIFAR-10, average FPR95 is 0.80% (vs WOODS 3.40%, a ~76% relative reduction). On CIFAR-100, average FPR95 is 5.42% (vs WOODS 6.74%, a ~20% relative reduction). Standard deviations over 5 runs are small (FPR95 std 0.01–0.75).

3. **Motivating experiment (Figure 1) grounds the algorithm design.** The monotonic increase in EWM deviation as OOD samples are added provides empirical support for the core hypothesis and directly motivates the algorithm's convergence criterion.

## Weaknesses

### Fatal
None.

### Major

1. **Theory-algorithm gap: Theorems 4.1 and 4.2 bound an unspecified "EWM filtering rule" with no formal connection to Algorithm 1.** The bounds depend on population-level parameters (π, σ, m_in, m_out, Δ) and do not involve the algorithm's hyperparameters (k, ε), its greedy leave-one-out selection rule, its convergence criterion, or any approximation error introduced by the sequential procedure. The paper states "we now present the theoretical guarantees of Medix's filtering stage" (Section 4) and the introduction claims "a theoretical foundation that guarantees minimal error," but the theorems never reference Algorithm 1 or account for its greedy dynamics. The algorithm removes k samples per iteration based on local δ_i values, which could diverge from the idealized rule that the theorems analyze. The paper must either prove that Algorithm 1 achieves these bounds, characterize the gap between the idealized rule and the greedy procedure, or clearly delineate which aspects of the method are theoretically justified.

2. **Missing comparison with the closest prior work, Du et al. (2024a).** Du et al. (2024a) also uses unlabeled wild data for OOD detection, provides theoretical guarantees, and explicitly filters outliers from the wild mixture — the same two-stage structure Medix adopts. Medix even follows Du et al.'s detector training protocol for Stage 2. Yet Du et al. (2024a) does not appear in Tables 1 or 2. The paper mentions in related work that Du et al.'s "thresholding technique differs fundamentally from ours," but without an empirical comparison, the reader cannot evaluate whether Medix's median-based filtering offers a practical advantage over the thresholding approach. This omission undermines the claim of comprehensive comparison against 20 baselines.

### Minor

1. **Matched OOD evaluation setting.** As described in Section 5.1, the wild OOD data and the test OOD data are drawn from the same distribution (e.g., PLACES365 is used both in the wild mixture and as the OOD test set). This allows the detector to learn distribution-specific features rather than general OOD-ness. The paper acknowledges this limitation and provides unseen-OOD experiments in Appendix A.4, but the headline claims and Tables 1–2 all rely on the matched setting. Following the standard protocol of Katz-Samuels et al. (2022a) mitigates this concern but does not eliminate it.

2. **Greedy algorithm optimization is unanalyzed.** Algorithm 1 removes k samples per iteration based on leave-one-out δ_i values that depend on the EWM of the remaining samples. Earlier removal decisions affect later δ_i values, creating path-dependence. The algorithm could converge to a local optimum far from the global optimum of Eq. 4, especially with large k. The paper does not analyze this behavior or provide recovery guarantees.

3. **Synthetic experiment (Figure 2) uses an extremely easy separation.** The OOD mean is placed at [20, 2√3] while the nearest InD class mean is at [0, 2√3] — a 20-unit gap in the x-coordinate with covariance 0.25I. The 87.5% extraction rate on this toy 2D setting provides limited evidence for the method's mechanism on high-dimensional real data. The paper explicitly states this is "designed to be simple to facilitate better understanding," so this is a minor concern about presentation weight rather than a flaw in the main results.

### Trivial

- Slightly lower InD accuracy on CIFAR-100 (73.33% vs WOODS 73.91%), acknowledged by the paper as due to using 25,000 labeled InD samples versus the 50,000 used by InD-only baselines.

## Nice-to-Haves

- Empirical validation of the dataset-level vs. batch-level mixing advantage claimed in related work (Section 6). The paper contrasts Medix's dataset-level mixing with the batch-level assumption of Katz-Samuels et al. (2022a) and Du et al. (2024a) but does not directly compare against these methods under batch-level mixing to substantiate the claimed advantage.
- Per-sample gradient distribution plots on real (not synthetic) data to directly validate whether the separation assumption in Theorem 4.2 (‖μ_out − ∇̄_in‖₂ ≥ Δ√d) is empirically satisfied.
- Sensitivity analysis for π values beyond the default 0.5 (e.g., approaching or exceeding the 50% threshold) to directly test the theory's bound.

## Removed Points

These points are flagged to be removed; treat them with caution.

- *Harsh critic's claim that theoretical bounds are "standard" and "not novel":* This is a judgment assertion, not a verifiable weakness. The bounds are specific to the median-based wild-OOD setting and are among few such treatments. The critique adds no concrete, verifiable information about the paper's content.
- *"Figure 1 is not surprising":* A dismissive observation, not a concrete weakness. The experiment serves its stated motivating purpose.
- *"Improvement on CIFAR-100 is modest":* 5.42% vs 6.74% FPR95 is a ~20% relative improvement. Characterizing this as "modest" is subjective and not a substantive weakness.
- *Criticism about the optimization objective (Eq. 4) not guaranteeing separation:* The paper uses hedged language ("may well represent") and the theory bounds the error. The criticism overstates what the paper claims.
- *Formatting/style nitpicks, missing appendix content, pure speculation about missing proofs:* These reflect parser artifacts or reviewer knowledge gaps, not author errors.
- *Strength finder's generic strengths* (e.g., "paper addresses an important problem"): Removed for being superficial/sycophantic. Only concretely evidenced strengths are retained.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Connect the theory to Algorithm 1.** Either prove that the greedy procedure achieves the stated bounds, characterize the gap between the idealized rule and the algorithm, or clearly delineate what the theorems guarantee vs. what is heuristic.
2. **Include Du et al. (2024a) in the main comparison.** This is the most directly comparable prior work and its absence is a significant gap. If direct comparison is infeasible (e.g., due to differing mixing assumptions), explain why clearly.
3. **Elevate unseen-OOD results (currently Appendix A.4) to the main paper.** The matched-setting results alone are insufficient to demonstrate that Medix learns general OOD-ness rather than distribution-specific features.
4. **Add an analysis of the greedy algorithm's convergence behavior and sensitivity to k.** Provide wall-clock time and scaling behavior rather than a footnote to the appendix.

## Calibration Anchors

**Round 1 bracket:** 5.0 – 7.0 (narrowed from initial bracketing)
**Final score:** 6.0

Anchors retrieved:
- *Du et al. (2024a) — How Does Unlabeled Data Provably Help OOD Detection?* (avg 6.5, accept). Same problem setting (wild OOD), two-stage framework, theoretical guarantees + strong empirics. Medix has a larger theory-algorithm gap and omits Du et al. from its comparison, making it slightly weaker. Score 6.0 vs 6.5.
- *GM Matching for Robust Data Pruning* (avg 3.0, reject). Also uses median-based approach with theory + CIFAR experiments. Medix has substantially more comprehensive experiments (20 baselines vs 3) and a more novel application domain (OOD detection vs data pruning). Score 6.0 vs 3.0.
- *Pathologies of OOD Detection* (avg 4.75, reject). Critique paper without new method. Not directly comparable.
- *ImageNet-OOD* (avg 6.5, accept). Benchmark/dataset paper. Different contribution type.
- *Provably Safeguarding a Classifier from OOD* (avg 5.5, accept). Different approach (extreme value theory). Medix has stronger empirics.
- *Gradient norm as a powerful proxy to OOD error estimation* (avg 5.5, reject). Similar gradient-based approach but different objective. Medix has stronger results and cleaner theory.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>