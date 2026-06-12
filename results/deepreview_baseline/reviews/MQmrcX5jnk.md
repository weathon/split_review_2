## Summary
The paper introduces Constrained Mass Transport (CMT), a variational framework for sampling from unnormalized distributions, applied to molecular Boltzmann generators. CMT constructs an annealing path by solving a sequence of constrained optimization problems that bound both the KL divergence and the entropy decay between successive intermediate densities, mitigating mode collapse and mass teleportation. The method is instantiated with normalizing flows and achieves state-of-the-art results on established benchmarks and a new, larger ELIL tetrapeptide system, consistently outperforming prior methods in effective sample size and mode coverage without relying on MD samples.

## Strengths
- **Principled theoretical framework.** The paper provides clean analytical derivations (Propositions 2.1–2.3, Theorem 2.4) showing that trust-region and entropy constraints yield well-defined annealing paths (geometric, tempered, geometric-tempered), with monotonic schedule parameters. This connects reinforcement-learning trust-region ideas to sampling in a rigorous way.
- **Strong empirical performance.** On all four molecular systems, CMT achieves the best EUBO, highest effective sample size, and competitive Ramachandran TV distance across the board, often by a wide margin (e.g., 2.5× higher ESS on ELIL tetrapeptide). The ablation study clearly demonstrates that both constraints are necessary for stable training and mode coverage, and that CMT avoids the collapse seen in reverse-KL or unconstrained forward-KL training.
- **New large-scale benchmark.** The ELIL tetrapeptide (d=219) is the largest molecular system studied to date under the pure-energy-evaluation setting, providing a useful testbed for future work on Boltzmann generators.
- **Computational efficiency.** CMT uses an importance-sampling estimator for the Lagrangian dual that adds negligible overhead (≈0.01% of training time on alanine dipeptide), and the trust-region constraint naturally controls importance-weight variance. The method requires fewer or comparable target evaluations than baselines while delivering better results.

## Weaknesses

### Fatal
None.

### Major
- **Hyperparameter sensitivity of constraints is not fully explored.** The trust-region bound ε_tr and entropy bound ε_ent are fixed to a single value across all experiments. While the paper notes that ε_tr controls importance-weight variance, it does not analyze how performance changes with different ε_tr values, especially across systems of varying dimension. A sensitivity analysis would strengthen the practical guidance.
- **Fixed annealing steps versus adaptive stopping.** The benchmark uses a fixed number of annealing steps I for fair comparison. The paper mentions that Lagrangian multipliers could serve as a stopping criterion, but this adaptive procedure is not tested. Without it, the method may over- or under-iterate on some problems, and the practical recommendation remains incomplete.

### Minor
- **No quantitative comparison to diffusion-based Boltzmann generators.** The paper states that diffusion-based methods are less competitive but does not include them in the main table. While the focus on state-of-the-art flow-based methods (FAB, TA-BG) is reasonable, adding a diffusion baseline (or citing results from prior work) would make the empirical evaluation more comprehensive.
- **Entropy constraint alone is not new in isolation.** The tempered path q ∝ p^{1/(1+η)} is essentially temperature annealing. The novelty lies in the combination with the trust-region constraint. This is acknowledged in the paper but could be stated more prominently.

### Trivial
None.

## Nice-to-Haves
- Include an adaptive stopping rule based on Lagrangian multipliers (λ, η → 0) and compare its performance and computational cost to the fixed-step schedule.
- Provide guidance on choosing ε_tr and ε_ent relative to system dimension and target entropy; an empirical sensitivity sweep would be valuable.
- Compare against one diffusion-based Boltzmann generator (e.g., Choi et al. 2025 or Kim et al. 2025) to further contextualize the method.

## Novel Insights
The key insight is that simultaneous control of both the KL divergence (trust-region) and the entropy decay between successive variational densities yields annealing paths that are neither purely geometric nor purely temperature-scaled, but a hybrid (geometric-tempered) that prevents mass teleportation while maintaining sufficient distributional overlap. This insight is theoretically characterized and empirically shown to outperform standard geometric or tempered paths, especially in high-dimensional, multimodal molecular systems. The connection to reinforcement-learning trust-region methods (TRPO/PPO) and their adaptation to sampling via the dual Lagrangian formulation is a clean conceptual bridge.

## Suggestions
- Perform a sensitivity analysis of ε_tr and ε_ent on at least one system (e.g., alanine hexapeptide) to demonstrate robustness and inform hyperparameter choice.
- Include a comparison to a diffusion-based Boltzmann generator in the main table or as an appendix entry to further substantiate the claim of state-of-the-art performance.
- Evaluate the method with an adaptive stopping criterion (using λ, η → 0) and report the number of steps and wall-clock time versus the fixed schedule.

## Score and Decision
MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>