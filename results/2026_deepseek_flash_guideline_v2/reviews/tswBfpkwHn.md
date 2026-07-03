Now let me produce the final consolidated review.

## Summary

This paper provides the first theoretical analysis of the training dynamics and ICL generalization of one-layer Mamba models, focusing on robustness to outliers. The authors prove convergence guarantees (Theorem 1), show that Mamba can maintain accurate ICL even when the outlier fraction approaches 1 under certain conditions (Theorem 2), and contrast this with a one-layer linear Transformer which can only tolerate α < 1/2 (Theorem 4). The theoretical analysis decomposes Mamba's mechanism into linear attention (pattern selection) and nonlinear gating (outlier suppression + local bias), with supporting synthetic experiments.

## Strengths

1. **First training-dynamics analysis of Mamba ICL.** The paper fills a genuine gap: prior theoretical work on Mamba ICL (Li et al., 2024b; 2025b; Bondaschi et al., 2025) analyzed what trained models represent at global minima, not whether SGD can reach those minima. The analysis handles the nonlinear gating that makes Mamba structurally different from Transformers (Remark 2, line 163).

2. **Rigorous quantitative comparison isolating the effect of nonlinear gating.** By proving that Mamba (with gating) can tolerate α → 1 while a one-layer linear Transformer (without gating) fails at α > 1/2 (Theorems 2 vs. 4), and experimentally validating these thresholds (Figure 2), the paper cleanly attributes the robustness difference to the gating mechanism. The comparison is deliberately scoped to isolate the gating as the only architectural difference (Remark 6, line 209).

3. **Mechanistic decomposition validated beyond the theoretical scope.** Corollary 1 proves attention selects same-pattern examples; Corollary 2 proves gating suppresses outliers and induces exponential local bias. These predictions are verified not only for the one-layer case analyzed theoretically but also in three-layer models (Figures 3-4). Table 1 provides a particularly strong test: when outliers are closest to the query (CQ), Mamba's accuracy drops to 82.73% versus the linear Transformer's 93.96% — a non-trivial consequence of the local bias predicted by Corollary 2(ii).

4. **Outlier model grounded in concrete attack scenarios.** The data formulation is motivated by data poisoning attacks (Example 1, Figure 1) and tested under three distinct outlier-labeling functions (flipped, targeted, random), not just one noise model.

## Weaknesses

### Major
None.

### Minor

1. **Framing of the Mamba-vs.-Transformer comparison overstates novelty.** The paper consistently specifies "linear Transformer" in its formal statements, but the narrative positions this as a broad comparison between architectures. The finding is fundamentally "gating helps compared to no gating in a linear-attention framework" — a valid and theoretically well-supported result, but one that does not address whether Mamba's robustness advantage holds against softmax-attention Transformers (which also have input-dependent reweighting). Remark 6 acknowledges this limitation, and the appendix is said to include softmax experiments, but the main text's framing invites over-interpretation.

2. **Test-time outlier coverage is structurally restricted.** Theorem 2, Condition (a) requires test outliers to lie in the set V' = { v | v = Σ λ_i v_i^*, Σ λ_i ≥ L > 0 } — i.e., positive-coefficient-sum linear combinations of training outlier patterns. This excludes test outliers orthogonal to all training outlier patterns. The paper claims this "captures a wide range of possible outlier patterns" (Remark 3), but the restriction is substantial and should be more prominently discussed as a limitation of the theoretical guarantee.

3. **Main experiments lack statistical characterization.** Figures 2-4 show results without error bars, confidence intervals, or indication of multiple runs. For a paper making quantitative theoretical claims validated empirically, this makes it difficult to assess the stability of the observed effects. The experiments also use the exact same synthetic data model as the theory, serving primarily as internal consistency checks rather than tests of broader applicability.

4. **Several technical conditions in Theorem 1 have complex interdependencies.** Conditions (i)-(iii) involve multiple coupled inequalities among V, β, κ_a, p_a, M_1, and ε. The paper does not provide worked numerical examples where all conditions are simultaneously satisfiable, nor does it discuss parameter regimes where they conflict. This makes it hard to assess whether the result covers practically relevant configurations.

### Trivial

1. The exponential decay structure in Corollary 2(ii) arises partly from the architecturally-prescribed multiplicative form of the gating function G_{i,l+1}(w) = σ(w^T p_i) Π (1-σ(w^T p_j)), not purely from learning. The paper could more clearly distinguish architectural properties from learned ones.

## Nice-to-Haves
- A worked numerical example showing parameter values that simultaneously satisfy all conditions of Theorem 1.
- Brief discussion of how the analysis might change if patterns were correlated or had varying norms.
- Visual indication of whether the α < 1/2 threshold for linear Transformers is proven necessary or just a sufficient condition.

## Removed Points

### From Harsh Critic
- **"Comparison is against a deliberately weakened Transformer"** — Retained in weakened form as Minor #1. The full-strength version is removed because the paper consistently specifies "linear Transformer" throughout its formal statements and Remark 6 explicitly explains the design choice. The paper is transparent about what it compares.
- **"Exponential decay is architectural, not learned"** — Retained as Trivial #1. The critic's stronger claim that this "conflates what is learned from what is built-in" overstates the issue: the paper proves specific post-training bounds that are not guaranteed by architecture alone.
- **"No comparison with softmax attention in the main text"** — Removed because the paper explicitly states (Remark 6, Appendix B.1) that softmax attention experiments are in the appendix, which is stripped by the parser. Per hard rules, missing appendix content is not a valid criticism.
- **"Missing related works"** — Removed per hard rules.
- **Various formatting/presentation nitpicks** — Removed per hard rules (parser artifacts, not author errors).

### From Strength Finder
- Generic strengths about "addressing an important problem" or "interesting question" — Removed; only concrete, evidenced strengths retained.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Add error bars or confidence bands to the main experimental figures (Figures 2-4).
2. Include a subsection or paragraph explicitly discussing the limitations of the test-time outlier condition (V' being a restricted cone over training outliers).
3. Add a brief empirical comparison with softmax attention in the main text, or at minimum reference the appendix results more prominently in the conclusion.
4. Provide a concrete numeric example illustrating that all conditions of Theorem 1 can be satisfied simultaneously.
5. Clarify in the discussion of Corollary 2(ii) which aspects of the exponential decay are architecturally dictated versus learned.

## Score and Decision

The calibration database was inaccessible, so I calibrate based on the paper's merits against ICLR standards. This paper makes a genuine theoretical contribution (first training dynamics analysis of Mamba ICL) with sound derivations and experimentally-validated predictions that extend beyond the theoretical scope (3-layer models, Table 1's non-trivial CQ prediction). The weaknesses — framing that somewhat overstates the novelty of the comparison (Minor #1), restrictive theoretical conditions (Minor #2), thin experimental characterization (Minor #3), and complex interdependent conditions (Minor #4) — are real but addressable and do not undermine the core findings. There are no fatal flaws. The paper sits between borderline accept and clear accept: well above the reject threshold due to substantive novel theory, but with enough limitations to prevent a score of 8. Score is rounded to the nearest .0 as per protocol.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>