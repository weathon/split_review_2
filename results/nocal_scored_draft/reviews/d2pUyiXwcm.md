Given the favorability signals — especially the 0.00 on the compute fairness weakness and the 1.00 on the core strengths — let me finalize the review with appropriate calibration.

---

## Summary

This paper introduces SCaSML, a framework that applies defect correction to derive a PDE for a surrogate model's error (the "Structural-preserving Law of Defect") and then solves that PDE using Multilevel Picard (MLP) Monte Carlo simulation at inference time. The method is tested on high-dimensional semi-linear parabolic PDEs up to 160 dimensions, using PINN and Gaussian Process surrogates. The core idea is mathematically principled: the defect PDE inherits the semi-linear structure of the original problem, enabling efficient Monte Carlo solvers that target the residual error left by the surrogate.

## Strengths

- **Principled core idea.** Using defect correction to derive a governing PDE for the surrogate's error (Fact 2.3) and solving it with Monte Carlo at inference time is mathematically sound and clearly presented. The derivation correctly shows that the defect PDE retains the semi-linear structure of the original problem, which is essential for using existing stochastic solvers.

- **Flexibility across surrogate types and problems.** SCaSML is demonstrated with both PINN and Gaussian Process surrogates on four challenging PDE families (Linear Convection-Diffusion, Viscous Burgers, HJB/LQG, and Oscillatory Diffusion-Reaction), showing that the correction step is plug-and-play with respect to the base approximator.

- **Clean theoretical structure.** Theorem 2.5 shows that the final error is bounded by the *product* of the surrogate error and the MLP simulation error. This is a principled characterization that directly implies an improved scaling law (Corollary 2.6), which is empirically verified in Figure 4.

- **Challenging high-dimensional test problems.** PDEs up to 160 dimensions (including the HJB and oscillatory diffusion-reaction equations) provide a genuine stress test. The naive MLP solver fails entirely on the LQG problem while SCaSML successfully refines the surrogate, demonstrating the value of the hybrid approach.

## Weaknesses

### Fatal
None.

### Major

- **The main experimental evaluation does not control for compute budget.** From Table 1, SCaSML costs 30–200× more than the surrogate baseline it is compared against (e.g., LCD 60d: 0.28s vs 37.59s; DR 160d: 0.37s vs 86.77s). The abstract and headline claims of "20-80% error reduction" are computed against these much cheaper surrogates without adequately quantifying this cost trade-off in the main text. The paper states that "a smaller base PINN can outperform a larger PINN under the same inference-time compute budget" (line 33) and references fixed-budget efficiency comparisons in Appendix G.7 (line 226), but this critical evidence is deferred to the appendix rather than appearing in the main body. As a result, a reader cannot determine whether the reported improvements stem from the method's design or simply from spending dramatically more computation. This makes the main comparative claims about error reduction incomplete.

### Minor

- **The abstract's claimed error reduction range is imprecise.** The abstract states "20-80%" error reduction, but the DR experiment (Section 3.4) shows improvements of only 6.6% to 10.9% (line 302), falling below this range. The abstract should accurately reflect the full range across all experiments.

- **The convergence rate intuition in the main text conflates different cost types.** Sections 2.1 (lines 105-106) and 2.4 (line 172) use the same symbol "m" to represent both training collocation points and Monte Carlo simulation paths, which have fundamentally different cost structures (one MLP path involves simulating an SDE over many time steps). The heuristic argument treats these as "2m function evaluations" in a way that oversimplifies the actual cost model. While rigorous analysis is deferred to the appendix, the main text presentation could mislead readers about the cost accounting.

- **The "first" claims are overstated.** The paper claims "the first physics-informed inference-time scaling framework," "the first derivation that preserves the semi-linear structure," and "the first inference-time scaling algorithm" (lines 31, 328). Defect correction for PDE solvers is classical (Bank & Weiser 1985; Stetter 1978), and using a learned model as a control variate to reduce Monte Carlo variance is established in computational finance. The paper's actual contribution — applying defect correction to SciML surrogates with Monte Carlo solvers in high dimensions — is legitimate and does not need these fragile novelty claims.

- **No error bars or confidence intervals in the main results table.** Table 1 reports only point estimates. For a method that relies on stochastic Monte Carlo simulation, the main text would benefit from reporting variability alongside the point estimates, especially since significance is only referenced as being in the appendix (line 226).

### Trivial

- The method name appears inconsistently across the paper: SCaSML (main text), SCA²SM¹ and SCa²SM¹ (Table 1 and Section 3), and SCSML (Figure 3 captions). This is distracting.

- Different clipping thresholds are used for MLP (10) and SCaSML (0.1) in the LQG experiment (line 250-251). While the paper explains this by the smaller magnitude of the defect, it complicates a clean head-to-head comparison between the methods.

## Nice-to-Haves

- A compute-controlled comparison in the main text (SCaSML vs. a better-trained surrogate vs. a more expensive MLP solver, all at matched budget) would directly support the "elastic compute" narrative.
- A discussion of when the correction cost is *not* justified (e.g., DR shows ~7% improvement at 200× cost) would strengthen the paper's intellectual honesty.
- Verify whether the DR improvement percentages fit the abstract's 20-80% range and correct if needed.

## Removed Points

These points from the input reviews are flagged to be removed; treat them with caution:

- **"Naive MLP baseline is deliberately weak"** (Harsh Critic Critical Issue 3): **Removed.** The MLP baseline uses the same configuration (2 levels, M=10 samples) as the MLP component within SCaSML. The comparison shows that the same solver applied to the original PDE struggles, while applied to the defect PDE it succeeds — this is the method's intended behavior, not a flaw.
- **"Closed-form unbiased correction claim is misleading"** (Section-by-section note): **Removed.** In context (line 129), the paper contrasts its exact analytical defect PDE identity against iterative methods that produce only approximate corrections. "Closed-form" refers to the PDE being an exact analytical identity (not a nested approximation), not to the Monte Carlo estimator.
- **Generic strengths** (from Strength Finder): **Removed** — strengths that were generic ("important problem," "timely topic") or lacked specific evidence were not carried forward.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Move the compute-controlled comparison (Appendix G.7) into the main text, or at minimum include a summary figure/table showing that SCaSML's improvement over the surrogate persists at matched compute budgets.
2. Add confidence intervals or standard errors to the main results table for the stochastic methods.
3. Correct the abstract's error reduction range to reflect all experimental results accurately.
4. Standardize the method name to a single form throughout.
5. Add a limitations paragraph discussing when the inference-time compute cost may not be justified.

## Score and Decision

The paper's core idea is sound, the theory is clean, and the method is demonstrated on genuinely hard problems. However, the main experimental evaluation has a significant gap: the headline error-reduction numbers compare methods at dramatically different compute costs without adequate discussion of this trade-off in the main text, and the compute-controlled experiments that would address this concern are deferred to the appendix. This issue is fixable and does not invalidate the method's contribution, but it prevents full confidence in the experimental claims as presented.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>