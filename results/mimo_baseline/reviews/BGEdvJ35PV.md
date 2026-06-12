## Summary
The paper identifies that molecular data distributions exhibit a "dense-concentrated structure" (DC-structure) where valid molecules occupy narrow, densely packed peaks separated by near-zero density regions, making diffusion models fragile to small errors during reverse inference. Based on this analysis, the authors propose DIST, a model-agnostic plug-in corrective sampling method that evaluates intermediate distributions and filters out off-distribution samples, steering trajectories back toward valid molecular regions. Experiments across three backbone models (EDM, GeoLDM, RADM) on QM9 and GEOM-Drugs demonstrate consistent improvements in generation quality while reducing inference timesteps by nearly half.

## Strengths
- **Well-motivated and novel problem identification**: The DC-structure concept is clearly articulated with an intuitive image-vs-molecule analogy (Fig. 1), formalized rigorously in Definition 3.1, and connected to concrete failure modes via the overshoot analysis (Eqs. 6–7). This provides a principled understanding of why molecular diffusion is fundamentally harder than image diffusion.

- **Strong model-agnostic empirical results**: DIST consistently improves all three architecturally diverse backbones (GNN-based equivariant EDM, latent-space GeoLDM, Transformer-based non-equivariant RADM) across both QM9 and GEOM-Drugs. For example, EDM+DIST improves molecule stability from 82.0% to 89.9% on QM9, and GeoLDM+DIST reaches 93.4%. The universality across architectures is a compelling demonstration that the DC-structure issue is fundamental, not architectural.

- **Efficiency gains alongside quality improvements**: Table 3 shows DIST reduces average timesteps from 1000 to ~400–560, which is a practically valuable benefit. The ablation in Table 4 shows even small pilot budgets (30 samples) yield significant improvements.

- **Theoretical grounding**: The TV-contraction result (Corollary 3.1) and selective reverse error bound (Proposition 3.1) provide formal support for the correction strategy, connecting intermediate distribution alignment to final output quality.

## Weaknesses
### Fatal
None.

### Major
- **Implementation details are underspecified in the main text**: The concrete algorithm is hard to reconstruct from the paper alone. Key details are vague: (1) which specific pilot score function $s_j$ is used in experiments (the paper lists four options without specifying), (2) how batches are constructed concretely (what perturbation, what radius $r$), and (3) how the threshold $\tau$ is selected in practice. While these may be in the appendix, the main paper's description is insufficient for understanding the actual procedure, which undermines reproducibility and clarity.

- **No comparison with alternative corrective/guidance methods**: The paper does not compare DIST with other inference-time correction strategies (e.g., classifier guidance, classifier-free guidance adapted for molecules, or simple resampling baselines). Without such comparisons, it is difficult to attribute the improvements specifically to the DC-structure insight rather than to inference-time filtering in general. The paper mentions Appendix B discusses this, but the main text should at least summarize the key distinctions.

- **Theoretical assumptions may be strong**: Definition 3.1 approximates the molecular distribution as a Gaussian mixture, and Corollary 3.1 assumes an ideal reverse kernel. The paper does not discuss how well these approximations hold in practice or the sensitivity of the results to violations of these assumptions.

### Minor
- **Wall-clock time not reported**: Table 3 counts timesteps but the pilot inference, batch construction, and filtering steps have their own computational overhead. Actual wall-clock time or FLOPs would give a more complete picture of efficiency.

- **Table 1 is limited to one backbone**: The degradation-with-starting-timestep experiment only shows EDM on QM9. Showing this across multiple backbones would strengthen the generality claim.

- **GEOM-Drugs results are less informative**: Stability and uniqueness are omitted (reportedly near 0% and 100% for all methods), leaving only two metrics for this important large-molecule benchmark.

### Trivial
- An explicit algorithm box/pseudocode would significantly improve clarity.

## Nice-to-Haves
- Concrete algorithm pseudocode for the full DIST procedure
- Wall-clock time comparisons alongside timestep counts
- Analysis of failure cases: when does DIST not help or hurt?
- Sensitivity analysis of threshold $\tau$ in the main text

## Novel Insights
The paper's central contribution—the formalization of DC-structure in molecular distributions and its connection to diffusion model fragility—is genuinely novel. The key insight that narrow, densely packed peaks cause the reverse update to overshoot into low-density regions (Eq. 7) is well-argued and explains a real failure mode. The empirical finding that this issue persists uniformly across GNN, Transformer, equivariant, non-equivariant, direct-space, and latent-space architectures is an important observation that challenges the community's focus on architectural solutions alone.

## Suggestions
- Add a concrete algorithm box summarizing the DIST procedure end-to-end, including the specific score function, batch construction, and threshold selection used in experiments.
- Include at least one comparison with a simpler inference-time correction baseline (e.g., random resampling of intermediate states or classifier-guided sampling) to isolate the contribution of the DC-structure-motivated design.
- Report wall-clock time or FLOPs in addition to timestep counts to give a complete efficiency picture.

## Score and Decision
The paper makes a genuine and well-motivated contribution by identifying and formalizing the DC-structure problem in molecular diffusion, and the proposed DIST method is effective and model-agnostic with strong empirical results. However, the underspecified implementation details in the main text and the lack of comparison with alternative corrective methods are notable gaps that prevent a stronger recommendation. The theoretical analysis, while elegant, rests on assumptions whose practical validity is not fully established.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: Accept