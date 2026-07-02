Now let me write the final consolidated review with proper formatting.

## Summary

This paper introduces SCaSML, a framework that improves pre-trained surrogate PDE solvers (PINNs, GPs) at inference time by deriving a "Structural-preserving Law of Defect" — a PDE that describes the surrogate's error while preserving the semi-linear structure of the original problem. This defect PDE is solved using Multilevel Picard (MLP) Monte Carlo simulation at inference time to produce a correction. The paper proves a product-form error bound and demonstrates consistent error reduction (20–80%) across four PDE families up to 160 dimensions.

## Strengths

- **Clean mathematical derivation preserving the semi-linear structure (Fact 2.3).** The derivation showing that the defect PDE inherits the semi-linear structure of the original problem is non-trivial and well-presented. This structural preservation is what makes the Monte Carlo correction step feasible for high-dimensional problems, and the paper correctly distinguishes this from classical finite-element defect correction, which relies on asymptotic error expansions that neural networks do not provide (Section 2.2, lines 125–129).

- **Product-form error bound (Theorem 2.5).** Showing that the final error is bounded by the product of the MLP simulation error and the surrogate model error — rather than their sum — is a genuinely informative theoretical result. It implies that improving either component pays compound dividends. The corollary on reduced computational complexity (Corollary 2.6) is a clean consequence.

- **Broad empirical coverage across high-dimensional settings.** The paper tests on four distinct PDE families (linear convection-diffusion, viscous Burgers, Hamilton-Jacobi-Bellman, diffusion-reaction) up to 160 dimensions, with two surrogate types (PINNs and GPs). SCaSML consistently achieves the lowest error across nearly all settings in Table 1, and the inference-time scaling behavior (Figure 3b) visually confirms the expected trend.

## Weaknesses

### Major

- **The main experimental comparison (Table 1) does not control for total compute budget, yet the paper's strongest practical claim depends on such a comparison.** SCaSML adds substantial computational overhead relative to the surrogate alone (e.g., 20× for VB-PINN 20d, 36× for VB-GP 20d, 88× for LQG 160d, 234× for DR 160d). The abstract claims "a smaller base PINN can outperform a larger PINN under the same inference-time compute budget by spending its additional computation on targeted refinement rather than parameter count" (line 33), but this comparison is deferred to Appendix G.7 (stripped from the review copy). The central Table 1 compares SCaSML (surrogate + expensive correction) against a lightly trained surrogate used alone — not against a surrogate that received comparable total compute. Without a fixed-budget comparison in the main text, the reader cannot assess whether the 20–80% error reduction justifies the 20–234× cost increase, or whether simply training the surrogate longer / with more collocation points would achieve comparable gains. This gap undermines the paper's core practical narrative.

### Minor

- **Asymmetric clipping thresholds for three of four problem families, without a sensitivity analysis.** For VB (1.0 vs. 0.01, line 242), LQG (10 vs. 0.1, lines 250–252), and DR (10 vs. 0.01, line 296), the naive MLP and SCaSML use clipping thresholds differing by 100–1000×. The paper explains that SCaSML can use smaller thresholds because the defect is smaller. However, clipping is a strong nonlinear modification that affects solver variance properties. The asymmetry is in the direction that gives the naive MLP *more* freedom (less restriction), so it does not obviously disadvantage the baseline — but a sensitivity study showing both methods under identical clipping policies (or without clipping) would strengthen confidence that the performance gap is not partially an artifact of hyperparameter choice. (Note: LCD uses the same threshold for both (line 234), partially addressing this concern.)

- **The heuristic convergence rate derivation in Section 2.4 oversimplifies the dependence structure.** The main text presents m^{−γ−1/2} as a generic improved rate, but the derivation implicitly assumes the residual ε ∼ m^{−γ} follows from surrogate error e(ũ) ∼ m^{−γ} in a straightforward way. As Assumption 2.4 acknowledges, this requires W^{1,∞} control — the PDE operator involves second derivatives that can amplify errors non-trivially. The product-form bound in Theorem 2.5 is stated as a clean factorization, but the simulation error E(M,N) is not fully independent of the surrogate since the defect PDE's nonlinearity $\tilde{F}$ depends on the surrogate through F(û + ũ) − F(û). The rigorous treatment is deferred to the appendix, which makes the main text's framing appear more generic than the assumptions warrant.

### Trivial

- Table 1 contains typesetting issues with the SCaSML name appearing as "SCA<sup>2</sup>SM<sup>1</sup>" and "SCSML" in different places.

## Nice-to-Haves

- Move a representative fixed-budget comparison (SCaSML + small surrogate vs. larger surrogate trained with the same budget) into the main text to directly substantiate the abstract's strongest claim.
- Add a sensitivity study on clipping thresholds for the naive MLP on at least one problem setting, showing error vs. threshold to confirm the performance gap is robust.
- A low-dimensional analytical example or Fourier analysis of the residual to support the claim (line 107) that Monte Carlo is well-suited because the residual is high-frequency.

## Removed Points

These points from the input review are removed with justification:

- **"Inference-time scaling framing borrowed from LLMs is misleading"** — The paper uses LLM inference-time scaling as inspiration ("this success inspires our central research question," line 19), not as a claim of mechanism equivalence. The method does add computation at inference time to improve output quality. This is a reasonable analogy.
- **"Firsts claims hard to verify without prior-work discussion"** — Per review policy, missing related-work coverage is not flagged as a weakness when the reviewer cannot independently verify what prior work exists.
- **"No spectral analysis of the residual"** — Moved to Nice-to-Haves; this is an enhancement, not a core weakness.
- **"Quadrature vs. Full-history MLP distinction not evaluated"** — Using one variant consistently is standard experimental practice.
- **"2-level MLP with M=10 means very coarse simulation"** — The method works and shows improvement with these settings.
- Various section-by-section presentation observations (traceability of Figure 3 values, notation inconsistencies) — These are minor and do not affect the paper's substance.

## Novel Insights

The harsh critic correctly identifies that the paper's most impactful experiment — a compute-normalized comparison showing a small surrogate + SCaSML outperforming a larger surrogate under equal budget — is deferred to the appendix and absent from the main text. This creates a gap between the paper's strongest framing ("inference-time scaling," "elastic compute," "smaller PINN outperforming larger PINN") and the evidence presented in Table 1, which compares SCaSML against lightly trained surrogates without controlling for total compute. The critic also usefully notes that the product-bound factorization in Theorem 2.5 is presented as a clean separation but actually depends on non-trivial assumptions (Assumption 2.4's W^{1,∞} control) that link the simulation error to surrogate quality through the defect PDE's nonlinearity.

## Suggestions

1. Include at least one representative fixed-budget experiment in the main text showing SCaSML + small surrogate vs. a larger surrogate trained with the same total compute budget. This directly addresses the paper's strongest claim.
2. Add a brief clipping sensitivity study for at least one problem to confirm the performance gap is not threshold-dependent.
3. Clarify in Section 2.4 that the product-form bound in Theorem 2.5 is conditional on Assumption 2.4, and that the independence of E(M,N) from the surrogate holds under these specific regularity conditions.

## Score and Decision

**Calibration Anchors (all rounds):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| HDmmwwTIlf (char NN + PDE) | 2.50 | R1 | 1D only, sparse experiments — weaker than SCaSML |
| 5rfj85bHCy (HyResPINNs) | 5.00 | R1 | 2 PDEs only, no complexity analysis — similar quality but narrower scope |
| 3ep9ZYMZS3 (Model-agnostic correction) | 5.00 | R2 | 1 benchmark, mixed reviews (8,6,3,3) — similar hybrid-correction idea, SCaSML has broader eval |
| 4KKqHIb4iG (Backprop-free PDE) | 5.60 | R1,R2 | 1-2D only, strong experiments — SCaSML has higher-D and stronger theory |
| wVADj7yKee (SINGER) | 6.33 | R1,R2 | High-D PDEs, theoretical guarantees — SCaSML has cleaner theory but weaker evidence for practical claim |
| x4ZmQaumRg (Active Learning) | 7.00 | R1 | Comprehensive benchmark, but low-D — SCaSML is more ambitious theoretically |

**Round 1 bracket:** 5.0–6.5. The paper has stronger theory and broader high-dimensional evaluation than the 5.0–5.6 anchors (HyResPINNs, Backprop-free PDE training) but a significant evidence gap prevents it from reaching the 6.33–7.0 level (SINGER, Active Learning). The compute-normalized comparison is the decisive missing piece.

**Final score:** 5.5. The paper makes a genuine theoretical contribution and demonstrates consistent error reduction across diverse settings. However, the main experimental table does not control for total compute budget, leaving the paper's central practical claim ("a smaller base PINN can outperform a larger PINN under the same inference-time compute budget") unsubstantiated in the main text. The contribution is worthy of further development, and the paper would be strengthened substantially by moving the fixed-budget comparison into the body and adding a clipping sensitivity analysis.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>