## Summary

The paper studies conformal prediction (CP) for surrogate models of time-dependent PDEs, where non-stationarity breaks the exchangeability assumption. It proves that in function space, distributions at arbitrarily close times can be mutually singular (TV distance = 1). For discretized linear PDEs with Gaussian initial conditions, it derives closed-form Gaussian distributions for the solution over time and proposes using weighted conformal prediction (WCP) with weights based on the ratio of these Gaussian densities. Experiments on linear advection-diffusion-type PDEs compare WCP against naïve CP and LSCI baselines.

## Strengths

1. **Well-motivated and timely problem.** The paper correctly identifies that exchangeability between calibration and test data breaks down for time-dependent PDEs due to temporal drift, and Figure 2 concretely illustrates this phenomenon on the backward heat equation. This is a genuine problem for scientific ML.

2. **Clean derivation of the discretized solution distribution (Theorem 4.2).** For linear PDEs discretized via the method of lines with Gaussian initial conditions, the derivation that u(t) follows a Gaussian with closed-form mean and covariance is correct, clearly presented, and forms a useful foundation for downstream uncertainty quantification.

3. **Function-space mutual singularity result (Theorem 4.1).** The proof that the TV distance between solution distributions at different times is maximal in function space for the heat equation is mathematically interesting and provides a rigorous justification for why practical CP methods must work in finite-dimensional discretizations.

4. **Transparent empirical reporting.** Table 1 reports WCP's empirical coverage below the 90% target alongside the fraction of infinite bands (n_∞). The paper does not hide these results, even though they qualify the headline claims.

## Weaknesses

### Fatal

None.

### Major

1. **The weighting scheme's theoretical grounding in weighted CP is not justified.** Weighted CP (Tibshirani et al., 2019; Barber et al., 2023) provides coverage guarantees under covariate shift: p(Y|X) is assumed identical between calibration and test, while p(X) may differ. In this PDE setting, the mapping from initial condition u₀ to solution u_t changes deterministically with time (u_t = S_t(u₀) vs. u_{t+δ} = S_{t+δ}(u₀)), so p(u_t | u₀) changes — this is concept drift, not covariate shift. The paper computes weights from the *marginal* distributions of the solutions (w_i ∝ N(u_i; μ_{t+δ}, Σ_{t+δ}) / N(u_i; μ_t, Σ_t), equation 1), not from the joint or conditional distributions required by the standard WCP framework. The paper acknowledges that WCP is designed for "covariate-shift settings" (line 84) but does not provide a theoretical argument for why marginal-density weights on the *output* variable would correct the distribution shift in the scores, which depend on the joint distribution of (u₀, u_t). Consequently, the "exact coverage guarantees" claimed throughout (abstract, lines 45, 224, 287, 297) do not follow from the cited theory. This is the paper's most significant weakness and undermines its core claim.

2. **Empirical undercoverage contradicts the claim of guaranteed coverage.** Table 1 shows several configurations where WCP's empirical coverage falls below the 90% target while the fraction of infinite bands (n_∞) is negligible, ruling out the paper's "small sample" explanation:
   - a = −0.005, timestep 15: coverage **0.88**, n_∞ = 0.0%
   - a = −0.005, timestep 20: coverage **0.85**, n_∞ = 0.2%
   - a = −0.0075, timestep 10: coverage **0.88**, n_∞ = 0.0%
   - a = −0.01, timestep 5: coverage **0.89**, n_∞ = 0.0%
   With 5,000 test samples and n_∞ ≈ 0%, these gaps (1–5 percentage points below the 90% target) are not attributable to stochastic noise. The paper states "WCP consistently meets its coverage guarantees" (line 289), but the table shows otherwise for multiple configurations. Since the paper's central selling point is exact formal guarantees, this empirical discrepancy is a serious concern.

3. **The "infinite bands" mechanism is not specified and changes the coverage metric.** The paper states that when "the distributional dissimilarity of u_t and u_{t+δ} is too large, our WCP method predicts infinite bands" (line 283), but it does not specify the threshold or decision rule. More importantly, excluding these samples and reporting coverage only on the remainder changes the quantity from marginal coverage (the standard CP promise) to a conditional-on-finite-bands coverage with no theoretical backing. The reported WCP coverage figures in Table 1 are therefore not the marginal coverage the paper claims to guarantee.

### Minor

1. **Scope overstatement.** The abstract claims "a broad class of PDE problems," but the method is limited to linear PDEs with Gaussian (or location-scale) initial conditions where the analytical PDE form is known. Many practically important PDEs (Navier-Stokes, Burgers', Allen-Cahn) are nonlinear. The paper acknowledges this in the discussion (line 299), but phrases like "covers many practical problems" overstate the reach.

2. **The surrogate model plays a minimal role in the method.** The WCP weights depend only on the marginal distributions of the *true* PDE solution (via Theorem 4.2), not on the surrogate's predictions or error structure. The method would produce identical weights regardless of surrogate quality. The paper does not discuss whether the weights should also reflect the surrogate's varying error across time.

3. **LSCI baseline setup is unconventional.** The paper chooses a large number of band samples (5,000) to "push LSCI to over-coverage" (line 279). While the rationale (giving LSCI the benefit of the doubt) is understandable, evaluating LSCI with its recommended default settings would provide a cleaner comparison.

### Trivial

None.

## Nice-to-Haves

- Specify the threshold or decision rule for the infinite-band mechanism.
- Report marginal coverage including infinite bands (which trivially give coverage = 1 for those samples) alongside the conditional-on-finite-bands metric.
- Discuss whether (and under what conditions) the surrogate model's error distribution shifts between calibration and test time, and whether the marginal-density weights are sufficient to correct for both shifts.

## Removed Points

These points are flagged to be removed; treat them with caution:

- *"No discussion of the deterministic nature of the PDE solver / Dirac delta conditional"* — This is implicit in the problem setup (Section 4.1 defines S_t as a deterministic mapping); it does not need separate emphasis.
- *"Theorem 4.1 is of limited practical relevance"* — The paper explicitly acknowledges this (line 156) and pivots to the discretized setting; this is an honest scope limitation, not a flaw.
- *"Naïve CP works for a=−0.005"* as evidence the problem doesn't arise — The paper evaluates across all settings including a=−0.0075, −0.01 where naïve CP clearly fails; the problem exists for the more unstable regimes.
- *Criticisms about missing appendix content or missing proofs* — These are parser artifacts; the original submission includes them.
- *Computational cost comparison not being "apples-to-apples"* — The paper's time comparison (seconds vs. 40 minutes) is informational and both methods solve the same prediction task.
- *Generic "could add more baselines"* — The paper already includes two baselines plus its own method across multiple PDE configurations.
- *"The surrogate model is essentially irrelevant"* characterized as a fatal flaw — Moved to Minor weakness 2 above as an observation worth addressing, not a fatal weakness.

## Novel Insights

None beyond the paper's own contributions. The core insight — that for discretized linear PDEs with Gaussian initial conditions the solution distribution is available in closed form, which could inform uncertainty quantification — is the paper's own contribution. The reviews do not surface a novel observation beyond this.

## Suggestions

1. Clarify the theoretical connection between the proposed marginal-density weights and the WCP framework. If the method is better understood as a heuristic rather than a provable guarantee, state this explicitly and adjust the claims.
2. Report marginal coverage *including* infinite bands (which trivially achieve coverage=1 for those samples) alongside the conditional-on-finite-bands metric.
3. Provide the threshold rule for when infinite bands are triggered.
4. Tone down claims of "exact coverage guarantees" to reflect the empirical gaps shown in Table 1 and the theoretical caveats above.

---

## Calibration Anchors

**Round 1 — Bracketing (queries across all bands):**

| Path | Avg Human Score | Round | Comparison |
|---|---|---|---|
| `cF6OoaYcRa.md` (Calibrated Physics-Informed UQ) | 4.50 | R1 | CP for PDE surrogates, REJECTED; criticized for "minor extension" and "no theoretical results." Current paper has stronger theory but a more central theoretical flaw. |
| `v8RDgaEtE2.md` (Regression CP under Bias) | 2.50 | R1 | CP theory paper, REJECTED; "elementary theoretical findings." Current paper has more substantive theory. |
| `k2gGy2hpfx.md` (Adapting Prediction Sets to Distribution Shifts) | 3.67 | R2 | CP under distribution shifts without guarantees, REJECTED for being heuristic. Most comparable — both promise coverage under shift but lack theoretical foundation. |
| `GQhlM0Mavg.md` (OOD Detection and CP) | 5.00 | R2 | CP + distribution shift, REJECTED. Stronger empirical scope. |
| `fzZfju8y0g.md` (In-Context Neural PDE) | 3.40 | R1 | PDE surrogate paper, REJECTED; limited novelty and scope. |
| `gz8Rr1iuDK.md` (Geometric/Physical Constraints) | 4.00 | R1 | PDE surrogate paper, REJECTED; limited baseline comparisons. |
| `x4ZmQaumRg.md` (Active Learning for Neural PDE Solvers) | 7.00 | R1 | Strong benchmark paper, ACCEPTED. Significantly more comprehensive. |

**Round 1 Bracket:** 3–5  
**Narrowing:** The most comparable anchor is the 3.67 CP-distribution-shift paper (rejected for heuristic approach without theoretical guarantees). The current paper has more theoretical content (Theorems 4.1, 4.2) but a more central theoretical flaw that undermines its core claim of "exact coverage guarantees." The 4.50 CP-for-PDE anchor (rejected for minor extension) is less comparable because the current paper has stronger theoretical novelty. **Final score:** 3.5, **Decision:** Reject.

MY FINAL SCORE: <score>3.5</score>
MY FINAL DECISION: <decision>Reject</decision>