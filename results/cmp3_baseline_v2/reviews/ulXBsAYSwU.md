## Summary

MolMiner introduces a fragment-based, order-agnostic autoregressive transformer for molecular generation that supports conditional generation on up to twelve molecular properties simultaneously. The model incorporates dynamic 3D geometry via forcefield relaxation during generation, a symmetry-aware protocol for handling fragment attachments, and a GMM-based conditioning mechanism that allows users to specify any subset of target properties. The paper also proposes improved evaluation protocols including Wasserstein distance for distributional comparisons and calibration plots for conditional generation assessment.

## Strengths

- **Comprehensive multi-property conditioning:** Supporting simultaneous conditioning on twelve molecular properties is a significant practical advance. The GMM-based approach for completing partial conditioning vectors is well-motivated and enables flexible user control, which is directly relevant to real-world high-throughput screening pipelines.

- **Novel integration of capabilities:** The unification of dynamic 3D geometry, symmetry-aware fragment handling, order-agnostic generation, and multi-property conditioning within a single framework is genuinely novel. Each component addresses a known limitation in prior work, and their combination represents a meaningful step forward in controllable molecular design.

- **Principled evaluation methodology:** The introduction of Wasserstein distance for distributional comparisons and calibration plots for conditional generation provides more rigorous assessment than standard metrics alone. The calibration plots (Figure 2) offer clear, interpretable visualization of how well the model responds to conditioning across the full dynamic range of each property.

- **Well-motivated architectural choices:** The geometry-aware attention bias using Gaussian-decayed distance kernels is a clean way to incorporate 3D information without requiring explicit positional encodings. The focalized readout mechanism for aggregating context around attachment sites is sensible and well-explained.

## Weaknesses

### Major

- **Unconditional generation performance gap:** The model underperforms HierVAE on several key properties (molecular weight, TPSA, MR) by substantial margins (e.g., MolMinerD: 47 vs HierVAE: 15 for molWt Wasserstein distance). The authors acknowledge this but attribute it primarily to early termination bias. This is a significant limitation for a model that claims to advance the state of the art, and the explanation, while plausible, is not empirically validated. The paper would benefit from an ablation or analysis quantifying the termination bias and demonstrating that it is the primary cause.

- **Limited baseline comparisons:** The paper compares only against HierVAE for unconditional generation and explicitly excludes MARS and MoLeR. While the reasoning for excluding MARS is reasonable (different inference paradigm), the exclusion of MoLeR due to training difficulties is concerning. The authors should either (a) provide a more thorough attempt to get MoLeR working, (b) report results from the original MoLeR paper on comparable benchmarks, or (c) include additional baselines such as JTNN, G-SchNet, or diffusion-based models. The current comparison against a single baseline (HierVAE) is insufficient to establish the model's competitiveness.

- **Conditional generation evaluation lacks baselines:** The paper presents calibration plots for conditional generation but does not compare against any conditional generation baselines. Without comparisons to other conditional models (e.g., conditional VAEs, property-conditional diffusion models, or reinforcement learning-based approaches), it is difficult to assess whether the calibration quality represents a meaningful advance or merely a baseline level of performance. The claim that this is "the first model to support simultaneous conditioning across as many as twelve molecular properties" is a capability claim, not a performance claim, and the paper needs comparative evidence to demonstrate that the model does this well.

### Minor

- **Limited analysis of failure cases:** The calibration plots show clear systematic deviations for QED, molecular weight, and MR, but the paper provides only a brief hypothesis about early termination. A more detailed analysis of why certain properties are harder to control (e.g., correlation structure among properties, data distribution characteristics) would strengthen the paper.

- **No explicit validity metric:** The authors state they "omit validity, as our model enforces valence constraints during generation and consistently produces valid molecules." While this is reasonable, reporting the actual validity rate would be standard practice and would allow readers to verify this claim. Even with valence constraints, there can be edge cases.

- **Computational cost:** Training takes approximately 7 days on an RTX 3090 with 70GB RAM. While not prohibitive, this is a significant computational requirement that may limit reproducibility and adoption. The paper does not discuss whether smaller, more efficient variants are feasible.

### Trivial

- The paper states "to our knowledge, this is the first model to unify" several capabilities, but does not provide a systematic comparison table showing which prior models have which capabilities. Such a table would help readers quickly understand the novelty.

## Nice-to-Haves

- An analysis of how the model's performance scales with the number of conditioning properties (e.g., does calibration degrade as more properties are simultaneously conditioned?)
- A study of the model's behavior when conditioning on conflicting or impossible property combinations
- Examples of generated molecules at different conditioning values to provide qualitative intuition
- An investigation of whether the GMM-based conditioning completion introduces bias that affects downstream generation quality

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Add at least 2-3 additional baselines for unconditional generation (e.g., JTNN, G-SchNet, or a diffusion model) to strengthen the comparative evaluation
- Include a conditional generation baseline, even if simplified (e.g., a conditional VAE or a simple property-constrained sampling variant of HierVAE)
- Provide an empirical analysis of the termination bias hypothesis, including statistics on the distribution of generated molecule sizes vs. the training set
- Report validity rates explicitly, even if they are expected to be high
- Add a table comparing the capabilities of MolMiner against prior models (e.g., which support 3D geometry, symmetry handling, order-agnostic generation, multi-property conditioning)

## Score and Decision

The paper presents a well-motivated and technically sound framework that integrates several desirable capabilities for molecular generation. The multi-property conditioning and the evaluation methodology are genuine contributions. However, the limited baseline comparisons (only HierVAE for unconditional, no baselines for conditional) significantly weaken the empirical validation. The unconditional performance gap and the lack of conditional baselines make it difficult to assess whether the model represents a meaningful advance over existing approaches. The paper would benefit substantially from additional comparative experiments.

MY FINAL SCORE: 5.0</score>
MY FINAL DECISION: Reject</decision>