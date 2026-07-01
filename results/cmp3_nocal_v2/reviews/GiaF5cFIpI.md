## Summary

This paper presents a real-time integrated framework for adaptive stimulation of latent neural dynamics. It combines streaming latent space construction (including a novel streaming jPCA method), nonparametric kernel regression for stimulus-response mapping, and constrained optimization for stimulus design — all operating within a closed-loop pipeline that runs under 100ms per timestep. The method is evaluated on a toy dynamical system, on calcium imaging data from mouse visual cortex, and on electrophysiological recordings from nonhuman primate sensorimotor cortex, with synthetic stimulation effects overlaid on real background activity.

## Strengths

- **Novel integrated closed-loop framework.** The paper's primary contribution is the integration of streaming latent space estimation, online nonparametric stimulus-response modeling, and constrained optimization into a single real-time pipeline (Algorithm 1). Prior work addresses these pieces in isolation; the paper cleanly specifies how they fit together end-to-end.

- **Real-time runtime validated.** The paper reports end-to-end per-timestep runtimes averaging under 10ms and always below 100ms (Section 3). This is a genuine engineering contribution — it establishes that the kernel regression + gradient-based optimization loop can operate at timescales compatible with future *in vivo* closed-loop experiments.

- **Consideration of realistic experimental constraints.** The optimization in Equation (8) incorporates non-negativity constraints (excitation-only opsins), an L₁ sparsity proxy for the number of addressable targets, and box constraints on stimulation magnitude. These are grounded in real experimental limitations (holographic optogenetics, limited opsin expression) and make the framework more practically relevant than methods assuming unconstrained stimulus spaces.

## Weaknesses

### Fatal

None.

### Major

- **Real-data experiments evaluate the method on synthetic stimulation effects, not real neural responses to stimulation.** Section 4.1 (line 178) states explicitly: *"For each of the real datasets, we simulated stimulations using an autoregressive function to model a fast rise in neural activity of the perturbed neurons and a slower decay back to baseline levels."* The background neural activity is real, but the *effect* of stimulation is a hand-crafted AR(1) process ($a_t = 0.8 \cdot a_{t-1} + u_t$). The abstract's framing — *"We demonstrate our approach on both simulated and real neural data"* — is technically true of the background activity but likely to mislead readers into thinking the method has been tested against actual neural responses to delivered stimuli. The paper acknowledges this limitation in the Discussion (line 258: *"a second limitation is that our real data experiments were performed offline"*), but the gap between the claimed demonstration and what is actually shown remains significant. The method's ability to learn a stimulation-response mapping from real neural responses is not established by the current experiments.

- **The optimization is only compared against random and blind baselines, not against any prior stimulation design method.** The method is compared against: (i) a "blind" model that ignores stimulation effects (Figures 2e, 3c); (ii) random individual neuron stimulation, random groups, and shuffled versions of the method's own stimuli (Figure 4a). No comparison is made against existing methods for stimulation design that the paper itself cites, such as Bayesian optimization (Minai et al., 2024), active learning (Wagenmaker et al., 2024), or Bayesian variational inference (Draelos & Pearson, 2020). The bar "better than random" and "better than ignoring stimulations" is too low to establish practical utility. A reader cannot tell whether this framework offers advantages over principled alternatives.

### Minor

- **The sjPCA contribution is incremental, and the adaptive representation-selection claim is not empirically demonstrated.** The novel streaming method (sjPCA) adds an Orthogonal Procrustes step to stabilize each jPCA plane independently (Equation 2). This is a modest algorithmic modification. More importantly, the paper claims the framework can "adaptively select" between latent representations (abstract, Section 2.2) but does not test whether adaptive selection improves stimulation outcomes. Figure 1c visualizes which representations are locally predictive, but there is no closed-loop experiment showing that switching representations yields better stimulation targeting than sticking with any single method.

- **No analysis of how the kernel regression estimator's sample complexity scales with stimulus dimensionality.** The paper claims learning within 10–20 stimulations for stimulus spaces as large as 592 dimensions (calcium dataset). Kernel regression on a product of RBF kernels suffers from the curse of dimensionality, and the paper provides no evidence that the estimator is not essentially memorizing the few observations in a 592-dimensional space. A simple analysis of prediction error as a function of training set size would clarify this.

- **No ablation isolating the contribution of the temporal kernel ($K_3$) in Equation (7).** The temporal kernel is claimed to handle instabilities and drift, but the only comparison (Figure 2e) is against a "blind" baseline rather than against an ablated version without the temporal kernel. It is unclear whether the temporal weighting is responsible for the adaptive recovery shown, or whether the same behavior would arise from the spatial kernels alone.

### Trivial

- The notation $\|u\|_0^{\max}$ in Equation (8) and Algorithm 1 is used but never formally defined. From context it appears to be the maximum allowable L₀ norm (number of neurons that can be stimulated), but this should be stated explicitly.

## Nice-to-Haves

- Benchmarking against at least one prior stimulation design method (e.g., Bayesian optimization as in Minai et al., 2024) would substantially strengthen the evidence for the framework's advantages.
- A test on a more realistic nonlinear simulation (e.g., a recurrent neural network with optogenetic-like perturbation effects) would be more informative than the AR(1) overlay on real data.
- An ablation study comparing fixed-representation vs. adaptive-representation stimulation would justify the framework's multi-representation machinery.

## Removed Points

These points are flagged to be removed — treat them with caution:

1. **"Optimization evaluation conflates predicted error with actual performance"** — The paper explicitly reports both predicted and observed error (Figures 4a, 4c) and acknowledges that predicted error is a "loose lower bound" on observed error (line 215–217). The paper is transparent about this gap. Removed because the criticism is factually inaccurate.

2. **"Open loop/closed loop terminology is confusing"** — The paper defines its usage clearly (lines 228–230: open loop = identity mapping S(u)=Qᵀu; closed loop = learned Ŝ). The criticism applies a different domain's convention. Removed as a scope-creep nitpick.

3. **"Sherman-Morrison update is not derived"** — Removed as a formatting/precision nitpick that does not affect the paper's validity.

4. **"λ₁ hyperparameter not analyzed"** — A single scalar hyperparameter controlling a standard L₁/L₀ tradeoff. Not having a sensitivity analysis is not a meaningful weakness for a first integrated-framework paper. Removed as a low-significance request.

5. **"The toy model's S has only binary stimulus values"** — This is correct for the toy model specifically, but the real data experiments and the optimization formulation handle continuous u ∈ [0,1]^N. The reviewer incorrectly extrapolated this limitation beyond the toy model. Removed.

6. **"Figure 4b reports predicted angle, not observed"** — The paper clearly labels Figure 4b as predicted and Figure 4a as observed. The caption and text (line 210–211) distinguish them. Removed because the paper is explicit about what each panel shows.

## Novel Insights

The harsh review identifies a genuine gap between the paper's framing and its experimental validation: the paper presents itself as demonstrating on "real neural data" but the stimulation effects on that data are entirely synthetic. This mismatch between framing and evidence is the single most important observation. A more nuanced insight is that the paper's validation strategy is reasonable for a methodological first paper (toy model with ground truth + real background activity with synthetic perturbations + runtime guarantees) but the abstract and introduction overstate what the experiments establish. The review correctly identifies that the baseline comparison (random/blind) is insufficient to position the method relative to the existing literature that the paper itself cites.

## Suggestions

1. Rephrase the abstract and introduction to explicitly state that stimulation effects on real data are synthetic (e.g., "on real neural data with simulated stimulation responses"). The current phrasing is technically accurate but predictably misleading.
2. Add at least one comparison against a principled existing method (Bayesian optimization is a natural candidate) on the toy model where ground truth is known.
3. Provide an analysis of kernel regression error as a function of training set size for the stimulus dimensions used, to give readers a sense of the estimator's sample efficiency.
4. Add an ablation removing the temporal kernel $K_3$ to demonstrate its contribution to adaptive recovery from non-stationarities.
5. Run the adaptive representation-selection mechanism in a closed-loop experiment (even simulated) to test whether switching representations improves targeting outcomes.

## Score and Decision

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>