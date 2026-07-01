Now I have all the evidence needed. Let me produce the final consolidated review.

## Summary

The paper studies conformal prediction for surrogate models of time-dependent PDEs, where exchangeability fails because the solution distribution drifts. It proposes using weighted conformal prediction with closed-form likelihood ratios derived from linear PDE dynamics (Theorem 4.2): for discretized linear PDEs with Gaussian initial conditions, the solution remains Gaussian at all times, making density ratios tractable. The paper also presents a negative result (Theorem 4.1) about mutual singularity of solution distributions in infinite-dimensional function spaces. Empirically, the method is compared against naïve CP and LSCI on unstable linear PDEs.

## Strengths

1. **Theorem 4.2 cleanly bridges PDE theory and weighted CP.** The key insight — that linear PDEs with Gaussian initial conditions yield Gaussian solutions at all times, making the density ratio needed for weighted CP available in closed form — is mathematically sound and elegantly connects two literatures. The proof is in the main text and is correctly stated.

2. **The qualitative advantage over baselines is unambiguous.** In all configurations tested, naïve CP and LSCI exhibit severe coverage degradation as the PDE becomes more unstable (sometimes dropping to 0%), while WCP avoids total coverage collapse. This difference is visually evident in Figure 3 and Table 1 and is the core empirical message of the paper.

3. **The infinite-bands diagnostic is an honest feature.** Rather than silently undercovering, WCP reports when it cannot produce finite prediction bands. The paper correctly frames this as preferable to overconfident intervals in safety-critical settings.

4. **Real-world validation is provided.** The method is tested on a pulsed-thermography dataset (Wei et al., 2023) and achieves target coverage, demonstrating applicability beyond purely synthetic PDEs.

## Weaknesses

### Fatal

None.

### Major

1. **Empirical coverage drops below the target in the mildest test case, and the paper offers no applicable explanation.** For a = -0.005 at timestep 20, Table 1 shows WCP coverage = 0.85 against a 90% target, with only 0.2% of samples receiving infinite bands. With ~5000 test samples, a 5-percentage-point gap is far beyond statistical noise. The paper's stated explanation for coverage drops (Section 5: "When n_infinity approaches roughly 90%, WCP shows a slight drop in empirical coverage... with very few samples remaining, the empirical coverage is subject to higher stochastic noise") **does not apply** here — n_infinity is 0.2%, not ~90%. This directly contradicts the paper's claims of "exact coverage guarantees" (abstract, contribution 2) and "WCP consistently meets its coverage guarantees" (Section 5). The discrepancy needs investigation: possible causes include numerical errors in computing exp(t**A**) for unstable PDEs, finite-difference discretization effects that deviate from Theorem 4.2's ideal Gaussian characterization, or implementation issues. The paper neither acknowledges nor addresses this gap. This is the most serious weakness because it undercuts the paper's headline claim in the very setting where the method should work best (mildest instability, fewest infinite bands).

2. **Empirical results lack basic uncertainty quantification.** Coverage is a binary outcome, so binomial confidence intervals should accompany all point estimates in Table 1 and Figure 3. While the 0.85 gap is clearly significant, borderline values (e.g., 0.88, 0.89) are hard to evaluate without error bars. This is standard practice for empirical coverage reporting and would strengthen the paper's claims.

### Minor

1. **The method scope is narrower than the title and abstract suggest.** The approach requires: (i) a linear spatial differential operator, (ii) Gaussian (or location-scale) initial conditions, (iii) the analytical form of the PDE to be known, and (iv) a spatial discretization yielding a time-independent matrix **A**. The title "Weighted Conformal Prediction for Time-Dependent PDEs" and the abstract's "a broad class of PDE problems" overstate the generality. While the Discussion (Section 6) acknowledges this, the main claims are framed more broadly than what is delivered.

2. **Theorem 4.1 is presented as Contribution 1 but is disconnected from the method.** The function-space mutual singularity result is stated as a contribution, yet the paper immediately notes it is "not necessarily problematic for practical CP" because discretization mitigates the effect. The method works in discretized spaces precisely because the singularity disappears upon discretization. The paper would be substantively unchanged if Theorem 4.1 were removed. The paper itself cites Hairer (2023) acknowledging this as a known phenomenon, so its value as a novel contribution is limited.

### Trivial

None.

## Nice-to-Haves

- **Report effective coverage including infinite-band samples.** Currently, samples with infinite bands are excluded from the coverage calculation. Reporting overall coverage (treating infinite bands as trivially covering) alongside finite-only coverage would give a more complete picture and would partially address the concern about uninformative intervals.
- **Test sensitivity to the Gaussian initial condition assumption.** Remark 4.3 mentions the location-scale family, but no experiments verify whether coverage degrades under non-Gaussian ICs (e.g., uniform, bimodal distributions).
- **Ablation on discretization resolution.** The paper does not study how the number of spatial grid points affects either the validity of the Gaussian assumption or the frequency of infinite bands.
- **Investigate numerical conditioning.** For unstable PDEs, the matrix exponential exp(t**A**) can involve very large entries, potentially causing numerical issues in the Gaussian density ratio. A brief study of numerical conditioning would help explain or bound the coverage gap identified in Weakness #1.
- **Discuss how a practitioner should handle frequent infinite-band predictions.** The paper notes this is honest uncertainty quantification, but practical guidance (e.g., use a fallback method, refine the discretization, or collect more data) would strengthen the contribution.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"LSCI treatment is dismissive / lacks formal evidence"** (from harsh critic's Section-by-Section notes): The paper states that local exchangeability is "not verifiable" and that LSCI authors "assume" it. This is a fair characterization of prior work's limitation; the paper is not required to formally disprove local exchangeability to position its contribution. Removed as a non-issue.
- **"Remark 4.5 is vague / unsubstantiated"**: The remark references asymptotic guarantees that are likely detailed in the (removed) appendix. Per policy, we do not penalize gaps in removed supplementary material. Removed.
- **"Weight formula not fully specified"**: The paper states weights are computed "for all u_i belonging to the calibration set together with the target test point" and then normalized. This is standard weighted CP procedure. Removed as a nitpick.
- **"Real-world example relegated to appendix"**: The main text dedicates a paragraph and reports the key result. Appendix-level detail is standard practice. Removed.
- **"Nonconformity score conflates uncertainty sources"**: The max-absolute-error score is a standard choice from Diquigiovanni et al. (2022). The paper is not required to disentangle surrogate error from distribution shift. Removed.
- **"Theorem 4.2 assumes time-independent A"**: This is explicitly stated and is a correct scoping condition, not a flaw. Removed.
- **"Method resorts to infinite uninformative bands"** (Harsh Critic's Issue 4): The paper explicitly frames this as a feature (honest uncertainty), not a bug. The reviewer acknowledges it is "honest." Removed as a valid criticism; moved to Nice-to-Haves as a practical consideration.
- **"Theorem 4.1 is a known result from Feldman–Hájek"**: This is true but the paper does not claim novelty of the mathematical fact — it claims the *PDE-specific* instantiation as a contribution. The real issue (which is kept as a Minor Weakness) is that the result is disconnected from the method, not that it is unoriginal.

## Novel Insights

None beyond the paper's own contributions. The reviews correctly surface the tension between the claimed "exact coverage guarantees" and the empirical 0.85 coverage in Table 1, but do not offer genuinely novel observations beyond what is apparent from comparing the paper's claims against its own data.

## Suggestions

1. **Diagnose and explain the coverage gap for a=-0.005 at step 20.** Determine whether the cause is numerical (matrix exponential precision), discretization-induced (finite-difference deviation from ideal Gaussian dynamics), or implementation-related. Bound the gap theoretically or correct the implementation and report updated results. This is the single most important improvement the paper needs.
2. **Add binomial confidence intervals** to all coverage point estimates in Table 1 and Figure 3.
3. **Qualify the framing.** Adjust the title or abstract to reflect that the method is developed for linear PDEs with Gaussian/location-scale initial conditions.
4. **Report coverage with infinite-band samples included** as a supplementary metric alongside the finite-only coverage, so readers can assess the method's practical utility directly.

## Score and Decision

<score>6</score>
<decision>Borderline Accept</decision>