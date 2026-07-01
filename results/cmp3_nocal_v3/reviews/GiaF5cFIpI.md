## Summary

This paper proposes a real-time framework for designing high-dimensional neural stimulations that drive latent neural dynamics in desired directions. The method integrates three streaming components: (1) latent space construction (with a novel sjPCA method plus existing proSVD and mmICA), (2) nonparametric stimulus-response modeling using kernel regression with temporal adaptation, and (3) constrained optimization that designs stimulation patterns under sparsity and non-negativity constraints. The authors demonstrate computational feasibility (<10 ms average runtime) and evaluate the pipeline on a synthetic toy model and two real neural datasets (calcium imaging, electrophysiology) where stimulation effects are synthetically injected.

## Strengths

1. **Computationally practical pipeline with real-time benchmarks.** The end-to-end runtime (<10 ms average, <100 ms worst-case) is credible for the intended closed-loop application, and the integration of streaming latent space construction, kernel regression, and constrained optimization into a single online loop (Algorithm 1) is a nontrivial engineering achievement.

2. **Temporal adaptation mechanism is well-motivated and demonstrated.** The non-stationary kernel regression (time kernel in Eq. 7) that can recover from abrupt flips and continuous drift in the stimulus-response mapping (Figure 2d–e) addresses genuine experimental concerns such as probe drift, photobleaching, and plasticity. This goes beyond most prior work that assumes a static response model.

## Weaknesses

### Fatal
None.

### Major

1. **The real-data experiments use synthetically injected stimulation effects, not actual closed-loop neural control.** Section 4.1 (lines 178–179) states: *"For each of the real datasets, we simulated stimulations using an autoregressive function to model a fast rise in neural activity… we transformed the data using: y_t = r_t + a_t, a_t = 0.8·a_{t-1} + u_t."* The "observed" response to stimulation is an additive artifact the authors themselves injected into real recordings; the biological system never actually responded to a perturbation. This tests the learning component on real background activity but does **not** demonstrate that the method can drive real neural dynamics, where the stimulus-response mapping depends on opsin expression, network state, plasticity, and other biological factors absent from the synthetic injection. The paper acknowledges this in the Discussion (line 258–259: *"our real data experiments were performed offline"*) but the abstract claims demonstration *"on both simulated and real neural data"* without adequate caveat, and the severity of the gap is understated. The toy model (Eq. 9) provides a ground-truth closed-loop setting, but it is a highly simplified 3D system that does not bridge the gap to a real biological preparation.

2. **No comparison against any existing method from the cited literature.** The paper cites prior work on stimulation design — Bayesian optimization (Minai et al., 2024), active learning (Wagenmaker et al., 2024), input-output dynamical modeling (Yang et al., 2021) — but never benchmarks against any of them. The comparisons provided are: (a) a "blind" model that simply withholds stimulation times from the dynamical model (Section 4.1), and (b) random/naive stimulation strategies — single neurons, random groups, shuffled stimuli (Section 4.2). Neither constitutes a competitive baseline. Without even a simple parametric linear stimulus-response model or an existing method from the cited papers, it is impossible to assess whether the proposed approach advances the state of the art.

### Minor

3. **sjPCA is a modest algorithmic modification with no downstream evaluation.** The claimed novel contribution (Section 2.1, lines 74–83) is adding an Orthogonal Procrustes step to stabilize jPCA planes. While reasonable, this is a minor modification, and the paper does not compare sjPCA against running standard jPCA on a sliding window or any other streaming variant. More importantly, sjPCA is never used in the stimulation experiments (only proSVD is used in Sections 4.1–4.2), so whether it provides any practical advantage is untested.

4. **Parallel latent space capability is described but never exercised in the stimulation experiments.** The abstract and Section 2.1 (lines 91–92) advertise the ability to run multiple latent spaces in parallel and adaptively select the best one (Figure 1c). Yet all stimulation experiments use only proSVD. There is no demonstration that switching between representations improves stimulation design or that the adaptive selection mechanism works in practice. This is a claimed capability with zero experimental support.

5. **Open-loop optimization evaluation is partially circular.** In open-loop mode (line 228), the assumed mapping is S(u) = Q^T u. The optimization (Eq. 8) maximizes alignment between s(u) = Q^T u and target v, and the "observed" response s_obs is also computed from Q^T u. The near-perfect results for "Feasible" (517/600 <1°) and "Q0" (508/600 <1°) targets primarily measure the optimizer's ability to solve its own objective, not the method's ability to design effective stimuli under real biological uncertainty. The closed-loop mode (Figure 5) is more meaningful but receives limited quantitative detail and no comparison against alternative response models.

6. **Missing ablations and optimization solver details.** The kernel regression (Eq. 7) has three kernel components (state, stimulus, time) plus continuing-effect β coefficients — none are ablated. The three dynamical models (KF, VJF, Bubblewrap) are never compared in the main results (only KF is used). The solver for the non-convex objective in Eq. 8 is described only as *"Solve with box constraints"* (Algorithm 1, line 56) with no specification of algorithm, initialization, convergence criteria, or number of restarts.

### Trivial
7. The claim that the method learns within *"roughly 10-20 total stimulations"* (line 23) is asserted without supporting quantification (learning curves, variance across runs).

## Nice-to-Haves
- Adding a comparison against a parametric linear stimulus-response model or Gaussian process regression would significantly strengthen the evaluation.
- Ablating the individual kernel components and continuing-effect β coefficients would clarify which parts of the model are driving performance.
- If a real closed-loop experiment is infeasible, a rigorous generative simulation (with a known ground-truth S function, realistic nonlinearities, and state-dependent effects) would provide stronger support than the current autoregressive injection on real data.

## Removed Points
These points are flagged to be removed; treat them with caution:

- **"No statistical comparisons"**: The paper reports means and standard deviations, which is standard for this type of empirical work. Formal hypothesis tests are not customary for all evaluations in this setting.
- **"The description of sjPCA is terse" / "Section-by-section presentation notes"**: These are style observations, not substantiated weaknesses.
- **Strength "The problem is well-motivated and timely"**: Generic; could apply to any paper on this topic.
- **Strength "The pipeline is end-to-end" (the part about "not a trivial engineering feat")**: Too subjective; the concrete runtime benchmarks are already kept as a strength.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions
1. Clearly separate the "closed-loop" evaluation (toy model with ground-truth S) from the "open-loop with real data" evaluation in the abstract and claims, or add a real closed-loop experiment or a much more realistic generative simulation.
2. Add at least one comparison against a method from the cited literature (e.g., a parametric linear model, Bayesian optimization, or a Gaussian process approach) so the reader can assess relative performance.
3. Either provide evidence that sjPCA improves stimulation outcomes, or reposition it as a practical utility rather than a core contribution.
4. Either test the parallel latent space selection in a stimulation experiment or remove the claim from the Abstract.
5. Provide optimization solver details (algorithm, initialization, restarts) to enable reproducibility.

## Score and Decision

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>