## Summary

This paper studies conformal prediction (CP) for surrogate models of time-dependent PDEs, where the non-stationarity of the solution distribution over time breaks the exchangeability assumption required by standard CP. The authors prove that in the infinite-dimensional function space setting, distributions at different times are mutually singular (TV distance = 1), making standard CP impossible. For discretized linear PDEs with Gaussian initial conditions, they derive closed-form densities of the solution at any time, enabling weighted conformal prediction (WCP) with exact coverage guarantees. Experiments on synthetic and real-world PDEs show that WCP maintains target coverage while naive CP and local-exchangeability-based methods (LSCI) systematically undercover.

## Strengths

- **Important and well-motivated problem**: Uncertainty quantification for PDE surrogate models is critical for safety-critical applications (e.g., weather forecasting, aerodynamic optimization), and the paper directly addresses the fundamental issue of non-exchangeability in time-dependent settings.
- **Rigorous theoretical analysis**: Theorem 4.1 establishes mutual singularity of solution distributions in function space, providing a clear theoretical barrier for standard CP. Theorem 4.2 gives the exact Gaussian distribution for discretized linear PDEs, which is the key enabler for weighted CP.
- **Principled solution with exact guarantees**: By leveraging the known density ratio, WCP provides exact finite-sample coverage guarantees (modulo discretization error), unlike heuristic baselines that lack formal guarantees under distribution shift.
- **Thorough empirical validation**: Experiments cover multiple PDE parameter configurations, compare against two baselines (naïve CP and LSCI), and include a real-world thermography dataset. The results consistently show WCP achieving target coverage while baselines fail, especially as the PDE becomes more unstable.
- **Clear exposition**: The paper is well-structured, with a logical flow from problem setup to theoretical analysis to method to experiments. The figures and tables effectively illustrate the key points.

## Weaknesses

### Fatal
None.

### Major
- **Limited to linear PDEs and Gaussian initial conditions**: The method requires the PDE to be linear and the initial condition to be Gaussian (or from a location-scale family). While the paper acknowledges this, it does not discuss how to extend to nonlinear PDEs or non-Gaussian initial conditions, which are common in practice. This significantly restricts the applicability of the method.
- **Assumes full knowledge of the PDE and discretization**: The density ratio computation requires knowing the PDE operator, the discretization scheme, and the initial distribution. In many real-world scenarios, the surrogate model is trained on data without access to the underlying PDE solver, or the PDE is not fully known. The paper does not address how to handle such cases.
- **Real-world experiment is insufficiently detailed**: The pulsed-thermography example is described only briefly in the appendix. It is unclear how the density ratio was computed (e.g., whether the PDE was assumed known, how the discretization was chosen, how the initial distribution was estimated). A more thorough case study would strengthen the practical claims.

### Minor
- **Comparison with LSCI could be more nuanced**: The paper states that LSCI has "no formal guarantees" in their experiments because local exchangeability is not verifiable. However, LSCI does provide guarantees under local exchangeability; the experiments simply show that this assumption is violated. The paper should clarify this distinction rather than dismissing LSCI's guarantees entirely.
- **Infinite bands as a fallback**: When the distribution shift is too large, WCP reports infinite bands. While this preserves coverage, it is not useful in practice. The paper could discuss alternative strategies (e.g., using a different calibration set, adaptive time windows) to avoid trivial bands.
- **No comparison with density-ratio estimation methods**: In settings where the PDE is not known, one could estimate the density ratio from data (e.g., using kernel density estimation or a classifier). A comparison with such approaches would provide a more complete picture.

### Trivial
None.

## Nice-to-Haves

- Discussion of potential extensions to nonlinear PDEs, e.g., via local linearization, ensemble methods, or using the linearized dynamics around a reference trajectory.
- Analysis of the effect of discretization error on the coverage guarantee (Remark 4.5 is mentioned but not elaborated).
- A more detailed real-world case study with explicit steps for computing the density ratio.

## Novel Insights

The paper provides a novel connection between conformal prediction and PDE theory, showing that the infinite-dimensional function-space setting is fundamentally incompatible with standard CP due to mutual singularity of measures, but that finite-dimensional discretization restores tractability and enables exact weighted CP. This insight bridges the gap between the neural operator literature (which often works in function space) and practical CP, and it highlights why discretization is not just a computational convenience but a theoretical necessity for coverage guarantees.

## Suggestions

- Discuss potential extensions to nonlinear PDEs, e.g., using the linearized dynamics or a local Gaussian approximation.
- Provide more details on the real-world experiment, including how the density ratio was computed and what assumptions were made.
- Consider comparing with a method that estimates the density ratio from data (e.g., using a classifier to approximate the likelihood ratio) to handle cases where the PDE is not fully known.
- Clarify in the abstract and introduction that the method applies to linear PDEs with Gaussian initial conditions, to set accurate expectations.

## Score and Decision

The paper makes a solid contribution by identifying a fundamental issue in CP for time-dependent PDEs and providing a principled solution for an important class of problems. The theoretical analysis is rigorous, and the empirical validation is convincing. However, the limited scope (linear PDEs, Gaussian initial conditions, known PDE) prevents the paper from being a breakthrough. The paper is well above the ICLR median and deserves acceptance.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>