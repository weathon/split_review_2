## Summary

This paper introduces Constrained Mass Transport (CMT), a variational framework for sampling from high-dimensional, multimodal unnormalized probability distributions, with a focus on molecular Boltzmann generators. CMT constructs a sequence of intermediate distributions by imposing constraints on both the KL divergence (trust-region) and entropy decay between successive steps, which mitigates mass teleportation and mode collapse. The authors derive analytical forms for the optimal intermediate densities under these constraints, instantiate the framework with normalizing flows, and demonstrate consistent improvements over state-of-the-art methods on molecular benchmarks, including the newly introduced ELIL tetrapeptide.

## Strengths

- **Novel and principled framework**: The combination of trust-region and entropy constraints for constructing annealing paths is theoretically well-motivated and grounded in convex optimization. The analytical characterization of optimal intermediate densities (Propositions 2.1-2.3) provides a clean mathematical foundation.

- **Strong empirical results**: CMT consistently outperforms strong baselines (FAB, TA-BG) across all four molecular systems, achieving up to 2.5× higher effective sample size while using comparable or fewer target evaluations. The improvements are particularly pronounced on the larger systems (alanine hexapeptide and ELIL tetrapeptide), where the gap widens substantially.

- **Comprehensive ablation study**: The authors systematically investigate the effect of each constraint individually and in combination, providing clear evidence that both constraints are necessary for optimal performance. The ablation on alanine hexapeptide (Figures 2-3) convincingly demonstrates that omitting either constraint leads to mode collapse or unstable training.

- **Introduction of a challenging new benchmark**: The ELIL tetrapeptide (d=219) is a meaningful contribution to the community, representing the largest molecular system studied to date under the purely energy-based variational sampling setting.

## Weaknesses

### Fatal
None.

### Major
- **Computational cost is not adequately characterized**: The paper reports that CMT uses a fixed number of annealing steps and comparable target evaluations to baselines, but does not provide wall-clock training times or GPU hours. Given that CMT requires solving a 2D convex optimization problem at each step and performing importance-weighted forward KL minimization, the actual computational overhead relative to simpler methods like reverse KL is unclear. The claim that Lagrangian dual optimization accounts for only 0.01% of training time on alanine dipeptide is helpful but insufficient—this may not scale linearly.

- **Limited analysis of hyperparameter sensitivity**: The trust-region bound ε_tr and entropy bound ε_ent are critical hyperparameters, yet the paper provides minimal guidance on how to set them. The ablation study only examines the presence/absence of constraints, not the sensitivity to different bound values. For a method to be practically useful, practitioners need to understand how to choose these parameters and how robust performance is to misspecification.

- **The connection to existing methods is underdeveloped**: While the paper cites related work on trust-region methods in RL and annealing paths, it does not clearly articulate how CMT differs from or improves upon the closest related work—Blessing et al. (2025) on path space measures. The paper would benefit from a more explicit comparison of the technical differences and advantages.

### Minor
- **The ELIL tetrapeptide benchmark lacks ground-truth characterization**: The paper introduces this system but does not provide sufficient analysis of its properties (e.g., number of metastable states, energy barriers, comparison to existing benchmarks). Without this context, it is difficult for readers to assess the significance of the results on this system.

- **The Ramachandran plot TV distance metric is not well justified**: The paper states that TV distance is preferred because it is "symmetric and more naturally reflects the bidirectional nature of matching generated and target Boltzmann distributions." However, the Ramachandran plots are 2D projections of a high-dimensional distribution, and TV distance on these projections may not reflect the true distributional match. The authors should discuss potential limitations of this metric.

- **The paper claims CMT "avoids mode collapse" but the evidence is mixed**: On the ELIL tetrapeptide, CMT achieves the best EUBO and ESS but has a slightly worse RAM TV than TA-BG (3.13×10⁻² vs 2.54×10⁻²). This suggests that CMT may not fully avoid mode collapse on the most challenging system, or that the RAM TV metric may not capture all aspects of mode coverage.

### Trivial
- The notation in Proposition 2.3 has a redundant "(x)" in the integrand of Z_{i+1}(λ, η).

## Nice-to-Haves

- A discussion of how the number of annealing steps I should be chosen in practice, and whether there is a principled stopping criterion based on the Lagrangian multipliers.
- An analysis of the variance of the importance weights used in the Lagrangian dual optimization, particularly as dimensionality increases.
- A comparison to diffusion-based Boltzmann generators (e.g., Liu et al., 2025; Choi et al., 2025) mentioned in the related work, to understand the relative strengths of flow-based vs. diffusion-based approaches under the CMT framework.

## Novel Insights

The key insight of this paper is that constraining both the KL divergence and entropy decay between successive variational distributions yields a principled annealing path that balances exploration and convergence. While trust-region constraints have been used in RL and entropy regularization in policy optimization, their combination and application to sampling problems is novel. The analytical result that the optimal densities under these constraints take a geometric-tempered form (Proposition 2.3) provides a clean theoretical characterization that connects constrained optimization to annealing paths. The empirical finding that both constraints are necessary—the trust-region constraint prevents rapid entropy collapse while the entropy constraint prevents mass teleportation—is a practically useful insight for designing sampling algorithms.

## Suggestions

1. Provide wall-clock training times and GPU memory usage for all methods to enable practitioners to assess the practical trade-offs.
2. Include a sensitivity analysis of the trust-region bound ε_tr and entropy bound ε_ent, showing how performance varies with different values across systems of different dimensionality.
3. Add a more detailed characterization of the ELIL tetrapeptide benchmark, including the number of metastable states, energy barriers, and a comparison of its difficulty to existing benchmarks.
4. Discuss the limitations of the Ramachandran plot TV distance metric and consider reporting additional metrics (e.g., Wasserstein distance on dihedral angles) for a more comprehensive evaluation.

## Score and Decision

This paper makes a solid contribution to the variational sampling literature with a novel, well-motivated framework, strong empirical results, and thorough ablation studies. The weaknesses are primarily around practical considerations (computational cost, hyperparameter sensitivity) rather than fundamental flaws. The paper is clearly written and the theoretical development is sound. I recommend acceptance.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>