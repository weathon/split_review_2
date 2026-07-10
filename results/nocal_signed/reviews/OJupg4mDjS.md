Now let me compile my final review.

## Summary

This paper addresses Geodesic PCA (GPCA) on probability measures in the Wasserstein space. It proposes two algorithms: (1) for centered Gaussian distributions, lifting the problem to the flat space GL_d of invertible matrices (Proposition 3), and (2) for general absolutely continuous measures (GPCAGEN), using the Otto parametrization of Wasserstein geodesics with neural networks. The paper also provides a theoretical characterization of when TPCA (the linearized approximation) deviates from GPCA (Proposition 4).

## Strengths

- **Clean theoretical lifting for Gaussian GPCA (Proposition 3, lines 108–114).** The geodesic PCA problem on SPD matrices is reduced to a least-squares problem in the flat space GL_d, with the only remaining complexity being optimization over rotation matrices Q_i in the fibers. This is a genuinely elegant and sound reduction that produces a computable formulation where none existed for exact GPCA in this setting.

- **Quantitative characterization of TPCA distortion (Proposition 4, lines 136–144).** Provides an explicit expansion showing that the ratio between the true Bures-Wasserstein distance and its linearized approximation at the barycenter depends on (a−b)/(a+b) and cos²θ. This is a concrete, verifiable theoretical result that directly predicts where TPCA will fail, making the paper's theoretical contribution durable.

- **Otto-parametrization avoids ICNNs (Section 4, lines 92–96, 156–162).** The use of Otto's formulation (equation 9) instead of McCann's (equation 10) replaces the architectural constraint of input-convex neural networks with a Hessian eigenvalue monitoring check. This is a genuinely useful design choice that could benefit other Wasserstein-geometry work beyond this paper.

## Weaknesses

### Fatal
None.

### Major

- **GPCAGEN evaluation is insufficiently quantitative to support the paper's claims.** The synthetic dataset with known geodesics (line 238) is mentioned in a single sentence with no quantitative results reported in the main text. The MNIST experiment (lines 258–260) claims the method "successfully recovers" the ground-truth geodesics with no numerical measure of recovery quality (no geodesic distance between recovered and true curves, no error bars, no ablation). The 3D point cloud and landscape image experiments (Section 5.2) rely entirely on visual interpretation ("first component distinguishes chairs from armchairs," "second component separates blue from green") with no measured objective values, no error bars, and no quantitative assessment of how well equation 1 is optimized. The reader cannot distinguish a correctly working method from one that has found a local minimum with visually acceptable but quantitatively poor solutions.

- **Baselines are dismissed rather than engaged with meaningfully.** The paper states TPCA comparison is "not meaningful" (lines 264–265) because TPCA acts on discrete measures while GPCAGEN is continuous, but does not attempt common-ground comparisons that would be feasible (e.g., evaluating the Sinkhorn divergence of projections onto both methods' components on held-out samples, or comparing the correlation of projection times). The closest prior work — Seguy & Cuturi (2015), which solves an approximate GPCA using generalized geodesics — is cited in the related work (line 26) but is never experimentally compared against. If GPCAGEN is meant to improve on this prior work, the absence of any comparative experiment is a major omission.

### Minor

- **The "exact" framing is overstated for GPCAGEN.** While the paper qualifies "exact in the sense that they do not rely on a linearization" (line 28), the method itself uses the Sinkhorn divergence S_ε (a regularized approximation with entropic bias), Monte Carlo sampling with finite batch size m, finite-capacity MLPs, Hessian eigenvalue estimates from finite samples, and soft regularization constraints (λ_I, λ_O). Presenting GPCAGEN as "exact" alongside the genuinely exact Gaussian method invites over-interpretation, especially in the abstract and introduction.

- **The orthogonality condition on line 90 is mathematically incorrect.** The condition for two geodesics μ(t) (defined by f) and μ̃(t) (defined by f̃) to be orthogonal at t=0 is stated as ⟨∇f̃ ∘ φ, ∇f̃ ∘ φ⟩_{L²(ρ)} = 0, which uses ∇f̃ on both sides and would mean μ̃ is orthogonal to itself (implying zero velocity). The condition should involve the cross-term ⟨∇f ∘ φ, ∇f̃ ∘ φ⟩ = 0. This is a concrete error on the page.

- **No discussion of the Sinkhorn regularization parameter ε** (line 168) or its effect on the recovered geodesics. Since S_ε is a biased approximation of W₂², the choice of ε directly affects what the optimization solves, but no guidance or sensitivity analysis is provided.

- **No ablation of the regularization terms λ_I and λ_O**, which are fixed at 1.0 for all experiments (line 256). Without this, it is unclear whether the orthogonality and intersection constraints are easy or hard to satisfy, or how sensitive the recovered components are to these weights.

- **Computational cost of GPCAGEN is not reported** — no training time, number of iterations, or convergence behavior for any of the experiments. The paper notes that computing R* is "computationally expensive" (line 196) but gives no actual cost figures for the method that was used.

### Trivial
None.

## Nice-to-Haves

- Quantify recovery quality on the synthetic dataset: report residual Sinkhorn divergence (or estimated W₂²), compare to the theoretical minimum, and compute the angle between recovered and true geodesic directions.
- Report the objective value (equation 15) achieved by GPCAGEN for each real dataset, and compare with the same metric evaluated for TPCA projections as a common ground.
- Run an ablation removing the orthogonality and intersection regularization terms to measure their effect.
- Add a dedicated limitations section discussing the reliance on Sinkhorn ε, Hessian eigenvalue estimation reliability, soft-constraint nature of regularizers, and the lack of global convergence guarantees.

## Removed Points

- "Paper undermines its own motivation" — The paper transparently reports when GPCA and TPCA are similar and when they differ (lines 208, 232). The Discussion (line 280) explicitly acknowledges the edge case where GPCA can be "worse-behaved." This is honest characterization, not a flaw.
- Missing hyperparameters from main text (batch size m, ε, optimizer, learning rate, iterations) — The paper states these are in Appendix E (line 256). Standard conference practice; the parser strips appendices.
- The "Strengthening the Paper on Its Own Terms" action items — These are constructive suggestions, folded into Nice-to-Haves and Suggestions above.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- For the synthetic dataset experiment, add a concrete numerical evaluation: report the residual Sinkhorn divergence (or W₂² estimate) achieved, compare to the known theoretical optimum, and compute the angle between recovered and true geodesic directions.
- For each real dataset, report the objective value (equation 15) achieved by GPCAGEN. Use the Sinkhorn divergence of TPCA projections onto GPCAGEN components (and vice versa) as a common-currency quantitative comparison.
- Add an ablation study: remove the orthogonality term and measure the angle between components; remove the intersection term and measure the distance between geodesics at their closest approach.
- Add a limitations section explicitly discussing: (a) reliance on Sinkhorn ε, (b) reliability of Hessian eigenvalue estimation from finite samples, (c) soft-constraint nature of the regularizers, (d) absence of global convergence guarantees for the non-convex optimization.

## Score and Decision

The paper has a genuine, well-executed theoretical contribution in the Gaussian GPCA (Section 3), accompanied by informative analysis (Proposition 4) and a clean algorithmic formulation (Proposition 3). The Otto-parametrization design choice for GPCAGEN (Section 4) is a genuinely interesting idea that avoids ICNNs. However, the GPCAGEN evaluation is fundamentally insufficient — it lacks any quantitative assessment of recovery quality, error bars, or objective values, and the baselines are dismissed rather than compared against. The "exact" framing is also somewhat overstated for the general-case method. The Gaussian half alone would be a solid contribution; the general-case half is a promising idea whose validation does not yet meet that standard. The paper's overall contribution is positive but held back by inadequate evaluation of its broader claims.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>