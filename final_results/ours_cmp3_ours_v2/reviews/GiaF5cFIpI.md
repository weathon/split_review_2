## Summary

This paper develops a streaming framework for adaptive stimulation-response modeling in latent neural spaces. The method integrates three components: (1) streaming latent space construction (including a proposed streaming jPCA variant alongside proSVD and mmICA), (2) a nonparametric kernel regression estimator that learns stimulus-response mappings while accounting for state-dependence, delayed responses, and temporal drift, and (3) a constrained optimization procedure that designs high-dimensional stimulation patterns to drive latent dynamics along desired directions, respecting realistic experimental constraints (non-negativity, sparsity, magnitude limits). Experiments include a toy circular dynamical system with known ground truth and two real neural datasets (calcium imaging, electrophysiology) where stimulations are simulated via an additive autoregressive model.

## Strengths

- **Practically motivated design choices for delayed responses and temporal drift** (Sections 2.3–2.4): The explicit handling of non-instantaneous stimulation responses (delay $d$) and the time kernel $K_3$ that discounts older observations are thoughtful acknowledgments of real experimental realities (optogenetic response latencies, photobleaching, plasticity). These go beyond what most purely algorithmic papers consider. The toy-model experiments in Figure 2e showing recovery after a 180° flip (within ~15s) and continuous drift convincingly demonstrate that the adaptive temporal kernel provides a real benefit.

- **Parallel comparison of multiple latent representations with adaptive selection** (Sec. 2.1–2.2, Fig. 1c): Rather than committing to one manifold hypothesis, the framework tracks multiple latent spaces (sjPCA, proSVD, mmICA) in parallel and evaluates which is most predictive in local regions of the latent space. This is a genuinely useful design for detecting switches in neural dynamics or comparing representational hypotheses during the same experiment.

- **Runtime benchmarks demonstrating real-time feasibility** (Section 3): The reported <10 ms average and <100 ms total computation time per timepoint is necessary for any claim about future *in vivo* use and is convincingly demonstrated across multiple experimental settings.

- **Comprehensive treatment of feasibility constraints**: The optimization framework accounts for non-negative stimulation magnitudes, a limit on the number of targeted neurons, and bounds on total stimulation power — realistic experimental constraints that are often abstracted away in prior work.

## Weaknesses

### Fatal
None.

### Major

- **The optimization objective's sparsity-penalty term is mathematically incoherent with the claimed intent.** Equation (8) contains the penalty $\lambda_1 (\|u\|_0^{\max} - \|u\|_1)$. The text explains this is to "encourage a solution with the number of non-zero elements close to $n$." However, minimizing this term requires making $\|u\|_1$ as **large** as possible (close to $N$ or $\|u\|_0^{\max}$), which encourages dense, high-magnitude solutions — the opposite of sparsity enforcement. A standard L1 relaxation of an L0 cardinality constraint would penalize $\|u\|_1$ (e.g., $+\lambda\|u\|_1$), driving entries toward zero. The sign here is reversed relative to what a sparsity-inducing penalty requires. Either the formulation is incorrect or the explanation is incoherent with the mathematics. This does not invalidate the entire optimization (the cosine-similarity term still drives useful solutions), but it means a component claimed as a contribution does not do what the paper says it does.

- **Evaluation on real data uses simulated, not real, stimulations — creating a gap between central claim and evidence.** The paper's headline contribution is designing real neural stimulations, but the experiments on real datasets (calcium imaging, electrophysiology) involve no actual stimulation delivery. Instead, additive AR(1) perturbations are synthetically injected (Section 4.1: "$y_t = r_t + a_t$, $a_t = 0.8 \cdot a_{t-1} + u_t$"). This additive, linear, time-invariant model is far simpler than the complex, nonlinear, network-mediated effects of real optogenetic or electrical stimulation. The model then learns this injected mapping — which it naturally does since the mapping aligns with the model's own assumptions. The Discussion acknowledges this ("our real data experiments were performed offline"), but the gap between what the paper claims (a method for *real* stimulation) and what it validates (learning synthetic additive perturbations on real background activity) remains substantial. This is the single biggest limitation.

- **No comparison against existing adaptive stimulation methods.** The paper cites prior work on adaptive stimulation design (Minai et al., 2024; Wagenmaker et al., 2024; Draelos & Pearson, 2020) but never compares against any of them. The primary comparison is against a "blind" model that simply withholds stimulation information from the dynamics — showing that a model accounting for stimulations outperforms one that ignores them is unsurprising. The other comparators (random single-neuron, random group, shuffled stimuli) are also weak baselines. Without comparison to a reasonably competent alternative (e.g., Bayesian optimization, online linear system identification with active learning), it is impossible to assess whether the framework's complexity is warranted or if simpler methods would perform as well.

### Minor

- **The sjPCA contribution is underspecified and insufficiently validated.** sjPCA is described as a "novel streaming formulation" (Section 2.1) in roughly 8 lines with no quantitative comparison against proSVD on the same data. The convergence curves in Figure 1a use different synthetic data for different methods (sjPCA/proSVD on a rotational linear system; mmICA on Laplace-generated independent components), so the three panels are not directly comparable. There is no ablation showing that sjPCA's convergence properties benefit downstream stimulation tasks. If sjPCA is a contribution, it needs its own validation; if incidental, it should not be called "novel."

- **The open-loop baseline makes an unrealistically favorable assumption.** The open-loop condition assumes $S(u) = Q^\top u$ — that stimulating a neuron with intensity $u_i$ produces an effect exactly equal to $u_i$ times that neuron's loading in the latent space. Real optogenetic effectiveness varies widely across neurons (opsin expression, point-spread functions). The closed-loop results are compared against this favorable baseline, making the improvement less impressive than it would be against a more realistic open-loop model.

- **No characterization of optimization degradation under imperfect $\hat{S}$.** The key results on stimulation alignment (<1° error for 85% of Feasible/Q0 optimizations, Section 4.2) assume either an identity mapping or a $\hat{S}$ learned from simulated stimulations. The paper does not characterize how performance degrades when $\hat{S}$ is imperfect (limited training data, misspecified kernels, non-stationary responses), which is the realistic scenario that would determine whether the closed-loop framework is practically useful.

### Trivial
None.

## Nice-to-Haves
- Replace the additive AR(1) stimulation model with a more realistic forward model (nonlinear intensity-response curves, cross-neuron coupling, state-dependence) to stress-test the method against the complexity it is designed to handle.
- Add a comparison against at least one simpler adaptive baseline (e.g., online linear regression for $\hat{S}$) to demonstrate that the kernel regression complexity is warranted.
- Characterize how optimization alignment degrades as a function of $\hat{S}$ estimation error (number of training stimulations, noise level, model mismatch).

## Removed Points
These points from the input review are not included in the main review, with justifications:

1. "The problem is genuinely hard and well-formulated" — Generic praise, not specific to this paper's contribution.
2. The harsh critic's designation of the simulated-stimulation issue as "structural/fatal" — Demoted to Major. The paper transparently acknowledges this limitation in the Discussion, and the evaluation still demonstrates that the framework components work correctly on real neural background activity. The paper positions itself as a methods framework for future *in vivo* use, not as a validated closed-loop system.
3. "The paper cannot be accepted in its current form" — This is a judgment reflected in the score, not a substantive weakness.
4. Section-by-section notes about the toy model being "very simple" — The toy model is appropriately simple for ground-truth validation; requiring higher-dimensional or more complex toy models is scope creep.
5. Criticism about missing error bands in Figure 2e — The paper states "bold lines show smoothed average errors over 50 experiments," which is standard for this type of plot. Statistical rigor demands in systems neuroscience benchmarks are not the same as in ML and the paper's presentation is adequate.
6. "Kernel regression is a standard Nadaraya-Watson estimator" — This is not a weakness; using a standard well-understood estimator is appropriate.
7. Criticism about the "flip" and "rotate" toy perturbations not being benchmarked against simpler adaptive methods — Merged into the broader weakness about missing baselines.
8. "Strengthening the Paper on Its Own Terms" section — Filtered to Nice-to-Haves.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. **Fix the sparsity penalty sign** in Equation (8), or clarify what the objective actually enforces. This is a technical error that needs correction.
2. **Add at least one meaningful baseline** from existing adaptive stimulation literature (e.g., replace kernel regression with online linear regression, or compare against Bayesian optimization over the stimulus space).
3. **If real stimulation experiments are infeasible**, replace the additive AR(1) model with a substantially more realistic forward model that includes nonlinearities, cross-neuron coupling, and state-dependence, and characterize how the method performs under these harder conditions.
4. **Either validate sjPCA properly** (quantitative comparison against proSVD on the same data, ablation showing benefit to downstream tasks) or remove the "novel" claim.
5. **Characterize degradation** of optimization alignment under imperfect $\hat{S}$ estimates (varying numbers of training stimulations, noise levels, model misspecification).

## Score and Decision

**Bracket (Round 1):** 3.5–5.5. The paper has a well-motivated framework for a hard problem with thoughtful practical design, but the evaluation has significant gaps (simulated stimulations on real data, weak baselines) and a technical error in the optimization objective. This sits between clearly rejected papers (~3, which have fundamental method flaws or missing evaluations) and solidly accepted papers (~6+, which have comprehensive evaluations with competitive baselines).

**Final Score: 4.5**
**Decision: Reject**

**Calibration Anchors (all rounds):**
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/BBldjKEBlJ.md` (QuantFormer, avg: 3.00, Round 1) — Neural forecasting paper rejected for weak baselines and missing comparisons. The paper under review has a more coherent framework and tackles a harder problem, but shares similar evaluation gaps.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/N83O2FcqzN.md` (TiDeSPL-VAE, avg: 5.00, Round 1) — Rejected VAE paper with mixed scores (3,3,6,8). The paper under review has a comparable contribution level but less evaluation rigor.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/WQwV7Y8qwa.md` (MR-SDS, avg: 5.80, Round 1) — Accepted paper with comprehensive comparisons and ablation studies. The paper under review has weaker evaluation.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/3usdM1AuI3.md` (BRAID, avg: 6.25, Round 1) — Accepted paper with strong baselines and extensive experiments. The paper under review does not reach this evaluation standard.

The paper makes a genuine contribution in its framework design and practical considerations for a hard problem, but the evaluation falls short of what is needed to accept it. The two most critical issues are (1) the optimization objective's sparsity penalty does not do what is claimed, and (2) the real-data experiments use simulated, not real, stimulations, leaving the central claim unvalidated against real stimulation complexity. These issues, together with the lack of comparisons to existing adaptive stimulation methods, outweigh the framework's strengths at this stage.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>