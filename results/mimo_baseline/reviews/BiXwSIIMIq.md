## Summary

This paper proposes the AC-DC denoiser, a three-stage score-based denoising mechanism (Auto-Correction via additive Gaussian noise, Directional Correction via conditional Langevin dynamics, and score-based denoising via Tweedie's lemma or ODE) designed to be embedded in the ADMM plug-and-play framework for solving inverse problems. The authors provide convergence guarantees showing that under proper scheduling, ADMM with the AC-DC denoiser converges to a fixed-point neighborhood (ball convergence) with high probability, under both strongly convex losses with constant step size and general losses with adaptive step size. Experiments across seven inverse problems on FFHQ and ImageNet demonstrate consistent improvements over strong baselines.

## Strengths

- **Well-motivated three-stage design with clear intuition.** The AC-DC denoiser addresses a genuine and underexplored problem: the geometry mismatch between ADMM iterates (which are distorted by dual variables) and the noisy data manifolds on which score functions are trained. The directional correction stage via Langevin dynamics targeting the conditional distribution p(z_σ|z_ac) is a novel and principled approach to bridging this gap, going beyond simple noise injection used in prior work.

- **Theoretical contribution extending ADMM-PnP convergence to score-based denoisers.** The paper generalizes the convergence theory of Ryu et al. (2019) and Chan et al. (2016) to handle the stochastic nature of score-based denoisers. The weakly nonexpansive operator framework with ball convergence (Theorems 1-3) is technically sound and provides the first convergence guarantees for score-based ADMM-PnP. The handling of probability across iterations via union-bounds (Theorem 2(b)) is a nontrivial technical contribution.

- **Comprehensive empirical evaluation.** The method is tested on seven diverse inverse problems (super-resolution, Gaussian/motion deblurring, random/box inpainting, phase retrieval, HDR, nonlinear deblurring) across two datasets, with consistent improvements. The ablation study on DC iteration count (Figure 5) convincingly demonstrates the value of the directional correction stage. Both Tweedie and ODE variants are evaluated.

## Weaknesses

### Fatal

None.

### Major

- **Stationary distribution assumption for DC step is strong and unverifiable in practice.** Theorems 2 and 3 assume that the DC Langevin dynamics step reaches the stationary distribution p(z_σ(k)|z_ac(k)) at each iteration k. With only J=10 DC steps used in experiments, this is far from achieved in practice. The authors note Appendix E.2 contains counterparts removing this assumption, but the main paper's results depend on it, and the gap between the theory and practice is significant. This weakens the practical relevance of the convergence guarantees.

- **Missing efficiency analysis.** Each AC-DC denoiser invocation requires J=10 score function evaluations (DC steps) plus 1 denoising evaluation, totaling ~11 NFEs per ADMM iteration, compared to 1 NFE for methods like DiffPIR. Combined with up to K=W+10 iterations (where W is the decay window), the total computational cost is substantially higher than baselines. The paper does not report runtime comparisons or discuss whether the quality gains justify the 10×+ cost increase, making it difficult to assess practical value.

### Minor

- **Incomplete table entries.** In Table 1, PMC results are missing for many tasks (random inpainting, Gaussian blur, motion deblur on both datasets, and several others). Similarly, some method/task combinations lack results. While this may be due to parser issues or methods not being applicable, it makes the comparison less complete.

- **Convergence only to a ball, not a fixed point.** The authors honestly acknowledge this limitation (Section 4.3 remark), but ball convergence under constant step size requires strongly convex loss, which excludes many practical inverse problems (e.g., phase retrieval, nonlinear deblurring). The adaptive step-size alternative (Theorem 3) removes convexity but has other drawbacks as noted.

- **Hyperparameter sensitivity not explored.** The schedules for σ^(k), η^(k), σ_s^(k), and the DC iteration count J are set by heuristics. The paper does not provide sensitivity analysis on these critical hyperparameters, making reproducibility and adaptation to new problems more difficult.

### Trivial

None.

## Nice-to-Haves

- Wall-clock time comparisons against baselines to contextualize the computational overhead
- Analysis of the gap between the theoretical stationary distribution assumption and the practical J=10 DC steps
- Sensitivity analysis on the noise schedules and DC parameters
- Extension to other optimization frameworks beyond ADMM (the authors mention this is possible but don't demonstrate it)

## Novel Insights

The paper makes a genuinely novel observation that the directional correction via conditional Langevin dynamics can serve as a principled bridge between ADMM iterates and the noisy data manifolds on which score functions are trained. While noise injection before score evaluation is common in prior work (DiffPIR, SNORE, RED-diff), the DC stage represents a qualitative advance: it doesn't merely add noise but actively moves the iterate toward the manifold via targeted Langevin dynamics. This insight—that a few steps of conditional Langevin dynamics can correct for the geometry mismatch caused by dual variables in ADMM—is nontrivial and could influence future designs of score-based optimization methods.

## Suggestions

- Add runtime/efficiency comparisons to justify the computational overhead of the DC stage
- Provide the main results from Appendix E.2 (removing the stationary distribution assumption) in the main paper, as these are critical for establishing the practical relevance of the convergence guarantees
- Include sensitivity analysis on the DC iteration count J and noise schedules to guide practitioners
- Consider a simplified variant that reduces NFEs (e.g., warm-starting the DC step from the previous iteration's output)

## Score and Decision

The paper addresses an important and underexplored problem (convergence of score-based ADMM-PnP), proposes a principled and novel solution (the AC-DC denoiser), and provides both theoretical convergence guarantees and strong empirical results. The theoretical contribution—extending ADMM-PnP convergence theory to handle stochastic score-based denoisers—is meaningful. However, the convergence results rely on a strong stationarity assumption for the DC step that is unlikely to hold in practice, and the computational overhead is not addressed. These issues prevent the work from being a clear accept but the overall contribution is above the borderline.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>