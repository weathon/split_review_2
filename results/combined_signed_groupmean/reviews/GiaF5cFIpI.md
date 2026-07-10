Now I have all the calibration information needed. Let me write the final review.

## Summary

This paper develops a streaming method for stimulation-response modeling in latent neural spaces, combined with an optimization framework for designing high-dimensional stimulation patterns to drive low-dimensional latent dynamics. The system integrates streaming dimensionality reduction (including a novel streaming jPCA variant), nonparametric kernel regression for learning stimulus-response mappings, and constrained optimization to select stimuli that push latent activity along desired directions. The method is evaluated on a toy dynamical model and on two real neural recording datasets (calcium imaging and electrophysiology) with synthetically-added stimulation effects.

## Strengths

- **Demonstrated real-time runtime (impact: +9.87).** The paper substantiates <100ms end-to-end per timepoint (average <10ms) with concrete hardware specifications (line 154), making future in vivo application plausible. This is a meaningful sanity check that many computational neuroscience proposals lack.

- **Adaptive temporal kernel handles instabilities in the stimulus-response mapping (impact: +9.64).** The experiments in Fig. 2d,e show the model recovering from a step-change (180° flip) and continuous drift in the ground-truth $S$, demonstrating a genuine advantage over a non-adaptive baseline that assumes a stable mapping. This is the paper's strongest evidence that the design choices matter.

- **Thoughtful handling of realistic experimental constraints (impact: +7.15).** The optimization (Eq. 8) explicitly incorporates non-negativity (excitation-only opsins), sparsity via L₁ relaxation of L₀, and box constraints. The optimizer correctly identifies when a requested direction is infeasible (Fig. 4b, Negative and Dense cases), and the violin plots (Fig. 4a) show that the designed stimuli meaningfully outperform random baselines.

## Weaknesses

### Major

1. **The "real neural data" experiments use synthetic stimulation effects, not real biological responses.** The abstract and introduction claim validation on "real neural data" without qualification. In practice (line 178), the stimulations are additive AR(1) processes superimposed on prerecorded data: $y_t = r_t + a_t$, $a_t = 0.8 \cdot a_{t-1} + u_t$. The ground-truth stimulation effect is entirely defined by the authors' own synthetic model. The core challenge that motivates the paper — complex, non-stationary, state-dependent biological responses to stimulation (lines 112-113) — is absent by construction. While the discussion partially acknowledges this (lines 252-253, 258-259), the framing in the abstract and introduction overstates the validation. The method has not been tested against the very difficulties it was designed to address.

2. **Baseline comparisons are too weak to establish the method's advantages.** The quantitative comparison for stimulus-response modeling (Fig. 2e, Fig. 3c) is only against a "blind" model that withholds stimulation times — trivially showing that accounting for stimulations helps. The optimization results (Fig. 4a) compare only against random baselines (single neurons, groups, shuffled). No comparison is made against any alternative stimulation design method, despite the paper citing several closely related approaches in its prior-work section (Bayesian optimization, active learning, Bayesian variational inference). This makes it difficult to assess whether the specific design choices matter relative to reasonable alternatives.

3. **The "closed-loop" comparison is not a closed-loop experiment.** The open-loop vs. closed-loop distinction in Fig. 5 is whether $S$ is assumed known ($S(u) = Q^\top u$) or estimated via $\hat{S}$. Both modes are evaluated entirely in simulation with a synthetic ground-truth $S$. There is no experiment where the optimized stimulus is applied, its effect observed, and the next stimulus re-optimized based on the new state — which is what "closed-loop" means in a neural stimulation context. The claim that closed-loop stimuli "have a larger proportion of their magnitude aligned with $v$" (lines 237-239) is only shown for the synthetic setting.

### Minor

4. **The sjPCA contribution is incremental.** Adding Orthogonal Procrustes alignment to stabilize jPCA planes (Eq. 2) is a sensible but modest extension. Fig. 1a shows convergence to offline fits, which is the minimum requirement; the paper does not demonstrate that sjPCA provides any advantage over standard streaming PCA or offline jPCA on tasks relevant to the main contribution.

5. **The "novel streaming estimator" for model selection is underspecified.** Highlighted in the abstract as a contribution, it is described in a single paragraph (lines 107-108) and amounts to running models in parallel and picking the one with lowest predictive error. No dedicated quantitative results demonstrate its performance or benefit.

6. **No ablation of the kernel regression design choices.** The three-way product kernel (Eq. 7) over latent state, stimulus, and time is never ablated. It is unclear which dimensions matter most or whether a simpler model (e.g., linear regression in latent space) would suffice — particularly important given the claim of working with only 10-20 stimulations.

7. **The optimization solver for Eq. (8) is not specified.** The paper does not describe whether it uses gradient-based methods, grid search, or another approach, nor the computational cost of solving a potentially high-dimensional non-convex problem at each decision timepoint.

### Trivial

None.

## Nice-to-Haves

- A closed-loop simulation with a nonlinear, state-dependent $S$ where the optimized stimulus is applied, the response observed, $\hat{S}$ updated, and the next stimulus re-optimized, would validate the integrated pipeline that is the paper's core selling point.
- Comparison against at least one alternative stimulation design method from the cited prior work (e.g., Bayesian optimization) would help calibrate the method's relative merit.
- An ablation showing the contribution of each kernel dimension and a simpler baseline (e.g., linear regression) would clarify which design choices drive performance.

## Removed Points

These points from the input review were filtered out per the review guidelines:

1. **Critic's claim that the paper "does not acknowledge" the real-data limitation.** Factually incorrect: the paper explicitly states at line 252-253 "synthetic data and two real experimental datasets with simulated effects of arbitrary stimulations" and at lines 258-259 "A second limitation is that our real data experiments were performed offline." The broader concern about misleading abstract/introduction framing is retained as Major weakness #1.

2. **Formatting/presentation nitpicks** (orphaned text at lines 170-171, figure description issues). These are parser artifacts and formatting issues, not author errors.

3. **Demand for real closed-loop experiment with biologically realistic nonlinear S.** Scope creep beyond what the paper sets out to demonstrate as a methods proof-of-concept. Moved to Nice-to-Haves.

4. **Demand for specific alternative baseline comparisons (GP, Bayesian optimization).** The concern about weak baselines is kept as a Major weakness, but prescribing specific alternatives is a suggestion, not a structural flaw. The core point (no comparison against any alternative method) is retained as Major weakness #2.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Revise the abstract and introduction to accurately describe the validation: "real neural data with simulated stimulation effects" rather than unqualified "real neural data."
2. Add at least one comparison against a principled alternative stimulation design method.
3. Run a simulation (even fully synthetic) where the closed-loop pipeline operates: stimulus → observe response → update $\hat{S}$ → re-optimize, to validate the integrated loop.
4. Add an ablation study for the kernel regression components.
5. Specify the optimization algorithm used for Eq. (8).

---

## Score and Decision

**Anchor analysis.** The most topically relevant anchor is *"Identifying neural dynamics using interventional state space models"* (iSSM, avg score 5.0, Reject). Both papers share critical weaknesses: inadequate baseline comparisons (iSSM: -10.00 impact, this paper: -10.00) and a gap between claimed and demonstrated validation. However, the iSSM paper was validated on actual neural perturbation data (real optogenetic / micro-stimulation experiments), whereas this paper only uses synthetic perturbations on real recordings — widening the claim-evidence gap. On the other hand, this paper has demonstrated real-time runtime (+9.87) and adaptive kernel handling (+9.64) that the iSSM paper lacked. A second relevant anchor, *"Dynamical modeling for real-time inference of nonlinear latent factors in multiscale neural activity"* (MRINE, avg 4.25, Reject), was criticized as a combination of existing techniques with limited novelty — a concern that partially applies here (sjPCA is incremental, the streaming estimator is underspecified). The round-1 bracket was **3.5–5.5**; within that bracket the closest anchor is iSSM at 5.0, but this paper's wider validation gap places it below that anchor.

**Final score:** 4.0. The paper targets an important problem with a sensible architecture and delivers encouraging runtime numbers. However, the validation falls short of the claims: the "real neural data" experiments use synthetic stimulations, no alternative method is compared against, and the closed-loop experiments are not actually closed-loop. These gaps prevent the paper from meeting the bar for acceptance at this venue.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>