## Summary

This paper studies conformal prediction (CP) for surrogate models of time-dependent PDEs, where non-stationarity breaks the exchangeability assumption required by standard CP. The authors prove that in infinite-dimensional function spaces, distributions at different times are mutually singular (TV distance = 1), making exact coverage impossible. They then show that for discretized linear PDEs with Gaussian initial conditions, the solution distribution remains Gaussian with known parameters, enabling weighted conformal prediction with exact coverage guarantees. Experiments on synthetic PDEs and a real-world thermography dataset demonstrate that their method maintains target coverage while baselines (naïve CP and LSCI) systematically undercover.

## Strengths

- **Principled theoretical analysis of the fundamental challenge**: Theorem 4.1 rigorously shows that in function spaces, measures at different times are mutually singular even for simple PDEs like the heat equation. This is an important negative result that clarifies why standard CP approaches cannot work in the infinite-dimensional setting and justifies the need for discretization.
- **Clean, practical solution for an important class of problems**: Theorem 4.2 provides closed-form expressions for the solution distribution under discretized linear PDEs with Gaussian initial conditions, enabling exact likelihood ratio computation for weighted CP. The method is computationally efficient (seconds vs. 40 minutes for LSCI) and provides formal guarantees.
- **Strong empirical validation**: Experiments across multiple PDE parameter configurations show that naïve CP and LSCI systematically undercover (sometimes dropping to 0% coverage), while WCP maintains target coverage. The method also gracefully degrades by reporting infinite bands when distribution shift is too large, which is the correct behavior for safety-critical applications.

## Weaknesses

### Fatal
None.

### Major
- **Limited to linear PDEs with Gaussian initial conditions**: The core theoretical result (Theorem 4.2) and the weighted CP method rely on the PDE being linear and the initial distribution being Gaussian (or location-scale family). While the authors acknowledge this limitation, it significantly restricts applicability. Many important PDEs in science and engineering are nonlinear (Navier-Stokes, Burgers, reaction-diffusion with nonlinear terms). The paper would be substantially stronger if it discussed how to extend the approach to nonlinear settings (e.g., via local linearization, ensemble methods, or density ratio estimation).

- **The practical relevance of the function-space result (Theorem 4.1) is unclear**: The authors prove that TV distance is maximal in function spaces, but then immediately note that "this is not necessarily problematic for practical CP on surrogate models" because we work with finite discretizations. The theorem feels disconnected from the actual method—it serves as motivation but doesn't inform the solution. The paper would benefit from either (a) showing how this result constrains what is theoretically possible even in discretized settings, or (b) acknowledging that the function-space analysis is primarily a conceptual contribution and focusing more on the discretized setting.

### Minor
- **The real-world experiment is underdeveloped**: The pulsed-thermography dataset is mentioned but results are relegated to the appendix. Given that real-world validation is crucial for demonstrating practical impact, this deserves more prominence in the main text.
- **Comparison with trajectory-based methods is missing**: The related work section mentions trajectory-level CP (Moya et al., 2025; Gray et al., 2025) as an alternative approach, but these methods are not included as baselines. A comparison would help contextualize the advantages of WCP over this natural alternative.
- **The "infinite bands" behavior is not fully analyzed**: When WCP reports infinite bands, the paper reports coverage only on the remaining samples. This can be misleading—if 86.4% of samples get infinite bands (as in Table 1, a=-0.0075, timestep 15), reporting 84% coverage on the remaining 13.6% is not very informative. The paper should discuss how practitioners should interpret and use such results.

### Trivial
- The notation in equation (1) uses $\mathbf{u}_i$ for both calibration and test points, but the test point's density ratio should be computed with respect to its own (unknown) value. The paper should clarify that the test point weight is computed using the observed test input $x_{n+1}$ (the initial condition) rather than the unobserved $y_{n+1}$ (the solution).

## Nice-to-Haves

- An extension to nonlinear PDEs via local linearization or density ratio estimation would dramatically increase impact.
- A discussion of how the discretization resolution affects the quality of the coverage guarantees (e.g., does a finer grid make the Gaussian approximation more accurate?).
- A sensitivity analysis showing how robust the method is to misspecification of the initial distribution (e.g., if the true initial distribution is not exactly Gaussian).

## Novel Insights

The paper's key insight is that the function-space perspective (common in neural operator literature) is fundamentally incompatible with conformal prediction for time-dependent PDEs due to mutual singularity of measures, but that discretization resolves this issue and enables exact weighted CP via closed-form density ratios. This bridges a gap between the theoretical PDE literature (which works in function spaces) and practical ML (which works with discretized data). The observation that coverage guarantees can be maintained by explicitly modeling the distributional shift through the PDE dynamics, rather than relying on exchangeability or local exchangeability assumptions, is a clean and principled contribution.

## Suggestions

1. Add a discussion or preliminary experiments on how to extend the method to nonlinear PDEs, even if only via approximation (e.g., linearization around a nominal trajectory, or using the method's Gaussian approximation as a heuristic).
2. Include trajectory-level CP as a baseline in the experiments to provide a more complete comparison.
3. Move the real-world experiment results to the main text, or at least provide a summary table/plot.
4. Clarify how practitioners should handle cases where a large fraction of samples receive infinite bands—e.g., by suggesting a threshold on $n_\infty$ below which the bands are considered reliable.

## Score and Decision

The paper makes a clear, well-motivated contribution to an important problem (uncertainty quantification for PDE surrogate models). The theoretical analysis is rigorous, the method is elegant and computationally efficient, and the experiments convincingly demonstrate that existing approaches fail while WCP succeeds. The main limitation is the restriction to linear PDEs with Gaussian initial conditions, which the authors acknowledge. This is a genuine limitation but not a fatal one—the paper is a solid contribution within its scope.

Score: 8

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>