Now I have sufficient calibration data. Let me produce the final review.

## Summary
This paper presents a real-time framework for adaptive neural stimulation targeting latent neural dynamics. It integrates three components: (1) a novel streaming jPCA method (sjPCA) plus proSVD and mmICA for online latent space construction, (2) a nonparametric kernel regression estimator for stimulus-response mapping conditioned on latent state, stimulus, and sample age, and (3) a constrained optimization procedure to select high-dimensional stimulation patterns (excitation-only, sparsity-constrained) that drive latent dynamics along desired directions. The framework is evaluated on a toy model with genuine state-dependent stimulation responses and on two real neural datasets (calcium imaging, electrophysiology) with simulated stimulation effects, demonstrating real-time runtimes (<100ms).

## Strengths
- **Novel streaming jPCA (sjPCA) with demonstrated convergence**: The Sherman-Morrison update for the skew-symmetric fit (Eq. 1) and Orthogonal Procrustes stabilization (Eq. 2) provide a genuine algorithmic extension of offline jPCA to streaming settings. Figure 1a confirms convergence to offline solutions within seconds, with standard deviations over 10 runs. jPCA is widely used in neuroscience but previously required offline computation, so this fills a real gap.
- **Complete real-time pipeline with principled constrained optimization**: The framework integrates streaming latent spaces, adaptive response modeling, and stimulation optimization into a single pipeline. Equation 8 formulates stimulation design as cosine-similarity maximization with L1 sparsity offset and non-negativity box constraints, matching holographic optogenetic experimental constraints. 517/600 optimizations achieve <1° misalignment for feasible directions (Fig. 4b), demonstrating the optimization works under realistic constraints.
- **Adaptive recovery from non-stationarities**: Figure 2e shows the kernel estimator recovers within ~15s from a 180° jump discontinuity and continuously tracks a rotating mapping, while a stimulation-blind baseline shows persistently elevated error. The temporal kernel K₃(t,Tᵢ) for discounting old samples is a practical design choice.
- **Designed stimuli significantly outperform random/shuffled baselines**: Figure 4a shows optimized stimuli produce markedly tighter and lower-angle distributions than single-neuron, multi-neuron random, and shuffled-stimulus baselines.
- **Real-time computational feasibility demonstrated concretely**: End-to-end runtimes benchmarked at <10ms average and <100ms on consumer hardware (NVIDIA 3060 Ti), critical for the translational claim.
- **Parallel evaluation across multiple latent spaces with adaptive selection**: Running proSVD, sjPCA, and mmICA simultaneously with streaming predictive-probability estimation (Fig. 1c) enables adaptive selection among competing subspace hypotheses — a novel and practically useful feature.

## Weaknesses

### Fatal
None

### Major
- **Real data experiments use state-independent simulated stimulation, limiting the scope of validated claims**: The paper's central contribution is modeling state-dependent, non-trivial stimulation responses (S(x_t, u_t) in Eq. 3). However, all real-data experiments use the simulation `y_t = r_t + a_t`, `a_t = 0.8 · a_{t-1} + u_t` (line 178), which is entirely state-independent — the additive term a_t depends only on previous stimulation history, not on latent position x_t. This means the kernel regression's x-conditioning fits noise on real data, and the "real data" validation cannot distinguish the proposed method from a simpler linear/constant model. The paper's claims about handling "idiosyncrasies of any individual experiment" (line 21) and adapting to "the specific system responses under a wide variety of possible conditions" (line 112) are only tested on the toy model (Eq. 9), not on actual neural data. The toy model does test state-dependence convincingly, but real neural stimulation responses involve opsin heterogeneity, network-level nonlinearities, and manifold-dependent effects that the additive AR simulation does not capture. This is the most significant gap between the paper's claims and its evidence.

- **Baselines are too weak to establish the method's complexity is necessary**: The primary comparisons are a "blind" model ignoring stimulation entirely (Figs. 2e, 3c) and random/shuffled stimulation (Fig. 4a). The blind comparison only shows that knowing stimulation occurred helps — it does not show the kernel regression approach is better than simpler alternatives. The random comparison only shows optimization beats random selection in a large space, which is expected. Missing are comparisons against: (a) any existing stimulation design method (Bayesian optimization as in Minai et al., 2024; active learning as in Wagenmaker et al., 2024), or (b) a simpler parametric model of stimulus-response (e.g., a linear map from stimulus to latent response). Without such comparisons, it is impossible to assess whether the nonparametric kernel regression and the full framework's complexity are justified over simpler alternatives.

### Minor
- **Optimization solver details not described in main text**: Equation 8 defines the constrained optimization problem, but the paper does not describe the solver algorithm, convergence properties, or computational complexity of the optimization step itself (only the end-to-end runtime is reported). Since the paper claims real-time feasibility, knowing the solver matters for reproducibility. (Note: appendix content was stripped from the review copy, so details may exist there.)
- **No systematic validation of the 10-20 stimulation sufficiency claim**: The paper claims "roughly 10-20 total stimulations" suffice (line 23) for learning the response mapping, but this is not systematically validated with an ablation showing alignment error as a function of stimulation count.
- **Closed-loop vs. open-loop advantage (Fig. 5b) demonstrated only on the toy model**: The demonstration that closed-loop stimuli outperform open-loop for non-trivial S is convincing, but since the real-data stimulation model is linear/open-loop by construction, this advantage cannot be verified on real data.

### Trivial
None

## Nice-to-Haves
- Compare against at least one alternative stimulation design approach (Bayesian optimization, linear stimulus-response baseline) to justify the method's complexity.
- Include a simulation with physiologically realistic state-dependent stimulation effects on real neural data (e.g., responses varying by manifold position) to bridge the gap between the toy model and in-vivo applications.
- Show how performance degrades when the latent space estimate is poor (e.g., sjPCA not yet converged).

## Removed Points
These points are flagged to be removed, treat them with caution:
- Criticism about missing solver details in appendix — the appendix is stripped from the review copy and the paper likely includes this information.
- Criticism about missing proofs or supplementary material — not available in the review copy.
- Any formatting or typographical issues — parser artifacts, not author errors.

## Novel Insights
The paper's most genuinely novel observation is the integration of streaming latent space construction with real-time stimulation-response modeling and constrained optimization as a complete, real-time-capable pipeline. The parallel evaluation of multiple latent spaces (proSVD, sjPCA, mmICA) with adaptive selection based on predictive probability (Fig. 1c) is an interesting idea beyond the individual algorithmic contributions — it could enable experiments to dynamically distinguish between competing neural subspace hypotheses during an experiment, which is conceptually new.

## Suggestions
- Replace the additive AR stimulation simulation on real data with a state-dependent model (e.g., responses varying by manifold position or neuron-specific opsin expression) to validate the core claim on real neural geometry.
- Add a linear stimulus-response model as a baseline to justify the nonparametric kernel regression.
- Add an ablation on number of stimulations vs. alignment error to substantiate the 10-20 stimulation practicality claim.
- Describe the optimization solver algorithm in the main text for reproducibility.

---

## Calibration Report

**Anchors retrieved:**

| Round | Path | Avg Human Score | Comparison |
|-------|------|----------------|------------|
| 1 | FwW3jqchtY.md (iSSM) | 5.00 | Very similar topic: neural dynamics under causal perturbation. Has real perturbation data + identifiability theory but was rejected for model limitations. Our paper has more complete pipeline but weaker real-data evaluation. |
| 1 | BBldjKEBlJ.md (QuantFormer) | 3.00 | Neural activity forecasting for optogenetics. Clearly weaker paper with minimal novelty; our paper is substantially stronger. |
| 1 | 4AlNpszv66.md (FCCA) | 4.75 | Dimensionality reduction for neural controllability. Rejected with serious derivation and presentation issues. Our paper is stronger. |
| 1 | MFCjgEOLJT.md (locomotion control) | 5.75 | Control-theoretic approach to behavioral modeling. Accepted with "good but not novel" assessment. Comparable quality to our paper. |
| 1 | 4ltiMYgJo9.md (closed-loop EEG) | 5.75 | Closed-loop stimulation framework. Rejected with clarity/soundness concerns despite one reviewer giving 8. Comparable topic, similar quality. |
| 1 | WQwV7Y8qwa.md (MR-SDS) | 5.80 | State-dependent neural dynamics model. Accepted borderline with real multi-region data. Our paper has comparable novelty but weaker real-data validation. |
| 1 | F5lcN7329a.md (FDA) | 6.00 | Consistent neural embeddings via flow matching. Rejected at 6.0 despite all reviewers giving 6. Our paper has comparable contribution. |
| 1 | cNmu0hZ4CL.md (causal OT) | 8.00 | Comparing neural dynamics with optimal transport. Clear accept with rigorous methodology. Substantially stronger than our paper. |
| 1 | kbjJ9ZOakb.md (invariance manifolds) | 8.00 | Learning invariance manifolds in visual cortex. Strong accept. Higher methodological rigor than our paper. |
| 1 | N83O2FcqzN.md (TiDeSPL-VAE) | 5.00 | Time-dependent VAE for visual neural activity. Rejected with split scores. Our paper has stronger practical contribution. |
| 1 | SyPrLti4PG.md (few-shot prediction) | 5.67 | Few-shot prediction for neural latents. Rejected borderline. Our paper is slightly more novel in scope. |

**Round 1 Bracket:** 5.0–6.0. The paper sits above iSSM (5.0, reject) which had real perturbation data but less practical contribution, and below cNmu0hZ4CL (8.0, accept) which has stronger methodology. The paper is most comparable to the borderline cluster at 5.5–6.0: MR-SDS (5.80, accept), 4ltiMYgJo9 (5.75, reject), F5lcN7329a (6.0, reject).

**Final calibration reasoning:** The paper has genuine algorithmic novelty (sjPCA, complete pipeline) that is stronger than several rejected papers in the 5.0–5.5 range. However, the real-data evaluation gap (simulated state-independent stimulation) and weak baselines prevent it from reaching the quality of accepted papers at 6.5+. Comparing to MR-SDS (5.80, accept, with real multi-region data), our paper has comparable framework novelty but weaker validation. Comparing to F5lcN7329a (6.0, reject), our paper has more novel components but similar evaluation limitations. This places it at 5.5 — right at the accept/reject boundary with a lean toward reject due to the evaluation gap, but with enough algorithmic substance that a strong rebuttal (e.g., adding a state-dependent simulation on real data or a linear baseline comparison) could push it to accept.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>