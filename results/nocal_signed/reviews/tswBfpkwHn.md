Now let me compose the final review.

## Summary

This paper presents the first theoretical analysis of training dynamics for one-layer Mamba models in the in-context learning (ICL) setting, focusing on binary classification tasks where prompts may contain additive outliers. The authors decompose one-layer Mamba into a linear attention component plus a nonlinear gating mechanism (Equation 3), prove convergence rates and generalization bounds (Theorems 1–2), and compare these with an equivalent analysis for one-layer single-head linear Transformers (Theorems 3–4). The key finding is that Mamba's gating provides provably stronger outlier robustness — tolerating an outlier fraction approaching 1 versus the linear Transformer's 1/2 barrier — at the cost of more training iterations and larger batch sizes. Supporting synthetic experiments verify the theoretical predictions and the mechanistic insights from Corollaries 1–2.

## Strengths

- **First theoretical analysis of Mamba ICL training dynamics.** The paper provides concrete convergence rates (Theorem 1) and sample complexity bounds for training one-layer Mamba on ICL tasks with outliers, going beyond prior work (Li et al., 2024a; 2025b) that studied global minima but not training dynamics. (+8.2 impact)

- **Clean architectural decomposition (Equation 3).** Deriving the one-layer Mamba output as linear attention + nonlinear gating with an explicit cascading product form is technically useful and pedagogically valuable. It reveals how the Transformer comparison can be instantiated (by setting G=1) and clarifies the role of each component. (+6.2 impact)

- **Mechanistic interpretability from Corollaries 1–2.** The paper extracts an interpretable story: the linear attention layer concentrates on examples sharing the query's relevant pattern (Corollary 1), while the nonlinear gating suppresses outlier-containing examples and introduces a positional decay that prioritizes nearby clean examples (Corollary 2). The experiments (Figures 3 and 4) provide direct empirical evidence for these mechanisms. (+9.0 impact)

- **Honest about scope limitations.** Remark 6 explicitly notes that real Transformers with multi-head attention and softmax may behave differently, and that the comparison is made at the one-layer single-head linear level. (+0.1 impact)

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **No statistical reporting for experimental results.** All experiments are on synthetic data with modest dimensions, but no error bars, standard deviations, or confidence intervals are reported for any figure or table. Results are presented as point values, making it impossible to assess stability across runs or parameter instances. While this is common in purely theoretical papers, the presence of experimental results invites standard empirical reporting practices. (-8.1 impact)

- **Training-cost trade-off not empirically validated.** The theoretical analysis shows that Mamba requires more iterations (T_M = Θ(l_tr) · T_T) and larger batch sizes than the linear Transformer. However, the experimental section (Section 4.1) compares only final classification error as a function of outlier fraction and does not show training curves, convergence speed, or the number of iterations each model needs to reach a given accuracy. Including this would give a more complete empirical picture of the trade-off. (-0.5 impact)

### Trivial

- **Unspecified polynomial term.** The term `poly(M_1^{κ_a})` in Theorem 1 condition (iii) (line 149) and Theorem 2 condition (d) (line 175) is not defined. While placeholder polynomials are common in theoretical statements, specifying the degree or providing a reference would improve interpretability. (-0.2 impact)

## Nice-to-Haves

- Add a brief proof-sketch paragraph for Theorem 1 in the main text so readers not diving into the appendix can follow the high-level argument.
- The multi-layer (3-layer) experiment in Table 1 is interesting but the paper is primarily about one-layer models; clarify whether the same theoretical guarantees are expected to extend or if this is purely an empirical probe.

## Removed Points

The following points from the input review were removed after cross-checking against the paper:

1. **"Central comparison claim is broader than what is actually compared"** — **REMOVED.** The paper consistently says "linear Transformer" in the abstract, Contribution 2, Section 3.4, and Remark 6. The comparison is properly scoped. The reviewer's framing criticism does not accurately reflect the paper's explicit qualifiers.

2. **"Unseen outliers claim is narrower than it appears"** — **REMOVED.** The paper explicitly states at line 93 and in Theorem 2 condition (a) that test outliers must be positive linear combinations of training outlier patterns. The "unbounded number of outlier variations" language (line 137) is accurate since a V-dimensional subspace yields infinitely many such combinations.

3. **"Mismatch between theoretical sufficient condition and experimental parameters"** — **REMOVED.** The bound α < min(1, p_a l_tr/l_ts) = 0.6 is a *sufficient* condition, not a necessary one. The paper explicitly notes at line 187 that it compares "sufficient conditions." It is standard and expected that actual performance can exceed sufficient conditions; no discrepancy exists.

4. **"Proof sketch entirely deferred"** — **REMOVED.** The parser strips the appendix; a proof sketch exists in the original submission per line 161.

5. **"CQ performance needs more discussion"** — **REMOVED.** The paper discusses this limitation at lines 277–283, explaining that outliers close to the query push clean examples farther away, causing gating values to decay exponentially.

6. **"Notation table needed"** — **REMOVED.** Stylistic preference; many theory papers are dense with parameters.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add error bars or report results over multiple random seeds for all experiments in Section 4.
2. Include a training-curve comparison (e.g., loss or accuracy vs. iterations) between Mamba and the linear Transformer to empirically illustrate the training-cost trade-off identified in the theory.
3. Specify the `poly(M_1^{κ_a})` term in the theorem statements or provide a reference.

## Score and Decision

The paper makes a genuine theoretical contribution: it provides the first analysis of training dynamics for one-layer Mamba in the ICL setting, with a clean decomposition, non-trivial convergence and generalization bounds, and mechanistic insights supported by experiments. The weaknesses are addressable (statistical reporting, training-curve comparison, notational clarity) and do not undermine the core theoretical claims. The paper's framing is appropriately scoped to one-layer linear attention models with and without gating.

**Final score: 8 — Accept.** The paper delivers a solid, novel theoretical contribution with well-supported claims, and the limitations are minor and fixable.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>