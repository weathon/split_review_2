## Summary
This paper argues that encoding geometric structure as inductive biases in ML models for dynamical systems enables robust generalization with far fewer parameters than structure-naive approaches. The argument is supported through two use-cases: (1) system identification of a 2D heat transfer system via Riemannian optimization on the symmetric positive definite (SPD) manifold, and (2) learning the 18D Fermi-Pasta-Ulam-Tsingou system using symplectic Hamiltonian neural networks (SHNNs), demonstrating that compact structure-aware models outperform much larger baselines in long-horizon rollout and energy conservation.

## Strengths
- **Well-articulated geometric framing**: The paper clearly connects the geometry of dissipative systems (SPD manifold, Riemannian optimization) and conservative systems (symplectic manifold, Hamiltonian structure) to practical ML, making a compelling case that these priors are underutilized. Figure 1's SPD manifold visualization and Figure 2's energy-surface projections are effective at conveying the underlying geometry.
- **Compelling experimental evidence for the core thesis**: The conservative use-case results are particularly strong. Table 2 and Figure 3 show that a 1,441-parameter SHNN achieves better rollout MSE than the best 97,074-parameter LSTM, with dramatically lower energy drift. The phase-space visualizations in Figure 4 vividly demonstrate why structure-naive models fail—the LSTM trajectory visibly crosses energy levels while the SHNN stays on the correct level set.
- **Comprehensive model size sweep**: Rather than comparing at a single model size, the paper sweeps across multiple widths and depths (Table 2), showing that structure-naive models do not reliably close the gap even when scaled up significantly, which directly supports the "smaller models" thesis.
- **Physically meaningful generalization test**: The dissipative use-case uses a genuine out-of-distribution test (London training → Chicago testing with different climate extremes), and the conservative use-case tests on unseen initial conditions. These are more informative than typical ML benchmarks.

## Weaknesses
### Fatal
None.

### Major
- **Modest methodological novelty**: The SHNN for the conservative case directly adopts the architecture from David & Méhats (2023) without algorithmic contribution. The SPD-constrained optimization, while more original, is demonstrated only on a 2-dimensional system with a 2×2 matrix. The paper's main value is as a comparative empirical study rather than a methods contribution, which limits its significance at a venue like ICLR.
- **The dissipative baselines conflate multiple factors**: The comparison of RieOpt against RF, XGBoost, and LSTM involves fundamentally different model classes (linear state-space vs. non-parametric vs. recurrent). The performance gap on the Chicago test (Table 1) could arise partly from the physics-informed model class (linear state-space) rather than specifically from Riemannian optimization. The EucOpt ablation helps isolate the Riemannian component, but EucOpt itself is still a physics-informed LSSM, so the comparison to RF/XGBoost/LSTM conflates structure-preservation with model-class selection.
- **Limited rollout horizon for FPUT**: The 1,000-step rollout (~100 time units with τ=0.1) is relatively short given the 30,000-step training trajectory. For a system where long-term structure preservation is the primary selling point, evaluating over longer horizons (e.g., 5,000–10,000 steps) would strengthen the energy drift argument substantially.

### Minor
- **Two disconnected use-cases**: The dissipative (2D linear) and conservative (18D nonlinear) systems are quite different in character, making it hard to draw unified conclusions. A natural question is whether the SPD approach scales to higher-dimensional dissipative systems, or whether the SHNN insight applies to more realistic conservative systems beyond FPUT.
- **Missing stronger baselines for FPUT**: Other symplectic integrator-based or structure-preserving approaches (e.g., SympNets from Jin et al. 2020, which is cited but not benchmarked) would provide a more informative comparison than LSTM and NeuralODE alone.
- **Cholesky parameterization mentioned but not explored**: Section 2.1.2 mentions an alternative Cholesky decomposition approach for SPD constraints but provides no comparison with the Riemannian optimization approach.

### Trivial
None.

## Nice-to-Haves
- A unified figure or table comparing both use-cases side by side to reinforce the "smaller models" message across both system types.
- Analysis of how the SPD manifold constraint affects training convergence speed in the dissipative case, complementing the accuracy results.

## Novel Insights
The paper's most novel contribution is the connection between time-discretization of linear state-space models and projection onto the SPD manifold, interpreting the matrix exponential as a map from the Euclidean space of symmetric dynamical systems to the curved SPD manifold of stable discrete-time systems. This geometric reinterpretation of a standard system identification procedure is genuinely insightful and could motivate further work on structure-preserving identification for higher-dimensional dissipative systems. However, beyond this connection and the paper's own demonstrations, the broader insight that structure-preserving models are more parameter-efficient is well-established in the literature.

## Suggestions
- Expand the FPUT evaluation to longer rollout horizons and include SympNets as a baseline to provide a more complete picture of the symplectic methods landscape.
- For the dissipative case, include a controlled experiment where all methods share the same linear state-space model class but only differ in whether Riemannian or Euclidean optimization is used, to isolate the effect of geometric optimization from model-class selection.
- Consider a third use-case at intermediate complexity (e.g., a higher-dimensional dissipative system) to bridge the gap between the two current examples.

## Score and Decision
The paper presents a clear and well-executed empirical study with a sound geometric framing. The experimental evidence for the conservative case is compelling, particularly the energy drift analysis and the model-size sweep. However, the methodological novelty is limited (the SHNN is from prior work; the SPD optimization is only on a 2D system), the dissipative baselines conflate multiple factors, and the two use-cases are too disconnected to form a cohesive narrative. As a comparative empirical study, it provides useful evidence for the community but falls short of the contribution level typically expected at ICLR.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <score>Reject</score>