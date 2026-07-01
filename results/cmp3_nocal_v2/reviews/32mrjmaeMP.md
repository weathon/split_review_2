## Summary

This paper proposes TAK (Task Arithmetic with KFAC regularization), a method to promote weight disentanglement in task arithmetic without requiring full access to other tasks' training data during fine-tuning. The core insight is that representation drift regularization (which normally requires other tasks' data) can be reframed as a generalized Gauss-Newton (GGN) matrix quadratic form, which can then be approximated via Kronecker-Factored Approximate Curvature (KFAC). The paper additionally proposes a Kronecker-accumulation heuristic that keeps storage and computation constant in the number of tasks, and demonstrates thorough empirical results on vision (3 CLIP backbones, 8 datasets) and language (T5-base), covering both task addition and negation.

## Strengths

- **Clean theoretical connection between representation drift regularization and curvature.** The derivation from representation drift (Eq. 2) to the Jacobian Gram matrix (Eq. 3), and the identification of the Gram matrix as a GGN under squared-error loss (Sec. 3.2), is elegant and principled. This link is what unlocks the use of KFAC and gives the method its theoretical foundation.

- **Constant-complexity multi-task aggregation via Kronecker merging.** The heuristic in Eq. (8) reduces storage from O(T) to O(1). Tab. 3 validates that the accuracy gap relative to the idealized O(T) formulation is small (~0.1–0.8 points absolute), making the trade-off well-supported empirically.

- **Broad and thorough empirical validation.** The paper evaluates on three CLIP vision backbones (ViT-B/32, ViT-B/16, ViT-L/14), T5-base for language, covers both task addition and negation, compares against multiple baselines (τ-Jp, TaLoS, Attn-Only FT, Diag. GGN, TSV, ISO, TIES), and includes thorough ablations on the number of KFAC examples (Fig. 7a), MC samples (Fig. 7a), loss frequency (Fig. 8), compression strategies (Fig. 7b), and the Kronecker-accumulation heuristic (Tab. 3).

- **Practically useful robustness properties.** The insensitivity to the scaling coefficient α (Fig. 4a) is a practically valuable result — it eliminates the need for held-out validation data to tune α. The task localization analysis (Fig. 5) provides a concrete demonstration that the regularizer achieves its intended effect.

## Weaknesses

### Fatal
None.

### Major

- **No statistical uncertainty reported for any main result.** Throughout Tabs. 1, 2, and 3, every number is a single point with no standard deviations, confidence intervals, or indication of how many random seeds/runs were used. Several key comparisons are close: e.g., on ViT-B/16 (Tab. 1, α=1), τ-Jp gets 88.2/98.3 vs. TAK's 88.3/97.9; on ViT-B/16 (Best α), τ-Jp leads 88.6/98.7 vs. TAK's 88.3/98.1. Without uncertainty estimates, the reader cannot determine whether these differences are signal or noise. This weakens the paper's central empirical claim ("state-of-the-art results") for the task addition setting. The task negation results (Tab. 2) are clearer in TAK's favor, but the absence of any error bars across the entire experimental section is a significant gap in a paper that stakes its contribution on quantitative comparisons.

### Minor

- **"Dataless" framing is an overstatement.** The abstract calls TAK a "dataless approach" and says it improves weight disentanglement "without using external data." In reality, the method requires 128–256 examples per task to estimate the KFAC factors (Fig. 7a). The paper is transparent about this in Sec. 3.1 ("after initial pre-computation") and Fig. 7, but the central framing inflates the contribution. The method's advantage is better described as "requires orders of magnitude less data than τ-Jp" rather than "dataless."

- **The MC sampling degradation is reported but unexplained.** The paper notes (Sec. 4, "KFAC estimation") that "Surprisingly, performance deteriorates beyond [1–2 MC samples], with variance across seeds increasing as the number of MC samples grows." For an unbiased Monte Carlo estimator, increasing samples should reduce variance, not increase it. The paper offers no explanation or investigation of this counterintuitive behavior. This is a methodological gap in a paper whose practical method relies on this estimation procedure.

- **The Kronecker merging heuristic lacks characterization of when it might break down.** Eq. (8) approximates a sum of Kronecker products as a Kronecker product of sums, which is not generally correct. The paper relies entirely on empirical validation on one testbed. While Tab. 3 shows the gap is small for the evaluated settings, there is no analysis of conditions under which the approximation degrades (e.g., when task factor matrices are very dissimilar). The ViT-B/32 results in Tab. 3 (86.6 idealized vs. 86.0 accumulated) already hint at sensitivity to model scale that is not explored.

### Trivial
None.

## Nice-to-Haves

- Adding per-task numerical results for T5-base in a table (rather than only radar charts) would be more informative.
- A comparison with other curvature approximations (e.g., EKFAC, diagonal Fisher with more sophisticated estimation) would further contextualize the KFAC choice, though the comparison with diagonal GGN already provides a reasonable baseline.
- Investigating and resolving the MC-sample degradation would strengthen the methodological contribution.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Training details deferred to appendix:** The harsh reviewer noted that "training details are deferred to the appendix (which is stripped — I cannot verify them)." This is removed because the parser strips appendix content from all papers; the details exist in the original submission.
- **"No dedicated limitations section":** The reviewer noted the paper lacks a dedicated limitations section, but the conclusion does discuss limitations and future directions. This is a stylistic preference, not a substantive weakness, and is removed.

## Novel Insights

The harsh review's most valuable insight beyond the paper's own contributions is that the unexplained MC-sample degradation (more samples → worse performance) is genuinely unusual for an unbiased estimator and may point to either a subtle implementation issue or a real phenomenon the paper does not understand. This is a useful flag for the authors to investigate. The review also correctly notes that the paper's "state-of-the-art" claim in the abstract is slightly stronger than what the results in the linearized regime support — τ-Jp and TAK are roughly on par for task addition, with TAK having an advantage on negation.

None beyond the paper's own contributions.

## Suggestions

1. **Report error bars.** Run 3–5 seeds for the main comparisons (Tab. 1, especially TAK vs. τ-Jp) and report means ± std dev or confidence intervals. This is the single most important addition.
2. **Investigate the MC-sample degradation.** Determine whether this is a scaling issue in the MC estimate, an implementation bug, or a genuine phenomenon, and either fix or explain it.
3. **Recalibrate the "dataless" framing.** Replace "dataless approach" with language like "requires only 128 examples per task" or "data-efficient" in the abstract and introduction.
4. **Provide a synthetic or analytical characterization of the Kronecker merging approximation error** — even a simple experiment varying the divergence between task factor matrices would help users understand when the heuristic can be trusted.

## Score and Decision

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>