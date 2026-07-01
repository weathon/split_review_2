## Summary
This paper introduces the AC-DC denoiser, a three-stage score-based denoiser (Auto-Correction, Directional Correction, Tweedie/ODE denoising) designed to mitigate the manifold mismatch between ADMM iterates and the noisy data manifolds on which diffusion score functions are trained. The authors embed this denoiser into ADMM-PnP, provide convergence guarantees under weak nonexpansiveness (constant step size, strongly convex loss) and under adaptive step sizes (nonconvex loss), and demonstrate consistent improvements over a wide range of baselines across multiple inverse problems on FFHQ and ImageNet.

## Strengths
1. **Well-motivated and principled denoiser design.** The paper identifies the fundamental geometry mismatch problem when plugging score-based denoisers into ADMM—especially the additional distortion from dual variables—and proposes the AC-DC denoiser to address it. The three-stage pipeline (AC, DC, score denoising) is logically constructed and clearly explained.
2. **Novel convergence theory for score-based denoisers in ADMM.** The paper establishes two convergence results: (i) weak nonexpansiveness of the AC-DC denoiser leading to high-probability fixed-point ball convergence under constant step size with strongly convex loss, and (ii) boundedness of the denoiser leading to convergence under adaptive step sizes without convexity. These results extend the ADMM-PnP convergence literature (Ryu et al. 2019; Chan et al. 2016) to a class of score-based denoisers for the first time.
3. **Strong and comprehensive empirical validation.** The method is evaluated on seven inverse problems (super-resolution, Gaussian/motion deblurring, random/box inpainting, phase retrieval, HDR) on two datasets (FFHQ, ImageNet) against nine baselines. Both variants (Ours-tweedie and Ours-ode) consistently achieve best or second-best results across nearly all metrics. Qualitative results show visibly cleaner reconstructions with fewer artifacts.

## Weaknesses
### Major
1. **Strong assumption on the DC step.** The convergence theorems (Theorems 2 and 3) assume that the Langevin dynamics DC step reaches the stationary distribution at each ADMM iteration. In practice only a finite number \(J\) of steps are run, so this assumption is violated. The paper mentions that counterparts without this assumption exist in the appendix (which is not provided), but the main theoretical claims rely on an assumption that is not met in the experiments.
2. **High-probability rather than deterministic guarantees.** The convergence results hold with probability \(1-\eta\) and depend on \(\nu_k\) growing logarithmically. While this is a reasonable relaxation for score-based denoisers, it weakens the guarantees compared to classical ADMM-PnP analyses that provide deterministic convergence. The practical reliability depends on the actual failure probability, which is not discussed.
3. **Computational cost.** Each ADMM iteration requires many score network evaluations: \(J\) Langevin steps (typically 10) plus either a Tweedie evaluation or 10 ODE steps. This makes the method significantly more expensive than simpler baselines like DiffPIR or DPS. The paper acknowledges this as a limitation but does not provide wall-clock time comparisons or efficiency analyses.

### Minor
1. **Fixed-point convergence only.** The analysis establishes convergence to a fixed point (or \(\delta\)-ball) of the ADMM operator, not convergence to a stationary point of the original problem. The paper correctly notes this is standard for PnP with implicit regularizers, but it limits the strength of the theoretical contribution.
2. **Hyperparameter sensitivity.** The noise schedules (\(\sigma^{(k)}\), \(\eta^{(k)}\), \(\sigma_{s^{(k)}}\)) are set by heuristics. While the paper provides specific schedules, there is no ablation or analysis of how robust the method is to these choices. The theoretical results impose conditions on the schedules (e.g., \(\sigma^{(k)} \to 0\)), but the empirical schedules do not decay to zero (lower bound 0.1) and thus may not satisfy the convergence conditions exactly.
3. **Table formatting issues.** In Table 1, some entries are duplicated (e.g., PMC appears multiple times for the same task) and some cells are empty. While likely parser artifacts, they make the quantitative comparison slightly harder to follow.

### Trivial
None of consequence.

## Nice-to-Haves
- Wall-clock time or NFE comparisons to help readers assess the practical trade-off between improved quality and computational cost.
- An ablation on the number of DC steps \(J\) on more tasks (only shown for phase retrieval) to understand the robustness of the benefit.
- A discussion of how the theoretical conditions on \(\sigma^{(k)}\) and \(\sigma_{s^{(k)}}\) relate to the empirically used schedules (e.g., the lower bound 0.1 means the conditions \(\lim \sigma^{(k)} = 0\) are not literally met, though the neighborhood convergence might still hold in practice).

## Novel Insights
None beyond the paper’s own contributions.

## Suggestions
1. Clarify in the main paper what the convergence results without the stationary-distribution assumption look like, even if the full proofs are deferred to appendix. Currently a reader may overinterpret the theoretical claims.
2. Provide a brief analysis (theoretical or empirical) of how the finite \(J\) affects the satisfaction of Assumption 1.
3. Include a runtime or NFE comparison table so that the community can weigh the performance gain against the computational overhead.

## Score and Decision
The paper makes a solid contribution by addressing a well-recognized challenge (manifold mismatch in PnP with score denoisers) with a principled algorithm and a significant theoretical extension of ADMM-PnP convergence theory to score-based denoisers. The experimental validation is thorough and demonstrates clear improvement over strong baselines. The major weaknesses (strong stationarity assumption for DC, high-probability guarantees, computational cost) are acknowledged and partially addressed through appendices and limitations. The paper brings sufficient value to the community and contributes new knowledge. I recommend acceptance.

MY FINAL SCORE: <score>8.0</score>
MY FINAL DECISION: <decision>Accept</decision>