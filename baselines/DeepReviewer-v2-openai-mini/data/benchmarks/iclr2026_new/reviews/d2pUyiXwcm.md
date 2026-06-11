## Summary
# Final Review Report

## Summary

This paper introduces **Simulation-Calibrated Scientific Machine Learning (SCaSML)**, a framework that improves pre-trained surrogate models (PINNs, GPs) for high-dimensional PDEs at inference time via defect correction. The core idea is to derive a PDE for the surrogate error — the **Structural-preserving Law of Defect** — which retains the semi-linear structure of the original problem, enabling correction via multilevel Picard (MLP) Monte Carlo simulation. The authors prove a product-form error bound (Theorem 2.5) and demonstrate 20–80% error reduction on four benchmark PDE problems up to 160 dimensions.

**Overall assessment:** The paper addresses a relevant and timely problem — combining the speed of machine-learned surrogates with the rigor of numerical simulation. The core idea of deriving an error PDE that preserves structure is mathematically sound and the empirical results show consistent improvement. However, the manuscript has several significant weaknesses: (1) the convergence rate argument conflates surrogate error with PDE residual, which may invalidate the claimed rate improvement; (2) the experimental comparisons are not controlled fairly — the naive MLP baseline uses poorly tuned hyperparameters; (3) the "first" and "inference-time scaling" claims are overstated relative to the technical novelty; (4) the computational overhead (10–170x) is not adequately discussed; and (5) key theoretical details and assumptions are deferred to the appendix, making central claims hard to verify from the main text. The paper makes a useful contribution but requires substantial revision before publication.

## Strengths
1. **Intellectually sound core idea.** The derivation of the Structural-preserving Law of Defect — showing that the error PDE retains the semi-linear structure of the original problem — is mathematically clean and principled. This insight enables the use of existing Monte Carlo PDE solvers (MLP) in a plug-and-play manner, which is a useful contribution to the SciML literature.

2. **Consistent empirical improvement across diverse settings.** The paper demonstrates error reduction (20–80% relative $L^2$) across four distinct PDE families (convection-diffusion, viscous Burgers, HJB/LQG, diffusion-reaction) using two surrogate types (PINN and GP). The improvement is observed in all 22 problem/dimension combinations reported in Table 1, with SCaSML achieving the lowest error in every case. This breadth of validation strengthens the claim of versatility.

3. **Product-form error bound theory.** Theorem 2.5 and the associated scaling law (Corollary 2.6) provide a formal characterization of why error reduction occurs: the final error is the product of the surrogate error and the MLP simulation error. This multiplicative relationship is both intuitive and theoretically meaningful, suggesting the method becomes more efficient as surrogates improve.

4. **Elastic compute concept.** The framing of inference-time compute vs. accuracy trade-off (elastic compute) is practically relevant. In applications where real-time constraints are relaxed but accuracy demands are high (e.g., offline scientific computing, rare-event analysis), the ability to allocate more compute at inference time without retraining is valuable.

5. **Reproducibility-oriented implementation.** The use of JAX and DeepXDE, along with detailed experimental configurations (network architecture, optimizer hyperparameters, collocation point counts, clipping thresholds), provides a solid foundation for reproducibility.

## Weaknesses
### W1 (Major) — Convergence rate argument conflates surrogate error and PDE residual (F5)

The central claim of faster convergence (Corollary 2.6) relies on the argument in Section 2.1 (Page 3, "Intuition for Faster Convergence") that the PDE residual $\epsilon$ decays at the same rate $m^{-\gamma}$ as the surrogate error $e(\tilde{u})$. However, $\epsilon$ involves second-order derivatives of $\hat{u}$ (through the $\mathcal{L}$ operator), while $e(\tilde{u})$ is measured in $W^{1,\infty}$ (only function value and first derivatives). Higher-order derivative errors of neural networks can converge significantly slower than function values, especially in high dimensions — a well-known issue in PINN theory. Without an explicit bound linking $\|\epsilon\|_\infty$ to $e(\tilde{u})$ using the PDE structure and smoothness assumptions, the claimed rate improvement from $m^{-\gamma}$ to $m^{-\gamma-1/2}$ is not substantiated.

**Required fix:** Provide an explicit bound connecting the PDE residual $\epsilon$ to the surrogate error measure $e(\tilde{u})$, or add a separate assumption bounding $\epsilon$ directly, and revise the convergence intuition accordingly. This is publication-critical.

### W2 (Major) — Unfair experimental comparison for the naive MLP baseline

The "naive MLP" baseline is used to demonstrate that SCaSML succeeds where pure simulation fails. However, the comparison is not controlled fairly:

- **Differing clipping thresholds:** In the LQG experiment (Section 3.3), the naive MLP uses a clipping threshold of 10 while SCaSML uses 0.1 — a 100x difference. The paper attributes this to the "smaller magnitude of the defect," but clipping is a critical stability hyperparameter. Without sweeping this parameter for the MLP baseline, it is unclear whether the MLP's catastrophic failure ($L^2$ error > 5.0) is genuine or an artifact of poor tuning. Standard MLP methods are known to work for high-dimensional HJB equations.

- **Fixed 2-level architecture:** All MLP and SCaSML experiments use $n=2$ levels with $M=10$. This shallow configuration may disadvantage the MLP solver. The number of levels should be treated as a tunable hyperparameter.

- **Missing variance reporting:** Table 1 reports only point estimates without standard deviations. Given the stochastic nature of both MLP sampling and surrogate training, readers cannot assess whether reported improvements are statistically significant. The claim "$p \ll 0.001$" is made in the text but the test details, sample sizes, and multiple testing corrections are not provided in the main paper.

**Required fix:** Report all results with mean $\pm$ std over $\ge 3$ seeds, sweep clipping thresholds and MLP levels for the baseline, and include explicit statistical test details. This is publication-critical if the "naive MLP fails" narrative is central.

### W3 (Major) — Overstated novelty claims without literature verification (Deferred)

The paper makes strong "first" claims:
- "the first physics-informed inference-time scaling framework"
- "to our knowledge, the first derivation that preserves the semi-linear structure"
- "the first inference-time scaling algorithm that enhances the learned surrogate solution"

Defect correction is a well-established technique in numerical analysis, and combining surrogate models with error PDEs has been explored in various forms (a posteriori error estimation, residual-based adaptivity, etc.). The "inference-time scaling" framing borrows from the LLM literature but the underlying technique is classical. The claim of structural-preservation in Fact 2.3 follows directly from algebraic manipulation of the original PDE — it is a useful observation but the derivation itself is not novel.

**Note:** External literature verification could not be performed in this run (Retrieval-Disabled Mode). These novelty conclusions are marked as **deferred manual verification**. The authors should carefully scope their claims with explicit comparisons to the closest prior work and adopt "to our knowledge" qualifications consistently.

### W4 (Moderate) — Theorem 2.5 and Corollary 2.6 are not verifiable from the main text

The proof sketch in Section 2.4 is highly compressed (one paragraph) and key assumptions (Assumptions E.2–D.7) are entirely deferred to the appendix. The error term $E(M,N)$ in Eq. (9) is described as "depending on $M$ and $N$ but independent of the surrogate," but its explicit form (e.g., does it scale as $M^{-1/2}$? What is the $N$ dependence?) is not given. Without this, the bound is not quantitatively interpretable and the claimed improvement in Corollary 2.6 cannot be assessed from the main text alone.

**Required fix:** (a) Clearly define $e(\tilde{u})$ as a scalar error measure. (b) Provide the explicit form of $E(M,N)$ in the main text. (c) Expand the proof sketch to show the decomposition structure. (d) State which regularity assumptions are specific to this work vs. standard in MLP analysis.

### W5 (Moderate) — Cost-benefit analysis is absent despite large computational overhead

Table 1 shows SCaSML is 10–170x slower than the surrogate alone (e.g., LQG 160d: SR 0.34s vs. SCaSML 29.95s). Yet the paper does not discuss whether the additional compute is worthwhile relative to training a larger surrogate. The "elastic compute" concept is presented as a benefit, but without a Pareto-style analysis of error vs. total compute time, the practical value proposition is unclear. For small improvements (6.6–10.9% on DR), the 50–80x overhead is particularly hard to justify.

**Required fix:** Add a computational efficiency analysis comparing error vs. total wall-clock time for (a) surrogate-only with varying capacity, (b) MLP-only with varying budget, and (c) SCaSML with varying inference budget. This can be a single additional figure.

### W6 (Minor) — Spectral bias justification does not apply to GP surrogates

Section 2.1 justifies Monte Carlo correction via spectral bias (neural networks learn low frequencies first, so residual is high-frequency). However, Gaussian Process surrogates do not share this spectral bias. The paper successfully tests SCaSML with GP surrogates (VB-GP experiments), but the motivation paragraph is written as if NP-complete generality applies. The spectral bias argument should be scoped to NN surrogates, and a separate justification (e.g., defect magnitude reduction) should be given for GP surrogates.

### W7 (Minor) — Conclusion introduces unsupported claims and lacks limitations

The conclusion states "the surrogate handles the low-frequency part, allowing the simulation to focus on the small high-frequency residual" — a claim that is never verified experimentally (no spectral analysis is performed). The conclusion also entirely omits limitations: the method requires differentiable surrogates, has 10–170x computational overhead, requires clipping threshold tuning, and targets only semi-linear parabolic PDEs.

### W8 (Minor) — LCD experiment is a trivial benchmark

The linear convection-diffusion equation has an explicit linear solution. Using it as a primary benchmark gives limited insight into the method's performance on the target class (semi-linear PDEs). It should be moved to an appendix or replaced with a more challenging problem.

## Score
**Final Score: 6/10**

**Rationale:** The paper makes a useful conceptual contribution — combining defect correction with MLP simulation for inference-time refinement of PDE surrogates. The core idea is mathematically sound, and the empirical validation is broad (4 problem classes, 2 surrogate types, up to 160 dimensions). However, the score is constrained by:

- **Novelty (moderate):** The technical core (defect correction + MLP solver) is a well-motivated combination of existing ideas. The paper's "first" claims are overstated relative to the actual technical increment. Novelty conclusions are deferred for external verification. (Sub-score: 5/10)

- **Validity of theoretical claims (moderate concern):** The central convergence rate argument (W1) conflates surrogate error and PDE residual in a way that may invalidate the claimed improvement. This is a non-trivial gap that needs resolution. (Sub-score: 5/10)

- **Experimental rigor (moderate concern):** Unequal hyperparameter settings between SCaSML and the naive MLP baseline (W2), missing variance reporting, and absence of cost-benefit analysis weaken the empirical case. However, the consistent improvement across all settings suggests the method has genuine value. (Sub-score: 6/10)

- **Presentation and reproducibility (adequate):** Experimental details are well-documented but the main text defers too many theoretical details to the appendix. The conclusion lacks limitations. Writing quality is generally clear. (Sub-score: 7/10)

- **Research value (moderate-high):** The elastic compute concept and the plug-and-play framework address a real need in scientific computing. The product-form error bound provides useful theoretical insight. (Sub-score: 7/10)

**Overall:** The paper represents a solid step toward integrating machine learning surrogates with classical numerical methods, but the convergence theory needs tightening, the experiments need fairer baselines, and the claims need more careful scoping. With substantial revision addressing the major weaknesses, this work could make a meaningful contribution to the SciML community.