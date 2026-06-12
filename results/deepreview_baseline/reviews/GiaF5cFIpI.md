## Summary

This paper presents a real-time adaptive stimulation framework for manipulating latent neural dynamics. The method integrates streaming latent space construction (including a novel streaming jPCA variant), dynamical models, a nonparametric stimulus-response mapping via kernel regression with temporal discounting, and a constrained optimization procedure to design high-dimensional stimulation patterns that drive latent activity in desired directions. The framework is demonstrated on simulated data and two real neural datasets (calcium imaging and electrophysiology) with simulated stimulation effects, showing fast learning and real-time feasibility.

## Strengths

- **Important problem**: Causally testing latent neural dynamics hypotheses via targeted stimulation is a key open challenge in neuroscience. The paper addresses a genuine gap by providing a method for driving latent dynamics in real time under realistic experimental constraints.
- **Comprehensive framework**: The modular design integrates streaming dimensionality reduction, dynamical modeling, nonparametric stimulus-response learning, and constrained optimization. This allows swapping components and comparing multiple latent representations in parallel.
- **Practical constraints**: The optimization formulation explicitly handles non-negativity (excitation-only interventions), sparsity (limited number of targets), and magnitude constraints, which are directly relevant to real optogenetic experiments.
- **Real-time feasibility**: End-to-end runtimes below 100ms (often <10ms) are demonstrated, making the method compatible with future *in vivo* closed-loop experiments.
- **Non-stationarity handling**: The temporal kernel in the stimulus-response mapping allows the model to adapt to changes in the underlying mapping (demonstrated with flip and rotate perturbations in simulation).

## Weaknesses

### Fatal
None.

### Major
1. **Validation only with simulated stimulations on real data**: The core claim is about adaptive stimulation of neural dynamics, but all real-data experiments use artificially simulated stimulation effects (autoregressive additive model). The stimulus-response mapping is learned from these simulated responses, not from actual neural responses to real optogenetic or electrical stimulation. This significantly weakens the demonstration that the method would work in a real closed-loop experiment where stimulation effects are noisy, nonlinear, and state-dependent in ways not captured by the simulation.

2. **Weak baselines**: The stimulation optimization is compared only against random single-neuron stimulation, random groups, and shuffled versions of designed stimuli. No comparison is made to existing stimulation design methods cited in the related work (e.g., Bayesian optimization, active learning, input-output dynamical modeling). The "blind" model baseline for prediction error simply ignores stimulation entirely, which is a straw man. A more meaningful baseline would be a linear model using the stimulation vector directly.

3. **Incremental novelty of sjPCA**: The novel streaming jPCA (sjPCA) adds an Orthogonal Procrustes stabilization step to an existing method. The convergence demonstration is only on simulated data, and it is unclear how much practical benefit sjPCA provides over simply using proSVD or other streaming PCA methods. The paper does not show that sjPCA leads to better stimulation outcomes.

4. **L1 relaxation for sparsity not validated**: The optimization uses an L1 penalty to encourage sparsity (controlling the number of stimulated neurons), but the paper does not analyze how well this relaxation approximates the desired L0 constraint in practice. The relationship between the penalty parameter λ₁ and the actual number of non-zero elements is not characterized.

5. **No ablation studies**: The framework has multiple components (streaming latent space, dynamical model, kernel regression, optimization). There are no ablation experiments showing the contribution of each component to overall performance. For example, how much does the temporal kernel help versus a static kernel? How does performance degrade without the learned stimulus-response mapping (i.e., using only open-loop optimization)?

### Minor
- The paper is dense and could benefit from clearer organization, particularly separating novel contributions from standard techniques.
- The choice of kernel hyperparameters (length scales for latent state, stimulus, and time) is not discussed; sensitivity to these choices is not explored.
- The optimization solver is not specified (gradient-based? which algorithm?).

### Trivial
None.

## Nice-to-Haves
- A real closed-loop experiment, even with a simple preparation (e.g., cultured neurons or slice), would dramatically strengthen the claims.
- Comparison to existing methods like Bayesian optimization or active learning for stimulation design.
- Ablation studies isolating the contribution of each component (sjPCA vs. proSVD, kernel regression vs. linear model, temporal kernel vs. no temporal kernel).
- Analysis of how the L1 relaxation controls sparsity in practice.

## Novel Insights
The paper's primary insight is the integration of streaming latent space construction, nonparametric stimulus-response modeling with temporal discounting, and constrained optimization into a single real-time framework for driving latent neural dynamics. The use of kernel regression to learn a mapping from (latent state, stimulation, time) to latent response, combined with the ability to optimize high-dimensional stimulation patterns under realistic constraints, is a practical contribution. However, the individual components are largely existing techniques; the novelty lies in their combination and application to this specific problem.

## Suggestions
1. Perform at least one real closed-loop stimulation experiment (e.g., using optogenetics in a simple preparation) to validate that the learned stimulus-response mapping and optimization produce the intended latent-space effects.
2. Compare against a baseline that uses the stimulation vector directly in a linear regression model for the stimulus-response mapping, and against a simple optimization baseline (e.g., selecting the top neurons by weight in the desired latent direction).
3. Add ablation studies: (a) remove the temporal kernel, (b) replace kernel regression with a linear model, (c) use open-loop optimization (identity mapping) throughout, (d) use a fixed latent space instead of streaming.
4. Characterize the relationship between the L1 penalty parameter and the actual number of non-zero stimulation targets, and discuss how to set this parameter for a desired sparsity level.

## Score and Decision

**Score**: 4.0

**Decision**: Reject

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>