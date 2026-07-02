## Summary

The paper proposes PI-CCA (Prompt-Invariant CCA Certificates), a replay-free continual learning framework for vision-language models that preserves cross-modal alignment by directly maintaining a compact certificate of the top-\(k\) canonical correlations and subspaces of the whitened image-text covariance. During adaptation on new tasks, the method enforces spectral and subspace-angle consistency with this certificate using only mini-batch statistics, and induces prompt robustness by averaging over prompt perturbations. Across multiple benchmarks (MTIL, X-TAIL, VLCL, ConStruct-VL), PI-CCA achieves state-of-the-art performance among replay-free methods and provides analyses linking alignment-geometry stability to retention.

## Strengths

- **Principled conceptual reframing.** The paper recasts forgetting in VL-CL as drift in alignment geometry rather than mismatches in proxy quantities (logits, similarities, parameters). This perspective is novel and leads to a more direct preservation of the cross-modal structure that underlies zero-shot generalization.
- **Strong empirical results.** PI-CCA consistently outperforms all replay-free baselines across four diverse VL-CL tracks, often by clear margins, and even exceeds a synthetic-replay method (GIFT) without storing or generating data.
- **Comprehensive analysis.** The paper provides thorough ablations (Table 3), a certificate-capacity Pareto analysis (Figure 2), geometry-to-performance correlation evidence (Figure 3), prompt invariance stress tests (Figure 4), and task-order sensitivity (Figure 5). These analyses convincingly demonstrate that the method’s effectiveness stems from preserving the CCA invariants, not from incidental regularization.
- **Replay-free and constant memory.** The method uses only a fixed-size certificate (sketched projectors) and streaming covariances, making it practical for privacy-constrained or memory-limited deployment. It is also compatible with parameter-efficient adaptation like LoRA.
- **Prompt invariance component.** The explicit prompt-invariance loss (\(\mathcal{L}_{\text{pi}}\)) is well-motivated and shown to flatten performance degradation across both ID and OOD template perturbations, an important robustness property that prior methods lack.

## Weaknesses

### Fatal

None.

### Major

None.

### Minor

- **Suspiciously perfect correlations in Fig 3.** The reported Pearson and Spearman correlations of 1.00 and 0.99 between geometry drift and performance drop are implausibly high for real data. While the overall trend is convincing, the exact values suggest either a very small number of samples, deterministic relationships due to shared computation, or rounding. The paper should clarify the source of this near-perfect linearity (e.g., by showing bootstrap intervals or noting that each point corresponds to a distinct hyperparameter setting that directly affects both drift and performance in a closed-form way). This does **not** invalidate the core claim, but the reporting should be more careful.

- **Hyperparameter sensitivity.** The method introduces several hyperparameters (\(\lambda_1,\lambda_2,\lambda_3,\eta,k,h,\alpha,\beta,J,\xi,M\)). Although the appendix (partially available) and the Pareto analysis show robustness, the number of tunable components may make the method harder to apply in practice without a validation set. The paper does not provide a clear default recipe or ablation on hyperparameter ranges beyond the knee configuration.

- **Computational overhead not fully quantified.** The paper reports peak memory and step time for the Pareto analysis, but does not compare the computational cost of PI-CCA (including per-step SVD of the whitened cross-covariance) against simpler baselines (e.g., ZSCL) in terms of absolute wall-clock time or FLOPs. The sketch reduces cost but the overhead relative to a standard InfoNCE loss could be substantial.

### Trivial

- The correlation analysis in Figure 3 seems to use the same data as the hyperparameter sweep; the drift measures may be naturally linked to the performance drop because both are affected similarly by the underlying hyperparameter changes. This is not a flaw but the interpretation as a causal “prediction” should be slightly tempered.

- The paper could explicitly state that the certificate refresh (Eq. 13) uses a slow EMA that effectively prevents the certificate from drifting too fast, but this is already clear.

## Nice-to-Haves

- Extend the certificate to also track the canonical correlation *structure* for new tasks (e.g., by maintaining multiple certificates or a mixture), which could further improve retention in longer task sequences.
- Investigate whether the CCA certificate can be updated with less than per-step SVD (e.g., via streaming SVD updates) to reduce computational overhead further.
- Provide a practical rule-of-thumb for setting \(k\) and \(h\) based on embedding dimension and expected task diversity.

## Novel Insights

The paper demonstrates that directly constraining the canonical correlation spectrum and subspaces of the cross-modal alignment is a significantly more effective regularizer for continual vision-language learning than matching proxy signals (logits, similarities, parameters). This provides a clear mechanism for forgetting (drift in alignment geometry) and explains why previous methods that act on surrogate objectives still exhibit slow degradation. The insight that preservation of the “alignment skeleton” via a compact, prompt-invariant certificate can be achieved without replay, generators, or task-specific metadata is both new and practically valuable.

## Suggestions

- **Clarify the near-perfect correlation values** in Figure 3 by reporting confidence intervals (e.g., bootstrapped Pearson/Spearman) or explaining that the points are not independent samples. A simple note that the drift and performance drop are computed from the same hyperparameter settings and thus share variance would be sufficient.
- **Provide a computational overhead comparison** against a baseline (e.g., ZSCL or Mod-X) in terms of per-step wall-clock time and GPU memory for a fixed batch size and embedding dimension, to give practitioners a clearer picture of the trade-off.
- **Include a simple default configuration** (e.g., “for new datasets, start with \(k=64, h=256, \lambda_1=\lambda_2=1.0, \lambda_3=0.2, M=4\)”) and show that it works reasonably without tuning, to lower the adoption barrier.

## Score and Decision

The paper makes a strong conceptual and empirical contribution to continual multimodal learning. The method is novel, principled, and convincingly demonstrates state-of-the-art results across multiple benchmarks with thorough analysis. The identified weaknesses are minor and do not undermine the core contributions. I recommend acceptance.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>