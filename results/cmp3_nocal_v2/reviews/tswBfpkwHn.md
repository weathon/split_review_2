## Summary

This paper provides the first theoretical analysis of SGD training dynamics for a one-layer Mamba model performing in-context learning (ICL) on binary classification tasks with additive outliers, and compares it to a one-layer linear Transformer under identical conditions. The authors prove convergence and generalization bounds, characterize Mamba's mechanism as "attention selects, gating filters" (Corollaries 1–2), and demonstrate a tradeoff: Mamba requires more training effort but tolerates a larger fraction of outlier-containing context examples than the ungated linear attention baseline.

---

## Strengths

1. **First analysis of SGD training dynamics for Mamba ICL.** Prior theoretical work (Li et al., 2024b; 2025b) analyzed global minima of the loss landscape for Mamba-like models. This paper goes further by analyzing whether SGD can actually find solutions, giving quantitative convergence rates and sample complexity bounds — a meaningful distinction since representational capacity and learnability are different questions.

2. **Clean mechanistic decomposition.** Corollaries 1 and 2 provide a crisp characterization: the linear attention layer (W_B, W_C) concentrates weight on examples sharing the query's relevant pattern (Corollary 1, Eq. 16), while the nonlinear gating G_{i,l+1}(w) suppresses outlier-containing examples (Eq. 17) and imposes a position-dependent exponential decay favoring examples closer to the query (Eq. 18). This yields an interpretable "attention selects, gating filters" story that goes beyond the asymptotic/minima analyses of prior work.

3. **Well-controlled comparison isolating the gating mechanism.** The paper compares Mamba against a linear Transformer obtained by setting G = 1, isolating the effect of nonlinear gating as the only architectural difference. The results are internally coherent: Mamba requires larger batch sizes and more iterations (Theorems 1 vs. 3) but achieves better outlier tolerance (α < min(1, p_a·l_tr/l_ts) vs. α < 1/2, Theorems 2 vs. 4). Remark 6 appropriately acknowledges that real Transformers use softmax attention and can achieve robustness through other means.

4. **Empirical validation of key theoretical predictions.** Figure 2 confirms the α < 1/2 threshold for linear Transformers and Mamba's superior robustness across three labeling functions. Figures 3–4 validate Corollaries 1 and 2 on a 3-layer model, showing that the attention/gating patterns predicted by the one-layer theory persist in deeper models. Table 1's CQ result (82.73% for Mamba) provides an honest failure mode consistent with the gating's distance-decay property.

---

## Weaknesses

### Fatal
None.

### Major

1. **Discrepancy between the sufficient condition on α and the experimental regime.** Theorem 2, Condition (c) states that the trained Mamba generalizes if α < min(1, p_a·l_tr/l_ts). In the experiments (Section 4.1, p. 8), p_a = 0.6 and l_tr = l_ts = 20, giving α < 0.6. Yet Figure 2 reports results up to α = 0.8, where Mamba maintains error < 0.01. The paper does not acknowledge this gap.

   This matters because: (i) If the bound is loose, the paper should state this explicitly — the quantitative comparison with Transformers (whose bound α < 1/2 appears tighter given the sharp error increase at α ≈ 0.5 in Figure 2) becomes asymmetric without this acknowledgment. (ii) The abstract and introduction claim theoretical findings are "supported by empirical experiments," but the central quantitative bound (α < 0.6) is not actually tested — experiments go to α = 0.8. The paper presents Theorem 2's bound and Figure 2 as mutually reinforcing without addressing the α ∈ (0.6, 0.8] regime where the sufficient condition does not apply.

### Minor

2. **Oversimplified "α → 1" claim.** The abstract and introduction state that Mamba can maintain accurate ICL "even when the fraction of outlier-containing context examples approaches 1." The actual condition is α < min(1, p_a·l_tr/l_ts), which requires p_a·l_tr/l_ts ≥ 1 for α to approach 1 — meaning either training prompts are mostly outliers (p_a close to 1) or training prompts are longer than test prompts (l_tr > l_ts). These are meaningful constraints not reflected in the headline claim. Moreover, the experiments only test up to α = 0.8 and do not test the regime where α truly approaches 1 (e.g., α = 0.95 with l_tr > l_ts), so the claim is sustained only by the theory's sufficient condition (which itself requires specific conditions), not by direct evidence.

3. **Test-time outliers restricted to positive linear combinations of training outliers.** Theorem 2, Condition (a) (Eq. 11) requires test-time outliers to satisfy v = Σ λ_i v_i^* + u with Σ λ_i ≥ L > 0. This means test outliers must lie in the positive cone spanned by training outlier directions. A genuinely orthogonal outlier direction — one not represented in training — would have Σ λ_i = 0 and would not satisfy the condition. The paper calls this "a wide range of possible outlier patterns" (Remark 3), but the constraint is meaningful: the model can generalize to unseen *magnitudes/combinations* of seen outlier directions but not to structurally novel outlier directions.

4. **Missing variance information for experiments.** Figures 2–4 and Table 1 report single values without standard deviations, confidence intervals, or number of random seeds. Given that the data generation involves random sampling (κ, outlier selection, task selection), reporting variance is important for assessing whether the observed differences between Mamba and the linear Transformer are reliable. This is especially relevant for Figure 2 where Mamba's error is near the noise floor (10⁻²–10⁻⁴).

5. **No discussion of violating Condition (a) of Theorem 2.** The paper does not discuss what happens when test outliers are orthogonal to all training outlier directions — perhaps the most natural definition of a truly "unseen" outlier. This silence limits the paper's characterization of its own scope.

### Trivial
None.

---

## Nice-to-Haves

- Testing the α → 1 regime directly (e.g., α = 0.95 with l_tr > l_ts to satisfy the sufficient condition) would demonstrate that the bound is not vacuous.
- A brief discussion of which assumptions in the stylized data model (orthogonal patterns, equal norms, one relevant + one irrelevant pattern per input) are critical vs. relaxable would help readers assess robustness of the conclusions.

---

## Removed Points

These points were raised in the input review but removed after cross-checking against the paper:

- **"Comparison baseline is linear attention, not a realistic Transformer"** — Removed. The paper consistently specifies "linear Transformers" throughout (abstract, contributions, Section 3.4 title, Remark 6). Remark 6 explicitly acknowledges that real Transformers use softmax attention and that large Transformer models can achieve robustness through other means. The paper's framing is accurate for what it analyzes.

- **"First theoretical analysis claim should acknowledge prior work"** — Removed. The paper's claim is specifically about "training dynamics" (line 29), which is distinct from prior work on loss landscapes/global minima (Li et al., 2024b; 2025b). The paper already acknowledges these prior works and correctly distinguishes its contribution.

- **Various formatting/style/Section-by-Section nitpicks** — Removed per filtering rules.

---

## Novel Insights

None beyond the paper's own contributions.

---

## Suggestions

1. **Resolve the α-bound discrepancy.** A revision should either: (a) acknowledge that the sufficient condition is loose and discuss how loose (e.g., by comparing predicted vs. observed critical α), or (b) adjust the experimental parameters to align with the proven bound (e.g., test at α up to 0.6 with l_tr = l_ts = 20), or (c) tighten the bound. This single fix would substantially strengthen the paper's central claim.

2. **Calibrate the "α → 1" language.** In the abstract and introduction, qualify the claim with the conditions under which it holds (p_a·l_tr/l_ts ≥ 1), or replace it with a statement about "exceeding the 1/2 threshold that linear Transformers can tolerate" which is directly supported by both theory and experiments.

3. **Report variance** for the experimental results.

---

## Score and Decision

This paper makes a genuine theoretical contribution — the first SGD training dynamics analysis for Mamba ICL, a clean mechanistic characterization, and a well-controlled comparison isolating the gating mechanism. The core mathematical analysis appears sound, and the mechanistic story (attention selects, gating filters) is both novel and interpretable.

However, the paper's central quantitative claim about outlier tolerance is presented in a way that creates a misalignment between the theoretical bound (α < 0.6 for the experiment's parameters) and the experimental evidence (success at α = 0.8), without acknowledgment. The headline "α → 1" claim in the abstract oversimplifies the conditions required. These are fixable presentation and calibration issues, not fatal flaws in the mathematical results.

A revised version that explicitly acknowledges the looseness of the sufficient condition and calibrates its claims accordingly would be a solid contribution.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>