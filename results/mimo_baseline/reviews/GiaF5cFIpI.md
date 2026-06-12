## Summary

This paper presents a real-time framework for designing neural stimulations that perturb latent neural dynamics in desired directions. The framework integrates streaming dimensionality reduction (with a novel sjPCA method), nonparametric kernel regression for stimulus-response mapping under state and time dependence, and a constrained optimization procedure for selecting high-dimensional stimulation patterns that produce targeted effects in low-dimensional latent spaces. The method is demonstrated on simulated and real neural datasets (calcium imaging, electrophysiology) with simulated stimulation effects.

## Strengths

- **Comprehensive real-time framework with realistic constraints.** The paper addresses a genuinely important problem—causal interrogation of latent neural dynamics—and provides a complete pipeline from data acquisition through latent space construction, dynamics modeling, response estimation, and stimulation optimization. Crucially, the optimization respects practical constraints (non-negativity for excitation-only stimulation, sparsity limits on number of targets, magnitude bounds), which distinguishes this from theoretical stimulation design work that ignores feasibility.

- **Novel streaming jPCA (sjPCA).** The extension of jPCA to a streaming setting via Sherman-Morrison updates plus an Orthogonal Procrustes stabilization step is a clean and useful contribution. The convergence analysis in Figure 1a shows that sjPCA and proSVD converge rapidly to their offline counterparts, and the parallel operation of multiple latent space representations with adaptive selection based on predictive performance (Figure 1c) is a practical and novel idea for experiments where the best representation may change over time.

- **Nonparametric, state-dependent stimulus-response mapping.** The kernel regression model in Eq. 7 is a principled choice that makes minimal assumptions about the form of the stimulus-response function, accounts for the neural state at the time of stimulation, and includes a temporal discounting mechanism to handle non-stationarity (e.g., plasticity, probe drift). The demonstrations in Figures 2d-e showing recovery from jump discontinuities and continuous drift in the response mapping are compelling evidence of adaptivity.

- **Computationally efficient and well-specified.** The algorithm is presented with clear pseudocode (Algorithm 1), all components are mathematically well-defined, and the reported runtimes (<10ms average, <100ms worst case) credibly demonstrate real-time feasibility. The use of differentiable kernel regression enables gradient-based optimization of the stimulation vector, which is a key design insight.

- **Multi-modal validation.** Testing across toy models, calcium imaging data, and electrophysiological recordings provides breadth in demonstrating the framework's applicability across data modalities with different temporal resolutions and noise characteristics.

## Weaknesses

### Fatal

None.

### Major

- **All real-data experiments use simulated stimulations.** The most significant limitation is that no real stimulation experiments were conducted. Stimulation effects on real neural systems are notoriously variable, state-dependent, and often not well-captured by simple autoregressive models. The simulated stimulation model used ($y_t = r_t + a_t$, $a_t = 0.8 \cdot a_{t-1} + u_t$) assumes a fixed, deterministic additive response that does not capture inter-neuron variability in response magnitude, failures of opsin expression, off-target effects, or the highly nonlinear saturation dynamics typical of optogenetic stimulation. While the authors acknowledge this, the entire empirical validation rests on this assumption, making it difficult to assess how well the method would perform under realistic experimental conditions.

- **Response magnitude not evaluated.** The evaluation focuses almost entirely on angular alignment between observed and predicted responses (Figures 4-5), but ignores response magnitude. A stimulation could align perfectly in direction yet produce a negligibly small response that is indistinguishable from noise. Without assessing both alignment and magnitude, the practical utility of the designed stimulations remains uncertain.

- **Limited sensitivity analysis.** Key design choices—kernel bandwidths, response delay $d$, number of latent dimensions $k$, regularization parameter $\lambda_1$, number of simultaneous targets—lack systematic sensitivity analysis. The paper reports results for specific settings (e.g., $k=4$ for proSVD, $\lambda_1$ unspecified, 14 stimulated neurons in Figure 3) without characterizing how performance degrades as these parameters change.

### Minor

- **Comparison to alternative stimulation strategies is limited.** The comparison methods (random single neuron, random multiple neurons, shuffled) are weak baselines. A comparison against principled baselines such as greedy approaches, LASSO-based methods, or Bayesian optimization would more convincingly demonstrate the advantage of the proposed differentiable optimization.

- **Parallel latent space selection is underdeveloped.** The idea of tracking multiple latent spaces and adaptively selecting the best one is intriguing but the mechanism for switching (aggregating predictive error within local latent regions) is heuristic. When and how the algorithm switches between representations is not clearly analyzed, and it's unclear how this interacts with the stimulation-response model, which would need to be learned independently for each representation.

- **Delayed response model lacks experimental validation.** The delayed response framework (Section 2.3) is introduced as an important extension but is only tested with a single delay setting on one dataset. The assumption that no new stimulus is delivered before seeing effects of a previous one significantly limits the throughput of the system.

### Trivial

None.

## Nice-to-Haves

- A discussion of how the kernel regression's curse of dimensionality scales with the number of simultaneously stimulated neurons would help set expectations for practical limits on stimulation dimensionality.
- A comparison of the optimization's solution quality against the true optimal solution on the toy model, where the true $S$ is known, would strengthen the optimization claims.
- Quantification of how many stimulation trials are needed before the system becomes practically useful (i.e., before the predicted response reliably exceeds noise levels).

## Novel Insights

The integration of streaming dimensionality reduction with nonparametric stimulus-response modeling and constrained optimization for real-time neural stimulation design is genuinely novel. The observation that kernel regression with temporal discounting can simultaneously handle state-dependent responses and non-stationary mappings (drift, discontinuities) is a valuable insight for closed-loop neuroscience. The parallel tracking of multiple latent spaces with predictive performance-based selection provides a principled approach to the underappreciated problem that different computational hypotheses about neural manifold structure may be locally valid, and that stimulation experiments could be designed to discriminate between them.

## Suggestions

1. Conduct at least one experiment with actual neural stimulation (even in a reduced preparation) to validate the simulated stimulation assumptions.
2. Add a joint evaluation metric that combines angular alignment and response magnitude (e.g., projection of $s_{\text{obs}}$ onto $v$) to assess practical stimulation effectiveness.
3. Include a sensitivity analysis on the number of stimulated neurons and $\lambda_1$ to characterize the operating regime where the method is effective.
4. Compare against at least one non-trivial baseline stimulation strategy (e.g., greedy neuron selection based on functional tuning).

## Score and Decision

The paper presents a well-motivated, technically sound, and clearly presented framework that addresses an important problem in computational neuroscience. The streaming architecture, novel sjPCA, nonparametric response modeling, and constrained optimization are each well-executed. However, the complete reliance on simulated stimulation effects for empirical validation is a significant limitation that prevents confident assessment of real-world performance. The evaluation metrics (directional alignment only) further limit the conclusions that can be drawn. These concerns place the paper in the borderline territory—promising and well-designed, but needing stronger empirical validation to be fully convincing.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: Reject