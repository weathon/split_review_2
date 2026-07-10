## Summary

The paper proposes SCaSML, a framework that corrects pre-trained neural PDE surrogates at inference time by (1) deriving a "Structural-preserving Law of Defect" — a new PDE that governs the surrogate's error while retaining the original semi-linear structure — and (2) solving this defect PDE via Multilevel Picard (MLP) Monte Carlo simulation. The key theoretical result is a product-form error bound (Theorem 2.5), showing the final error factorizes as simulation error × surrogate error. Experiments on four high-dimensional PDEs (up to 160d) with PINN and GP surrogates demonstrate error reductions of 20–80%.

---

## Strengths

- **Clean mathematical derivation of the Structural-preserving Law of Defect (Fact 2.3).** Subtracting the surrogate's approximate PDE from the original PDE yields a new PDE for the error that preserves the semi-linear structure. This structural preservation is what makes Monte Carlo correction tractable in high dimensions and distinguishes the approach from classical grid-based defect correction (Sec. 2.2). This is the paper's strongest contribution.

- **Product-form error bound (Theorem 2.5).** The global L² error of SCaSML is bounded by the product of the MLP simulation error and the surrogate model error. This formalizes the intuition that the correction step compounds advantages and is a genuine theoretical result — the cost of correction decreases as the surrogate improves.

- **Empirical scope covering diverse settings.** Experiments span four distinct PDE problems (linear convection-diffusion, viscous Burgers, HJB, diffusion-reaction with oscillatory solution) at dimensions up to 160, with two surrogate families (PINN, Gaussian Process). The method works across both surrogate types, demonstrating it is a plug-and-play corrector.

---

## Weaknesses

### Major

**1. Boundary condition gap between theory and experiments.** The PDE (1) is posed on ℝ^d, and the Feynman-Kac / MLP theory assumes the stochastic process evolves freely on ℝ^d. However, every experiment solves the PDE on a *bounded* domain (hypercube [0,0.5]^d or unit ball B^d) with Dirichlet boundary conditions enforced by the PINN loss. The paper never explains how the Monte Carlo simulation handles domain boundaries (e.g., absorption, reflection, or killing of paths upon exit). Without addressing this, it is unclear whether the numerical results are solving the intended PDE or a different problem with modified boundary treatment. This is a measurable gap between the theory as presented and the experiments as conducted.

**2. Cost-accuracy Pareto analysis absent from the main paper.** SCaSML is 10–234× more expensive than the surrogate baseline (Table 1: LCD 60d: 37.59s vs 0.28s, DR 160d: 86.77s vs 0.37s). The paper claims "fixed-budget efficiency comparisons" in Appendix G.7, but no such analysis appears in the main text. Without a cost-accuracy Pareto curve comparing SCaSML to (a) training a better surrogate longer and (b) running more MLP iterations at the same total budget, the practical claim that SCaSML provides valuable error reduction is unsupported at the level of the main paper. The reader cannot determine whether the error reduction is worth the large runtime increase.

**3. Convergence rate claim in Corollary 2.6 conflates distinct computational budgets.** The argument treats "m training points" (used to fit the surrogate) and "m Monte Carlo paths" (used at inference) as directly comparable units. Training a PINN on m collocation points involves backpropagation through a neural network for thousands of optimizer steps, while evaluating m Monte Carlo paths requires discretizing SDEs along each path — these are fundamentally different computational operations. The heuristic intuition in Section 2 (lines 105, 172) is clearly labeled as intuition, but Corollary 2.6 makes the same rate claim (O(m^{-γ-1/2})) without clarifying the relative cost scaling. Theorem 2.5 (the product bound) is more rigorous; the rate claim in Corollary 2.6 requires assumptions about cost equivalence that are not validated.

### Minor

**4. Unequal clipping thresholds between SCaSML and the naive MLP baseline.** For VB-PINN/GP, LQG, and DR, SCaSML uses 10–1000× smaller clipping thresholds than the naive MLP (1.0 vs 0.01, 10 vs 0.1, 10 vs 0.01). The paper argues that SCaSML can use smaller thresholds because the defect is inherently smaller, which is reasonable. However, the naive MLP baseline is compared with much looser clipping, so it is unclear how much of the improvement over MLP stems from the defect-correction framework versus parameter tuning. For LCD, thresholds are equal. Since the paper's primary comparison is surrogate vs SCaSML (with MLP included "for reference"), this does not invalidate the main claim, but it weakens the MLP baseline comparison.

**5. No uncertainty quantification in main results.** Table 1 reports only point estimates for all error metrics (L², L∞, L¹) and runtimes. For a method whose core mechanism is Monte Carlo estimation, the absence of error bars, confidence intervals, or variance estimates in the main results is notable. (The paper mentions p ≪ 0.001 significance tests in Appendix G.4, but the headline Table 1 lacks any measure of variability.)

### Trivial

**6. Notation inconsistency.** The surrogate is denoted $\hat{u}$ (hat) in Section 2 but switches to $\tilde{u}$ (tilde) in Section 3. Moreover, Section 3 uses $\tilde{u}$ for both the surrogate and the correction term in the same equation ("$u = \tilde{u} + \tilde{u}$"), creating confusion.

**7. Theorem 2.5 uses a mixed norm** $\sup_{(t,x)} \|\cdot\|_{L^2}$ which is non-standard (supremum of an L² norm over points, rather than an L² norm over the domain).

---

## Nice-to-Haves

- A sensitivity analysis showing how performance varies with MLP parameters (number of levels, base samples M) beyond the single configuration (2 levels, M=10) used in all experiments.
- Clarification of whether the MLP correction is per-query (as suggested by Remark 2.2) or a global solve — this distinction matters for computational cost and the "inference-time scaling" framing.

---

## Removed Points

These points from the input review are not included above:

- **LLM analogy is "superficial" / "first physics-informed inference-time scaling" is overclaimed.** These are framing preferences that do not affect the technical contribution. The paper's LLM reference is a motivation device, not a technical claim.
- **Missing related works.** Cannot be verified without external sources.
- **MLP description too compressed, cross-references missing appendix equations.** The appendix was stripped by the PDF parser; this is not assessable from the provided text.
- **LCD is "not a stress test."** It is presented as a sanity check, which is appropriate.
- **DR improvements are small and expensive.** The paper honestly reports this data; it is not a methodological flaw.
- **Monte Carlo gradient cost (needing ∇_y û).** This is intrinsic to the approach and acknowledged in the method description.
- **The critic's criticism about "boundary condition issue is fundamental" being framed as "structural — missing component."** Retained and downgraded to Major (not Fatal) because the Feynman-Kac formula can be adapted to bounded domains with stopping times, but the paper's failure to address it at all is a genuine gap.

---

## Novel Insights

None beyond the paper's own contributions. The reviews surface no observation about the method or results that the paper does not already state.

---

## Suggestions

1. **Address the boundary condition gap.** Either restrict the theory to bounded domains with appropriate boundary conditions incorporated into the Feynman-Kac/MLP formulation, or explain why the ℝ^d theory applies to the bounded-domain experiments.
2. **Include a cost-accuracy Pareto plot in the main paper** for at least one problem, comparing SCaSML vs. better-trained surrogates and more MLP iterations at matched compute budgets. This is the minimal evidence needed to support the "elastic compute" claim.
3. **Equalize clipping thresholds** between SCaSML and the naive MLP baseline (or run the MLP baseline with the same aggressive clipping to check robustness).
4. **Add error bars** (e.g., standard deviation over multiple simulation runs) to the main results table.
5. **Qualify Corollary 2.6** by stating the cost equivalence assumption explicitly, or present the rate as a heuristic scaling intuition rather than a proven result.
6. **Fix the notation inconsistencies** between Sections 2 and 3.

---

## Score and Decision

**Calibration anchors (all rounds):**

| Path | Avg Score | Round | Itemized? | Comparison to this paper |
|------|-----------|-------|-----------|--------------------------|
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/5sPgOyyjG5.md | 3.00 | R1 | Yes | PINN+FeynmanKac estimator — weaker theory, smaller experiments, worse presentation. Our paper is significantly stronger. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/R5FzCFR5yU.md | 3.33 | R1 | Yes | Hybrid numerical PINNs — contrived examples, missing literature. Our paper has clearer contributions. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/wUaOVNv94O.md | 4.00 | R2 | Yes | Neural net as MC control variate — most similar structurally. Weaker theory, only 2D/3D experiments. Our paper has stronger math and higher-dim experiments. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/3ep9ZYMZS3.md | 5.00 | R2 | Yes | HyPER: RL-based surrogate correction — accepted but only 2D NS, no theory. Comparable quality but different methodology. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/wVADj7yKee.md | 6.33 | R1 | Yes | SINGER: high-dim PDE solver — cleaner evaluation, no boundary gap. Our paper has stronger theory but unresolved gaps. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/HDmmwwTIlf.md | 2.50 | R1 | No | Hyperbolic conservation laws + neural nets — much weaker paper. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/5rfj85bHCy.md | 5.00 | R1 | No | HyResPINNs — similar domain, higher score due to cleaner eval. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/Q9OGPWt0Rp.md | 5.25 | R1 | No | Meta-learning PINNs — comparable score range. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/4KKqHIb4iG.md | 5.60 | R1 | No | Backprop-free neural PDE solvers — slightly higher but different focus. |

**Round-1 bracket:** 4.5–6.0 (between Auto Neural Spatial Integration at 4.00 and SINGER at 6.33).

**Round-2 narrowing:** 4.5–5.5. The paper sits between Auto Neural Spatial Integration (4.00, weaker overall but no boundary gap) and HyPER (5.00, accepted but weaker theory). Its theoretical contribution (product-form bound, defect PDE derivation) is stronger than both, but its unresolved evaluation gaps (boundary conditions, cost analysis) prevent it from reaching the 5.5–6.0 range occupied by SINGER.

**Comparison of rated items:** The paper's strengths (derivation, product bound, empirical scope) receive favorability ratings of 11.4–12.8, comparable to the strongest items in accepted anchors. Its three Major weaknesses (boundary gap at 2.98, convergence conflation at 4.99, cost analysis at 3.39) have notably lower favorability than any weakness in the SINGER anchor (which had only one weakness at 0.05). The boundary-condition gap (2.98) and missing cost analysis (3.39) are the primary drag — they are items that, if addressed, would bring the paper into the 5.5+ range. In their current state, they place the paper in the borderline zone.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>