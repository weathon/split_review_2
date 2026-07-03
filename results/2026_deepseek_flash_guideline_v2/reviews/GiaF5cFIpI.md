Now I have verified all claims. Let me produce the final consolidated review.

## Summary
The paper presents a streaming framework for closed-loop stimulation design in latent neural spaces. It integrates (1) streaming dimensionality reduction including a novel streaming jPCA (sjPCA), (2) a nonparametric kernel regression model that maps (latent state, stimulus, time) → response, (3) a constrained optimization over high-dimensional stimuli to drive latent activity in desired directions, and (4) parallel evaluation of multiple latent representations with adaptive selection. The method is validated on a toy model and on real neural data (calcium imaging, electrophysiology) with simulated AR(1) stimulation effects, demonstrating sub-100ms per-timepoint runtimes.

## Strengths
1. **End-to-end real-time feasibility with concrete runtime benchmarks.** The paper reports <10 ms average and <100 ms maximum per timepoint (Section 3, line 154), directly supporting real-time applicability. This goes beyond prior streaming methods (e.g., Draelos et al., 2021) that did not demonstrate closed-loop-latency timing for the full stimulation-selection pipeline.

2. **Quantitative demonstration of optimization precision.** 517/600 optimizations for feasible directions achieve <1° misalignment between desired and predicted stimulation effect (Section 4.2, line 214). Optimized stimuli substantially outperform random baselines (Single, Multiple, Shuffled) in aligning with target latent directions (Figure 4a).

3. **Robust recovery from non-stationary stimulus-response mappings.** The temporal kernel K₃ in Eq. (7) allows the model to discount old samples. Recovery from a 180° jump within ~15 s and tracking of continuous drift (1 revolution per 30 s) is demonstrated (Section 4.1, Figure 2e). The adaptive model's prediction error drops substantially below the "blind" comparison model after these instabilities.

4. **Streaming jPCA provides the first online approximation to offline jPCA.** sjPCA adds an Orthogonal Procrustes step to stabilize each discovered rotational plane in real time (Section 2.1, Eqs. 1-2). Figure 1a shows convergence to the same subspace as offline jPCA.

5. **Parallel evaluation of multiple latent representations with adaptive selection.** The framework simultaneously tracks three streaming dimensionality reduction methods (proSVD, sjPCA, mmICA) and three dynamical models (KF, VJF, Bubblewrap), using predictive error to determine which representation is most useful at each timepoint or local region (Figure 1c, line 108).

6. **Optimization handles realistic biophysical constraints jointly.** Eq. (8) simultaneously enforces non-negativity (compatible with excitatory opsins), an L₁ penalty approximating an L₀ constraint on the number of targeted neurons, and bounded stimulation magnitude. Infeasible directions (Negative, Dense) are correctly identified by the optimizer (Section 4.2, lines 212-214).

## Weaknesses

### Fatal
None.

### Major
1. **Semi-synthetic stimulation on real data does not test biological stimulus-response relationships.** On both real datasets (calcium imaging, electrophysiology), the effects of stimulation are injected via a first-order AR(1) process: `y_t = r_t + a_t`, `a_t = 0.8·a_{t-1} + u_t` (Section 4.1, line 178). The method is evaluated on its ability to learn this injected linear filter. This does not demonstrate that the pipeline can handle *biological* stimulus-response relationships, which involve network dynamics, nonlinearities, neuromodulation, and other complexities not captured by a first-order linear filter. The paper's framing (end of Introduction: "enable the next generation of experiments capable of designing and testing stimulations of latent neural dynamics in real time") implies readiness for real causal intervention. The Discussion (lines 258-259) acknowledges the experiments were offline but understates the issue — the problem is not the offline processing but that the stimulation-response data itself was synthetic.

2. **The "blind" comparison baseline is too weak to isolate the method's value.** The main prediction-error baseline withholds stimulation times from the dynamical model (Figures 2e, 3c), trivially ensuring worse performance. This does not test whether the paper's specific design choices (kernel regression, temporal kernel, etc.) are better than reasonable alternatives. More informative comparisons would include other nonparametric response models (e.g., Gaussian processes), ablations of the temporal kernel, or a fixed non-adaptive S-hat.

### Minor
1. **No ablation isolating kernel regression from simpler alternatives.** Given that the injected stimulation-response mapping in the real-data experiments is a linear AR(1) process, a linear regression model might perform as well. An ablation comparing kernel regression to a linear baseline would clarify whether the nonparametric complexity is warranted for this setting.

2. **No statistical testing on key quantitative claims.** Results such as "508/600 optimizations gave a misalignment of less than 1°" (line 214) are reported without confidence intervals, bootstrap estimates, or tests across random seeds/splits.

3. **The optimization solver is underspecified.** The objective in Eq. (8) is non-convex (cosine similarity), and the paper states only that it is solved with "box constraints" (Algorithm 1, line 19) without describing the solver, convergence criteria, or handling of local optima. For a method claiming real-time feasibility, this matters.

4. **sjPCA novelty is modest.** Adding Orthogonal Procrustes alignment to stabilize streaming jPCA planes is a sensible engineering contribution, but is an incremental addition rather than a conceptually novel dimensionality reduction method. The paper should frame this more accurately.

### Trivial
None.

## Nice-to-Haves
- A single experiment with real optogenetic or electrical stimulation data — even on a simple benchmark — would substantially strengthen the central claim.
- At minimum, replacing the AR(1) injection with a more realistic nonlinear response model (e.g., learned from real optogenetic perturbation data, or a spiking network model that produces complex state-dependent responses).
- Comparison against alternative stimulus selection methods (e.g., Bayesian optimization, random search with the same sample budget).
- Quantifying the gap between the learned S-hat and an oracle S to show how much room for improvement remains.

## Removed Points
- **"Optimization evaluation conflates predictive accuracy with control performance"** — The paper does compare predicted vs. observed error (Fig 4c, Fig 5) and shows they are correlated. This is a valid concern about the real-data experiments, but it is essentially a restatement of Weakness #1 (semi-synthetic evaluation) applied specifically to the optimization results. Merged.
- **"The central question — whether the method can actually drive latent dynamics in a desired direction in a real neural system — remains unanswered"** — True, but this is the same limitation as Weakness #1, not a separate issue. Demoted to merged with #1.
- **"Section 4.2 would be strengthened by an ablation comparing closed-loop learned S-hat against oracle S"** — This is a useful suggestion but belongs in Nice-to-Haves, not a weakness.
- **"The parallel latent space comparison (Fig 1c) is not evaluated beyond illustrative heatmap"** — The contribution is the framework enabling this comparison, not a rigorous benchmark of adaptive selection. Demoted to Nice-to-Have.
- **"Kernel regression with high-dimensional stimuli may suffer curse of dimensionality"** — The kernel uses product kernels over latent state (low-dim), stimulus, and time. The latent state is low-dimensional, and the stimulus kernel is one of several product components. The paper does not evaluate this directly, but the concern is speculative without evidence of actual performance degradation. Removed.

## Novel Insights
None beyond the paper's own contributions. Both the harsh critic and strength finder accurately identified the paper's key strengths (real-time feasibility, quantitative optimization results, adaptive recovery from non-stationarity) and its most consequential limitation (semi-synthetic real-data experiments). Neither reviewer identified a fundamentally novel angle that the paper itself does not articulate.

## Suggestions
1. Address the semi-synthetic evaluation gap by (a) running at least one experiment with a more realistic stimulation response model (nonlinear, network-based), or ideally with real optogenetic/electrical stimulation data; and (b) being more upfront in the abstract about the nature of the real-data evaluation.
2. Add ablations: kernel regression vs. linear regression for S-hat, closed-loop learned S-hat vs. oracle S, adaptive vs. fixed temporal kernel.
3. Replace or supplement the "blind" prediction baseline with comparisons against alternative response models (Gaussian process regression, neural network) and alternative stimulus selection methods (random search, Bayesian optimization).
4. Add statistical testing (confidence intervals, bootstrap) for key quantitative results like the 508/600 <1° claim.
5. Detail the optimization solver used for the non-convex objective in Eq. (8), including convergence criteria and local optima handling.

## Score and Decision
Based on these considerations, the paper has genuine contributions (a well-motivated end-to-end framework, streaming sjPCA, real-time feasibility, and quantitative optimization results) but a significant evaluation gap: the real-data experiments use injected AR(1) stimulation rather than real biological responses, and the baselines are too weak to isolate the method's specific advantages. The paper is not fatally flawed — the framework is sound and its components are individually validated — but the evidence does not fully support the most ambitious claims about enabling causal latent dynamics experiments. This places it in borderline territory.

**MY FINAL SCORE: <score>5.5</score>**
**MY FINAL DECISION: <decision>Accept</decision>**