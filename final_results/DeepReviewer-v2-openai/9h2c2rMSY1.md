## Summary
This paper studies conformal prediction (CP) for time-dependent PDE surrogate models. The authors first show that in infinite-dimensional function spaces, solution distributions at different times are mutually singular (TV distance = 1), making standard CP guarantees impossible. They then propose a weighted conformal prediction (WCP) method for *linear* PDEs after spatial discretization, leveraging closed-form Gaussian densities to compute likelihood-ratio weights. Experiments on a family of linear second-order PDEs (with backward-parabolic coefficients) show that WCP maintains target 90% coverage, while naïve CP and LSCI (local spectral conformal inference) exhibit undercoverage as prediction horizon increases.

**Core Contributions:**
- C1: Analysis showing TV distance=1 between function-space PDE solution distributions at different times (Theorem 4.1).
- C2: Closed-form Gaussian densities for discretized linear PDE solutions enabling likelihood-ratio weighting for CP (Theorem 4.2).
- C3: Empirical validation on linear PDEs showing WCP outperforms naïve CP and LSCI in coverage reliability.

**Key Strengths:** Novel combination of PDE semi-discretization theory with weighted CP; mathematically rigorous derivation of the Gaussian solution distribution; clear demonstration of the failure of exchangeability-based CP in time-dependent settings.

**Key Weaknesses:** The method is restricted to **linear PDEs with Gaussian initial conditions**, which is a much narrower class than claimed ("broad class of PDEs"); the infinite-band regime in unstable PDEs renders WCP practically unusable (up to 100% infinite bands); experimental validation is limited to a single family of linear PDEs with no nonlinear or well-posed forward-parabolic tests; novelty of Theorem 4.1 is debatable given existing measure-theoretic results on Gaussian measures on Hilbert spaces.

## Strengths
**S1 — Rigorous mathematical framing of the non-exchangeability problem.** The paper correctly identifies and formalizes why time-dependent PDEs break CP exchangeability through the pushforward measure formalism ($\mathcal{P}_t = (S_t)_\# \mathcal{P}_0$). Theorem 4.1 on mutual singularity in function spaces, while based on standard measure-theoretic results, provides a clean demonstration that the function-space perspective is insufficient for practical CP. The inclusion of the Barber et al. (2023) TV-distance bound and its breakdown in infinite dimensions is technically sound.

**S2 — Elegant use of PDE semi-discretization for closed-form densities.** Theorem 4.2 is the paper's strongest technical contribution. The observation that the method-of-lines spatial discretization converts a linear PDE into a linear ODE system, preserving Gaussianity of the initial distribution, enables an exact likelihood ratio. This is a clever and principled approach that connects PDE theory with CP in a way not previously done in the literature.

**S3 — Clear empirical demonstration of coverage degradation.** The experimental results in Table 1 and Figure 3 convincingly show that both naïve CP and LSCI (local spectral conformal inference) undercover as prediction horizon increases when the PDE is unstable ($a < 0$). The comparison is fair in that both baselines are given reasonable default parameters, and the trend of increasing undercoverage with $|a|$ is consistent across configurations.

**S4 — Computational efficiency under assumptions.** When the linear-Gaussian assumptions hold, WCP is dramatically faster than LSCI (seconds vs. ~40 minutes), making it practical for rapid evaluation. This computational advantage is correctly reported and would be relevant for real-time applications within the method's scope.

**S5 — Transparency about infinite-band cases.** The paper honestly reports $n_\infty$ (fraction of samples with infinite bands) rather than hiding these cases. This transparency is valuable for safety-critical applications where knowing when a method cannot produce a meaningful interval is as important as knowing when it can.

## Weaknesses
**W1 — Overclaimed contribution scope (Major).** The paper consistently overstates the generality of its method. The title "Weighted Conformal Prediction for Time-Dependent PDEs" and abstract phrases like "broad class of PDE problems" and "exact coverage guarantees without limiting assumptions" suggest general applicability. In reality, the method is restricted to:
- **Linear** PDEs (Theorem 4.2 requires a linear spatial operator $\mathcal{L}_x$).
- **Gaussian** initial conditions (or location-scale family, Remark 4.3).
- Known analytical PDE form (to compute $\boldsymbol{\mu}_t$, $\boldsymbol{\Sigma}_t$ in closed form).
- Semi-discretization via method of lines.

Nonlinear PDEs (Navier-Stokes, Burgers, reaction-diffusion), which constitute most practically relevant problems, are explicitly excluded and only mentioned as future work. This gap between claimed and actual scope is the paper's most significant weakness. The contribution statements in the Introduction (bullet 2) and the abstract need to be scoped down to "linear PDEs" and the assumptions must be clearly stated upfront.

**W2 — WCP produces infinite bands in precisely the regime where it is needed most (Major).** Table 1 shows that for $a=-0.0075$ at timestep 15, $n_\infty = 86.4\%$, and at timestep 20, $n_\infty = 100\%$. For $a=-0.01$, $n_\infty = 35.4\%$ already at timestep 10. The paper presents this as a strength ("reporting trivial bands is usually more valuable than delivering bands with undercoverage"), but in practice, a method that outputs infinite intervals on 35–100% of test cases is of limited operational value for safety-critical applications like flood forecasting or aerodynamic optimization. The paper should:
- Report overall coverage **including** infinite-band cases (as guaranteed coverage = 1.0 for those, but effective coverage = coverage on non-infinite samples × fraction non-infinite).
- Discuss the practical implications of the infinite-band regime more candidly.
- Provide diagnostic tools to detect when infinite bands are likely.

**W3 — Limited experimental validation (Major).** The synthetic experiments test only one PDE family: $u_t + a u_{xx} + b u_x + c u = 0$ with $a < 0$ (backward-parabolic). Missing experiments include:
- **Well-posed forward-parabolic PDEs** ($a > 0$), where coverage degradation would be slower and the method's advantage less clear.
- **Nonlinear PDEs** (even simple ones like Burgers' or Allen-Cahn) to demonstrate what happens when Gaussianity breaks.
- **Higher-dimensional problems** beyond 1D (the "real-world" example is 2D but very small).
- **Different surrogate models** (the paper only tests one: geometry-informed neural operator).
- **Different discretization sizes** to test sensitivity to $n$.

Additionally, no confidence intervals, standard errors, or statistical significance tests are reported for coverage values. The claim that WCP "consistently meets its coverage guarantees" is not strictly true — for $a=-0.005$, coverage drops to 0.85 and 0.88 at later timesteps, below the 0.90 target, even without infinite-band cases.

**W4 — Theorem 4.1 novelty is overstated (Major).** The result that Gaussian measures on function spaces with different covariance operators are mutually singular (TV distance = 1) is a standard consequence of the Feldman–Hájek theorem and is well-known in the probability on Hilbert spaces literature. The paper presents this as a novel finding ("We analyze the function-space formulation... and show that..."), but it is essentially applying known measure-theoretic results to the PDE context. The paper should cite the relevant foundational literature (e.g., Da Prato–Zabczyk, Bogachev, or the Feldman–Hájek theorem directly) and present Theorem 4.1 as an *illustration* of the issue rather than a novel discovery.

**W5 — Practical applicability limitations not adequately discussed (Minor).** Several practical concerns are missing:
- **Computational cost of matrix exponentials.** For an $n$-point spatial grid, computing $\exp(t\mathbf{A})$ costs $O(n^3)$. For high-resolution 2D/3D problems with $n=10^5$-$10^7$, this is prohibitive. The paper does not discuss this.
- **Numerical stability of density ratios.** The ratio of two high-dimensional Gaussians can underflow; the paper does not discuss log-space computation.
- **Knowledge of PDE parameters.** The method requires knowing the PDE coefficients $a, b, c$ and boundary conditions exactly. In many real-world applications, these are uncertain or estimated, which would propagate into the weight computation.
- **Surrogate model choice.** The paper claims "the choice of surrogate model is not important for downstream analysis," but the surrogate's residuals are the basis for CP scores. A poorly calibrated surrogate with biased residuals could invalidate the coverage guarantees.

**W6 — Missing explicit comparison baseline: trajectory-level CP (Minor).** The Related Work section discusses trajectory-based exchangeability (Moya et al., Gray et al., Gopakumar et al.) as a method to avoid the exchangeability problem, but the experiments do not include a trajectory-level CP baseline. Since the experimental setup uses 5000 training trajectories and 5000 calibration trajectories, trajectory-level CP is feasible. Including this baseline would show whether the extra complexity of WCP is justified beyond the simpler trajectory-level approach.

**W7 — Writing and presentation issues (Minor).**
- The backward heat equation (Figure 2) is ill-posed, which is not stated; this choice amplifies the coverage loss artificially.
- The abstract uses "facilitate" and "address it directly" which are vague; the abstract should state the linear-PDE restriction explicitly.
- The paper structure is unusual: the Conclusion is labeled "Discussion" and is only two short paragraphs. The Reproducibility Statement is over 5 lines long while the Discussion is ~8 lines.
- The "asymptotic... guarantees" claim in Remark 4.5 is not substantiated; no asymptotic analysis is provided in the main text or appendix (as presented in the markdown, the appendix is removed).

## Score
**Final Score: 6/10**

**Rationale:** The paper presents a technically sound combination of PDE semi-discretization theory with weighted conformal prediction (Theorem 4.2), and the main methodological idea — using closed-form Gaussian densities from linear PDE dynamics to compute likelihood-ratio weights — is clever and correctly executed. The function-space mutual singularity result (Theorem 4.1) appropriately motivates the need for discretization.

However, the score is constrained by three critical factors centered on research value and novelty:

1. **Scope overclaim (major validity risk):** The paper presents the method as applicable to a "broad class of PDEs" when it is restricted to linear PDEs with Gaussian initial conditions. Nonlinear PDEs, which dominate real-world scientific computing, are excluded. This gap between presentation and actual contribution reduces the research value.

2. **Infinite-band regime (major practical limitation):** In the very settings where WCP is most needed (unstable PDEs with large distribution shift), the method outputs infinite bands on 35–100% of test cases, providing no useful prediction intervals. This fundamentally limits practical deployability.

3. **Limited experimental validation:** Tests are confined to a single linear PDE family with no well-posed forward-parabolic or nonlinear benchmarks. Missing statistical rigor (no error bars, no significance tests).

The paper's strengths in mathematical rigor and the cleverness of the WCP-density approach argue for a score in the mid-range, but the overclaiming and practical limitations prevent a higher evaluation. Revision addressing the scope claims and expanding the experimental validation could raise the score to 7/10.