## Summary

This paper identifies a fundamental challenge in applying diffusion models to 3D molecular generation: molecular data distributions exhibit a "dense-concentrated structure" (DC-structure) where valid molecules correspond to narrow, densely packed probability peaks separated by near-zero density regions. The authors formalize this structure, analyze how it causes error accumulation and trajectory drift during reverse inference, and propose DIST (Diffuse and Steer), a plug-in corrective sampling method that filters intermediate distributions to realign trajectories toward valid molecular regions. Experiments across multiple backbone models (EDM, GeoLDM, RADM) on QM9 and GEOM-Drugs show consistent improvements in stability and validity metrics while reducing computational cost by nearly half.

## Strengths

- **Novel and well-motivated problem identification.** The paper is the first to formally characterize the DC-structure of molecular distributions and connect it to the fragility of diffusion models in this domain. The analysis of how narrow peaks cause overshoot during reverse steps (Equation 6-7) is insightful and provides a clear mechanistic explanation for observed failures.

- **Strong empirical results across diverse backbones.** DIST consistently improves atom stability, molecule stability, and validity across three different backbone architectures (GNN-based equivariant, latent-space, Transformer-based) on two datasets. The improvements are substantial (e.g., molecule stability on QM9: EDM 82.0% → 89.9%, GeoLDM 89.4% → 93.4%) and the method sets new state-of-the-art results.

- **Theoretical grounding.** The paper provides formal definitions (Definition 3.1), a TV-contraction result (Corollary 3.1), and a selective reverse error bound (Proposition 3.1) that connect the DC-structure to the need for corrective sampling. This theoretical framework elevates the work beyond a purely empirical contribution.

- **Computational efficiency as a bonus.** DIST not only improves quality but also reduces inference timesteps by roughly half, which is a practical advantage for molecular generation where sampling cost matters.

## Weaknesses

### Major

- **The corrective sampling procedure is underspecified.** The paper describes DIST at a high level (pilot samples, batch construction, score evaluation, threshold filtering) but lacks crucial implementation details. What exactly is the "pilot score" \(s_j\)? How is it computed from the pilot inference? The paper mentions "round-trip residual, self-consistency, ensemble variance, or chemistry-based penalty" as possibilities but never specifies which is actually used. Without this, the method cannot be reproduced. The appendix reference (Appendix F) is stripped, so the reader cannot verify the implementation.

- **The theoretical results do not directly connect to the actual algorithm.** Corollary 3.1 and Proposition 3.1 are stated in terms of an "ideal reverse Markov kernel" \(K_{t \rightarrow 0}\) and a batch selection procedure based on scores \(s_j\). However, the paper never defines how the actual DIST procedure (pilot inference, thresholding) maps onto this theoretical framework. The gap between the abstract theory and the concrete algorithm is significant, making the theoretical claims feel disconnected from the empirical results.

- **Missing comparison to existing corrective/guidance methods.** The paper mentions in Appendix B (stripped) a comparison with corrective methods, but the main text does not discuss how DIST relates to or differs from existing approaches like classifier guidance, classifier-free guidance, or resampling techniques (e.g., from the image generation literature). Given that DIST is fundamentally a guidance/correction method, this omission weakens the positioning of the contribution.

### Minor

- **The efficiency analysis is incomplete.** Table 3 reports average timesteps but does not account for the cost of running pilot inferences. The pilot step itself requires running full reverse inference on a subset of samples, which adds overhead. The paper should report total computational cost (including pilot overhead) rather than just the cost of the main trajectory.

- **The ablation study is limited.** Table 4 varies pilot subset size but does not ablate other critical design choices: the choice of intermediate timestep \(t\), the threshold \(\tau\), the batch radius \(r\), or the perturbation intensity. The paper mentions these are in Appendix H (stripped), but the main text should include at least one additional ablation to demonstrate robustness.

- **The definition of DC-structure (Definition 3.1) is somewhat circular.** It defines the structure in terms of the distribution at noise level \(t\), but the key claim is that molecular data distributions inherently have this structure. The definition would be stronger if it were stated in terms of the clean data distribution \(p_0\) and then derived for \(p_t\) via the forward process.

### Trivial

- The paper uses "dense-concentrated" as a technical term, but "dense" and "concentrated" are used somewhat interchangeably throughout the text, which can be confusing.

## Nice-to-Haves

- A comparison with a simple baseline: randomly dropping and resampling a fraction of trajectories at intermediate timesteps. This would help isolate whether the benefit comes from the specific selection mechanism or simply from any form of trajectory correction.

- An analysis of which types of molecules (e.g., by size, by functional groups) benefit most from DIST, to provide deeper insight into when the DC-structure issue is most severe.

- A visualization of the corrected vs. uncorrected trajectories in a low-dimensional projection (e.g., PCA of molecular features) to empirically validate the claim that DIST realigns \(q_t\) toward \(p_t\).

## Novel Insights

The paper's core insight—that the narrow, densely packed peaks of molecular distributions cause diffusion models to overshoot valid regions during reverse inference, and that this can be mitigated by selective correction at intermediate timesteps—is genuinely novel and well-supported. The observation that this issue persists across diverse architectures (equivariant, latent-space, Transformer-based) is important: it suggests that architectural innovations alone cannot solve the fundamental distributional challenge, and that trajectory-level correction is necessary. The theoretical framing of the overshoot condition (Equation 7) as a function of peak width \(\sigma_*\) and separation \(\Delta\) provides a clean, quantitative explanation for why molecular generation is harder than image generation.

## Suggestions

1. **Specify the pilot score computation.** The paper must clearly state how \(s_j\) is computed from the pilot inference. Is it based on the final validity of the pilot molecules? The reconstruction error? The variance across ensemble members? This is essential for reproducibility.

2. **Include a computational cost breakdown.** Report the total number of neural network evaluations (including pilot runs) for DIST vs. baselines, not just the average timesteps. This will give a fair comparison of efficiency.

3. **Add an ablation on the intermediate timestep \(t\).** The choice of when to apply correction is critical. Show how performance varies with \(t\) (e.g., early vs. late correction) to validate the theoretical analysis that correction is most needed when peaks have merged but are still narrow.

4. **Clarify the relationship to existing guidance methods.** Even a brief discussion in the main text (not just the appendix) of how DIST differs from classifier guidance or resampling would help position the contribution.

## Score and Decision

The paper identifies a genuine and important problem, provides a clean theoretical analysis, and demonstrates strong empirical results across multiple backbones. The main weakness is the underspecification of the corrective sampling procedure, which prevents full evaluation of the method's soundness and reproducibility. However, the core ideas are clear and the empirical evidence is compelling. With the missing implementation details provided (presumably in the appendix), this would be a strong paper.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>