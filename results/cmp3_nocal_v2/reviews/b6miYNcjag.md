## Summary

This paper introduces the problem of reliability scoring for datasets without ground truth, given access to outcomes of an unknown statistical experiment. The core contribution is the Gram Determinant Score — a measure of the volume spanned by class-conditional observation distributions — which provably preserves two exact reliability orderings (exact-match and Blackwell), approximately preserves Hamming/distance-based orderings under restricted conditions, and is uniquely experiment-agnostic (the same ranking of datasets holds regardless of which experiment generated the observations). The paper also contributes impossibility results that chart the boundaries of what any reliability score can achieve. Experiments on synthetic data, CIFAR-10 embeddings, and employment data provide sanity-check validation.

## Strengths

1. **Experiment agnosticism is genuinely novel and non-trivial.** Proposition 4.3 shows that the Gram determinant ranking of datasets is independent of the observation-generating experiment and, up to scaling, is uniquely characterized by this property under mild conditions. The decomposition Γ(PQ) = det(P^T P) det(Q)² cleanly separates the experiment from the misreport. This is the paper's strongest theoretical contribution and gives the score a characterization most comparable methods lack.

2. **The impossibility results (Section 3, Proposition 3.1) are responsibly scoped and informative.** Rather than overclaiming, the paper establishes fundamental limits (no score can preserve Hamming ordering under Q_dom; Blackwell ordering preservation fails with linearly dependent experiments) and then designs the Gram determinant to operate precisely within the feasible region. This gives the reader a clear picture of where the method applies and why.

3. **The geometric interpretation is elegant and accessible.** The intuition that the Gram determinant measures the volume spanned by class-conditional observation distributions, and that this volume shrinks as reports deviate from the truth (Figure 1), makes the method intuitive and provides a natural justification for the score.

4. **The theoretical guarantees for exact-match and Blackwell orderings (Theorem 4.2, parts 1 and 2) are exact and clean.** These are not asymptotic or approximate — they hold exactly under minimal assumptions that nearly match the impossibility results.

## Weaknesses

### Fatal
None.

### Major

1. **No baseline comparisons in the main-text experiments.** The experiments show that the Gram determinant score correlates monotonically with corruption level across six policies. This is necessary but trivial evidence — any reasonable reliability measure should correlate with corruption. The related work section identifies Kong (2024)'s determinant mutual information (described as the most related prior work), Zheng et al. (2025)'s pointwise mutual information, and various f-divergences as directly comparable approaches, yet none are compared against in the main text. The paper references Appendix G for comparisons with other candidates and the appendix for a comparison with Kong (2024), but these are stripped and in any case the main-text experiments stand alone without baselines. Without any baseline comparison, it is impossible to assess whether the Gram determinant adds value over existing approaches or merely reproduces what simpler scores already achieve.

2. **The α-dist ordering guarantee (Theorem 4.2, part 3) is very restrictive in practice.** The score preserves the (1/(4LΔ))-dist ordering under Q_{L, 1/(64L²d²)}. For Hamming distance (Δ=1) and balanced classes (L=1), α = 1/4, meaning the cleaner dataset must have ≤ 1/4 the Hamming distance of the noisier one for the score to rank them correctly. More critically, δ = 1/(64d²): for d=10 this caps Hamming distance at approximately N/6400 (essentially near-perfect labels); for d=1000, roughly N × 1.56×10⁻⁸. The paper is transparent that these conditions are "nearly tight" with impossibility results, and the theoretical value of delineating the boundary is clear. However, the practical consequence is that the Gram determinant cannot reliably distinguish datasets with moderate differences in label quality — only extreme ones — for the ordering most readers would associate with "reliability."

### Minor

1. **Mismatch between "finite-sample guarantees" claim and main-text evidence.** The conclusion states: "We develop plug-in and stratified-matching estimators with finite-sample guarantees." However, the main text only provides Proposition 4.5, which is an *asymptotic* guarantee. No concrete finite-sample bound (concentration inequality, high-probability statement, or sample complexity bound) appears in the main text; the stratified-matching estimator and any associated non-asymptotic results are deferred to the (stripped) appendix. The claim in the conclusion is stronger than what the main text demonstrates.

2. **Employment experiment lacks uncertainty quantification.** With N=209 discretized into 4 quantile buckets, the Gram determinant score for each vintage is a point estimate with no confidence interval, bootstrap interval, or significance test. Given the small sample size and coarse discretization, this weakens the real-data demonstration.

3. **CIFAR-10 experiment uses 8-dimensional embeddings with 10 classes.** The kernelized Gram determinant score with a linear kernel effectively computes the Gram matrix of class-mean embeddings. With 10 classes embedded into 8 dimensions, linear independence of the class means is not guaranteed (the theoretical guarantees for the kernelized score are in Appendix F). While this does not invalidate the experiment as a qualitative demonstration, it deserves discussion in the main text.

### Trivial
- No discussion of computational cost. Determinant computation is O(d³), which could be expensive for large label spaces (e.g., ImageNet with 1000 classes). The paper acknowledges scalability only as future work.

## Nice-to-Haves
- Adding even a single baseline comparison (e.g., against Kong (2024)'s determinant mutual information) on the synthetic data would transform the empirical evaluation from "the score correlates with corruption" to "the score outperforms or matches existing approaches."
- Including a synthetic experiment that deliberately violates the theoretical conditions (rank-deficient P, operating outside Q_{L,δ}) and shows the score breaks down as predicted would demonstrate that the theory captures real empirical behavior.
- If finite-sample bounds exist in the appendix, stating a concrete bound (e.g., sample complexity or high-probability statement) in the main text would resolve the claim-evidence gap cleanly.
- The Blackwell ordering requires Q to be "invertible and (row) diagonally maximized," which the paper acknowledges in footnote 3. Including a brief discussion of how frequently this condition is violated in practice would help readers assess applicability.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"Blackwell ordering restriction to Q_reg is too restrictive"** — The paper already acknowledges this in footnote 3 and provides an alternative condition. This is a known modeling choice, not an oversight.
- **"No held-out/validation split in experiments"** — Not a weakness; the score is computed from reported data and observations without using true labels, so this is appropriate for the setting as the critic correctly notes.
- **"Q must be invertible (GL_d) for experiment agnosticism"** — The method is designed for this setting and Proposition 4.3 explicitly restricts to GL_d; the paper is transparent about this condition.
- **"Missing related works"** — Cannot be verified without external sources.
- **Finite-sample guarantees being "not verifiable from the main text"** — The version kept in Minor above focuses on the claim-evidence gap (conclusion claims more than main text shows), not on the appendix being missing.
- **"The decomposition Γ(PQ)=det(P^T P)det(Q)² holds only when Q is square"** — This is inherent to the categorical setting and is not a weakness; the paper defines Q as d×d for a d-class label space.

## Novel Insights

None beyond the paper's own contributions. The reviews surface the core tension: the paper has a genuinely novel theoretical contribution (experiment-agnostic scoring with impossibility boundaries) but the empirical validation is much weaker than what a reader needs to assess practical value. The reviewers add no fundamentally new insight about the method that the paper does not already articulate.

## Suggestions

1. Add at least one baseline comparison in the main-text experiments — the synthetic data setup with Kong (2024)'s determinant mutual information would be the most natural choice given its direct relevance and shared determinant-based structure.
2. Either state a concrete finite-sample bound in the main text or adjust the conclusion to match what is demonstrated (asymptotic preservation).
3. Add bootstrap confidence intervals or similar uncertainty quantification to the employment data experiment.
4. Explicitly discuss whether the 8-dimensional CIFAR-10 embeddings (10 classes) can yield a positive-definite G_K, and whether this matters for the kernelized score's guarantees.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>