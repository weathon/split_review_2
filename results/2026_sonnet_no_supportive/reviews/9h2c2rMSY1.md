## Summary
This paper studies conformal prediction (CP) for surrogate models of time-dependent PDEs. It proves that in function space, the total variation (TV) distance between PDE solution distributions at any two distinct times is maximal (= 1) for the heat equation with Gaussian initial conditions (Theorem 4.1), which forecloses TV-bound-based coverage corrections in that setting. For discretized linear PDEs with Gaussian initial conditions, it derives exact Gaussian propagation formulas (Theorem 4.2) enabling closed-form density ratios and weighted CP (WCP) with provable coverage guarantees. Experiments on a 3×3 grid of PDE parameters and a real-world thermography dataset validate that WCP maintains coverage where baselines fail.

---

## Strengths

- **Theorem 4.1 (mutual singularity) is a concrete, nontrivial result.** The paper proves `d_TV(P_t, P_{t+δ}) = 1 for all t ≥ 0, δ > 0` for the heat equation with Gaussian initial conditions. This is not a trivial consequence of general infinite-dimensional measure theory; it requires working through the specific structure of the heat semigroup and the Gaussian prior, and it quantitatively forecloses an entire class of TV-bound-based CP corrections that prior work might have hoped to apply.

- **The duality between function-space impossibility and finite-dimensional tractability is the paper's intellectual core and is executed cleanly.** Theorem 4.2 provides closed-form Gaussian distributions for discretized solutions via the method of lines, enabling exact density ratios for WCP. The step from "impossible in function space" to "closed-form tractable in discretized space" is well-motivated and well-placed relative to the literature.

- **WCP is extremely computationally efficient.** Table 1 and Section 5 document WCP taking seconds vs. ~40 minutes for LSCI on the same hardware. This matters for practical deployment.

- **Experiments are well-designed for validating the method's scope.** The 3×3 grid of PDE parameters (varying `a` and `c`), including unstable regimes where baselines collapse to zero coverage, provides a clear and fair evaluation of when WCP maintains its guarantees while Naïve CP and LSCI fail.

---

## Weaknesses

### Fatal
None.

### Major

- **Scope overclaim in abstract and introduction.** The abstract claims the method works "for a broad class of PDE problems," and Section 1 cites weather prediction, aerodynamics, and financial modeling as motivations. However, the method requires (a) a linear PDE, (b) Gaussian initial conditions, and (c) a computable discretization matrix **A** to compute exp(t**A**). Nonlinear PDEs—Navier-Stokes, reaction-diffusion with polynomial nonlinearities, etc.—are entirely excluded. The mismatch between the motivating examples and the method's actual scope ("linear PDEs with Gaussian initial conditions and known discretization") is a genuine presentational overclaim that misleads readers about applicability. Section 6 acknowledges this ("extending the analysis to nonlinear PDEs is a natural next step"), but the abstract and introduction should state the restriction explicitly rather than burying it in the conclusion.

### Minor

- **Coupling between surrogate errors and WCP weights is not explicitly justified.** Equation (1) weights calibration points by the ratio of PDE solution distributions P_{t+δ}/P_t evaluated at each calibration point's solution value. However, the conformal score is a function of the *surrogate error* (|u_true − u_pred|), not of u_true alone. WCP's coverage guarantee for weighted CP requires weights representing the ratio of joint (input, output) distributions under test vs. calibration. The paper defers this to Remark 4.5 ("we provide asymptotic—and in some cases even non-asymptotic—guarantees… by leveraging numerical error guarantees of the scheme") without directly addressing whether the solution-distribution density ratio is the correct quantity to weight the surrogate error scores. A brief justification in the main text is warranted.

- **Coverage dip at high n_∞ is not quantified.** For `a = −0.0075`, timestep 15, WCP achieves 0.84 coverage (below the 90% target) with n_∞ = 86.4%. The paper attributes this to "higher stochastic noise" from small remaining sample size (Section 5), which is plausible, but the effective remaining sample size is not reported and no confidence interval or standard error is given. With only 13.6% of 5000 calibration samples (roughly 680 samples) retained, whether 0.84 is within expected sampling noise of 0.90 can be quantified straightforwardly.

- **Infinite-bandwidth behavior deserves a more complete treatment.** For `a = −0.01`, WCP reports 100% infinite bands at timesteps 15 and 20 (Table 1). The paper acknowledges this correctly as principled safety behavior (Section 5: "reporting trivial bands is usually a more valuable result"), but the acknowledgment is brief given that this is the most significant practical limitation. In precisely the regimes where uncertainty quantification matters most (large instability, long horizon), WCP provides no usable intervals. A closed-form criterion for when WCP produces finite vs. infinite bands—in terms of the eigenspectrum of **A** and the prediction horizon t—would make this outcome predictable rather than opaque.

### Trivial
None beyond the scope overclaim already noted.

---

## Nice-to-Haves

- A formal criterion (as a corollary to Theorem 4.2) characterizing when exp(tA)Σ₀exp(tAᵀ) produces finite vs. degenerate density ratios, stated in terms of the eigenvalues of **A** and horizon t, would transform the "infinite bands" failure mode into an interpretable regime.
- For the real-world thermography experiment, including a quantitative check that the linear-Gaussian assumption approximately holds (e.g., a Gaussianity test on residuals at calibration time) would strengthen the connection between theory and application.
- A brief discussion of the case where **A** is unknown (e.g., when the surrogate is a black-box neural operator), clarifying when the method is and is not applicable, would prevent misapplication.

---

## Removed Points

*These points are flagged as removed; treat them with caution.*

- **"Real-world experiment fails to extend validation beyond the method's regime"** (flagged as evidential gap): The paper explicitly scopes to linear PDEs and the thermography example correctly demonstrates the method on real data satisfying those assumptions. Demanding an experiment on nonlinear PDEs is scope creep given the paper's stated contributions. Demoted to Nice-to-Have.

- **"Generalization to nonlinear PDEs as a missing contribution"**: The paper explicitly scopes to linear PDEs and labels nonlinear extension as future work (Section 6). Not a weakness within the paper's stated scope.

- **Remark 4.3's Gaussianity discussion**: The remark acknowledges the Gaussian assumption explicitly and cites additional experiments in appendix A.8 for location-scale distributions. Not a weakness.

- **LSCI baseline tuning asymmetry**: The critic notes "the decision to set LSCI with a large number of band samples to push LSCI to over-coverage… is a fair and well-documented methodological choice." Retained only as a positive observation; not a weakness.

---

## Novel Insights

The paper's most intellectually interesting contribution is the clean duality between function-space impossibility (TV = 1 always under Gaussian-linear heat dynamics, Theorem 4.1) and finite-dimensional tractability (exact Gaussian propagation enabling closed-form density ratios, Theorem 4.2). The mutual singularity result has implications beyond PDE surrogate models: it suggests that any CP method operating in infinite-dimensional function spaces (e.g., for functional data analysis) encounters the same singularity barrier, and that tractable finite-sample guarantees necessarily require working in discretized or finite-dimensional projections. This insight is broadly applicable to the neural operator literature and related CP works.

---

## Suggestions

1. Revise the abstract and Section 1 to replace "a broad class of PDE problems" with "a class of linear PDEs with Gaussian initial conditions," and be explicit that the motivating examples (weather, aerodynamics) are outside the method's current scope.
2. Add a brief remark (or extend Remark 4.5) directly justifying why the density ratio of the PDE solution (Eq. 1) is the appropriate importance weight for the surrogate error scores—either by a direct argument or by citing the relevant weighted CP theorem that covers this case.
3. For the `a = −0.0075`, step 15 result, report the effective remaining sample size and whether 0.84 coverage is within one or two standard errors of 0.90.
4. Consider adding a corollary to Theorem 4.2 giving a closed-form condition on the eigenvalues of **A** and horizon t under which the density ratio is finite (i.e., when WCP produces non-trivial bands).

---

## Score and Decision

**Anchor papers retrieved and compared:**

| Path | Avg Score | Round | Comparison |
|---|---|---|---|
| v8RDgaEtE2 (Regression CP under Bias) | 2.50 | R1 | Weaker theoretical framing, incremental contribution; clearly below this paper |
| RcNzwKrjTo (CP with Trust Scores) | 5.00 | R1 | Comparable to this paper's scope; borderline reject |
| k2gGy2hpfx (CP under Distribution Shift, unlabeled) | 3.67 | R1 | Comparable topic; less theoretical, below this paper |
| aJ3tiX1Tu4 (Wasserstein CP under General Distribution Shift) | 6.67 | R1+R2 | Most topically similar; broader distribution-shift framework with Wasserstein; similar contribution size |
| oP7arLOWix (Kernel-based Weighted CP for Time Series) | 6.00 | R1 | Direct analog: weighted CP for time series with coverage guarantees; similar depth |
| ojIJZDNIBj (Copula CP for Multi-Step Time Series) | 6.25 | R1 | CP for time series with theoretical guarantees; similar contribution scope |
| 33XGfHLtZg (Conformal Risk Control) | 7.00 | R1 | Broader, more general extension of CP; slightly stronger contribution |
| j511LaqEeP (Non-Exchangeable Conformal Risk Control) | 6.00 | R2 | Direct analog: non-exchangeable CP with formal guarantees; similar depth |
| LgfaMR6Sst (Active Learning for PDE Trajectories) | 6.80 | R2 | PDE surrogate setting; broader experimental scope but less theoretical novelty |
| x4ZmQaumRg (Active Learning for Neural PDE Solvers) | 7.00 | R2 | PDE surrogate benchmark; less CP-theoretic, different contribution type |

**Round 1 bracket**: 5.5–7.0. The paper is clearly above the "borderline reject" cluster (papers around 4–5) and sits comfortably in the "borderline accept" range alongside comparable conformal prediction papers (oP7arLOWix: 6.0, ojIJZDNIBj: 6.25, j511LaqEeP: 6.0, aJ3tiX1Tu4: 6.67).

**Round 2 narrowing**: The paper's theoretical contribution (Theorem 4.1) is clean and novel for the PDE-CP intersection; the method (WCP) is correct and computationally efficient. The scope limitation (linear PDEs only) and the presentational overclaim are genuine Major weaknesses that distinguish this from the 7.0 anchors. The paper is most comparable to oP7arLOWix and j511LaqEeP (both 6.0) in contribution depth and scope. The scope overclaim is a genuine issue but not fatal, and the experiments are well-executed for the stated scope. A score of **6.0** is appropriate.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>