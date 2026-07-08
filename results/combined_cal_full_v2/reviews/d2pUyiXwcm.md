## Summary

This paper proposes SCaSML, a framework that combines pre-trained surrogate PDE solvers (PINNs, GPs) with Monte Carlo defect correction at inference time. The core insight—the *structural-preserving law of defect*—is that subtracting the PDE approximately satisfied by the surrogate from the original PDE yields a new PDE for the error that retains the semi-linear parabolic structure, making it solvable by the same stochastic methods (Feynman-Kac, Multilevel Picard) that work for the original problem. The paper provides a product-form error bound (Theorem 2.5), claims an improved convergence rate (Corollary 2.6), and validates the method on four PDE types up to 160 dimensions.

## Strengths

- **The structural-preserving law of defect (Fact 2.3) is a genuinely clever and useful insight.** The observation that the defect PDE inherits the semi-linear structure of the original PDE is non-trivial: because the defect PDE remains semi-linear parabolic, it stays amenable to the same stochastic solvers (Feynman-Kac, MLP) that work for the original problem. This is the linchpin of the approach and is mathematically sound (Section 2.2).

- **Theorem 2.5 provides a concrete, testable error bound.** The product-form bound (total error ≤ simulation error × surrogate error) gives a clear engineering principle: invest in a better surrogate and the correction step becomes cheaper multiplicatively. This is the right kind of theoretical claim for this hybrid setting.

- **The empirical scope is reasonably broad for a methods paper.** Four PDE types (linear convection-diffusion, viscous Burgers, HJB, diffusion-reaction) across dimensions 10–160, with two surrogate classes (PINN and GP). The Burgers experiments showing SCaSML can correct both PINN and GP surrogates demonstrate versatility.

## Weaknesses

### Major

- **The convergence rate argument (Corollary 2.6) depends on an unverified assumption about derivative errors.** The claimed O(m^{-γ-1/2}) rate requires that the PDE residual ε—which involves first and second derivatives of the surrogate—scales like the function-value error e(ũ) (Assumption 2.4). For neural network surrogates, derivative errors are known to converge more slowly than function errors (spectral bias, cited by the paper itself). The paper provides no justification that Assumption 2.4 holds for the surrogate classes tested, making the headline convergence claim heuristic rather than guaranteed. This is significant because the improved convergence rate is a central advertised contribution.

- **Asymmetric clipping thresholds compromise the fairness of the empirical comparison in 3 of 4 problem settings.** For VB-PINN (MLP clip = 1.0, SCaSML clip = 0.01), LQG (10 vs 0.1), and DR (10 vs 0.01), the naive MLP is run with thresholds 100–1000× looser than SCaSML. The clipping threshold directly controls numerical stability, so this confounds the method comparison with an uncontrolled hyperparameter difference. LCD uses equal clipping, which is good, but the pattern across the other three problems is concerning. The paper explains this as "reflecting the smaller magnitude of the defect," but this does not resolve the confound.

- **The key practical claim—that a smaller PINN + correction can outperform a larger PINN under the same compute budget—is deferred entirely to the appendix (Appendix G.7).** Without this comparison in the main paper, the practical value proposition cannot be assessed from the presented results. Table 1 shows SCaSML is often 30–200× slower than the surrogate with only modest accuracy gains (e.g., DR at 160d: 7% improvement at 234× the cost). The claim about elastic compute (trade inference time for accuracy) needs empirical support in the main text.

### Minor

- **Notation is inconsistent across sections in a way that impairs readability.** In Sections 2.1–2.2, û is the surrogate and ũ = u − û is the defect. But in Section 3 (line 222), ũ is used for the surrogate itself ("train a baseline surrogate model ũ") and also for the correction term, creating ambiguity. The method name also appears as SCaSML, SCSML, SCa²SM¹, SCA²SM¹, and SCaML across different parts of the text, figures, and Table 1.

- **Table 1 reports only point estimates without uncertainty quantification.** Since SCaSML is a Monte Carlo method, the results are random variables. Standard errors or confidence intervals are needed to assess the reliability of the reported improvements. The abstract claims p ≪ 0.001 significance but this is not visible in the main results.

- **The paper makes "first" claims** ("the first physics-informed inference-time scaling framework," "the first inference-time scaling algorithm") that are not essential to the contribution and are difficult to substantiate given the long history of defect correction and hybrid surrogate-simulation methods. These should be qualified or removed.

### Trivial

None.

## Nice-to-Haves

- Run a compute-budgeted comparison (smaller PINN + SCaSML correction vs. larger PINN alone) in the main paper.
- For experiments with asymmetric clipping, provide a sensitivity study showing the relative ranking is robust to clipping choice, or use a shared adaptive clipping strategy.
- Discuss when Assumption 2.4 is reasonable and when it fails (e.g., surrogates with poor derivative approximation).
- Add standard errors or confidence intervals to Table 1.

## Removed Points

These points from the input review were removed with justifications:

- **"Product bound is actually additive" (original weakness #5):** REMOVED as factually incorrect. The SCaSML final solution is u_SCaSML = û + ũ_MC, and u − u_SCaSML = ũ − ũ_MC exactly. Therefore ||u − u_SCaSML|| = ||ũ − ũ_MC||, which is exactly what Theorem 2.5 bounds. The product bound applies directly to the total error of the corrected solution, not just a subcomponent.

- **Speculation about LQG reference solution quality:** REMOVED as speculative. The paper states "sufficiently large sample sizes (e.g. 100d)" which is standard practice, and no concrete evidence of an issue is provided.

- **Criticism of LLM framing analogy:** REMOVED. The paper acknowledges this distinction in Remark 2.2. The framing as "inference-time scaling" is a reasonable analogy.

- **Hutchinson estimator being mentioned in one sentence:** REMOVED. This is a standard technique with well-known references; the description is appropriately brief for a methods paper.

- **Pure style/formatting nitpicks and section-by-section commentary:** REMOVED per filtering rules.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Clarify the gap between Assumption 2.4 and what is known about neural network derivative convergence, and present the convergence rate as conditional on this assumption rather than as a guarantee.
- Standardize the clipping procedure or run a sensitivity analysis across clipping thresholds.
- Move at least one compute-budgeted comparison from the appendix to the main text.
- Unify notation throughout (one consistent symbol for the surrogate, one for the defect, one method name).
- Add variance estimates to Table 1.

## Score and Decision

**Calibration Summary.** All anchors retrieved across rounds (aggregating both bracket and narrowing rounds):

| Anchor | Avg Score | Round | Itemized? | Comparison |
|--------|-----------|-------|-----------|------------|
| Hybrid Numerical PINNs | 3.33 | Bracket | Yes | Weaker: contrived examples, missing baselines. Our paper has a genuinely novel insight and broader experiments. |
| Diff. Implicit GNN Solver | 2.00 | Bracket | No | Lower quality, different scope. |
| Adjoint PDE Discovery | 3.00 | Bracket | No | Lower quality. |
| In-Context Neural PDE | 3.40 | Bracket | No | Lower quality. |
| HyResPINNs | 5.00 | Bracket | Yes | Comparable: both are hybrid PDE methods. HyResPINNs has a -1.65 negative weakness; our paper's most negative weakness is only -0.16. |
| Model-Agnostic Knowledge Guided Correction (HyPER) | 5.00 | Bracket | Yes | Similar hybrid ML-simulation spirit but with more damaging weaknesses (-1.54, -1.19). Our paper has stronger core theory. |
| Connecting Solutions PINNs | 5.25 | Narrow | No | Comparable score band. |
| Learning from Integral Losses PINNs | 5.25 | Narrow | No | Comparable score band. |
| PDE-constrained Multi-time-stepping | 5.67 | Narrow | No | Similar hybrid approach. |
| GP for High-Freq PDEs | 5.75 | Bracket | Yes | Has a -4.25 negative weakness (incorrect novelty claims) yet scored 5.75. Our paper's worst weakness is only -0.16. |
| SINGER | 6.33 | Narrow | Yes | All weaknesses positive (non-damaging). Our paper has one slightly negative weakness (-0.16), placing it slightly below. |
| Spectral-Refiner | 6.00 | Narrow | Yes | All weaknesses positive. Our paper has one slightly negative weakness. |

**Round 1 bracket** placed the paper between 5.5 and 7.5 based on topical similarity and strength profiles. **Round 2 narrowing** compared weighted item profiles against SINGER (6.33), Spectral-Refiner (6.00), GP-PDEs (5.75), and HyResPINNs/HyPER (5.00). The key comparison: our paper has slightly higher-weighted strengths (8.14–9.58) than the 5.0-band papers, and its most damaging weakness (-0.16 for the convergence rate assumption) is much less negative than the -1.5 to -4.25 weaknesses found in the 5.0–5.75 band. However, unlike SINGER (6.33) and Spectral-Refiner (6.00) which have entirely non-negative weakness profiles, our paper has a genuinely negative-weight item, which places it below those anchors. The final score of **5.5** reflects: strengths comparable to 6.0-level papers, one genuine but non-fatal negative weakness (convergence rate assumption gap), and several addressable minor issues.

**MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>**