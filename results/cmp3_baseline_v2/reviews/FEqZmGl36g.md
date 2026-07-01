## Summary

This paper introduces ESS-Flow, a training-free method for controlled generation with pretrained flow-based generative models. The key idea is to perform Bayesian inference in the Gaussian source space of flow models using Elliptical Slice Sampling (ESS), which avoids gradient computations through the generative model or potential function. The method is demonstrated on materials design with target properties and protein structure prediction from sparse distance measurements, showing competitive or superior performance compared to gradient-based alternatives.

## Strengths

- **Novel and well-motivated approach**: The paper identifies a genuine limitation of existing methods—their reliance on gradients—and proposes a principled gradient-free alternative. The connection between flow-based models with Gaussian priors and ESS is clever and technically sound.

- **Strong empirical results on materials generation**: ESS-Flow achieves substantially lower absolute errors (e.g., 8.99 vs 39.14 for bulk modulus) and higher S.U.N.T. rates compared to D-Flow, PnP-Flow, and DAPS across multiple material property tasks. The space group experiment (92.3% success vs 2.5% unconditional) convincingly demonstrates the value of gradient-free operation.

- **Theoretical grounding**: The paper provides a convergence guarantee (Proposition 1) adapted from existing ESS theory, and the method inherits the asymptotic exactness of ESS, which is a significant advantage over optimization-based point estimates.

- **Multi-fidelity extension**: The proof-of-concept multi-fidelity sampling (Section 4.2) is a practical contribution that addresses the computational cost of MCMC with expensive ODE solvers.

## Weaknesses

### Major

- **Protein structure prediction results are weak**: While the paper correctly notes that ADP-3D and DAPS produce unrealistic structures, ESS-Flow's RMSD_gt (13.55) is only marginally better than D-Flow (14.44) and substantially worse than ADP-3D (11.45) and DAPS (11.41). The d_y metric (37.02) is also much worse than ADP-3D (3.43) and DAPS (11.79). The claim that ESS-Flow achieves "a better trade-off between data fidelity and sample realism" is not well-supported—the ELBO values are similar to unconditional (8.89 vs 8.70), suggesting the conditioning barely influences the prior. This experiment does not convincingly demonstrate the method's value for protein structure prediction.

- **Limited comparison to concurrent work**: The paper mentions Wang et al. (2025) as concurrent work using HMC in source space but provides no experimental comparison. Given that Wang et al. (2025) is also a source-space MCMC method (though gradient-based), a comparison would help clarify when gradient-free sampling is genuinely beneficial versus when gradient-based MCMC suffices.

- **Computational cost not adequately addressed**: ESS-Flow requires many forward passes through the ODE solver (one per ESS proposal), and the paper does not report wall-clock time or number of function evaluations for the main experiments. The multi-fidelity section shows low effective sample sizes (0.1% for band gap), indicating the simple importance weighting approach is often ineffective. The paper acknowledges this but does not provide a practical solution.

### Minor

- **The toy example (Figure 2) is not fully convincing**: The claim that D-Flow gets trapped in disconnected manifolds while ESS-Flow avoids this is illustrated on a 2D toy problem, but the mechanism is not explained. ESS-Flow's ellipse proposals could also get trapped if the disconnected components are separated in source space. A more rigorous analysis of when ESS-Flow succeeds/fails would strengthen the paper.

- **Limited discussion of ESS limitations**: The paper mentions that ESS fails when the target is constrained to a lower-dimensional manifold but does not discuss practical diagnostics (e.g., acceptance rates, effective sample sizes) that would help practitioners assess convergence.

### Trivial

- The paper uses "gradient-free" and "training-free" somewhat interchangeably, though they are distinct concepts. ESS-Flow is training-free (no retraining) and gradient-free (no gradient computation), but these are separate advantages.

## Nice-to-Haves

- A comparison with Wang et al. (2025) on at least one task would significantly strengthen the paper.
- Reporting effective sample sizes and acceptance rates for the main experiments would help assess MCMC efficiency.
- An ablation study showing how ESS-Flow performs with different numbers of ODE steps would be useful for practitioners.

## Novel Insights

The key insight—that flow-based models with Gaussian priors enable gradient-free Bayesian inference in source space via ESS—is genuinely novel and well-executed. The paper correctly identifies that this approach preserves the fast generation properties of minibatch-OT coupling (unlike guidance methods that modify the velocity field) and works with non-differentiable potentials. The multi-fidelity extension, while preliminary, points toward a practical research direction for reducing computational cost.

## Suggestions

1. Add a comparison with Wang et al. (2025) on at least the materials tasks to clarify when gradient-free sampling is beneficial.
2. Report wall-clock time and number of ODE evaluations for all methods to contextualize the computational trade-offs.
3. Provide acceptance rates and effective sample sizes for ESS-Flow on the main experiments.
4. For the protein experiment, consider a simpler setting (e.g., fewer residues, more observations) where ESS-Flow can demonstrate clear advantages.

## Score and Decision

The paper presents a novel, well-motivated, and technically sound method with strong empirical results on materials generation. The protein structure prediction results are weaker but do not invalidate the core contribution. The main limitations are the lack of comparison to concurrent work and insufficient reporting of computational cost. Overall, this is a solid contribution that advances the state of training-free controlled generation.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>