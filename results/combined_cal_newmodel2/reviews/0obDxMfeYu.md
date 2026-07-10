Now I'll produce the final consolidated review with the calibrated score.

## Summary

This paper introduces Medix, a framework that uses the element-wise median (EWM) of gradients to identify OOD samples from unlabeled "in-the-wild" data mixtures. The approach is two-stage: (1) an iterative greedy algorithm removes candidate outliers from the wild set based on their marginal contribution to the EWM deviation from a reference InD gradient, and (2) a binary OOD detector is trained on the identified outliers and labeled InD data. The paper provides theoretical bounds on inlier and outlier misclassification rates for median-based filtering and evaluates against 20 baselines across 11 InD-OOD pairs.

## Strengths

- **Conceptually novel use of the element-wise median of gradients for OOD filtering (Section 3.1).** The median's robustness to contamination is well-motivated, and the motivating experiment (Figure 1) showing monotonic deviation as OOD samples are added provides clear empirical intuition. This is genuinely different from existing approaches like WOODS (constrained optimization) and Du et al. (2024a) (singular-value-based thresholding).

- **Formal theoretical guarantees bounding both inlier and outlier misclassification rates (Section 4, Theorems 4.1 and 4.2).** Few prior works in the unlabeled wild setting provide theoretical foundations. The two-sided bounds — controlling both false flagging of inliers and missed detection of outliers — are a genuine contribution, and the explicit modeling of contamination, concentration, and separation effects is informative.

- **Broad empirical evaluation covering 11 InD-OOD pairs, 20 baselines, and both CIFAR-10 and CIFAR-100 as InD data (Section 5, Tables 1-2).** Results show consistent improvements across all OOD datasets. Reporting standard deviations over 5 runs is good practice. On CIFAR-10, Medix achieves notably strong results (average FPR95 0.80% vs. 3.40% for WOODS).

- **The paper explicitly addresses the most obvious objection to its theoretical assumption by providing a looser bound (Theorem C.3) that removes the sub-Gaussian assumption and holds under bounded second moments (Remark 4.3).** The Q-Q plot validation (Figure 4, appendix) further supports the plausibility of the sub-Gaussian assumption.

## Weaknesses

### Major

- **Structural disconnect between the theoretical analysis (Section 4) and the algorithm actually used (Algorithm 1).** The theory bounds the error of an "EWM filtering rule" — but this rule is never explicitly defined in the main text, and the paper does not establish how Algorithm 1's iterative, greedy leave-one-out procedure relates to or implements this rule. Theorem 4.1 and 4.2 analyze a one-shot classification decision based on the EWM, while Algorithm 1 iteratively removes the top-k points by marginal contribution to the EWM deviation. The paper's headline claim of providing "theoretical guarantees for Medix" is not fully substantiated when the object of analysis differs from the actual algorithm used in experiments. This is the paper's most significant weakness and should be addressed in revision.

### Minor

- **Algorithm 1's termination condition uses a logical OR (line 110: `while t ≤ T or |δ_max| > ε`) instead of AND.** With OR, the loop runs exactly T+1 iterations regardless of convergence (since t ≤ T is true for the first T iterations irrespective of whether |δ_max| > ε), rendering the ε-based convergence check ineffective. This contradicts the textual description ("The algorithm repeats until there is no significant drop in δ_i or a maximum number of iterations is reached"), which implies the loop stops when either condition is met.

- **The computational cost of Algorithm 1 is a practical concern deferred to the appendix.** Each iteration requires computing EWM(G_{S\{i}}) for every remaining sample i, which is O(|S|²·d) per iteration. With a wild set of 25,000 samples and penultimate-layer gradient dimensionality, the first iteration alone is computationally heavy. The paper defers this discussion to Appendix A.6, but for a method whose practical feasibility is in question, this warrants discussion in the main body.

- **The improvement over the most directly comparable wild-data baseline (WOODS) is modest on CIFAR-100:** 1.32% average FPR95 reduction (from 6.74% to 5.42%). The headline figure of a 40.98% improvement over KNN+ compares against methods that do not use wild data at all. While both comparisons are reported, the more meaningful comparison against wild-data methods shows more incremental gains on the harder InD dataset.

- **The variable m_min is used in Theorem 4.1 (line 134) but is not defined in the main text.** Given that appendix content is stripped during review, this missing definition prevents readers from fully interpreting the bound.

- **The synthetic 2D experiment (Figure 2) places OOD data at a mean 30+ standard deviations from the nearest InD cluster** (mean [20, 2√3] vs. InD means within [-2,2]×[0,3.5], all with covariance 0.25I). The 87.5% detection rate for such extreme separation is surprisingly low, which limits this experiment's informativeness as a validation of the method.

### Trivial

None.

## Nice-to-Haves

- The paper could strengthen its case with a main-paper ablation showing what happens when using the mean instead of the median for filtering, which is the most natural baseline for justifying the "median perspective" framing.
- The empirical connection to the separation condition in Theorem 4.2 would be strengthened by experiments that vary the InD-OOD gradient separation distance and show where the method degrades.

## Removed Points

These points from the input review are flagged to be removed; treat them with caution:

- **"Reliance on predicted labels for wild samples is under-discussed"** — The paper explicitly acknowledges evaluating pseudo-label quality in Appendix A.5 and states the method is resilient to noisy labels. This concern is acknowledged and deferred, not ignored.
- **"Algorithm may not actually run the leave-one-out procedure on 25k samples"** — Speculative, not verifiable from the paper as written.
- **"The optimization objective has a trivial empty-set solution"** — The paper starts from the full wild set and only removes points; the objective motivates the greedy procedure, not an exact combinatorial search.
- **"WOODS/OE training data usage not stated"** — The paper states it follows the protocol of Katz-Samuels et al. (2022a), which is an acceptable reference.
- Pure formatting nitpicks and missing-related-work complaints.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Align the theory and algorithm.** Either (a) define the one-shot EWM filtering rule explicitly and prove that Algorithm 1's greedy procedure approximates its output with bounded error, or (b) extend the theoretical analysis to cover the iterative greedy removal process directly.
2. **Fix Algorithm 1's termination condition** to use `while t ≤ T and |δ_max| > ε`.
3. **Include a runtime/complexity discussion in the main paper,** or describe algorithmic optimizations that make the leave-one-out procedure practical at scale.
4. **Define m_min in the main text** when stating Theorem 4.1.
5. **Replace or supplement the synthetic 2D experiment** with a more challenging setup that varies separation distance and demonstrates where the method breaks down, linking to the separation condition in Theorem 4.2.

---

**Calibration Report:**

| Anchor | Path | Avg Score | Round | Itemized | Comparison |
|--------|------|-----------|-------|----------|------------|
| Du et al. (2024a) — SAL | jlEjB8MVGa.md | 6.50 | R1+R2 | Yes | Most directly comparable: same wild-OOD setting, theoretical guarantees, SOTA results. Current paper has a novel median approach and comparable strength ratings (12.66-16.13 vs. 6.36-13.94) but has a structural theory-algorithm disconnect that Du et al. lacks. |
| ProMix — Guaranteed OOD Detection | voVjW1PT2c.md | 6.00 | R2 | Yes | Similar score and approach (auxiliary data + theory). Current paper has a more novel filtering mechanism but a more significant theory-algorithm gap. |
| Conformal Prediction + OOD | GQhlM0Mavg.md | 5.00 | R1 | Yes | Different paper type; lower score due to novelty concerns. Current paper is stronger. |
| Semantic/Covariate OOD | uWUovmBRUq.md | 4.00 | R1 | Yes | Primarily theoretical paper; current paper has stronger empirical contributions. |

**Round 1 bracket:** [5.5, 7.5], identified via query-based calibration. Within this bracket, the Du et al. (2024a) anchor (6.50) is the most directly comparable.

**Round 2 narrowing:** The Du et al. anchor (6.50) has strength favorability up to 13.94 and weakness favorability down to -0.77. The current paper has strength favorability up to 16.13 but weakness favorability down to -2.00 (synthetic experiment) and a structural weakness at 0.80 (theory-algorithm disconnect). Compared to the 6.50 anchor, the current paper has comparable or slightly stronger strengths but a more significant structural weakness. The theory-algorithm disconnect and the -2.00/-0.98 weakness items place this paper slightly below 6.50 but above 5.50, which is the score of the weakest acceptable anchor (ProMix at 6.00, which Rejected at 6.00). The final score of **6.0** reflects this positioning: a genuine contribution with a novel idea and strong experiments, but held back by a theory-algorithm gap that prevents the theoretical claims from being fully substantiated.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>