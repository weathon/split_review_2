## Summary

The paper proposes Medix, a framework that uses element-wise median (EWM) of gradients to filter outliers from unlabeled wild data mixtures for OOD detection. It provides theoretical bounds on misclassification rates under sub-Gaussian assumptions and demonstrates strong empirical results, outperforming WOODS on CIFAR-10 (average FPR95 0.80% vs 3.40%) and CIFAR-100 (5.42% vs 6.74%).

## Strengths

1. **Conceptual novelty of median-based filtering.** The core idea—using the element-wise median of gradients to separate InD from OOD samples in unlabeled wild data—is genuinely novel in OOD detection. The intuition that the median is robust to contamination as long as OOD proportion stays below 50% is clean and well-motivated.

2. **Monotonicity experiment (Section 3.1, Figure 1).** A simple motivating experiment shows the L₂ distance between the InD mean gradient and the EWM of wild gradients increases monotonically as OOD samples are added, grounding the optimization in Equation (4).

3. **Strong empirical results on CIFAR-100 (Table 2).** Medix achieves average FPR95 of 5.42% compared to WOODS's 6.74%, with consistent improvement across all five OOD datasets. Results are reported with standard deviations over five runs.

4. **Near-perfect results on CIFAR-10 (Table 1).** Average FPR95 of 0.80% with very low variance, outperforming all baselines on every OOD dataset.

5. **The theory captures the median's core robustness property.** The contamination term π/[2(1-π)] in Theorem 4.1 formally captures why the median is robust when π < 0.5, and the recognition that looser bounds hold under only bounded second moments (Theorem C.3) shows awareness of the assumption's scope.

## Weaknesses

### Fatal
None.

### Major

1. **Theory-algorithm disconnect.** Theorems 4.1 and 4.2 bound misclassification rates for what is called "the EWM filtering rule," but this rule is never precisely defined. The paper acknowledges (line 93) that the optimization in Equation (4) is "computationally prohibitive" and Algorithm 1 is a "greedy approximation." However, the theoretical section never analyzes the approximation gap, accounts for the iterative greedy removal of k samples per step, models the convergence criterion, or explains how the bounds degrade under the greedy procedure. As a result, the paper credibly claims theoretical backing for its method, but the theory analyzes a different (static, one-shot) procedure than the one evaluated in experiments (iterative, greedy Algorithm 1). This disconnect means the reader cannot determine whether the formal guarantees apply to the method that produced the reported results.

2. **Missing DRL and CONJ baseline results.** The conclusion (line 262) states Medix "outperformed state-of-the-art methods such as WOODS and DRL." DRL (Zhang et al., 2024) and CONJ (Peng et al., 2024) are listed in the baselines (Section 5.1) but their results do not appear in Tables 1 or 2. The paper asserts superiority over these methods without presenting their results to the reader.

### Minor

3. **Synthetic outlier extraction experiment (Figure 2) is trivially easy.** The OOD cluster mean is at [20, 2√3] while the nearest InD class center is at [0, 2√3] ≈ [0, 3.46], separated by a distance of ~20. With covariance 0.25·I (std=0.5), this is approximately 40 standard deviations. Any reasonable detection method would achieve near-perfect separation. The reported 12.5% error rate on such trivially separable data does not provide meaningful evidence of robustness.

4. **Pseudo-label dependence not analyzed.** Equation (4) and Algorithm 1 compute gradients for wild samples using predicted labels (ŷ) from the InD classifier. For genuinely OOD samples, this predicted label is essentially arbitrary. The paper defers analysis to Appendix A.5 (not available in the submission) and the claim of being "resilient to noisy or low-confidence labels" addresses a different issue (label noise) rather than the core concern that OOD samples have no correct label in the label space 𝒴. The theory in Theorems 4.1/4.2 does not model this effect.

5. **Main evaluation uses ℙ_out^wild = ℙ_out^test.** Section 5.1 states wild data is constructed by combining InD data with the same distribution used for OOD testing. While this follows the WOODS protocol and makes comparisons fair, the abstract's claim of "open-world settings" overstates the generality. The unmatched setting (ℙ_out^test ≠ ℙ_out) is deferred to Appendix A.4 and not shown in the main paper.

### Trivial

6. **The 40.98% improvement figure is an absolute difference.** From Table 2, this is 46.40 − 5.42 = 40.98 percentage points. The relative reduction is ~88.3%. Stating it as "40.98%" without clarification inflates the perceived gain.

## Nice-to-Haves
- Include DRL and CONJ results in the main tables to substantiate claimed outperformance.
- Move the ℙ_out^test ≠ ℙ_out results to the main paper if favorable, or revise the abstract to reflect the actual evaluation scope.
- Add wall-clock time comparison with baselines (computational cost characterization).
- Ablate the greedy iterative procedure against simpler alternatives (single-shot removal, random removal, oracle).

## Removed Points
These points are removed from the input review but kept for reference:
- **Computational cost as O(|S|·d·log|S|).** Removed because the complexity analysis may itself be approximate; deferring to Appendix A.6 is standard practice.
- **While-loop condition `or` inconsistency.** Removed as a minor presentation detail; the described behavior is functionally correct.
- **Sub-Gaussian not validated for OOD gradients.** Removed because Remark 4.3 validates for InD, and Theorem C.3 provides looser bounds under bounded second moments.
- **Hyperparameter overfitting concern.** Removed as speculative; no evidence presented of overfitting to specific OOD sets.
- **Du et al. (2024a) already provides theory.** Removed; a paper can be "one of the few" even with one prior work.
- **General evaluation rigor concerns.** Removed as speculative without concrete anchors in the paper.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Either extend the theoretical analysis to cover Algorithm 1 directly (bounding the greedy iterative procedure), or clearly define and evaluate the static EWM filtering rule that the theorems analyze, and report the empirical gap between the two.
2. Include DRL and CONJ results in the main tables.
3. Provide a more informative synthetic experiment where the separation is nontrivial.
4. Discuss how the use of pseudo-labels for OOD samples affects gradient informativeness.

## Score and Decision

**Calibration details:**
Retrieved anchors used:
- *SAL - How Does Unlabeled Data Provably Help OOD Detection?* (avg 6.50, accept, Round 2): Closest related work — same problem, same two-stage paradigm. Has clean theory-algorithm alignment that Medix lacks. Medix has a more novel core idea (median vs. top singular value) but the theory-algorithm disconnect makes it weaker overall.
- *DOS - Diverse Outlier Sampling* (avg 7.33, accept, Round 1): Clean, well-executed OOD detection paper with simple idea and compelling experiments. Medix's theory-algorithm disconnect is a weakness DOS doesn't have.
- *Rectifying Gradient-based OOD Detection via FIM* (avg 4.20, reject, Round 1): Gradient-based OOD detection with theory-alignment issues. Medix has stronger empirical results and more novel core idea.
- *Splitting & Integrating for OOD Detection* (avg 5.00, reject, Round 1): Gradient-based OOD with marginal improvements. Medix has more novel approach and better results.
- *NC-OOD* (avg 4.50, reject, Round 2): OOD detection with mixed reviews. Medix is clearly stronger.

**Round 1 bracket:** 5.0–6.5. **Narrowing:** Compared to SAL (6.50, accept, closest paradigm), Medix introduces a more novel core idea but has a theory-algorithm disconnect that SAL avoids. Compared to the reject-band OOD papers (4.2–5.0), Medix is significantly stronger in both novelty and empirical results. The final score of 5.5 reflects a paper with a genuinely novel contribution and strong empirical results, held back by a structural gap between theory and implementation that prevents it from reaching the clean accept level.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>