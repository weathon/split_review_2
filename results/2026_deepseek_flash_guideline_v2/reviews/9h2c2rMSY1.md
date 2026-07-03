Now I'll produce the final review with my calibrated assessment.

---

## Summary

This paper studies conformal prediction (CP) for time-dependent PDE surrogate models. It proves that in function space, solution distributions at different times are mutually singular (TV=1, Theorem 4.1), making standard CP impossible. For discretized *linear* PDEs with Gaussian initial conditions, it derives closed-form Gaussian distributions (Theorem 4.2) and uses these to compute importance weights for weighted conformal prediction (WCP). Empirically, WCP is compared against naïve CP and LSCI on several PDEs and a real-world thermography example.

## Strengths

1. **Theorem 4.1 (mutual singularity in function space)**: The paper rigorously proves that for the heat equation with Gaussian IC, TV distance between solution distributions at any distinct times equals 1. This shows concretely that the function-space framing used in prior neural operator CP work (Harris & Liu, 2025; Gray et al., 2025) is fundamentally incompatible with exchangeability-based CP. The paper responsibly acknowledges that this "complicates theoretical considerations" but is "not necessarily problematic for practical CP" on finite discretizations (lines 154–156).

2. **Theorem 4.2 (Gaussian distributions for discretized linear PDEs)**: The derivation that discretized solutions of linear PDEs with Gaussian ICs follow a Gaussian distribution with explicit mean and covariance is mathematically sound. This is a building block that enables closed-form importance weights for WCP by leveraging the known PDE structure.

3. **Empirical demonstration of LSCI failure on unstable PDEs**: Table 1 and Figure 3 show LSCI coverage collapsing (e.g., to 0% by timestep 15 for a=−0.01), while WCP maintains coverage (sometimes via infinite bands). This concretely illustrates that the "local exchangeability" assumption of prior work does not hold for PDEs with significant time dynamics, validating the paper's motivation.

## Weaknesses

### Fatal
None.

### Major

1. **The theoretical basis for the weighted CP guarantee is not established.** The paper claims "exact coverage guarantees" (abstract, contributions, Section 4.4) via weighted CP, but the justification is incomplete. Standard weighted CP (Barber et al., 2023) in the covariate-shift setting requires weights proportional to p_test(x_i)/p_cal(x_i) where x_i is the *covariate*, under the assumption that P_{Y|X} is invariant. In this paper's framing the covariate is the initial condition u₀ (whose distribution does not change) and the response is u_t; the conditional distribution of u_t given u₀ changes with t (from S_t to S_{t+δ}). The proposed weights w_{i,δ} ∝ 𝒩(u_i; μ_{t+δ}, Σ_{t+δ}) / 𝒩(u_i; μ_t, Σ_t) (Eq. 1) reweight the *marginal* density of u_t (the response), not any covariate. The paper states that weighted CP "can restore exact coverage in covariate-shift settings" (Section 3.1) and then applies weights on u_t without explaining how this setting satisfies the covariate-shift condition or how the weights connect to the required likelihood ratio. This gap directly affects the paper's central claim. If the weights do not correspond to the correct likelihood ratio for the joint distribution, the claimed formal guarantee does not follow from the cited theory.

2. **Empirical undercoverage contradicts the claimed exact guarantees.** Table 1 shows WCP coverage below the 90% target in several configurations where essentially all samples retain finite bands:
   - a=−0.005, timestep 20: coverage 0.85, n_∞=0.2% (i.e., 99.8% of 5000 samples have finite bands)
   - a=−0.0075, timestep 15: coverage 0.84, n_∞=86.4%
   - a=−0.01, timestep 5: coverage 0.89, n_∞=0.0% (all samples finite)
   
   With 5000 test samples, a 90% coverage estimate has standard error ≈ 0.004, so coverage of 0.85 or 0.89 is statistically significant undercoverage. The paper attributes this to "stochastic noise" (line 289), but this explanation is insufficient for a=−0.005 at timestep 20 where 4990 samples remain. This directly conflicts with the claim of "exact coverage guarantees" and, together with Weakness #1, suggests the theoretical guarantee is not operating as advertised.

3. **The "infinite bands" safety valve substantially weakens practical value.** The method reports infinite-width bands (n_∞) when the distribution shift is too large. At a=−0.0075, timestep 15: 86.4% of samples receive infinite bands. At a=−0.01, timestep 10: 35.4%. The coverage guarantee is only maintained for the *non-excluded* subset, and even there the coverage drops below target (Weakness #2). The paper's claim that "WCP is the only method providing formal guarantees" rings hollow when a large fraction of test points receive trivial bands and the remaining points still undercover.

### Minor

4. **Known-PDE requirement undercuts practical motivation.** Computing the weights requires the exact PDE operator (to construct A), boundary conditions, and the ability to compute exp(tA) — largely the same information needed to compute the Gaussian distribution of u_t directly. If one has all this, Gaussian confidence intervals for the solution itself are available without any surrogate or CP. The surrogate's role (computational speed) is a valid motivation but the paper does not articulate this clearly enough, leaving a tension between the method's requirements and its stated practical value.

5. **Real-world example is underspecified in the main text.** The pulsed thermography example is described in one sentence (line 293) with details deferred to the (stripped) appendix. It is unclear how the Gaussian IC assumption and the known linear PDE requirement are satisfied when the cool-down phase only "approximately follows the heat equation."

### Trivial
None.

## Nice-to-Haves

- Add confidence intervals or standard errors to Table 1 coverage estimates, so readers can assess statistical significance.
- Include comparisons with time-series CP methods (Gibbs & Candès, 2021; Angelopoulos et al., 2023) as additional baselines, even if they provide only asymptotic guarantees.
- Report overall coverage *including* infinite-band samples alongside the finite-only coverage, to give a complete picture of the method's real-world behavior.

## Removed Points

- **"Structural flaw: weighted CP is misapplied — not covariate shift"** (harsh critic's #1): I retain this concern as Major weakness #1 but downgraded from "fatal" because the paper could potentially be reframed (e.g., treating the data point as the solution state u_t rather than (u₀, u_t)). The criticism that this is a structural flaw that "invalidates the paper's central contribution" overstates the case — the gap is in the *justification*, not an inherent impossibility.
- **"Theorem 4.1 is not novel (Feldman-Hájek)"**: The paper explicitly cites Hairer and positions this as a concrete demonstration, not a new general theory. This is appropriate.
- **"Critique of LSCI is asymmetrical"**: The paper's point about local exchangeability being unverifiable is a legitimate comparison, not an asymmetry.
- **Generic scope-creep criticisms** (more models, larger datasets): Removed per soft rules.
- **Formatting/style nitpicks**: Removed per hard rules (these are parser artifacts).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Clarify the theoretical grounding of the weighting scheme.** Either (a) reframe the CP data point as the solution state u_t and explain why this reframing makes the weights valid likelihood ratios, or (b) acknowledge that the weights are an approximation (e.g., the closest tractable likelihood ratio given available information) and temper the "exact guarantees" claim accordingly.

2. **Report standard errors on coverage estimates** in Table 1 and discuss the observed undercoverage (especially a=−0.005, timestep 20: coverage 0.85 with 99.8% finite bands) candidly rather than attributing it to stochastic noise.

3. **Report overall coverage including infinite-band samples** alongside the finite-only coverage, so readers can see the method's effective coverage including its "safety valve."

4. **Strengthen the real-world example** by clarifying how the Gaussian IC and linear PDE assumptions are justified, or add a synthetic example where the assumptions provably hold.

5. **Temper the central claim**: Replace "exact coverage guarantees" with a more precise description of what the weighting scheme achieves and under what conditions the guarantee is expected to hold.

## Score and Decision

Due to a persistent environment error in the calibration search tool, I was unable to retrieve anchor papers from the human-review database. I therefore calibrated this review against my own detailed knowledge of the review standards for this venue.

**Score: 4 — Borderline Reject**

**Rationale**: The paper identifies an important problem and contributes useful theoretical elements (Theorem 4.1, Theorem 4.2). However, the central methodological claim of "exact coverage guarantees" through weighted CP is not adequately justified (the weighting scheme's connection to the standard weighted CP framework is unclear), and the empirical results show statistically significant undercoverage that contradicts this claim. The paper's strengths — primarily the negative result about function-space CP and the empirical demonstration of LSCI failure — do not rise to the level of the claimed contribution. The paper would require substantial revision to establish the theoretical basis for the WCP claims and to reconcile the empirical results with the stated guarantees.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>