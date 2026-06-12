## Summary

This paper introduces Count Bridges, a stochastic bridge process on the integers that uses Poisson birth-death dynamics to provide closed-form conditionals for generative modeling of integer-valued count data. The framework is extended to handle deconvolution of aggregated measurements via an EM-style algorithm that treats unit-level counts as latent variables. The authors demonstrate state-of-the-art performance on synthetic integer benchmarks and two real-world biological applications: nucleotide-resolution bulk RNA-seq deconvolution and spatial transcriptomic deconvolution.

## Strengths

- **Novel and well-developed theoretical framework.** The Poisson birth-death bridge formulation (Prop. 3.1) with closed-form conditionals via Bessel-distributed slack variables is a non-trivial technical contribution. The derivation elegantly parallels the Gaussian bridge (Prop. 2.1), and the connection to Schrödinger bridges—showing that Count Bridges solve entropy-regularized OT with the KL-to-discrete-OT limit as κ→0—provides genuine theoretical insight.

- **Principled treatment of the distributional nature of the problem.** The paper correctly identifies that the discrete nature of count data necessitates a distributional loss (energy score) rather than point-estimate regression, and motivates this through Holderrieth et al. (2024) and the need to capture joint structure beyond cross-entropy. The comparison between cross-entropy and energy score (referenced in App. D.1) and the theoretical justification for distributional scoring rules (Gneiting & Raftery, 2007) is sound.

- **Strong and comprehensive experimental evaluation.** The paper evaluates across three synthetic tasks (8-Gaussians-to-2-Moons, low-rank mixtures, deconvolution of mixtures) and two real biological applications, consistently outperforming relevant baselines (CFM, DFM, Enformer, CIBERSORTx, MuSiC, STDeconvolve) across multiple metrics. The scaling experiment (Fig. 3) convincingly demonstrates CB's advantage in high-dimensional settings.

- **Practical biological impact.** The nucleotide-resolution modeling of scRNA-seq and the ability to deconvolve bulk RNA-seq into single-cell count profiles (rather than just cell-type proportions) represents a meaningful advance over existing approaches. The spatial transcriptomics application using MERFISH data with nuclear images as side information is well-designed and practically relevant.

## Weaknesses

### Fatal
None.

### Major

- **Fairness of some baseline comparisons.** For bulk RNA-seq deconvolution (Table 3), CB produces nucleotide-level counts then aggregates to gene level to compare against CIBERSORTx and MuSiC, which operate natively at gene resolution. While this is a reasonable evaluation strategy, the comparison conflates two different tasks—nucleotide-level generation versus gene-level proportion estimation. For spatial transcriptomics (Table 5), the only baseline for count profiles is the spot-mean, which is quite weak. A comparison against other generative baselines (e.g., a properly adapted DFM or VAE) would strengthen the claim.

- **EM/projection theoretical guarantees are acknowledged as weak.** The authors themselves note in the limitations that the projection step (Prop. 4.1) is a "first-order surrogate" lacking "serious theoretical support." The generalized KL projection in Prop. 4.1 is derived under unstated regularity conditions (deferred to App. B.1), and the EM convergence guarantees are not analyzed. While this is honestly noted, it leaves a significant theoretical gap in a core component of the method.

- **Limited analysis of computational cost and scalability.** The distributional loss requires m samples per training step, and the Bessel sampler is called at each reverse step during inference. The paper provides a custom CUDA kernel but does not report wall-clock training/inference times, GPU memory requirements, or a comparison of computational cost against baselines, making it difficult to assess practical scalability.

### Minor

- **Architecture details are sparse.** The PBMC model uses "residual multi-head attention blocks and a final softplus head," and the spatial model uses a UViT, but detailed architecture specifications, hyperparameter choices, and ablations are relegated to appendices that I cannot evaluate. The choice of λ₊, λ₋ and w(t) and their sensitivity is not discussed in the main text.

- **The synthetic bulk data generation for PBMC experiments may be overly clean.** The synthetic bulking procedure (summing held-out patients' cells) is well-controlled but may not fully capture the technical noise, composition shifts, and batch effects present in real bulk RNA-seq, potentially overstating the method's practical utility.

### Trivial
None.

## Nice-to-Haves

- An ablation studying the effect of the number of EM iterations and convergence behavior.
- A comparison of wall-clock training and inference cost between CB, DFM, and CFM.
- Analysis of how the choice of λ₊, λ₋ affects the Schrödinger bridge solution and generation quality.

## Novel Insights

The identification of Count Bridges as solutions to the static Schrödinger bridge problem on integers is a genuinely novel observation. The paper shows that the bridge parameter κ plays the same role as entropy regularization strength in Gaussian diffusion (σ→0 recovers quadratic OT for Gaussians, κ→0 recovers discrete OT with L1 cost), providing a unified view of interpolation between distributions across discrete and continuous settings. The demonstration that the slack variable concentrates near zero for large displacements, connecting the forward process to optimal transport, is a clean and insightful result that will be useful beyond this specific application.

## Suggestions

- Add a computational cost comparison table (wall-clock time, FLOPs, memory) for CB vs. DFM vs. CFM on the synthetic benchmarks.
- Include an ablation on the number of EM iterations for the deconvolution task to show convergence behavior.
- Strengthen the count profile comparison in Table 5 with at least one additional generative baseline beyond spot-mean.

## Score and Decision

The paper makes a genuine theoretical contribution—the Poisson birth-death bridge with closed-form conditionals and its connection to Schrödinger bridges—and backs it with comprehensive experiments on both synthetic and real biological data. The deconvolution framework addresses an important practical problem. While some baseline comparisons could be fairer and the EM theory is incomplete, these issues do not invalidate the core contributions. The paper represents a well-executed piece of work at the intersection of generative modeling and computational biology.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>