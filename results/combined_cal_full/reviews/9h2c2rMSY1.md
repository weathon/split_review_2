Now I have all the information I need. Let me compile the final review.

**Round 1 bracket:** Given the comparison with the closest anchor (cF6OoaYcRa at 4.50), my initial bracket is 3.5–5.0. This narrows to approximately 4.0 after comparing weighted items: my paper shares similar-weight major weaknesses (theoretical gap at -6.21 vs their -5.36, infinite bands limitation at -7.98) but has slightly weaker strengths (problem identification at +1.40 vs their +4.46 motivation). The coverage violations at -2.79 are a unique weakness not present in the anchor.

Here is the final consolidated review.

---

## Summary

This paper studies conformal prediction (CP) for time-dependent PDE surrogate models, where standard exchangeability fails because the solution distribution drifts over time. The authors prove that for discretized linear PDEs with Gaussian initial conditions, the solution at any time is Gaussian with closed-form mean and covariance (Theorem 4.2), enabling likelihood-ratio weights for weighted conformal prediction. They compare against naïve CP and Local Spectral Conformal Inference (LSCI) on a linear second-order PDE with tunable instability and on a real-world thermography dataset.

## Strengths

- **Identifies a genuine problem.** Exchangeability failure in time-dependent PDE surrogates is a real gap in the scientific ML literature. The paper correctly diagnoses why existing methods (trajectory-based exchangeability, local exchangeability) make assumptions that break for non-stationary or unstable dynamics.

- **Theorem 4.2 is correct and well-deployed.** The result that the discretized solution of a linear PDE with Gaussian initial condition remains Gaussian with analytically computable $\boldsymbol{\mu}_t$ and $\boldsymbol{\Sigma}_t$ (via matrix exponential) is a standard linear-systems fact, but its recognition as enabling closed-form likelihood ratios for weighted CP is the paper's main technical contribution and is correctly derived.

- **Qualitative empirical pattern is informative.** Figure 3 and Table 1 show that naïve CP and LSCI empirically undercover as the PDE becomes more unstable, while WCP is more robust. The idea of reporting infinite bands when the distribution shift is too large (rather than over-covering silently) is a useful diagnostic concept.

- **Real-world validation.** The thermography experiment (appendix) demonstrates the method on a non-synthetic problem where the cooldown phase approximately follows the heat equation, supporting practical applicability.

## Weaknesses

### Fatal
None.

### Major

- **The weighting scheme's theoretical justification is incomplete.** The paper frames this as a covariate-shift problem (Section 3.1: "weighted CP can restore exact coverage in covariate-shift settings") and applies weights $w_{i,\delta} \propto \mathcal{N}(\mathbf{u}_i; \boldsymbol{\mu}_{t+\delta}, \boldsymbol{\Sigma}_{t+\delta}) / \mathcal{N}(\mathbf{u}_i; \boldsymbol{\mu}_t, \boldsymbol{\Sigma}_t)$. However, the standard weighted CP framework (Tibshirani et al. 2019; Barber et al. 2023) requires the likelihood ratio for the *covariate* under the assumption that $P(Y|X)$ is invariant. In this PDE setting, the distribution of the initial condition $u_0$ is the same for calibration and test; the shift is in the mapping $S_t$ from $u_0$ to $u_t$, so $P(Y|X)$ is not invariant. The paper provides no argument that weighting by the *solution* density restores exchangeability of the *nonconformity scores* (which depend on both $u_0$ and $u_t$). This gap affects every formal coverage claim. Additionally, the weight formula (1) requires the true solution $\mathbf{u}_{n+1}$ for the test point, which is unknown at deployment—the paper does not address how this is resolved in practice. The method may still work as a heuristic, but the claim of "formal coverage guarantees" under the standard weighted CP framework is unsupported.

- **Empirical results show statistically significant undercoverage contradicting the claimed guarantees.** For the most stable configuration ($a=-0.005$, $b=c=-0.5$) at time steps 15 and 20, WCP reports coverage of **0.88 and 0.85** against a target of 0.90, with $n_\infty$ of only 0.0% and 0.2% (essentially no infinite bands). With 5000 test samples, these are approximately 5 and 12 standard errors below the target. The paper's attempted explanation ("when $n_\infty$ approaches roughly 90%, WCP shows a slight drop") does not apply here since $n_\infty$ is near zero. These are the least challenging settings for the method, and the coverage failures directly undermine the central claim of exact coverage guarantees. This result is consistent with the concern above that the weighting scheme may not provide the guarantees the paper claims.

- **The method's scope is narrower than the paper's framing suggests.** The title, abstract, and introduction discuss "time-dependent PDEs" broadly and claim applicability to "a broad class of PDE problems." The method in fact applies only to **linear PDEs** with linear boundary conditions and **Gaussian (or location-scale) initial conditions**, with discretization via method of lines. Many practically important PDEs (Navier-Stokes, Burgers, reaction-diffusion with nonlinear reactions, Euler equations) are nonlinear and thus excluded. The discussion relegates nonlinearity to "a natural next step," but this is a structural limitation of the method's mathematical foundation (Theorem 4.2 requires linearity), not an incremental extension.

- **The method produces infinite bands in most practically relevant unstable regimes.** From Table 1: for $a=-0.0075$ at step 15, $n_\infty=86.4\%$ and at step 20, $100\%$; for $a=-0.01$, $n_\infty=35.4\%$ at step 10 and $100\%$ at steps 15/20. The only regime yielding consistently finite bands is the most stable configuration ($a=-0.005$) where other methods also perform reasonably well. While reporting infinite bands is framed as a feature (safe refusal), it means the method is largely uninformative precisely when instability makes UQ most critical. This is a practical limitation that should be more prominently discussed.

### Minor

- **Surrogate model residuals and Gaussian dynamics.** The weights are computed using the known Gaussian distribution of the *true solution* $\mathbf{u}_t$, but the nonconformity scores operate on *residuals* of an imperfect surrogate model. The paper does not discuss whether or why the score distribution inherits the same Gaussian structure as the underlying solution. A mismatch here would cause the likelihood ratio to be misspecified.

- **LSCI baseline comparison could be more informative.** The paper pushes LSCI toward over-coverage by using 5000 band samples, then evaluates its undercoverage. While this is a conservative choice, the LSCI bandwidth is constant at 0.02 across all settings, and the paper does not report a version of LSCI with properly tuned parameters per setting. A more complete comparison would present both coverage and interval width honestly for each method under fair tuning.

- **Coverage estimates lack confidence intervals.** Coverage values in Table 1 are reported as point estimates. Given that the coverage violations at $a=-0.005$ are the most critical results, confidence intervals or standard errors would allow readers to directly assess statistical significance.

- **Scalability to large spatial grids is unaddressed.** Computing the Gaussian density requires inverting $n \times n$ covariance matrices, costing $O(n^3)$. For 2D or 3D PDEs with fine discretizations this becomes prohibitive. The paper does not discuss this limitation.

### Trivial
None.

## Nice-to-Haves

- Characterize the conditions under which infinite bands occur in terms of spectral properties of the PDE operator and the discretization, giving practitioners clear guidance.
- Include non-Gaussian initial condition experiments from the appendix in the main text.
- Discuss sensitivity of the method to the spatial discretization (grid spacing, finite-difference scheme).

## Removed Points

These points were raised by the harsh critic but are removed with justification:

- **Theorem 4.1 (function space mutual singularity) has weak connection to main method.** *Removed.* The paper explicitly acknowledges that the function-space result is "not necessarily problematic for practical CP" and positions it as motivation. This is a valid framing choice.
- **LSCI comparison is unfair.** *Demoted to minor.* Pushing LSCI to over-coverage and then evaluating undercoverage is actually a conservative test that strengthens the paper's point. The more substantive concern (constant bandwidth, lack of per-setting tuning) is kept as minor.
- **Characterization of Harris & Liu (2025) is unfair.** *Removed.* The paper's statement that LSCI "assumes local exchangeability" is factually accurate.
- **Theorem 4.2 novelty is modest.** *Removed.* The paper's contribution is recognizing the implication for weighted CP, not the theorem itself.
- **Formatting/style nitpicks.** *Removed per hard rules.*
- **Missing appendix content.** *Removed.* The parser strips appendices from all papers.

## Novel Insights

None beyond the paper's own contributions. The harsh critic's observation about the fundamental disconnect between the standard covariate-shift weighted CP framework and the PDE setting (where the shift is in the response distribution, not the covariate) is a genuinely insightful criticism that the paper should address, but it is captured in the weaknesses above rather than being a separate novel insight.

## Suggestions

1. **Justify the weighting scheme formally.** Provide a rigorous theoretical argument for why weighting by the solution density $\mathcal{N}(\mathbf{u}_i; \boldsymbol{\mu}_{t+\delta}, \boldsymbol{\Sigma}_{t+\delta}) / \mathcal{N}(\mathbf{u}_i; \boldsymbol{\mu}_t, \boldsymbol{\Sigma}_t)$ correctly adjusts the nonconformity score distribution. If the standard covariate-shift framework does not apply directly, provide a new result or clearly state the assumptions under which coverage guarantees hold.
2. **Investigate and explain the coverage violations** at $a=-0.005$, steps 15 and 20. If this is an implementation bug, fix it. If it reflects a fundamental limitation (e.g., the weighting scheme does not actually provide exact coverage), acknowledge this and adjust claims.
3. **Qualify the scope** in the abstract and introduction to clearly state that the method applies to linear PDEs with Gaussian (or location-scale) initial conditions.
4. **Add confidence intervals** or standard errors to all coverage estimates in Table 1.
5. **Explain test-time weight computation** — how is the test point's weight computed when the true solution $\mathbf{u}_{t+\delta}$ is unknown?
6. **Discuss the surrogate model mismatch** — whether the nonconformity scores inherit the Gaussian structure of the true solution, and what happens when they do not.

## Score and Decision

**Score: 4.0 — Borderline Reject**

**Decision: Reject**

**Reasoning.** The paper identifies a real and important problem (exchangeability failure in PDE surrogates) and contains a correct theoretical building block (Theorem 4.2). However, it has two structural issues that prevent acceptance. First, the application of weighted CP to this setting lacks theoretical justification — the paper does not explain how the standard covariate-shift framework applies when the shift is in the response distribution, and the test-point weight depends on the unobserved future solution. Second, the empirical results directly contradict the claimed guarantees: the method undercovers (0.88, 0.85 vs. 0.90) in the regime where it should work best, with no adequate explanation. Additionally, the method applies only to linear PDEs (a much narrower class than the paper's framing suggests) and resorts to infinite bands in precisely the unstable regimes where UQ is most needed. These weaknesses collectively undermine the paper's central claims. A revision would require a proper theoretical grounding of the weighting scheme and resolution of the coverage violations, not merely additional experiments.

**Calibration Anchors.**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| cF6OoaYcRa (Calibrated Physics-Informed UQ) | 4.50 | R1, R2 | Yes | Most similar paper (CP + PDE surrogates). Stronger problem motivation (+4.46 vs our +1.40) but similar-magnitude theoretical gaps. Our paper has unique coverage-violation weakness. Slightly below this anchor. |
| i3T0wvQDKg (Valid CP for Dynamic GNNs) | 5.80 | R1 | Yes | Addresses non-exchangeability in a different domain with rigorous theoretical guarantees. Our paper is notably weaker on theoretical rigor. |
| v8RDgaEtE2 (Regression CP under Bias) | 2.50 | R1 | Yes | Suffered from serious theoretical errors. Our paper's theory is correct (Theorem 4.2) and thus stronger than this anchor. |
| LwAG269lIq (Data-Driven PDE Discovery) | 3.00 | R1 | Yes | Different topic (PDE discovery, not CP). Comparable quality issues (limited scope, incomplete evaluation). |
| p8sr9kfUbQ (JANET: CP for Time-Series) | 3.50 | R2 | Yes | CP for non-exchangeable time series. Similar weakness profile: incremental theory, limited experiments. Our paper has more serious foundational gaps. |
| 5t57omGVMw (Learning to Relax) | 8.00 | R1 | Yes | High-quality theory paper in a different area. Not directly comparable. |

**Weighted-item comparison placing this paper at 4.0:** My paper shares a large-magnitude theoretical-concern weakness with cF6OoaYcRa (weighting-scheme gap at -6.21 vs their -5.36 theoretical void) and has an additional unique coverage-violation weakness (-2.79) that cF6OoaYcRa does not have. Meanwhile my paper's strengths (problem identification at +1.40, Theorem 4.2 at +3.45) are somewhat weaker than cF6OoaYcRa's (motivation at +4.46, methods clarity at +3.43). Weighting these together places this paper slightly below the cF6OoaYcRa anchor (4.50), in the 3.5–4.5 range. The coverage-violation weakness — which is a direct contradiction of the paper's core claim — justifies the lower end of this range, hence 4.0.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>