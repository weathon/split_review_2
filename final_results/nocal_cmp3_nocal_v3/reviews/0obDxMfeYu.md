## Summary
The paper proposes Medix, a median-based framework for OOD detection that filters potential outliers from unlabeled "in-the-wild" data. The method uses element-wise median (EWM) of gradients to identify OOD samples from a mixed wild dataset, then trains a binary OOD detector on the identified outliers plus labeled InD data. The paper provides theoretical bounds on misclassification rates (Theorems 4.1, 4.2) and demonstrates strong empirical results across 11 InD-OOD pairs, outperforming 20 baselines including WOODS and KNN+.

## Strengths
1. **Novel median-based filtering approach with theoretical guarantees.** The paper is one of the few works providing formal error bounds for OOD detection with wild data (Theorems 4.1, 4.2). The sub-Gaussian assumption is tested empirically (Remark 4.3, Figures 4a/4b), and a looser bound without it is provided (Theorem C.3). This theoretical grounding is rare in the OOD-with-wild-data literature.

2. **Strong and consistent empirical results (Tables 1 and 2).** On CIFAR-10, Medix achieves average FPR95 of 0.80% and AUROC of 99.74%, substantially beating WOODS (3.40%, 98.92%) and all 20 baselines across every OOD dataset individually. On CIFAR-100, average FPR95 of 5.42% improves over WOODS (6.74%). Standard deviations over 5 runs are reported and are small. The improvement is consistent across nearly all InD-OOD pairs.

3. **Clean motivating experiment linking empirical observation to algorithm design.** Section 3.1 (Figure 1) demonstrates monotonic increase in L2 deviation between the average InD gradient and the EWM of wild data gradients as OOD samples are added, directly motivating the optimization problem in Equation 4 and the stopping criterion of Algorithm 1.

## Weaknesses

### Fatal
None.

### Major
1. **The theoretical bounds are near-vacuous at the contamination level used in the main experiments (π = 0.5), creating a gap between the theory and the empirical evaluation.** Theorem 4.1 gives an inlier misclassification bound with a contamination term π/[2(1-π)]. At π = 0.5, this term equals 0.5; with typical sample sizes the full bound evaluates to ~0.52—barely above random guessing (50%). The paper explicitly states the bound is controlled "as long as the contamination ratio π < 0.5" (line 138), but the main experiments (Section 5.3) all use π = 0.5 as the default (line 170). No experiments are run at lower π values (e.g., 0.1, 0.2, 0.3, 0.4) where the bound would be informative. The theory provides insight into *why* median filtering is robust in principle, but as presented it does not offer tight support for the specific experimental configuration. This is not fatal—the empirical results stand on their own—but the claimed theoretical validation of the experiments is weaker than stated.

### Minor
2. **The separation condition assumed in Theorem 4.2 is not empirically validated.** The theorem assumes OOD gradients in the wild are i.i.d. sub-Gaussian with a mean μ_out satisfying ║μ_out − ∇̄_in║₂ ≥ Δ√d. However, the paper computes gradients for wild samples using *predicted* labels ŷ over K InD classes (lines 83, 91). For OOD samples, these predictions could be essentially arbitrary, and the paper does not characterize when the separation condition holds in practice. No empirical evidence (e.g., measuring the observed separation on real data) is provided to validate this core assumption.

3. **The main evaluation matches the OOD distribution in the wild data to the OOD test distribution.** Following the WOODS protocol (line 170), when testing on PLACES365, the wild mixture also uses PLACES365. The paper mentions an "unseen OOD" evaluation in Appendix A.4, but the headline results (Tables 1 and 2) all use the matched setting. The degree to which results generalize to unmatched settings (the more realistic scenario) is not given equal prominence.

4. **Computational cost of the filtering stage is not discussed in the main text.** Algorithm 1's leave-one-out approach per iteration has complexity that scales with the number of wild samples and gradient dimension, and hyperparameter k is selected from {4k, 7k, 10k, 20k}—values large enough that the algorithm may remove most wild data in 1–2 iterations, barely exercising the iterative mechanism. The main text defers efficiency details to Appendix A.6 without giving a rough order-of-magnitude runtime.

5. **Gradient computation details are underspecified.** The paper states it uses "penultimate layer weights" for gradient computation (line 170) but does not specify whether these are gradients w.r.t. the weights of the penultimate layer or gradients w.r.t. the penultimate layer's *activations*—a distinction important for reproducibility.

### Trivial
6. **Ambiguous phrasing of the FPR95 improvement claim.** The paper states Medix "outperforming [KNN+] by an average of 40.98% in terms of FPR95" (lines 27, 262), but this is 40.98 *percentage points* absolute reduction (from 46.40% to 5.42%), not 40.98% relative improvement. This should be clarified.

7. **Undefined notation m_min in Theorem 4.1.** The theorem uses m_min in the definition of ε and in the bound's concentration term, but its relationship to m_in and m_out is not explained in the main text (presumably min(m_in, m_out), but this should be explicit).

## Nice-to-Haves
- Run experiments at multiple contamination levels π ∈ {0.1, 0.2, 0.3, 0.4} to allow the theory (meaningful at π < 0.5) to directly support the experiments.
- Empirically measure the separation Δ assumed in Theorem 4.2 for each InD-OOD pair used.
- Report the number of iterations Algorithm 1 actually takes with the chosen k values.
- Add a brief complexity analysis (rough runtime in minutes on an A100) to the main text.

## Removed Points
The following points from the input review were assessed and removed per the filtering rules:
- Criticisms about missing related work (cannot be verified externally).
- The suggestion to contrast batch-level vs dataset-level mixing earlier in the Introduction (presentation suggestion, not a weakness).
- The comment about no formal analysis of the greedy-to-optimal gap (moved to Nice-to-Haves as it is scope-creep for an empirical systems paper that already provides strong results).
- Criticisms duplicating those already listed in the main weakness sections (merged).

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Add experiments at π < 0.5 to directly demonstrate the regime where the theoretical bounds are tightest.
2. Empirically characterize the OOD gradient structure (measure Δ for each InD-OOD pair) to bridge the gap between Theorem 4.2's assumptions and the experimental validation.
3. Clarify the "40.98%" claim as absolute percentage-point reduction rather than relative improvement.
4. Define m_min explicitly in the statement of Theorem 4.1.
5. Specify whether gradients are computed w.r.t. penultimate-layer weights or activations.
6. Report wall-clock time and iteration count for the filtering stage in the main text.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>