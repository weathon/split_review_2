## Summary
This paper proposes Pi-CCA, a replay-free continual learning method for vision-language models that preserves cross-modal alignment geometry by storing a compact certificate of top-\(k\) canonical correlations and sketched canonical subspaces. During adaptation on new tasks, the model enforces spectral and subspace consistency with this certificate using only mini-batch statistics, and incorporates prompt-invariance via projector averaging over prompt perturbations. Experiments on four VL-CL benchmarks (MTIL, X-TAIL, VLCL, ConStruct-VL) show state-of-the-art performance among replay-free methods, and extensive analyses connect alignment-geometry stability to downstream retention.

## Strengths
- **Novel conceptual framing**: Recasting catastrophic forgetting in continual multimodal learning as drift of the canonical correlation geometry (spectrum and subspaces) rather than matching proxy signals provides a principled and direct route to preserving zero-shot and retrieval capabilities.
- **Strong empirical results**: Pi-CCA achieves top performance among replay-free methods on all four standard benchmarks, and even surpasses a synthetic-replay baseline (GIFT) on retrieval and structured-concept tasks, without storing or generating any past data.
- **Thorough analysis and validation**: The paper includes systematic ablations, certificate capacity Pareto studies, geometry–performance correlation plots, prompt-invariance stress tests, and task-order sensitivity experiments, all of which support the method’s design choices and robustness.
- **Constant memory and replay-free**: The certificate is compact (\(O(hk)\)) and independent of dataset size, the approach requires no data storage or generator, and it is compatible with parameter-efficient adaptation (LoRA), making it practical for privacy- and budget-constrained deployment.

## Weaknesses
### Fatal
None.

### Major
None.

### Minor
- **Near-perfect correlation in Figure 3**: The Pearson/Spearman correlations (0.99–1.00) between geometry drifts and performance drops are extremely high, which may partly reflect that the drifts are directly minimized by the losses in the same runs. While the evidence is valid, the strength of the correlation could be inflated by the experimental design; a cleaner demonstration would measure drift on a held-out metric not directly optimized.
- **Hyperparameter load**: The combined loss includes four terms (\(\mathcal{L}_{\text{spec}}, \mathcal{L}_{\text{sub}}, \mathcal{L}_{\text{pi}}, \mathcal{L}_{\text{task}}\)) with coefficients \(\lambda_{1:3}\), \(\eta\), \(\xi\), along with EMA rates \(\alpha, \beta\), sketch dimensions \(k, h\), and multiple perturbation parameters. Although the paper reports sensitivity in the appendix, the number of knobs may hinder practical adoption without clear guidance on default values or a tuning strategy.
- **Limited task horizon**: Experiments span 7–11 tasks; it remains unclear how the EMA-based covariance estimation and slow certificate update behave over much longer sequences (e.g., 100+ tasks) where cumulative drift or estimation error could grow.
- **Computational overhead of prompt invariance**: The prompt-invariance loss requires computing \(M\) additional mini-batch SVDs per step (default \(M=4\)). While the Pareto analysis shows overall efficiency is acceptable, the incremental cost of this component is not isolated.

### Trivial
- The notation in Section 3.1 is dense and some symbols (e.g., \(R_v^\perp, R_t^\perp\) in the figure) are introduced but not explicitly used in the main loss derivations; a short recap would improve readability.

## Nice-to-Haves
- A study on longer task sequences (e.g., 20–50 domains) to validate the streaming estimation and certificate refresh over extended continual learning.
- A breakdown of per-component computational cost (e.g., wall-clock of \(\mathcal{L}_{\text{spec}}\) vs. \(\mathcal{L}_{\text{pi}}\)) to help practitioners assess trade-offs.
- Additional comparisons with very recent (2025) replay-free VL-CL methods that may have appeared after the submission deadline.

## Novel Insights
None beyond the paper’s own contributions. The key insight—that preserving the canonical correlation spectrum and subspaces of the whitened cross-covariance is a more direct and effective invariant for continual multimodal learning than proxy signals—is well articulated and convincingly supported.

## Suggestions
- Discuss potential failure cases when the approximation quality of the EMA covariances degrades under very long task horizons, and suggest adaptive mechanisms (e.g., resetting or reinitialization).
- Provide a simple hyperparameter selection rule (e.g., fix \(k=64, h=256, \lambda_1=\lambda_2=1.0, \lambda_3=0.2, \alpha=0.001, \beta=0.1\)) that works across all benchmarks to lower the barrier for reproduction.
- Clarify in the main text how the “geometry drift” values in Figure 3 are computed (e.g., on which data split) to alleviate concerns about potential circularity.

## Score and Decision
**Score**: 8  
**Decision**: Accept

The paper presents a conceptually novel, principled approach to replay-free continual learning for vision-language models, supported by extensive experimental validation and analysis. It directly addresses the core problem of alignment-geometry drift, achieves state-of-the-art results on multiple benchmarks, and offers practical benefits (constant memory, no data storage). The weaknesses are minor and do not undermine the paper’s contributions.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>