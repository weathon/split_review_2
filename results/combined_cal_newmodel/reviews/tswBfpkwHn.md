## Summary

This paper provides the first theoretical analysis of the training dynamics of a one-layer Mamba model for in-context learning (ICL) on binary classification tasks with outliers. It proves SGD-based convergence bounds (Theorem 1) and generalization guarantees under distribution-shifted test-time outliers (Theorem 2), showing Mamba can tolerate an outlier fraction α up to min(1, p_a·l_{tr}/l_{ts}) while linear Transformers are capped at α < 1/2 (Theorems 3, 4). The analysis decomposes Mamba's mechanism into a linear attention component that selects same-pattern examples (Corollary 1) and a nonlinear gating component that suppresses outliers and induces distance-based decay (Corollary 2). Synthetic experiments support the theoretical claims and honestly acknowledge a failure mode (CQ setting in Table 1).

## Strengths

- **First theoretical analysis of Mamba training dynamics (SGD-based convergence) for ICL.** Prior work analyzed global minima of simplified variants (Li et al., 2024b; 2025b) or expressiveness (Bondaschi et al., 2025). This paper delivers convergence bounds (Theorem 1) and generalization guarantees (Theorem 2) that go beyond those works. [favorability=11.78]

- **A genuine provable robustness finding with concrete threshold comparison.** Mamba can tolerate an outlier fraction α up to min(1, p_a·l_{tr}/l_{ts}) while linear Transformers are capped at α < 1/2 (Theorems 2 and 4, Remarks 3 and 5). The mechanism is clean: gating suppresses outliers (Corollary 2(i)) and induces distance-based decay (Corollary 2(ii)), while attention selects same-pattern examples (Corollary 1). [favorability=11.56]

- **Clean mechanistic decomposition into linear attention and gating components** (Corollaries 1 and 2). This gives a mathematically stated explanation of how each of Mamba's two components contributes to ICL, going beyond typical interpretability-by-analogy reasoning. [favorability=11.05]

- **Honest empirical evaluation that acknowledges failure modes.** Table 1 reveals Mamba's vulnerability when outliers are placed closest to the query (CQ setting, 82.73% vs 93.96% for linear Transformer), which is consistent with Corollary 2(ii)'s exponential decay mechanism and shows the paper does not overclaim. [favorability=10.50]

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **The robustness guarantee in Theorem 2 requires each test-time outlier v to satisfy a positive linear combination condition** (v = Σ λ_i v_i^* + u with Σ λ_i ≥ L > 0). The paper (line 93) is transparent about this, but the abstract and introduction could lead a casual reader to overestimate the generality of the result. The abstract says "even when the prompt includes additive outliers" without flagging this structural restriction. [favorability=1.91]

- **The claim that α can approach 1 (lines 95, 207) depends on the sufficient condition p_a·l_{tr} ≥ l_{ts} from Theorem 2(c).** In the experiments (p_a=0.6, l_{tr}=l_{ts}=20), the theoretical bound is α < 0.6, yet experiments test up to α=0.8. While the bound is sufficient rather than necessary (so experiments do not contradict theory), the presentation could mislead readers into thinking α→1 is guaranteed uniformly rather than conditionally. [favorability=1.31]

- **The gating formulation in (3) collapses the selective SSM discretization (Δ, A, B, C matrices) into a single gating function G.** The paper acknowledges this implicitly by discussing the simplification in (3), but some discussion of what properties of the full Mamba architecture are preserved or lost in this reduction would strengthen the paper's scope claims. [favorability=1.22]

- **The upper bound on l_{tr} in Theorem 1(iii) involves poly(M_1^{κ_a}), which can grow quickly since κ_a scales with V.** This limits the practical interpretability of the result, as the paper implicitly acknowledges. [favorability=2.89]

### Trivial
None.

## Nice-to-Haves
- A derived quantitative bound on the CQ failure case from Corollary 2(ii)'s exponential decay mechanism (e.g., a threshold on l_{ts} or the fraction of CQ outliers beyond which accuracy degrades).
- A parameter sweep varying the l_{tr}/l_{ts} ratio to directly test the prediction α < p_a·l_{tr}/l_{ts}.
- A discussion connecting the test-time outlier condition to a principled interpretation of why the gating mechanism can handle outliers sharing directional components with seen outliers but not completely novel orthogonal ones.

## Removed Points

These points are flagged to be removed, treat them with caution:

1. **"The CQ failure case is not discussed theoretically"** — Removed because the paper does discuss it (lines 277–283: 'because, when outliers are placed close to the query, the clean examples that share the same pattern as the query are pushed farther away, and the gating values on these examples decay exponentially according to (18)'). A quantitative threshold would be a nice-to-have extension, not a missing discussion.
2. **"No analysis of statistical vs. computational tradeoffs"** — Removed as scope creep. The paper's focus is convergence and generalization guarantees; tightness of bounds is a natural follow-up, not a core weakness.
3. **"Parameter sweep varying l_{tr}/l_{ts}"** — Removed as a nice-to-have experiment, not a weakness.
4. **Generic scope/formatting/style nitpicks** — removed per instructions.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. In the abstract and introduction, add a brief qualifier clarifying that the α→1 result requires p_a·l_{tr} ≥ l_{ts}, and that the test-time outlier must have a positive projection onto training outlier directions. The paper is transparent about these conditions in the technical sections, but the high-level claims could mislead readers who skip the detailed statements.
2. Add a brief discussion connecting the test-time outlier condition (positive linear combination) to a natural interpretation: the gating mechanism can be expected to handle outliers that share directional components with seen outliers, but not completely novel orthogonal outliers. This would make the limitation feel principled rather than incidental.
3. Clarify the relationship between the simplified model in (3) and the full Mamba architecture by noting which properties are preserved (gating behavior) and which may be lost (full selective state dynamics).

## Score and Decision

**Calibration:** Round 1 bracket = 5.5–7.0. Narrowed via comparison to anchors jwsPS8yRe4 (6.00, Accept, linear Transformer ICL theory without experiments) and n7n8McETXw (6.50, Accept, nonlinear Transformer CoT theory with experiments). The reviewed paper is above jwsPS8yRe4 because it provides experimental validation that paper lacks; it is below qtTIP5Gjc5 (7.50) because that paper's theory directly motivates architectural improvements. The paper's favorability profile (all strengths ≥10.5, all weaknesses ≤2.89) is consistent with a score in the 6.0–6.5 range.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>