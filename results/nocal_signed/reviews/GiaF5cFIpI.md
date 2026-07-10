Now I have all the evidence. Let me produce the final consolidated review.

---

## Summary

This paper presents a streaming framework for real-time adaptive stimulation of latent neural dynamics. It integrates streaming dimensionality reduction (including a novel sjPCA method), dynamical modeling (Kalman filter, VJF, Bubblewrap), a nonparametric kernel-regression estimator for the stimulus-response mapping, and a constrained optimization procedure to design high-dimensional stimulation patterns that drive latent dynamics along a desired direction. The method is tested on a toy model and on two real neural datasets (calcium imaging, electrophysiology) where stimulation effects are simulated synthetically.

## Strengths

1. **Integrated streaming pipeline.** Algorithm 1 provides a clean, modular architecture connecting streaming dimensionality reduction, dynamical modeling, a stimulation-response estimator, and optimization into a single real-time loop. Modularity is a genuine engineering virtue — swapping components (proSVD/sjPCA/mmICA, KF/VJF/Bubblewrap) does not break the rest of the pipeline.

2. **Runtime benchmarking is convincing.** The <10 ms average, <100 ms maximum end-to-end runtime (Section 3) is meaningful for real-time *in vivo* applications at 15–30 Hz data rates. This claim is well-supported.

3. **Well-motivated problem.** The gap the paper addresses is real and timely: as holographic optogenetics and high-density electrophysiology advance, methods for online adaptive stimulation of latent dynamics are genuinely needed, and the combinatorial explosion of possible stimulation patterns (Section 1) is a nontrivial constraint.

## Weaknesses

### Fatal
None.

### Major

1. **Real-data experiments use synthetic AR(1) stimulations, not biological responses.** The paper claims validation on "real neural data" (abstract, Section 4.1), but the stimulation effects on real datasets are simulated via a first-order autoregressive process (Section 4.1: *aₜ = 0.8·aₜ₋₁ + uₜ*). This is arguably the simplest possible dynamical model — linear, time-invariant, and deterministic given uₜ. There is no evidence this resembles biological responses to optogenetic stimulation, which are nonlinear, cell-type-specific, state-dependent, and variable across trials. The Discussion (Section 5) acknowledges experiments were "performed offline," but this understates the severity: **the core phenomenon the method is designed to model was replaced by a trivial synthetic surrogate**. The paper does not demonstrate that any component (kernel regression, optimization, closed-loop adaptation) works with actual biological response properties. This is the most consequential limitation and a significant gap between the claimed contribution and the validation provided.

2. **The kernel regression estimator Ŝ (Equation 7) operates in a high-dimensional stimulus space with very few samples, without analysis.** The stimulus u is a vector in ℝᴺ where N=130 (electrophysiology) or N=592 (calcium imaging). The paper claims the method learns within "roughly 10-20 total stimulations" (abstract, p.2). A Nadaraya-Watson kernel estimator with 10–20 support points in 130–592 dimensions is susceptible to the curse of dimensionality: inter-point distances concentrate, and the estimator can degenerate to a nearest-neighbor scheme or a constant. The paper provides no analysis of how sample complexity scales with N, and the toy model uses a 1D binary stimulus (uₜ ∈ {0,1}), which does not test this regime at all.

3. **Baselines are insufficient for the claims made.** The only quantitative comparison throughout the paper is against a "blind" model that ignores stimulation times (Figures 2e, 3c). Optimization results (Section 4.2, Figure 4) compare only against random stimulation (single neurons, groups, shuffled). Several relevant approaches are cited in Section 1 (Bayesian optimization, active learning, Bayesian variational inference) but never compared against. Beating a blind model and random search establishes basic functionality, but the paper does not demonstrate improvement over existing alternatives.

### Minor

4. **The optimization solver for the non-convex problem (Equation 8) is underspecified.** Equation (8) minimizes a non-convex objective (cosine similarity involving s(u)/‖s(u)‖, a unit-sphere projection) over u ∈ [0,1]ᴺ where N=130–592, with a <10 ms budget. Algorithm 1 states "Solve with box constraints" without describing the algorithm, how local optima are handled, or how many iterations are run. The paper notes the estimator is differentiable (Section 2.4), but the solver specifics are missing, creating a reproducibility gap.

5. **The sjPCA contribution receives minimal evaluation.** sjPCA adds an Orthogonal Procrustes stabilization step to jPCA (Section 2.1). The only evaluation (Figure 1a) shows convergence to an offline fit — the baseline expectation for any streaming algorithm. There is no comparison against a sliding-window jPCA, no ablation of the Procrustes step, and no demonstration that sjPCA's latent space improves downstream stimulation performance.

6. **The "multiple latent spaces in parallel" capability is described but unused in stimulation experiments.** This capability is discussed in Sections 1 and 2.2 and shown in Figure 1c, but all stimulation experiments use only proSVD. This capability should either be demonstrated or scoped out of the contribution claims.

7. **No learning curve analysis.** The abstract claims learning within "roughly 10-20 total stimulations," but no experiment varies this quantity to show how performance degrades with fewer samples or improves with more.

8. **Notation ‖u‖₀^max in Equation (8) is nonstandard and not clearly defined** in the text.

### Trivial
None.

## Nice-to-Haves

- Validate the method with actual biological responses to stimulation (e.g., on an existing optogenetic dataset with real stimulation responses, or in a closed-loop preparation). Failing that, use a biophysically grounded forward model incorporating opsin dynamics, nonlinear response curves, and cell-type heterogeneity.
- Specify the optimization solver (algorithm, initialization, convergence criteria, handling of local optima) and provide evidence that it reliably finds good solutions within the runtime budget.
- Add at least one non-trivial baseline comparison (e.g., Bayesian optimization with a GP, or a linear variant of Ŝ).
- Include a learning curve: how does Ŝ's prediction error vary with the number of stimulation samples?

## Removed Points
These points are flagged to be removed; treat them with caution.
- *"No statistical significance tests"* — The paper shows shaded regions (1 SD over runs), which is standard practice in this domain; removed as a generic request.
- *"Delayed response model has a critical issue about pending stimulation"* — The paper explicitly states the assumption that no new stimulus is delivered before the previous one's effects are observed (Section 2.3); this is a reasonable first-pass assumption that the reviewer mischaracterized as unaddressed.
- *"The delayed response model critical issue" (duplicate)* — Same as above.
- *Criticism that "flip/rotate non-stationarities tested only on toy model"* — This is not a separate weakness; it follows from the broader real-data validation gap already listed as Major Weakness #1.
- *Strength about "well-motivated problem"* — This is generic; however, it is kept because the reviewer grounded it in specific numbers (10^45 combinations), making it substantive.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Prioritize validation on data with real biological responses to stimulation — this is the single highest-leverage improvement.
2. Fully specify the optimization solver (algorithm, iteration count, handling of non-convexity).
3. Add baseline comparison against at least one prior method (e.g., Bayesian optimization for stimulation selection).
4. Provide a learning-curve analysis varying the number of stimulation samples to support the "10-20 stimulations" claim.

## Score and Decision

The paper identifies an important problem and builds a sensible modular pipeline. However, the experimental validation has a fundamental gap: the "real neural data" experiments replace biological responses with a trivial AR(1) filter, so the paper's central claim — enabling real adaptive stimulation experiments — is not supported by the evidence presented. Additional concerns about the kernel regression regime, underspecified optimization, and insufficient baselines compound this. The framework has genuine merit, but the validation is too weak for acceptance at the current stage.

MY FINAL SCORE: <score>3.5</score>
MY FINAL DECISION: <decision>Reject</decision>