## Summary

The paper presents ESS-Flow, a gradient-free method for controlled generation with pretrained flow-based generative models. By performing elliptical slice sampling (ESS) in the Gaussian source space of flow models, the Jacobian terms cancel, enabling Bayesian inference using only forward passes through the generative model and potential function. The method is demonstrated on materials design with target properties (including a non-differentiable space group task) and protein backbone structure prediction from sparse inter-residue distances.

## Strengths

- **Clean and well-motivated formulation.** The key insight that the Jacobian cancels when expressing both prior and posterior in source space (Equation 3) is elegant and makes the use of ESS natural given the Gaussian prior. The connection to the existing ESS convergence theory (Proposition 1) provides theoretical grounding.

- **Genuinely useful gradient-free property.** The paper convincingly argues for settings where gradients are unavailable or unreliable: quantization in material atomic numbers, non-differentiable simulators for space group symmetry, and simulation-based observations. The space group task (92.3% success vs. 2.5% unconditional) cleanly demonstrates this advantage. The method also avoids the need for the noising process used during training, requiring only the transport map.

- **Strong empirical results on scientific applications.** ESS-Flow achieves significantly lower mean absolute errors on material properties (e.g., 8.99 vs. 39.14 for bulk modulus compared to the next best method DAPS) and the highest S.U.N.T. rates across all tasks. For proteins, ESS-Flow produces structures with far fewer clashes (24.8 vs. 483-731 for ADP-3D/DAPS) and better ELBO scores, demonstrating better structural realism.

- **Multi-fidelity extension.** The importance re-weighting approach using coarse ODE discretization for exploration and fine discretization for final evaluation is a practical idea that reduces computational cost, with reasonable effective sample sizes reported for some tasks.

## Weaknesses

### Fatal
None.

### Major

- **No MCMC convergence diagnostics.** For an MCMC-based method, the paper reports no burn-in analysis, effective sample sizes, trace plots, or mixing diagnostics. How many ESS iterations are run? How is the chain initialized and how many samples are discarded? Without these, it is difficult to assess whether the reported results reflect the stationary distribution or transient behavior. This is a significant omission for a method whose correctness relies on MCMC convergence.

- **Scalability to high dimensions unclear in main text.** ESS is known to face challenges in high dimensions. The paper defers numerical scaling evaluations to Appendix A.1, but the main text should discuss expected scaling behavior and the practical dimensionality limits. The materials and protein experiments operate in moderate dimensions; the method's applicability to higher-dimensional settings (e.g., image generation) deserves explicit discussion.

- **Computational cost not compared.** Each ESS iteration requires at least one full ODE solve (forward pass through the generative model), and rejected proposals require additional solves. The paper mentions runtime costs are in the Appendix but does not discuss them in the main text. A fair comparison of wall-clock time and number of function evaluations across methods is important for practitioners choosing between approaches.

### Minor

- **Protein data fidelity is worse than baselines.** ESS-Flow achieves RMSD_gt of 13.55 compared to 11.41 for ADP-3D and DAPS. While the paper correctly argues that ESS-Flow produces more realistic structures, the trade-off between data fidelity and prior regularization could be more explicitly analyzed. The high RMSD values suggest the method may be over-regularizing.

- **Multi-fidelity results are preliminary.** The importance re-weighting approach fails for sharper target distributions (0.1% and 1.0% effective sample sizes for band gap and stability). The paper acknowledges this but doesn't explore the more sophisticated alternatives mentioned (delayed acceptance, parallel tempering), making this contribution feel incomplete.

- **The space group task is somewhat trivial for MCMC.** The potential is a binary indicator, so ESS simply needs to find any point in the acceptance region. While it demonstrates the non-differentiable capability, it doesn't stress-test the method.

### Trivial
None.

## Nice-to-Haves

- A comparison of wall-clock times across all methods would strengthen the practical evaluation.
- Analysis of how ESS-Flow performance degrades as the number of MCMC iterations varies, to guide practitioners on computational budgets.
- Application to a more standard inverse problem (e.g., image inpainting or super-resolution) to better characterize the method's limitations in settings where the prior poorly covers the target.

## Novel Insights

The observation that the Jacobian terms cancel when performing inference in source space (Equation 3) is the paper's central insight, and while the change-of-variables formula is standard, recognizing that this enables gradient-free MCMC with ESS specifically—leveraging the Gaussian structure of the source distribution—is a genuinely useful contribution. The demonstration that gradient-based methods can become trapped in disconnected manifold components (Figure 2) provides additional motivation beyond just computational cost. The multi-fidelity idea of exploiting different ODE discretization levels is also a novel practical observation for flow-based models.

## Suggestions

- Add MCMC convergence diagnostics: report effective sample sizes, autocorrelation times, and trace plots for at least the main experiments. Show how performance varies with number of MCMC iterations.
- Include a computational cost comparison table showing wall-clock time and number of generative model evaluations for each method.
- Discuss scalability more prominently in the main text, including the dimensionality of the source spaces used in experiments and expected behavior in higher dimensions.

## Score and Decision

The paper presents a clean, well-motivated method that fills a genuine gap in gradient-free controlled generation for flow-based models. The mathematical formulation is sound, the experimental results are strong in the targeted scientific domains, and the non-differentiable settings convincingly demonstrate the method's unique advantages. However, the absence of MCMC convergence diagnostics is a notable omission for a sampling method, and the lack of computational cost comparison limits the practical assessment. These are addressable issues that don't invalidate the core contribution but weaken the experimental evaluation.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <score>Accept</score>