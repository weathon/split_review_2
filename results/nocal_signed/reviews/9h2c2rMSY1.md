Now let me finalize my review.

## Summary

This paper studies conformal prediction for surrogate models of time-dependent PDEs, where the non-exchangeability of calibration and test distributions over time breaks standard CP guarantees. The paper contributes: (1) Theorem 4.1 showing that in function space, solution distributions at different times can be mutually singular (TV distance = 1), ruling out function-space approaches; (2) Theorem 4.2 providing closed-form Gaussian distributions for discretized linear PDEs with Gaussian initial conditions; (3) a weighted conformal prediction procedure using density ratios derived from these distributions; and (4) empirical evaluation on a synthetic linear advection-diffusion-reaction PDE and a real-world thermography dataset.

## Strengths

- **Clean problem diagnosis (Section 1, Section 4.1).** The paper correctly identifies a genuine and underappreciated problem: time-dependent PDE solutions produce distribution drift that violates the exchangeability assumption of standard conformal prediction.

- **Theorem 4.1 (Section 4.2).** Showing that for the heat equation with Gaussian initial conditions, the TV distance between solution measures at any two different times is maximal in the function-space setting is a striking negative result that cleanly rules out a family of function-space approaches.

- **Theorem 4.2 (Section 4.3).** The derivation showing that discretized linear PDEs with Gaussian ICs yield Gaussian solutions with explicit mean and covariance is mathematically sound and provides the technical foundation for the weighted CP approach.

- **Honesty about infinite bands (Table 1, Section 5).** The paper transparently reports `n_infinity` — the fraction of test samples for which WCP yields infinite (trivial) bands — and correctly argues that trivial coverage is preferable to false coverage in safety-critical settings.

## Weaknesses

### Fatal
None.

### Major

- **Table 1 shows systematic undercoverage below the 90% target in multiple settings where n_infinity is near zero.** Specific examples from Table 1: a=-0.005, timestep 15: coverage 0.88, n_infinity=0.0%; a=-0.005, timestep 20: coverage 0.85, n_infinity=0.2%; a=-0.0075, timestep 5: coverage 0.89, n_infinity=0.0%; a=-0.0075, timestep 10: coverage 0.88, n_infinity=0.0%; a=-0.01, timestep 5: coverage 0.89, n_infinity=0.0%. With 5000 test samples, these are not explainable by stochastic noise (e.g., 0.85 is ~12 standard errors below 0.90). This directly contradicts the paper's central advertised claim of "exact coverage guarantees" (abstract) and being "the only method providing reliable coverage" (Sec. 1). The paper's discussion of this effect (line 289) attributes similar drops only to high n_infinity ("higher stochastic noise"), which does not apply to these cases with near-zero n_infinity.

- **There is a conceptual ambiguity in how the weighted CP covariate-shift framework is applied.** Section 3.1 correctly states that weighted CP requires density ratios p_test(x)/p_cal(x) where x is the covariate. However, Eq. (1) defines weights using the ratio of marginal solution densities (p(u_t+δ)/p(u_t)), not the covariate (u_0) — and the covariate distribution (initial conditions) does not shift with time. The paper does not clarify what constitutes X and Y in its CP formulation, nor does it formally establish why the density ratio of the marginal solution distribution is the correct weighting for residuals of the surrogate model. This gap may explain the undercoverage in Table 1 and makes it unclear whether the claimed theoretical guarantee should hold in the reported experimental setup.

- **Remark 4.5 makes an unsupported claim.** It states that the paper provides "asymptotic—and in some cases even non-asymptotic—guarantees" for transferring discretized coverage to the original function-space solution, but provides no details — just an appeal to "numerical error guarantees of the scheme." This is too vague to constitute a contribution.

- **The real-world validation is substantively absent from the main paper.** It is described in a single sentence (line 293): "Our method achieves target coverage over all tested time steps," with no quantitative results, coverage numbers, bandwidths, or n_infinity reported. A paper claiming validation on real data should include these numbers in the main text. (Details relegated to the appendix do not remedy this, as the main text makes the claim without evidence.)

### Minor

- **The empirical evaluation lacks confidence intervals, standard errors, or any statistical significance test.** Given that the paper's core claim hinges on whether coverage reaches the target, this omission makes it difficult to assess which deviations from 90% are meaningful.

- **The baseline comparison is not maximally informative.** Naïve CP and LSCI are applied in settings where their assumptions (exchangeability and local exchangeability, respectively) are known to be violated, so their failure is unsurprising. Comparing WCP against an oracle baseline (e.g., exact Gaussian quantiles) would better isolate whether the CP machinery adds value beyond the parametric knowledge already used to compute the weights.

- **Theorem 4.1's connection to the rest of the paper is loose.** After proving it, the paper immediately notes that it is "not necessarily problematic for practical CP on surrogate models" (line 156) and moves on. The paper would benefit from discussing what this result implies about existing function-space CP work and whether it affects methods like LSCI.

- **The rationale for LSCI hyperparameter choices is unclear.** "We choose a large number of band samples to push LSCI to over-coverage, so undercoverage can be evaluated in a fair manner" (line 279) appears to assume a specific outcome and does not follow standard hyperparameter selection logic.

## Nice-to-Haves

- An ablation study varying the discretization resolution n, and a sensitivity analysis to misspecification of the operator A or the Gaussian assumption.
- A comparison to a simple Gaussian-quantile baseline (oracle) to reveal how much efficiency is lost or gained by using CP's distribution-free machinery.
- Discussion of how practitioners would obtain A or verify the Gaussian assumption in practice.

## Removed Points

*The following criticisms from the input review were filtered out as they do not survive the verification and filtering rules:*

- **Figure 3 described as a parser artifact** — this is a parser issue, not a paper flaw.
- **Testing only in the unstable regime** — the paper explicitly justifies this design choice (line 244), so this is not a valid weakness.
- **Lack of ablation study or sensitivity analysis** — moved to Nice-to-Haves (not a core weakness).
- **No comparison to Gaussian-quantile baseline** — moved to Nice-to-Haves.
- **Computational cost comparison uninformative** — subsumed by the more substantive baseline criticism above.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Resolve the undercoverage issue.** Before any other revision, understand why WCP undercovers in settings with near-zero n_infinity (Table 1). If the conceptual gap (weights based on solution densities rather than score densities) is responsible, either correct the weighting or formally justify why the solution density ratio applies to the score distribution. If the gap is not responsible, identify and fix the other source of the violation.

2. **Add statistical rigor to the evaluation.** Report binomial confidence intervals for all coverage numbers and test the null hypothesis that true coverage ≥ 0.90.

3. **Clarify the CP formulation.** Precisely specify what the covariate X and response Y are, and formally state why the covariate-shift framework (or an alternative) applies. Show the connection between Theorem 4.2's Gaussian solution distribution and the distribution of the scores used in weighted CP.

4. **Substantiate the real-world validation** with quantitative results (coverage, bandwidth, n_infinity) in the main text.

5. **Either substantiate or remove Remark 4.5's claim** about asymptotic/non-asymptotic guarantees.

## Score and Decision

The paper identifies a genuine problem and contributes interesting theoretical results (Theorems 4.1 and 4.2). However, the central empirical claim — that WCP provides "exact coverage guarantees" — is contradicted by the paper's own Table 1, which shows systematic undercoverage below the 90% target in multiple settings where near-zero samples were excluded. This is compounded by a conceptual ambiguity about whether the weighted CP framework is correctly applied to the surrogate model residual setting. The paper would need substantial revision to address these issues before its empirical claims could be accepted. I recommend rejection in its current form, with encouragement to resubmit after resolving the undercoverage problem and clarifying the theoretical justification.

MY FINAL SCORE: <score>3.0</score>
MY FINAL DECISION: <decision>Reject</decision>