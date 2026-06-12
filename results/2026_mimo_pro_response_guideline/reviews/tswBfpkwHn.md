Now I have enough information to write the final review. Let me compile it:

## Summary

This paper provides the first theoretical analysis of one-layer Mamba's training dynamics for in-context learning (ICL), with a focus on robustness to additive outliers in prompts. The key technical contribution is decomposing one-layer Mamba into a linear attention layer plus a nonlinear gating layer (Eq. 3), which enables direct comparison with linear Transformers (which lack gating). The central result is that Mamba can tolerate outlier fractions approaching 1 at test time, while linear Transformers are fundamentally limited to α < 1/2. Mechanistic insights (Corollaries 1–2) show that linear attention selects same-pattern context examples while nonlinear gating suppresses outliers and induces exponential positional decay.

## Strengths

- **First formal decomposition of one-layer Mamba into linear attention + nonlinear gating (Eq. 3):** The closed-form derivation reduces Mamba to a tractable analytical form where linear Transformers emerge as a special case (setting G_{i,l+1}=1 for all i), enabling rigorous apples-to-apples comparison of training dynamics, generalization, and outlier robustness. This decomposition is the analytical backbone of the entire paper.

- **Quantitative α < 1 vs. α < 1/2 threshold, well-supported by theory and experiments (Theorems 2 & 4, Figure 2):** Theorem 2 permits α < min{1, p_a·l_tr/l_ts} for Mamba (approaching 1), while Theorem 4 restricts linear Transformers to α < 1/2. Figure 2 empirically validates this divergence across three distinct outlier types (label flipping, targeted labeling, random labeling), with Mamba maintaining classification error below 10⁻² at α ≈ 0.8 while linear Transformer error rises sharply past α > 0.5.

- **Clean mechanistic characterization via Corollaries 1–2:** Corollary 1 proves linear attention concentrates weight on same-pattern examples (Eq. 16), while Corollary 2 proves nonlinear gating suppresses outliers to O(poly(M₁)⁻¹) (Eq. 17) and induces exponential decay Θ(1/2^{j-1}) for clean examples by distance from query (Eq. 18). Figures 3–4 directly validate these mechanisms. This dual-role characterization of gating—enabling robustness while also creating positional vulnerability—is the paper's most insightful contribution.

- **Methodologically sound Transformer comparison:** Setting G_{i,l+1}=1 is the correct ablation to isolate the gating effect—the only structural difference between the two models. Remark 6 explicitly scopes the comparison to one-layer single-head linear Transformers, and the authors acknowledge that practical Transformers with softmax attention have their own nonlinearities.

- **Transparent reporting of positional vulnerability (Table 1):** The three-layer experiment honestly reveals that Mamba accuracy drops to 82.73% when outliers are closest to the query (CQ) vs. 99.73% (FQ), mechanistically explained by the same exponential decay in Corollary 2. This nuanced finding strengthens the paper's credibility.

## Weaknesses

### Fatal
None.

### Major

- **Theorem 2 Condition (a) restricts test-time outlier generalization to positive-affine combinations of training outliers (lines 167–171):** Test-time outlier patterns must belong to V' = {v | v = Σλᵢvᵢ* + u with Σλᵢ ≥ L > 0}, meaning Mamba does not generalize to arbitrary unseen outlier directions—only those sharing a positive-affine relationship with training outliers. The L > 0 constraint is notable: if coefficients sum to zero or are negative, the guarantee breaks. This substantially qualifies the headline "robustness to unseen outliers" claim. The paper mentions this condition but does not discuss its practical implications (what real-world outlier distributions satisfy this? what happens when it's violated?). A paragraph-length discussion of what this condition buys and excludes would significantly improve the paper.

### Minor

- **Positional vulnerability from exponential gating decay limits the robustness claim (Table 1, lines 267–283):** When outliers cluster near the query (CQ setting), Mamba accuracy drops to 82.73% while linear Transformer maintains 93.96%. The paper acknowledges this and Corollary 2 explains it mechanistically, but the "α → 1" robustness claim in the abstract holds only when outliers are not concentrated near the query. This condition is not formally captured in Theorem 2. Including an explicit positional condition or at least a more prominent caveat in the abstract/introduction would be beneficial.

- **Thin experimental section in the main text (Section 4):** Only one hyperparameter configuration (d=30, M₁=6, M₂=10, V=3, δ=0.2, β=3, κ_a=2) is tested. No sensitivity analysis varying dimension, number of patterns, or outlier magnitude is presented in the main text (though appendix experiments exist). This limits confidence that the theoretical bounds are predictive across parameter regimes rather than post-hoc explanatory for a single setting.

- **Brief conclusion (4 sentences, line 287):** Given the rich mechanistic insights from Corollaries 1–2 and the practical implications for Mamba-based model design, a more thorough discussion of implications and future directions would add value.

### Trivial
- Parser artifact "(200)" on line 61 should be "(2)" referencing equation 2. (This is a PDF parsing issue, not a paper error.)

## Nice-to-Haves
- Formalize the positional sensitivity as an explicit condition on outlier distribution in Theorem 2.
- Add sensitivity analysis on κ_a and M₁ in main-text experiments to demonstrate that theory predicts practice.
- Discuss the connection between the sparse-pattern binary classification setup and practical ICL tasks.
- Expand the conclusion to discuss implications for designing robust Mamba-based models or prompt engineering strategies.

## Removed Points
These points are flagged to be removed, treat them with caution:

- **Harsh critic claim that the abstract doesn't specify "linear" Transformer:** Factually wrong. Line 9 of the abstract explicitly states "the proportion of outliers exceeds the threshold that a **linear Transformer** can tolerate." The paper consistently uses "linear Transformer" throughout.
- **"Weak Transformer baseline" concern:** The harsh critic correctly identifies this is NOT actually a problem—comparing Mamba to a linear Transformer with gating removed is the correct ablation design, and Remark 6 transparently scopes the comparison. The authors are admirably honest about this.
- **Parser artifact "(200)" on line 61:** Confirmed as a PDF parsing artifact, not an author error.
- **"Hard Rule" compliance:** All cited models, tools, benchmarks, and references are treated as existing and released. No claims about unreleased resources.

## Novel Insights

The paper's most novel insight is the identification of nonlinear gating as a dual-mechanism driver of Mamba's ICL: it simultaneously enables outlier suppression (Eq. 17, gating values near zero for outlier-containing examples) and induces exponential positional decay (Eq. 18, gating values decay as Θ(1/2^{j-1}) with distance from query). This single mechanism explains both Mamba's superior robustness advantage over linear Transformers (outlier suppression) and its specific vulnerability (positional sensitivity when outliers cluster near the query, Table 1). This is a clean, unifying theoretical result that connects previously separate empirical observations (Park et al., 2024; Wang et al., 2025) to a single architectural feature.

## Suggestions
- Add a paragraph discussing what the L > 0 constraint in Theorem 2 Condition (a) buys and excludes. What happens when coefficients sum to zero or are negative?
- Include at least a sensitivity analysis on κ_a and M₁ in the main text to strengthen the claim that theory predicts practice.
- Expand the conclusion to discuss practical implications for Mamba-based model design and prompt engineering strategies that exploit or mitigate the positional sensitivity.
- Consider adding the positional sensitivity caveat to the abstract/introduction's robustness claims.

---

**Calibration Report:**

Round 1 bracketing anchors retrieved:
- **Strong reject (0–1.5):** 8QTpYC4smR (1.0, survey/reject), 5kMwiMnUip (1.4, jailbreak/reject), P49gSPmrvN (1.0, UMAP/reject) — not topically similar, serving as floor anchors.
- **Weak reject (1.5–3.5):** VtP7CamOR5 (3.0, Mamba Neural Operator/reject), cagNCwQEEN (3.4, multimodal Mamba/reject), YK8eO7BEkJ (3.0, Mamba normalization/reject), 4y3GDTFv70 (3.25, latent space theory/reject) — Mamba-related but empirical or weak theory.
- **Borderline reject (3.5–5.5):** i9RTCC6whL (4.67, Mamba Lyapunov stability/reject), 52XG8eexal (4.0, SSM ICL gradient descent/reject), iVy7aRMb0K (4.5, Mamba mimetic initialization/reject), HuBFimORiz (4.33, ICL Markovian dynamics/reject) — closer topically but rejected for less complete analyses.
- **Borderline accept (5.5–7.5):** AL1fq05o7H (6.25, Mamba original paper/reject!), aKJr5NnN8U (6.5, in-context vs in-weight/accept), gK1rl98VRp (6.0, auto-regressive ICL/accept), ikwEDva1JZ (6.5, ICL with representations/accept), n7n8McETXw (6.5, CoT nonlinear Transformer theory/accept), vSh5ePa0ph (6.75, ICL linear regression/accept), jwsPS8yRe4 (6.0, trained Transformer ICL/accept), 8p3fu56lKc (6.0, optimal ICL linear attention/accept).
- **Strong accept (7.5–8.5):** GRMfXcAAFh (8.0, Oscillatory SSMs/accept), SPS6HzVzyt (8.0, context-parametric inversion/accept), Tzh6xAJSll (7.6, scaling laws/accept), STUGfUz8ob (7.6, abstract reasoning/accept).
- **Very strong accept (8.5+):** No results.

Round 1 bracket: **5.5–7.5** (between borderline accept papers).

Round 2 narrow pass: Anchored against n7n8McETXw (6.5, CoT nonlinear Transformer theory — most structurally analogous: first theoretical analysis of nonlinear attention variant for ICL, similar limitations), vSh5ePa0ph (6.75, ICL linear regression theory — well-developed theory but simpler setting), and 52XG8eexal (4.0, SSM ICL gradient descent — similar topic but less complete, rejected).

**Final score rationale:** The paper under review is most comparable to n7n8McETXw (6.5, accepted): both are first theoretical analyses of nonlinear attention variants for ICL with distribution-shifted test data, both provide convergence and generalization proofs with clean mechanistic insights, and both have similar limitations (simplified architecture, data assumptions). The Mamba paper has the additional advantage of a strong comparative result (α < 1 vs. < 1/2) that the CoT paper lacks, but also has the restrictive Theorem 2 Condition (a) and positional vulnerability. These factors roughly balance, placing this paper at 6.5.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>