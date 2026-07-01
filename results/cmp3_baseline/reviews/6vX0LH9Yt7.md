## Summary

This paper presents a hybrid neural-numerical framework for real-time interactive fluid simulation. The system combines a graph neural network that operates at low spatiotemporal resolution for efficiency with a fallback mechanism to the classical Material Point Method (MPM) when fluid complexity is high, aiming to balance latency and fidelity. Additionally, a diffusion-based generative controller is trained via a reverse simulation strategy to produce external force fields from freehand user sketches, enabling intuitive fluid manipulation. Experiments across 2D/3D water, sand, and mixed-material scenarios show latency reductions of 11–29% compared to MPM baselines while maintaining competitive simulation accuracy.

## Strengths

1. **Hybrid safeguard paradigm**: The idea of using a lightweight neural physics model as the default predictor and falling back to a classical numerical solver only when a cheap complexity metric indicates risk is practically motivated. The cosine-similarity trigger on acceleration history is computationally inexpensive and correlates with error (Figure 5), making the hybrid design plausible for real-time use.

2. **Novel data generation for controllable fluids**: The reverse simulation strategy (Equation 3) provides an automatic way to generate paired (sketch, force-field) training data without manual annotation, addressing a key bottleneck in learning-based fluid control. This is a clever and principled approach.

3. **End-to-end system across multiple domains**: The paper demonstrates the complete pipeline—hybrid simulation plus sketch-based control—on seven different scenarios covering 2D/3D water, sand, ramps, and mixtures, showing generality beyond a single material or geometry.

4. **Ablation studies on trade-offs**: Figures 6 and Table 1 systematically explore how spatial/temporal downsampling ratios and the fallback threshold affect the error-latency Pareto front, providing practical guidance for deploying such hybrid systems.

## Weaknesses

### Major

1. **Modest latency improvements undermine the claimed "real-time" breakthrough**: The reported latency reductions (11–29%) are relatively small, and the absolute latencies of the MPM baseline are already low (e.g., 0.114 s per frame for 2D Water-Sand, 1.02 ms per step for 3D Sand). The neural physics at low resolution already achieves sub-millisecond steps (0.40 ms). The hybrid adds latency back to nearly the MPM level (0.70 ms, Table 1) to recover accuracy. The paper frames this as a major improvement, but the practical benefit over running MPM alone is marginal, especially when MPM is GPU-accelerated with Taichi and already real-time for these problem sizes.

2. **Weak evaluation of the generative control**: The quantitative results for fluid control (Table 3) show only small improvements over a constant-force baseline (e.g., 0.0802 vs. 0.0908 RMSE for 2D Water). The visual comparisons in Figure 11 are not convincing; the "Ours" results still differ noticeably from the ground truth. Moreover, the control is only evaluated for a fixed 100-step horizon with simple sketches (arrows and ovals). There is no user study, no test with complex multi-stroke sketches, no robustness test to noisy or invalid sketches, and no ablation on the diffusion model design choices (e.g., number of denoising steps, guidance scale). The claimed "interactive fluid control" lacks the empirical depth needed to demonstrate practical usability.

3. **Inconsistency between training loss and evaluation metric**: The neural physics is trained with particle-level RMSE on velocity (RMSE_\(\tilde{p}\)) at low resolution, but all evaluations and ablations use grid-level RMSE on mass (RMSE_\(\tilde{m}\)) to compare across resolutions. The paper acknowledges this mismatch but does not analyze whether optimizing the surrogate loss effectively minimizes the grid-level metric. Without such analysis, the reported improvements may be coincidental rather than causal. A proper solution would be to train directly on the grid metric, but the authors avoid it due to computational cost—this weakens the methodological rigor.

4. **Limited novelty beyond combination of existing tools**: The individual components (GNN-based physics simulator [Sanchez-Gonzalez et al., 2020], MPM on Taichi [Hu et al., 2019], diffusion-based conditional generation [Zhang et al., 2023; Wang et al., 2024b]) are well-established. The core novelty is the hybrid trigger and the reverse simulation data generation. While the trigger is a reasonable heuristic, its design (cosine similarity with a single tuned threshold) is simple and its effectiveness is only shown on one 2D scenario (Figure 5). The reverse simulation is essentially solving the inverse dynamics via finite differences, which is straightforward. The paper does not compare against alternative triggers (e.g., divergence, kinetic energy rate) or alternative control methods (e.g., optimizing forces online, using physics-based guidances like Pan et al., 2013). The increment over prior work is therefore modest.

### Minor

5. **Lack of generalization analysis**: The paper trains separate models per scenario (following prior work), which limits the claim of a unified framework. It is unclear whether the same neural physics model or the same fallback threshold generalizes across domains or even to unseen initial conditions within the same domain. The evaluation uses held-out trajectories from the same distribution—this does not test robustness to distribution shift or out-of-domain complexity.

6. **Missing details on the diffusion-based Fluid ControlNet**: The architecture description is brief (Section 3.2.3 and Figure 9) and relies on an appendix that is not provided. Key design choices (e.g., U-Net vs. transformer backbone, conditioning mechanism, number of denoising steps, inference-time sampling strategy) are not specified, making the results irreproducible from the main text alone.

7. **The 11–29% latency range is inconsistently reported**: The abstract says "11~29% latency reduced", Table 1 shows only 0.40 ms to 0.70 ms for neural versus hybrid (increase, not reduction relative to MPM), and the text says "reduce latency of MPM by 11.8%...29.8%". The baseline comparison is not always clear: latency reduction is claimed relative to MPM at full resolution, but in Figure 10 the MPM baselines have higher error than the hybrid. The hybrid is positioned as better than both neural physics and MPM, but the numbers show it is sometimes slightly slower than the low-resolution neural physics while being faster than full MPM—this is expected from any approximate method. The framing as "acceleration" of MPM is accurate but the improvement is small.

### Trivial

None.

## Nice-to-Haves

- A user study with animators or designers to assess whether the sketch-based control actually meets practical needs.
- An analysis of how the fallback frequency varies across different scenarios and timesteps, and how sensitive performance is to the window size δt.
- Comparison to optimization-based fluid control methods (e.g., guiding forces solved via adjoint methods) as a stronger baseline.
- Ablation on the diffusion model: e.g., what happens if the force field is directly regressed instead of generated via diffusion?

## Novel Insights

None beyond the paper's own contributions: the hybrid trigger based on acceleration cosine similarity and the reverse simulation data-generation pipeline are the main novel elements. The insight that a simple one-dimensional metric can predict when a learned simulator will fail, enabling a fallback to a classical solver, is practical but not deeply analyzed theoretically. The reverse simulation idea is a straightforward application of finite-difference inverse dynamics and is not conceptually new (similar ideas appear in robotics for trajectory tracking). Overall, the paper does not produce a surprising or transformative insight; it combines known techniques in a reasonable engineering solution.

## Suggestions

1. Strengthen the evaluation of the generative control: include quantitative metrics beyond final-step RMSE (e.g., Chamfer distance between controlled particles and target sketch, temporal consistency of the force field, success rate across multiple random seeds), and test with more complex sketches (multi-arrow, evolving shapes).
2. Validate the fallback trigger on all seven domains, not just Water 2D, and show that the same threshold (r_c=0.8) works reasonably across them, or provide a domain-adaptive threshold.
3. Either train and evaluate on the same metric (grid-level RMSE) or provide empirical evidence that the surrogate particle loss correlates well with the grid metric.
4. Clarify the exact latencies and baselines: state explicitly for each domain the wall-clock time per step for MPM, neural physics, and hybrid, and report the reduction relative to the fastest method that achieves acceptable error for a given application.

## Score and Decision

Score: 4

Decision: Reject

The paper addresses a relevant problem (real-time interactive fluid simulation) and contains some clever components (hybrid fallback, reverse simulation data generation). However, the experimental evidence is not strong enough to support the claimed significance. The latency improvements are modest, the control evaluation is weak and limited to simple scenarios, and the methodological novelty is incremental. The hybrid trigger is under-validated, and the mismatch between training and evaluation metrics raises concerns about the soundness of the reported trade-offs. While the system is a reasonable engineering contribution, it does not meet the bar for a top venue like ICLR in terms of empirical rigor or conceptual depth.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>