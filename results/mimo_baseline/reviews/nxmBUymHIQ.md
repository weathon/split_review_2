## Summary
The paper introduces LoLoRA, a memory-efficient LoRA fine-tuning method that updates the adapter matrix A using local (gradient-free) learning rules—specifically Hebbian PCA (HPCA) or a local autoencoder loss—during the forward pass, while still training B via backpropagation. The authors provide theoretical analysis showing that under a random linear regression model, the optimal A spans the dominant eigensubspace of the input covariance matrix, and they validate this across NLU (GLUE/RoBERTa), mathematical reasoning (GSM8K/LLaMA-3.1), and multimodal (LLaVA) tasks.

## Strengths
- **Clean theoretical contribution**: Theorem 4.4 provides a precise characterization of the optimal A matrix (arbitrary nonsingular transformation of the top-r eigenvectors of the input covariance), and Theorem 4.5 shows the asymmetry between A and B initialization. This theoretically grounds the EVA initialization of Paischer et al. (2024) and extends it to a broader class of matrices. The autoencoder variant (Theorem 4.6) adds further depth.
- **Comprehensive experimental evaluation**: The method is tested across three different model families (RoBERTa-large, LLaMA-3.1-8B, LLaVA-v1.5-7B), covering NLU, mathematical reasoning, and multimodal tasks, with multiple seeds and thorough ablations of initialization strategies (Table 5) and local update rules (Table 6).
- **Practical simplicity and clean algorithmic presentation**: Algorithm 1 is straightforward, the method integrates easily into existing LoRA pipelines, and the paper clearly delineates the design space (Figure 1) between LoRA, LoRA-FA, and LoLoRA.

## Weaknesses
### Fatal
None.

### Major
- **Marginal empirical gains over the closest baseline**: Across all experiments, LoLoRA HPCA does not clearly outperform LoRA-FA with EVA initialization. On MetaMathQA (Table 3), both achieve exactly 82.9% ± 0.005 with identical 26 GB memory. On the LLaVA multimodal task (Table 4), LoLoRA HPCA actually performs slightly *worse* than LoRA-FA (EVA) on both perplexity (2.93 vs 2.92) and loss (1.075 vs 1.070). On the TinyLlama ablations (Table 6), LoLoRA HPCA at r=8 achieves 2.535 ± 0.011, essentially indistinguishable from LoRA-FA (EVA) at 2.536 ± 0.010. The paper's conclusion that "HPCA consistently outperforms standard LoRA-FA" is only true when comparing against uniformly-initialized LoRA-FA, not against EVA-initialized LoRA-FA.
- **Memory savings are modest and partially overstated**: The "up to 20% less GPU memory" claim on GLUE (Appendix D, not shown) and 13% on math reasoning are relative to standard LoRA. Since LoRA-FA already achieves the same memory reduction by freezing A, the incremental memory benefit of LoLoRA over LoRA-FA is negligible—LoLoRA actually introduces a small extra optimizer state for A's local updates. The fundamental memory bottleneck (storing B's activations) remains the same.
- **Strong theoretical assumptions limit practical relevance**: Assumption 4.1 posits that ΔW₀ entries are i.i.d. Gaussian, which is far from realistic—fine-tuning weight updates are highly structured and task-dependent. While the theory provides useful intuition, the tightness of the random regression model to actual LLM fine-tuning is not established, making the "optimal" claims aspirational rather than practically actionable.

### Minor
- **No clear advantage of online adaptation over one-shot EVA**: The primary stated advantage of LoLoRA over LoRA-FA (EVA) is that it adapts A online without needing a calibration pass. However, EVA's calibration is just a single forward pass over a small dataset, and the ablation results suggest the online HPCA converges to essentially the same subspace. The paper does not demonstrate scenarios where distribution shift during training would cause EVA initialization to degrade while LoLoRA adapts.
- **Inconsistent reporting of computational overhead**: HPCA updates add forward-pass computation and a local optimizer step per layer, but run-time comparisons are only provided for the LLaVA experiment (Table 4) and the methodology is not compared for GLUE/GSM8K. The practical time cost of the method is unclear.

### Trivial
- Some variable notation inconsistencies (e.g., A defined as R^{r×n} in Definition 3.1 context but R^{r×m} in the abstract).

## Nice-to-Haves
- A direct comparison on tasks or settings where input distribution shifts significantly during training would strengthen the case for online adaptation over one-shot EVA initialization.
- Wall-clock training time and throughput comparisons across all experimental settings.
- Analysis of how LoLoRA performs when the effective dimensionality of input representations varies significantly across layers, which is where the theoretical prediction about unbalanced spectra should yield larger differences.

## Novel Insights
The theoretical result (Theorem 4.4) establishing that optimal A under random regression is any nonsingular transformation of the top eigenvectors of the input covariance provides a clean information-theoretic explanation for why EVA initialization works and connects it to classical PCA theory. The asymmetry result (Theorem 4.5, any full-rank B is equivalent) is a useful insight about the distinct roles of A and B. However, the practical implications of these results are limited by the strong assumptions, and the paper's own experiments suggest that the theoretically optimal initialization is already achieved by existing methods (EVA).

## Suggestions
- Present LoLoRA's value proposition more honestly relative to LoRA-FA (EVA): the main advantage is not superior performance but rather eliminating the need for a separate PCA calibration step, making it a simpler single-pass method.
- Investigate settings where input distributions shift during training (e.g., curriculum learning, domain shift during multi-task fine-tuning) to demonstrate a clear advantage of online adaptation over static initialization.
- Report wall-clock time overhead of HPCA local updates consistently across all experiments to allow practitioners to assess the compute-memory tradeoff.

## Score and Decision
The paper presents a clean theoretical framework and a simple practical method, but the empirical results fail to demonstrate meaningful improvements over the existing closest baseline (LoRA-FA with EVA initialization). The theoretical contribution has intellectual merit but is predicated on assumptions (i.i.d. Gaussian targets) that are difficult to connect to real LLM fine-tuning. The memory savings are real but modest and mostly inherited from the LoRA-FA baseline. Overall, this is a competent paper with a nice theory section, but the practical contribution is insufficient for a top venue.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: Reject