## Summary

TDDM proposes a hierarchical trajectory generation framework that decouples spatial occupancy (where people move) from temporal dynamics (how they move). It conditions a diffusion model on spatial priors (marginal occupancy distributions over 3×3 km regions canonicalized via similarity transforms), enabling region-level generation that transfers across cities. Evaluated on three cities (Beijing, Porto, San Francisco), TDDM demonstrates strong distributional alignment and plausible qualitative outputs.

## Strengths

1. **Clean and well-motivated factorization.** The decomposition of trajectory generation into spatial priors + temporal dynamics is intuitively compelling (Section 3). The similarity-transform canonicalization is a practical alternative to equivariant architectures, achieving invariance to translation/rotation/scale at the I/O level without architectural complexity.

2. **Genuinely interesting generalization findings.** The observation that Porto-trained models generalize to other cities better than models trained on 25% of the target city (Section 4.3) is a non-obvious result with practical implications. The discussion of the tradeoff between length-accuracy (benefiting from local data) and distributional coverage (benefiting from a well-chosen source) is honest and informative.

3. **Visually convincing qualitative results.** Figure 2 shows TDDM trajectories clearly following road networks with gaps between roads, while baselines visibly bleed across roads or miss segments. This aligns with the Pattern score advantage (0.917 vs. ≤0.907).

4. **Comprehensive evaluation framework.** The five quality dimensions (Fidelity, Diversity, Proportionality, Usefulness, Generalization) and six metrics provide reasonable coverage. The three-city benchmark with unified preprocessing is a useful contribution.

## Weaknesses

### Fatal
None.

### Major

1. **Asymmetric comparison inflates the headline KL-divergence claims.** TDDM generates trajectories conditioned on spatial prior H, computed from real data (Algorithm 2, line 3: "Compute heatmap H = f(r_c, X_target)"). The KL and JS divergence metrics in Table 1 then compare the generated trajectories' spatial distribution against the same real spatial distribution that served as conditioning. Baselines (Diffusion-TS, DiffTraj, etc.) receive no such spatial conditioning—they must learn the full spatio-temporal joint distribution from scratch. This explains the dramatic gap (KL_sym: 0.277 vs. 1.153–1.232). The conclusion's headline claim of "up to 4 times lower KL divergences" is literally true but the comparison is fundamentally asymmetric; the gap is largely expected given the different information each method receives. The ablation (Table 2) confirms this: removing spatial priors degrades KL by ~5×, showing the prior itself, not the deaggregation framework, drives these results. On fairer metrics (TSTR: 0.011 vs. 0.013 for DiffTraj; Pattern: 0.917 vs. 0.907), TDDM's advantage is modest.

2. **Missing variance estimates for most metrics.** Table 1 reports only point estimates for all KL, JS, Density, Trip, Length, and Pattern metrics. The paper states "Models are trained, sampled and evaluated once per dataset." Only TSTR includes ± values (standard deviation across three datasets, n=3). With single training runs and no confidence intervals, it is impossible to assess whether reported differences are statistically significant or reflect training stochasticity. This is especially problematic for metrics where TDDM's advantage is small (TSTR, Pattern, Length).

### Minor

3. **"Zero-shot" framing requires qualification.** The method's "zero-shot" generalization means no gradient updates on target trajectories, but it requires access to target-city trajectory data to compute the spatial prior H (Algorithm 2). In a deployment with zero historical target-city trajectories, H could not be computed. The paper does explain this (lines 169–173), but the abstract and conclusion invite over-interpretation by not explicitly stating this limitation.

4. **Baseline adaptation for DiffTraj unclear.** DiffTraj is described as a conditional model relying on "strong sample-specific conditioning" (Section 1), yet Table 1 compares it on the unconditional generation task. The paper never explains how DiffTraj was adapted for unconditional use—what conditioning was removed or how the model was modified. This is a missing methodological detail affecting comparison validity.

5. **"w/o spatial prior + rejection" condition unexplained.** Table 2's ablation includes this condition but the main text never describes what rejection scheme was used. This is a non-trivial missing detail for a condition appearing in the primary ablation table.

6. **Memorization claim about baselines unsubstantiated.** The paper asserts that DiffTraj/ControlTraj's "strong sample-specific conditioning increases the risk of memorization and prevents cross-region generalization" (Section 1). No evidence of memorization from these methods is provided; this is asserted rather than demonstrated.

7. **Computational cost not reported.** The paper does not report training time, inference time, model size, or number of parameters for TDDM or any baseline. For a method targeting large-scale generation, this is a notable omission.

### Trivial
None.

## Nice-to-Haves

- Giving baselines access to spatial priors (computing H and providing it as additional conditioning) would enable a fairer comparison that isolates the benefit of the deaggregation framework itself.
- Providing variance estimates (e.g., bootstrapped confidence intervals from a single model) for the main KL/JS results would substantially strengthen the quantitative claims.
- Reporting training/inference compute costs would help practitioners assess practical applicability.

## Removed Points

The following points from the input review were removed after verification against the paper:

- **"Mismatch between training-time region sampling and inference-time grid sampling could affect performance"** — Speculative; the paper describes both regimes as intentional design choices (Section 3). No evidence of harm is presented.
- **"Hyperparameters deferred to appendix"** — Page-limit deferral is standard; the paper states they are in Appendix C.
- **Generic "important problem" strength** — Too generic; removed. Concrete strengths (clean factorization, interesting findings, visual quality, evaluation framework) are retained.

## Novel Insights

The key insight emerging from this review is that the paper's spatial-temporal factorization is a genuinely useful design pattern, but the evaluation conflates two distinct questions: whether the factorization approach works, versus how much of the improvement comes from having access to spatial marginal information rather than from the deaggregation framework itself. The Porto-as-universal-source finding is the most original empirical result—it suggests some cities' mobility patterns are sufficiently representative to serve as training sources, with practical implications for data-scarce deployment scenarios.

## Suggestions

1. Reframe the KL-divergence claims to acknowledge the asymmetric information available to TDDM vs. baselines. Present KL results as showing that spatial conditioning enables better distributional matching (by design), and highlight TSTR/Pattern as the fairer head-to-head comparison.
2. Add variance estimates (at minimum bootstrapped confidence intervals) for all main Table 1 metrics.
3. Explain how DiffTraj was adapted for unconditional generation and describe the "rejection" scheme in the ablation.
4. Clarify the "zero-shot" terminology—e.g., "prior-conditioned generation" or explicitly state "zero-shot refers to no gradient updates on target data; spatial priors must still be computable from target observations."

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>