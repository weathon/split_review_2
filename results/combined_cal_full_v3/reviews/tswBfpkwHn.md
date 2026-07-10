Here is the final consolidated review.

## Summary

This paper presents the first theoretical analysis of the training dynamics of a one-layer Mamba model for in-context learning (ICL) on binary classification tasks in the presence of additive outliers. The authors decompose one-layer Mamba into a linear attention component plus a nonlinear gating layer (Equation 3), enabling clean theoretical analysis. They prove convergence and sample complexity bounds (Theorem 1) and ICL generalization guarantees on distribution-shifted test prompts containing unseen outliers (Theorem 2). By comparing against a linear Transformer (Mamba with gating removed), they show that Mamba can tolerate a significantly higher fraction of outlier-containing context examples (α up to min(1, pₐ·l_tr/l_ts)) compared to linear Transformers (α < 1/2). The mechanism-level analysis (Corollaries 1 and 2) reveals how attention selects informative examples while gating suppresses outliers and induces a local bias. Synthetic experiments validate the qualitative α-threshold prediction and mechanism-level insights.

## Strengths

- **First theoretical analysis of Mamba training dynamics for ICL (favorability=9.36).** The paper correctly identifies that existing theoretical work (Li et al., 2024b; 2025b) studies the loss landscape at global minima, not training dynamics — a model could have desirable global minima that SGD never finds. Providing convergence guarantees is a genuinely new contribution.

- **Clean analytical decomposition in Equation (3) (favorability=9.55):** one-layer Mamba reduces to linear attention + a nonlinear gating layer. This makes the architecture analytically tractable and creates a natural baseline (linear Transformer = Mamba with gating fixed to 1), isolating the effect of gating.

- **Specific, falsifiable theoretical predictions (favorability=9.26).** The paper gives precise thresholds: linear Transformers fail when α ≥ 1/2, while Mamba can tolerate α up to min(1, pₐ·l_tr/l_ts). Figure 2 confirms the 1/2 threshold for linear attention in synthetic experiments across three different labeling functions (flipped, targeted, random).

- **Mechanism-level characterization (Corollaries 1 and 2) (favorability=10.33)** showing how the linear attention selects informative context examples and the nonlinear gating suppresses outliers while inducing exponential decay with distance. These mechanisms are verified experimentally in Figures 3 and 4.

- **The paper handles its limitations honestly (favorability=8.11).** Remark 6 acknowledges that real softmax Transformers can be robust, and Table 1 openly reports Mamba's significant performance drop (82.73%) when outliers are closest to the query (CQ setting).

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **Quantitative bounds not empirically validated (favorability=0.57).** Theorems 1–4 provide specific bounds on batch size, number of iterations, context length, and outlier magnitude (κₐ, κ'ₐ). The experiments only test the qualitative α-threshold comparison (Theorem 2 vs. Theorem 4 condition (c)) and the mechanism-level predictions (Corollaries 1 and 2). The abstract's claim that theoretical findings are "supported by empirical experiments" overstates what the experiments actually verify. The specific convergence rates, sample complexity bounds, and magnitude constraints are never validated, even in the synthetic setup.

- **Comparison of sufficient conditions vs. actual convergence rates (favorability=4.92).** The paper compares sufficient conditions (Theorems 1 vs. 3) and interprets the differences as convergence-rate advantages (Remark 4: "linear Transformers require smaller batch sizes, fewer iterations"). However, looser vs. tighter sufficient-condition bounds do not directly establish actual convergence-rate differences — they describe the derived bounds, not necessarily the underlying rates. The paper acknowledges this is a comparison of "sufficient conditions" (line 187) but the presentation in P2 and Remark 4 could be read as claiming established convergence-rate differences.

- **Interdependent conditions in Theorem 1 not discussed for simultaneous satisfiability (favorability=7.29).** For instance, condition (ii) requires Vβ⁻⁴ ≲ κₐ ≲ Vβ(1-pₐ)pₐ⁻¹ε⁻¹, which couples κₐ, V, β, pₐ, and ε. The paper would benefit from a concrete worked example showing parameter choices that simultaneously satisfy all conditions of Theorem 1 and Theorem 2.

- **CQ weakness under-discussed given its significance (favorability=5.99).** Table 1 shows Mamba dropping to 82.73% (vs. linear Transformer's 93.96%) when outliers are placed closest to the query. This is a substantial practical limitation — the gating mechanism's exponential decay with distance (Corollary 2) actively harms performance when outliers are near the query. Given the paper's central claim about Mamba's robustness, this limitation deserves more than one paragraph of discussion, ideally in the conclusion.

### Trivial
None.

## Nice-to-Haves

- Systematically vary l_tr, l_ts, p_a, and α to test whether the α < pₐ·l_tr/l_ts bound empirically predicts the failure point, rather than testing only one point on that bound.
- Provide a concrete worked example of parameter values satisfying all conditions in Theorems 1 and 2 simultaneously.
- Discuss the CQ limitation more prominently (conclusion or abstract) as it represents Mamba's main practical weakness in outlier robustness.
- Clarify the distinction between comparing sufficient-condition bounds and comparing actual convergence rates more explicitly in the main text (not just in the inline acknowledgment at line 187).

## Removed Points

These points were identified in the input review but removed after verification against the paper:

1. **Test-time outlier restriction being undersold** — REMOVED because the paper explicitly states the restriction in the abstract ("unseen outliers that are linear combinations of the training-time outliers"), in P1 ("should contain a positive linear combinations of outlier patterns seen during training"), and in Remark 3. The paper is transparent about this constraint.

2. **Comparison against linear Transformer rather than softmax Transformer** — REMOVED because (a) the paper explicitly frames the comparison as isolating the gating mechanism (Remark 6), (b) the abstract and contributions consistently say "linear Transformers," and (c) the paper states that softmax/multi-head experiments are in Appendix B.1 (assumed to exist). This criticism is scope creep beyond what the paper claims.

3. **"α can approach 1" presentation concern** — REMOVED because the theoretical condition α < min(1, pₐ·l_tr/l_ts) is clearly stated, and the bound can approach 1 when parameters are chosen accordingly. The experiments test α up to 0.8 (above the linear Transformer's 0.5 threshold), which validates the key qualitative prediction.

4. **Labels of outlier examples being pure noise** — REMOVED because this is by design in the data model (Definition 1: outliers have random labels), appropriate for modeling label noise and data poisoning.

5. **A = -Iₘ assumption** — REMOVED because this is a standard simplifying assumption following Theorem 1 of Gu & Dao (2023), appropriate for a theoretical analysis.

## Novel Insights

None beyond the paper's own contributions. The theoretical analysis of Mamba training dynamics for ICL is itself the novel contribution.

## Suggestions

- Provide a concrete worked example of parameter values satisfying all conditions in Theorems 1 and 2 simultaneously, demonstrating that the interdependent bounds are realizable for reasonable parameter ranges.
- Consider validating the theory more directly by systematically varying l_tr, l_ts, p_a, and α to test whether the α < pₐ·l_tr/l_ts bound predicts the empirical failure point.
- Discuss the CQ limitation more prominently (conclusion or abstract) as it represents Mamba's main practical weakness in outlier robustness.
- Clarify the distinction between comparing sufficient-condition bounds and comparing actual convergence rates more explicitly.

## Score and Decision

**Calibration anchors:**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| `8QTpYC4smR.md` (LLM survey) | 1.00 | R1 | No | Unrelated topic, not comparable |
| `YK8eO7BEkJ.md` (Normalization in Mamba) | 3.00 | R1 | No | Empirical Mamba paper, no theory of ICL |
| `VtP7CamOR5.md` (Mamba Neural Operator) | 3.00 | R1 | No | PDE application, not comparable |
| `u1cQYxRI1H.md` (Illumination harmonization) | 10.00 | R1 | No | Completely different topic, ignore |
| `uqLQjtSdFN.md` (Functional Gradients for ICL) | 3.57 | R1 | Yes | ICL theory paper, scored lower due to limited novelty and unclear contribution. Our paper has stronger novelty (first training dynamics for Mamba) and clearer theorems. |
| `Jwtpbhheoy.md` (ICL Uncertainty Quantification) | 5.00 | R1 | Yes | ICL theory paper with generalization bounds. Our paper provides both convergence and generalization analysis vs. only generalization bounds. |
| `STUGfUz8ob.md` (Transformers reason abstract symbols) | 7.60 | R1 | Yes | Strong theory paper with broader impact and more extensive experiments. Our paper is more niche but similar in structure. |
| `n7n8McETXw.md` (Training Nonlinear Transformers for CoT) | 6.50 | R2 | Yes | **Most comparable anchor.** Same paper type: first training dynamics analysis for a specific architecture, one-layer, synthetic experiments, orthogonal pattern data model. Our paper has comparable theoretical novelty, cleaner math (no formula errors), but more limited experiments (no real data, only qualitative α-threshold validated). |
| `aKJr5NnN8U.md` (In-context vs In-weight Learning) | 6.50 | R2 | Yes | Strong theory with real LLM experiments but criticized for theory-experiment gap. Our paper has cleaner theory-experiment alignment. |
| `gK1rl98VRp.md` (Auto-Regressive Next-Token Prediction) | 6.00 | R2 | No | ICL emergence theory paper with similar methodology. |
| `AL1fq05o7H.md` (Mamba original paper) | 6.25 | R2 | No | Architecture proposal, different type. |

**Round 1 bracket**: 5.5–7.0. **Round 2 narrowing**: Compared against the closest anchor `n7n8McETXw` (6.50, accept). Our paper has comparable theoretical novelty but more limited experiments (the CoT paper's experiments more directly validated its theory, while our paper tests only the qualitative α-threshold and mechanism, not the quantitative bounds). The anchor `aKJr5NnN8U` (6.50, accept) had stronger real-LLM experiments. Our paper has cleaner theory-experiment alignment than both anchors but less experimental scope.

**Final placement**: 6.0 — a solid theoretical contribution with clear, testable predictions and honest limitations, but the experimental validation is narrower than comparable accepted papers.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>