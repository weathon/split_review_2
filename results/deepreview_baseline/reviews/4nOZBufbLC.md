## Summary

This paper introduces Count Bridges, a generative framework for integer-valued count data based on Poisson birth-death processes that provides a tractable, discrete analogue of diffusion/flow matching models. The authors derive closed-form conditional bridge kernels, develop a distributional training loss using energy scoring rules, and extend the framework to deconvolution settings where only aggregated counts are observed via an EM-style procedure with projection-guided sampling. The method is evaluated on synthetic benchmarks (outperforming continuous and discrete flow matching baselines) and two real biological applications: nucleotide-resolution single-cell RNA-seq modeling with bulk deconvolution, and reference-free spatial transcriptomic deconvolution.

## Strengths

- **Principled discrete-native formulation**: The Poisson birth-death bridge provides an exact, tractable stochastic process on ℤ^d with closed-form conditionals (Proposition 3.1), satisfying the bridge consistency and projective posterior properties required for diffusion-style training and sampling. This is a genuine theoretical contribution that fills a gap between categorical discrete diffusion and continuous diffusion models.

- **Unified treatment of generation and deconvolution**: The paper presents a coherent framework that handles both direct count generation and deconvolution from aggregated observations within the same mathematical structure, using an EM approach with projection-guided sampling. This is novel and practically relevant for biological applications where aggregated measurements are common.

- **Strong empirical results on real biological tasks**: The method demonstrates meaningful improvements over strong baselines on nucleotide-level bulk RNA-seq deconvolution (Table 3: JSD 0.113 vs 0.194 for CIBERSORTx) and spatial transcriptomic deconvolution (Table 4: JSD 0.231 vs 0.288 for STDeconvolve), with the additional capability of producing full count profiles rather than just cell-type proportions.

## Weaknesses

### Fatal
None.

### Major

- **Limited theoretical justification for the projection-guided EM procedure**: The authors acknowledge that the projection step "lacks serious theoretical support" (Section 7), and Proposition 4.1 provides only a first-order approximation under unspecified regularity conditions. The EM-style training (Algorithm 4) uses approximate samples from the aggregate-conditional distribution without convergence guarantees. This is a significant gap for a core methodological contribution—the deconvolution framework is central to the paper's claimed contributions but rests on heuristic approximations.

- **Missing critical experimental details and ablations**: The nucleotide-resolution experiment (Section 6.2) is described at a high level without sufficient detail to assess reproducibility. Key architectural choices (e.g., "residual multi-head attention blocks"), training hyperparameters, and the exact form of the learned projection module Π_ψ are not specified. The ablation of the projection module (trained on only 10% of examples) is mentioned but not systematically evaluated—how sensitive are results to this fraction? The paper would benefit from ablations showing the contribution of each component (distributional loss vs cross-entropy, projection module vs simple rescaling, EM training vs direct supervision).

- **Incomplete comparison to relevant baselines**: For the spatial transcriptomic deconvolution task, the paper only compares to STDeconvolve (reference-free) but acknowledges that reference-based methods like cell2location and RCTD exist. While the authors note these require external references, a comparison would contextualize performance. More importantly, the paper does not compare against a simple baseline of training a standard count model (e.g., Poisson GLM or VAE) on the aggregate data, which would help isolate the benefit of the bridge formulation. The "spot mean" baseline in Table 5 is reasonable but weak.

### Minor

- **The synthetic benchmark comparisons could be more rigorous**: The paper compares against CFM and DFM but does not include Blackout Diffusion (the only existing count-specific method) in the main comparisons. The authors mention Blackout Diffusion is a special case of their framework, but empirical comparison would strengthen the case for Count Bridges.

- **Scalability claims are partially supported**: Figure 3 shows CB maintains low W1 as dimension increases, but the experiment uses a low-rank structure (rank 3) which may favor the method. The paper does not explore settings where the intrinsic dimensionality is high relative to ambient dimension.

- **The connection to Schrödinger bridges and optimal transport is interesting but not leveraged**: The paper shows Count Bridges solve an entropy-regularized OT problem (Section 3.1) but does not use this insight to provide guarantees on sample quality or convergence rates.

### Trivial
- The paper uses "Count Bridges" and "CB" interchangeably but the method name appears inconsistently in figures (e.g., "DCB" in Figure 2 caption vs "CB" in text).

## Nice-to-Haves

- A systematic ablation study showing the contribution of: (a) the distributional energy score vs cross-entropy loss, (b) the learned projection module vs simple rescaling, (c) the EM training procedure vs direct supervision when unit-level data is available.
- Comparison to a simple Poisson VAE or count-based normalizing flow baseline on the synthetic tasks.
- Theoretical analysis of the convergence properties of the projection-guided EM procedure, perhaps under a simplified setting.
- Analysis of computational cost: how does the Bessel sampler (CUDA kernel) scale with dimension and count magnitudes?

## Novel Insights

Beyond the paper's own contributions, the key insight is that the Poisson birth-death bridge provides a natural discrete analogue of Gaussian diffusion that preserves ordinal structure while enabling closed-form conditionals. The connection to entropy-regularized optimal transport (with κ controlling regularization strength, analogous to σ in Gaussian bridges) is elegant and suggests that Count Bridges could serve as a building block for more complex discrete generative models. The observation that the slack variable M_t concentrates near zero for large endpoint gaps (Figure 1) provides intuition for why the method works: large jumps are essentially deterministic, while small jumps benefit from the stochastic bridge structure.

## Suggestions

1. Provide a more rigorous theoretical analysis of the projection-guided EM procedure, even if only for simplified settings (e.g., one-dimensional case, or under asymptotic regimes). At minimum, characterize the bias introduced by the first-order projection approximation.

2. Add systematic ablations for the key design choices: distributional loss vs cross-entropy, learned projection vs simple rescaling, and the fraction of training examples with aggregate conditioning.

3. Include Blackout Diffusion as a baseline in synthetic experiments to directly compare against the only existing count-specific generative model.

4. Provide complete experimental details (architecture, hyperparameters, training compute) for the biological applications to ensure reproducibility.

5. Consider adding a simple baseline for the spatial deconvolution task: train a Poisson GLM or VAE on the aggregate data alone, to isolate the benefit of the bridge formulation over standard count models.

## Score and Decision

The paper presents a novel and principled framework for generative modeling of integer-valued data with a clean theoretical foundation. The biological applications are compelling and demonstrate practical value. However, the core deconvolution methodology—which is central to the paper's claimed contributions—relies on heuristic approximations without adequate theoretical support or systematic empirical validation. The missing ablations and experimental details further weaken the empirical contribution. The paper would benefit from additional work to substantiate the deconvolution framework before acceptance at a top venue.

MY FINAL SCORE: 6.0score

MY FINAL DECISION: Borderline Accept