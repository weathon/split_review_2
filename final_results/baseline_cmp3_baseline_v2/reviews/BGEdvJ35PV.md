## Summary

This paper identifies a fundamental challenge in applying diffusion models to 3D molecular generation: molecular data distributions exhibit a "dense-concentrated structure" (DC-structure) where valid molecules occupy narrow, densely packed probability peaks separated by near-zero density regions. The authors formalize this structure, analyze how it causes error accumulation and trajectory drift during reverse inference, and propose DIST (Diffuse and Steer), a plug-in corrective sampling method that filters intermediate distributions to realign trajectories toward valid molecular regions. Experiments on QM9 and GEOM-Drugs across multiple backbone diffusion models (EDM, GeoLDM, RADM) show consistent improvements in stability and validity metrics while reducing computational cost by nearly half.

## Strengths

- **Novel and well-motivated problem framing.** The paper provides a clear, intuitive explanation of why molecular generation is fundamentally harder for diffusion models than image generation, supported by a formal definition (DC-structure) and analysis of how narrow peaks cause overshoot and error accumulation. This is a genuine insight that goes beyond generic "molecules are hard" statements.

- **Theoretical grounding for the corrective approach.** The authors provide a formal analysis connecting the DC-structure to error propagation (Corollary 3.1, Proposition 3.1), establishing that bringing the intermediate model distribution closer to the true marginal reduces final distributional discrepancy. This provides principled justification for the corrective sampling strategy.

- **Strong empirical results across diverse backbones.** DIST consistently improves atom stability, molecule stability, validity, and validity×uniqueness across three different backbone architectures (GNN-based equivariant, latent-space, Transformer-based) on two datasets. The improvements are substantial (e.g., EDM molecule stability from 82.0% to 89.9% on QM9) and statistically significant with reported standard deviations.

- **Computational efficiency as an additional benefit.** The method reduces inference timesteps by roughly 40-60% while improving quality, which is a rare and valuable combination. The ablation study on pilot sample size provides practical guidance for the efficiency-quality trade-off.

## Weaknesses

### Major

- **The corrective sampling procedure is underspecified.** The paper describes the DIST framework at a high level (pilot samples, batch construction, score-based filtering) but lacks crucial implementation details. What exactly is the "pilot score" s_j? How is it computed from the pilot inference? The paper mentions "round-trip residual, self-consistency, ensemble variance, or chemistry-based penalty" as possibilities but never specifies which one is actually used in the experiments. Without this information, the method cannot be reproduced or properly evaluated. The threshold τ selection procedure is also not described.

- **The theoretical results do not directly connect to the implemented algorithm.** Corollary 3.1 and Proposition 3.1 provide general bounds on TV distance under ideal conditions (perfect reverse kernel, known batch partitions), but the actual DIST implementation uses heuristic pilot scores and thresholding. There is no analysis of how approximation errors from the pilot estimation, the choice of score function, or the threshold selection affect the theoretical guarantees. The gap between theory and practice is significant.

- **Missing comparison to existing corrective/guidance methods.** The paper mentions in Appendix B that a comparison with corrective methods is provided, but the main text lacks any comparison to established techniques like classifier guidance, classifier-free guidance, or resampling methods (e.g., replacement sampling, rejection sampling). Given that DIST is fundamentally a filtering/resampling approach, it should be compared to these baselines to demonstrate its advantages.

- **Limited evaluation on GEOM-Drugs.** Only atom stability and validity are reported for GEOM-Drugs, with no molecule stability or uniqueness metrics. The paper states these are "consistently close to 0% and 100%" for all methods, but this should be verified and reported. More importantly, the improvements on GEOM-Drugs are much smaller than on QM9 (e.g., EDM atom stability from 81.3% to 82.2%), raising questions about scalability to larger molecules.

### Minor

- **The efficiency analysis is somewhat opaque.** Table 3 reports average timesteps but does not explain the variance across methods (why does GeoLDM+DIST use 636.7 steps on GEOM-Drugs vs. 416.9 on QM9?). The relationship between the reported timesteps and the actual wall-clock time or FLOPs is not discussed.

- **The ablation study is limited.** Only the pilot sample size is ablated. The choice of intermediate timestep t, the threshold τ, and the perturbation intensity are mentioned as being in Appendix H but should be discussed in the main text to give a complete picture of the method's sensitivity.

- **The paper claims "nearly half" the computational cost but the actual reduction varies.** EDM+DIST on QM9 uses 556.1 steps (44% reduction), while RADM+DIST on GEOM-Drugs uses 438.8 steps (56% reduction). The claim is approximately correct but the variance should be acknowledged.

### Trivial

- The figure captions are overly long and contain redundant information that is already in the main text.

## Nice-to-Haves

- A comparison with simple rejection sampling (generate many samples, filter by validity) would help isolate the benefits of the corrective mechanism versus just generating more candidates.
- Analysis of how the method performs with different noise schedules or fewer total timesteps would strengthen the efficiency claims.
- Visualizations of corrected vs. uncorrected trajectories in a simplified 2D molecular-like distribution would make the mechanism more intuitive.

## Novel Insights

Beyond the paper's own contributions, the key insight is that the failure mode of diffusion models on molecular data is not primarily about model capacity or architectural expressivity, but about the geometry of the data distribution itself. The observation that narrow, densely packed peaks cause the score field to produce overshooting updates (equation 7) is a clean mechanistic explanation that could apply to other domains with similar distributional structure (e.g., protein conformations, crystal structures, constrained physical systems). The paper also makes the subtle point that architectural innovations (equivariance, latent spaces) do not address this fundamental geometric issue, which explains why even state-of-the-art models still struggle with molecular validity.

## Suggestions

1. **Specify the pilot score function and threshold selection procedure.** The paper must describe exactly how s_j is computed in the experiments and how τ is chosen. Without this, the method is not reproducible.

2. **Add comparisons to standard guidance/resampling baselines.** At minimum, compare to classifier-free guidance (if applicable) and simple rejection sampling to demonstrate that DIST's benefits are not just from filtering.

3. **Report full metrics on GEOM-Drugs** including molecule stability and uniqueness, even if they are near ceiling/floor, to provide a complete evaluation.

4. **Include wall-clock time or FLOPs comparison** alongside the timestep reduction to give a more practical efficiency measure.

5. **Discuss the limitations of the theoretical analysis** more explicitly, particularly the gap between the idealized setting (perfect reverse kernel, known batch partitions) and the practical implementation.

## Score and Decision

The paper addresses a genuine and important problem in molecular generation with a well-motivated approach, provides theoretical grounding, and demonstrates consistent empirical improvements. However, the underspecification of the core algorithm (pilot score, threshold selection) is a significant weakness that prevents proper evaluation and reproducibility. The missing comparisons to standard corrective methods further limit the assessment of the method's novelty and effectiveness. With the current level of specification, the paper cannot be accepted.

MY FINAL SCORE: 5.0score</score>
MY FINAL DECISION: Reject</decision>