## Summary
This paper introduces ESS-Flow, a training-free method for controlled generation with pretrained flow-based generative models. The key idea is to perform Bayesian inference in the Gaussian source space of flow models using Elliptical Slice Sampling (ESS), which avoids gradient computations through the generative model or potential function. The method is demonstrated on materials design with target properties and protein structure prediction from sparse distance measurements, showing competitive performance particularly in settings where gradients are unreliable or unavailable.

## Strengths
- **Novel and well-motivated approach**: The paper identifies a genuine limitation of existing gradient-based methods for controlled generation (unreliable gradients, local optima, inability to handle non-differentiable potentials) and proposes a principled gradient-free alternative. The connection between flow-based models with Gaussian priors and ESS is elegant and well-justified.
- **Strong empirical results on materials generation**: ESS-Flow achieves substantially lower absolute errors compared to D-Flow, PnP-Flow, and DAPS across all four materials tasks (bulk modulus, shear modulus, band gap, energy above hull). The S.U.N.T. rates demonstrate that ESS-Flow generates valid, stable materials while successfully targeting extreme property values.
- **Principled Bayesian formulation**: The method provides asymptotically exact samples from the target posterior distribution, unlike optimization-based methods that only give point estimates. The theoretical convergence guarantee (Proposition 1) adds rigor.
- **Demonstration of gradient-free capability**: The space group symmetry experiment (Section 5.1) convincingly shows ESS-Flow's advantage in truly non-differentiable settings where gradient-based methods cannot be applied at all.

## Weaknesses
### Major
- **Limited protein structure prediction results**: While ESS-Flow produces more realistic structures (higher ELBO, fewer clashes) than ADP-3D and DAPS, the RMSD_gt values are high (13.55 Å) and the L2 distance to observations (37.02) is substantially worse than ADP-3D (3.43) and DAPS (11.79). The paper acknowledges this but does not adequately address whether ESS-Flow is practically useful for this task. The trade-off between data fidelity and realism is not well-characterized—it's unclear if ESS-Flow's samples are "too conservative" in a way that limits practical utility.
- **Computational cost not adequately addressed**: The paper mentions using "moderate numbers of function evaluations" but does not provide a clear comparison of wall-clock time or number of ODE evaluations across methods. Given that ESS-Flow requires many MCMC iterations, each requiring a forward pass through the ODE, the computational cost could be prohibitive for high-dimensional problems. The multi-fidelity approach is presented as a proof-of-concept but shows poor effective sample sizes for sharp target distributions (0.1% and 1.0% for band gap and stability tasks).
- **Limited evaluation of MCMC convergence**: The paper provides a theoretical convergence guarantee but does not empirically assess mixing, autocorrelation, or effective sample sizes for the main experiments. Without such diagnostics, it's difficult to know how many MCMC iterations are needed for reliable inference or whether the chains have converged.

### Minor
- **Comparison fairness concerns**: For the materials experiments, D-Flow and PnP-Flow use a continuous approximation for atomic numbers (Equation 5) while ESS-Flow and DAPS use discrete sampling. This makes the comparison somewhat uneven—the gradient-based methods are operating under a fundamentally different (and potentially disadvantageous) representation. The paper should discuss whether this approximation is necessary or whether alternative gradient-based approaches could handle discrete variables.
- **Limited ablation studies**: The paper does not systematically study the effect of key hyperparameters (number of MCMC iterations, ODE solver steps, ESS bracket shrinkage) on performance. The multi-fidelity approach is only briefly evaluated with limited analysis.

### Trivial
- The paper states "ESS-Flow outperforms all other methods significantly" but the standard deviations in Table 2 show substantial overlap between ESS-Flow and DAPS for some metrics (e.g., band gap: ESS-Flow 1.85±1.66 vs DAPS 3.90±1.67).

## Nice-to-Haves
- An empirical analysis of MCMC mixing and convergence diagnostics (e.g., trace plots, autocorrelation, effective sample size) would strengthen the paper significantly.
- A more thorough investigation of the multi-fidelity approach, perhaps with adaptive discretization or tempering-based methods, could make it more practically useful.
- Comparison with a gradient-based source-space method (e.g., Purohit et al., 2025) would help isolate the benefits of gradient-free sampling versus gradient-based sampling in the source space.

## Novel Insights
The paper's key insight—that the Gaussian prior in flow-based models enables gradient-free Bayesian inference via ESS in the source space—is genuinely novel and well-executed. The observation that gradient-based methods can get trapped in disconnected manifold components (Figure 2) while ESS-Flow avoids this is a concrete demonstration of a real limitation. The paper also correctly identifies that many existing methods sacrifice prior regularization for data fit (as shown in the protein experiments), and ESS-Flow's explicit prior enforcement is a principled solution.

## Suggestions
- Add empirical MCMC diagnostics (trace plots, effective sample size, autocorrelation) for the main experiments to demonstrate convergence.
- Provide a clearer computational cost comparison (wall-clock time, number of ODE evaluations) across methods.
- Discuss the practical implications of the trade-off between data fidelity and sample realism in the protein experiments—when is ESS-Flow preferable despite higher RMSD?
- Consider evaluating on a simpler, well-understood inverse problem (e.g., image inpainting with known ground truth) to better characterize when ESS-Flow works well versus when it struggles.

## Score and Decision
The paper presents a novel, well-motivated, and principled method with strong empirical results on challenging scientific applications. The main weaknesses are the limited empirical validation of MCMC convergence and the incomplete characterization of computational cost. However, the core contribution is significant and the method addresses a genuine gap in the literature. The paper is clearly written and the experiments are well-designed.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>