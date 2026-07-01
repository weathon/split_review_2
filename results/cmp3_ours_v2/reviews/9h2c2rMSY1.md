Now I have all the information needed to produce the final consolidated review.

## Summary

This paper studies conformal prediction (CP) for surrogate models of time-dependent PDEs. It proves (Theorem 4.1) that for the heat equation with Gaussian initial conditions, solution distributions at distinct times are mutually singular in function space, explaining why a function-space CP approach cannot work. On discretized domains, it shows (Theorem 4.2) that the solution distribution for linear PDEs with Gaussian initial conditions remains Gaussian with closed-form mean and covariance, enabling weighted conformal prediction (WCP) with exact density ratios. Experiments on linear PDEs demonstrate that WCP maintains target coverage while baselines (naïve CP, LSCI) undercover.

## Strengths

1. **Theorem 4.1 (mutual singularity in function space) is a clean theoretical result.** It shows that for the heat equation with Gaussian IC, the TV distance between solution distributions at any two distinct times is maximal (=1). This crisply explains why a pure function-space CP approach (common in the neural operator literature) cannot work and justifies the turn to discretized domains. The proof is concrete and well-placed as motivation.

2. **The core technical idea (Theorem 4.2 + weighted CP) is sound and correctly executed.** Theorem 4.2 correctly characterizes the distribution of the discretized solution for linear PDEs with Gaussian ICs, and the weighted CP machinery (weights via closed-form Gaussian density ratios) is a precise application of established theory (Barber et al. 2023). Within its stated assumptions, the reasoning contains no error.

3. **The paper identifies a real and underappreciated problem.** Time-dependent PDEs break exchangeability, and existing CP-for-PDE work either ignores this, sidesteps it (trajectory-level calibration that does not address deployment shifts), or assumes local exchangeability without verification. The paper frames this gap clearly and motivates why naïve CP and LSCI fail.

## Weaknesses

### Fatal
None.

### Major

1. **Scope inflation: the title and abstract overstate the method's generality relative to what is actually delivered.** The title reads "Weighted Conformal Prediction for Time-Dependent PDEs," the abstract promises "a broad class of PDE problems," and the introduction claims "exact coverage guarantees for PDEs without limiting assumptions on their time-dependent behavior" (line 45). However, the method (Theorem 4.2) requires: (a) a **linear** spatial differential operator, (b) **linear** boundary conditions, (c) a **Gaussian** (or location-scale) initial condition distribution, and (d) full knowledge of the discretized PDE operator **A**. The claim about "time-dependent behavior" is defensible as referring to the temporal drift of the distribution (no stationarity/mixing assumptions), but a reader would reasonably infer broader PDE applicability from the title and abstract. The discussion (line 299) honestly states "the class of linear PDEs," but the abstract and introduction lack this qualification. For a conference where breadth of contribution matters, this mismatch is significant.

2. **The evaluation does not test the method under violations of its core assumptions.** The paper tests WCP only on linear PDEs where all assumptions hold — necessary but not sufficient. The most informative experiments would test robustness when assumptions are violated: (i) non-Gaussian initial conditions **outside** the location-scale family (multimodal, mixtures, heavy-tailed), (ii) nearly-linear PDEs with small nonlinear perturbations, (iii) a misspecified or coarsely discretized **A** matrix. The paper mentions location-scale experiments in Appendix A.8 (line 214), which covers some non-Gaussian cases, but robustness outside this family — where closed-form weights are misspecified — is untested. Without such experiments, it is unclear whether the method degrades gracefully or catastrophically when its conditions are not perfectly met.

3. **No uncertainty quantification on the coverage estimates.** Coverage numbers are reported without error bars, standard deviations, or confidence intervals (confirmed by grep — no matches for std, standard deviation, confidence interval, or ±). With 5000 test samples, coverage estimates have sampling variance. For example, the reader cannot assess whether WCP's reported coverage of 0.88 (a=-0.005, step 15) significantly differs from the 0.9 target or is just noise.

### Minor

4. **WCP frequently returns infinite (trivial) bands precisely when distribution shift is largest.** At a=-0.01 (steps 15, 20): 100% infinite bands; at a=-0.0075 (step 20): 100% infinite bands, (step 15): 86.4% infinite bands. Coverage=1.0 on zero or near-zero non-infinite samples is not meaningful (Table 1, rows a=-0.0075 and a=-0.01). The paper is transparent about n_∞ and argues (line 287) that trivial bands are safer than undercoverage, which is defensible in safety-critical settings. However, it means the method's practical utility is limited to regimes where distribution shift is mild enough for WCP to produce finite bands — and in those mild-shift regimes, the paper does not compare WCP against baselines restricted to the same regime.

5. **The baseline comparison could be strengthened.** The paper compares against naïve CP (expected to fail by design) and LSCI (which assumes local exchangeability the paper argues does not hold). The comparison is informative but reduces partly to "our method beats methods whose assumptions are violated." Missing are comparisons to approaches that address non-exchangeability without requiring closed-form density ratios, such as weighted CP with estimated (non-parametric) density ratios or adaptive conformal inference (Gibbs & Candès 2021). These would test whether the linear-Gaussian structure is necessary for good coverage or whether simpler alternatives could suffice.

6. **The real-world example is barely described.** It receives one sentence in the main text (line 293) with all details deferred to the appendix, making it impossible to evaluate from the main paper. The practical workflow (offline solver → compute μ_t, Σ_t → deploy surrogate → apply WCP with precomputed weights) is not clearly articulated, nor is the computational cost of the offline matrix exponentials discussed.

### Trivial

7. The abstract should state "linear PDEs with Gaussian initial conditions" rather than "a broad class of PDE problems" to accurately reflect the method's scope.

## Nice-to-Haves

- Test robustness to non-Gaussian ICs outside the location-scale family, nearly-linear PDEs with small nonlinear perturbations, and misspecified **A** matrices.
- Report bootstrapped error bars or confidence intervals on all coverage numbers.
- Compare against weighted CP with estimated density ratios and/or ACI (Gibbs & Candès 2021).
- Clarify the practical workflow and quantify the offline computation (matrix exponential, numerical integration) required.
- Compare WCP against baselines restricted to the regime where WCP returns finite bands.

## Removed Points

The following points from the harsh critic review were filtered out:

- **"Theorem 4.1 is tangential"** — The paper itself acknowledges this (line 156: "not necessarily problematic for practical CP") and positions it as motivation. Not a weakness.
- **"Method requires full knowledge of PDE operator, undermining the motivating scenario"** — The paper explicitly states the use case (line 126: "assume we have an analytical form of the PDE") and the rationale (solvers are slow, surrogates are fast). This is a clearly stated limitation, not an oversight. The critic's question "why do they need a surrogate" is answered: surrogates are fast at inference time.
- **"Background introduces nonlinear PDEs but method requires linearity"** — Standard practice: set up general context, then scope to the tractable case. Not a weakness.
- **"LSCI comparison reduces to 'our method beats methods whose assumptions are violated'"** — This is the paper's intended argument: showing that existing methods fail because their assumptions are violated is a valid experimental contribution, not a flaw.
- **Various claims about missing appendix content** — Parser-stripped; the original submission contains these sections.
- **Formatting and style nitpicks** — Parser artifacts, not author errors.
- **Generic "method is narrow" without concrete anchor** — Already captured in Weakness #1 with specific quotes.

## Novel Insights

The harsh critic makes an interesting observation that the paper could have connected Theorem 4.1's function-space mutual singularity more directly to the discretized setting (e.g., by showing that the infinite-dimensional TV distance provides a lower bound for the discretized case). Currently the paper presents Theorem 4.1 and then pivots to the discretized setting without a formal bridge. This is a missed opportunity to tighten the narrative, but not a flaw — the paper clearly states the function-space result is motivational.

## Suggestions

1. **Revise the abstract and title** to explicitly state "linear PDEs with Gaussian (or location-scale) initial conditions" rather than "a broad class of PDE problems." This is the single most impactful fix.

2. **Add robustness experiments** testing the method under: (a) non-Gaussian ICs outside the location-scale family, (b) nearly-linear PDEs with small nonlinear perturbations, (c) a misspecified **A** matrix from a deliberately coarse discretization.

3. **Include confidence intervals** (bootstrapped or based on Normal approximation) for all coverage estimates throughout Table 1 and Figure 3.

4. **Add comparisons** to weighted CP with non-parametrically estimated density ratios and/or ACI (Gibbs & Candès 2021) to test whether the closed-form weights are necessary or merely sufficient.

5. **Articulate the practical workflow clearly**: the practitioner knows the PDE and discretization, uses the solver offline to compute μ_t and Σ_t (including matrix exponentials), then deploys the fast surrogate online with precomputed WCP weights. Quantify the offline cost.

6. **Expand the real-world example** in the main text, or replace it with a more substantial demonstration.

## Score and Decision

**Round 1 bracket**: 4.5–6.0. The paper is stronger than the rejected CP-for-PDE anchor at 4.50 (which lacked theory and baselines) and the PDE discovery papers at 3.0–3.4. It is weaker than the accepted time-series CP papers at 6.0 (which have broader scope, error bars, and stronger evaluations). The scope inflation and missing robustness tests prevent it from reaching the 6.0 level.

**Final calibrated score**: 5.0. The paper has genuine contributions (Theorem 4.1, sound application of weighted CP to a real gap) but is held back by scope inflation in the abstract/introduction, no robustness tests under violated assumptions, and absence of error bars. These are fixable issues but significant enough in the current form to place the paper below the acceptance threshold.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>