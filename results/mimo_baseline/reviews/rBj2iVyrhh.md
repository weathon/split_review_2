## Summary

This paper proposes Classifier-Constrained Alternating Training (CCAT), a two-stage framework for mitigating modality imbalance in multimodal learning. Drawing an analogy to class imbalance, the method pretrains an unbiased shared classifier with contribution-aware regularization, then freezes it during modality-alternating training while using modality-specific LoRA adapters and sample-level secondary updates for severely imbalanced samples. Experiments on three benchmarks (CREMA-D, KS, MVSA) demonstrate consistent improvements over existing methods.

## Strengths

- **Well-motivated problem identification with clear experimental evidence.** The paper identifies that existing alternating training methods (e.g., MLA) still suffer from entrenched classifier bias toward dominant modalities, supported by Figure 1 showing persistent contribution disparities even with decoupled encoders. This is a genuine and practically important gap in the literature.

- **Clean, modular framework design with thorough ablation.** The two-stage approach (pretrain classifier → freeze with LoRA + alternating training + secondary updates) is well-structured. Table 2's ablation systematically validates each component across three datasets, showing that classifier freezing alone accounts for the largest single improvement (e.g., 82.80% → 85.89% on CREMA-D), confirming the core hypothesis.

- **Consistent and substantial empirical gains.** The method achieves SOTA on most metrics: +1.35% on CREMA-D, +6.76% on KS, and +1.92% on MVSA over best existing baselines. Notably, weak modality improvements are large (e.g., Video on CREMA-D: 68.01% → 73.79%), directly validating the paper's core claim about liberating suppressed modalities.

## Weaknesses

### Fatal
None.

### Major

- **Overstated theoretical contribution.** The paper claims to establish a "unified theoretical framework" and "theoretical isomorphism" between class and modality imbalance (Section 3.1). However, the analysis amounts to an informal analogy: Eq. (3) assumes γ₁ ≫ γ₂ (the extreme case) without bounds or formal characterization of when this approximation holds. This is better characterized as motivation than theory. The contribution labeled (i) in the introduction — "providing a new theoretical framework" — is not substantiated at the level expected.

- **Significant dataset-specific hyperparameter sensitivity.** The optimal LoRA rank r and threshold β vary substantially across datasets: (r=2, β=0.15) for CREMA-D, (r=2, β=0.30) for KS, (r=8, β=0.05) for MVSA. This suggests the method's effectiveness is contingent on careful per-dataset tuning, which limits practical applicability. No analysis is provided on robustness to suboptimal choices or guidance for selecting these in new settings.

- **Unclear computation of sample-level contribution scores during alternating training.** In Algorithm 1, line 10, contribution scores {c_i^m} are estimated after each epoch of alternating training. The paper states that "the computation of c follows the same decision-level fusion used in the inference stage," but the details of how this works when only one modality's encoder is actively updating at any given time, and how the fused features f_i are constructed from potentially stale representations, are not clearly specified.

### Minor

- **Limited experimental scope.** Only two-modality benchmarks are tested. The paper acknowledges this in future work but does not discuss how the framework's assumptions (e.g., binary modality contribution vector in Eq. 6–7) would generalize to three or more modalities.

- **Missing computational cost analysis.** The method introduces an additional pretraining stage plus secondary per-sample updates. No comparison of wall-clock training time or FLOPs is provided, making it difficult to assess the practical overhead relative to methods like MLA.

- **No statistical significance testing.** Results are reported as averages over three random seeds without standard deviations or confidence intervals. Given that some improvements (e.g., +1.35% on CREMA-D) are modest, variance information would strengthen the claims.

### Trivial
None.

## Nice-to-Haves

- A sensitivity analysis showing how performance varies with β and r jointly, rather than in separate grid searches, would help practitioners understand the tuning landscape.
- Reporting standard deviations across the three seeds would make the results more convincing.
- Including a training time comparison would contextualize the practical value of the approach.

## Novel Insights

The key novel insight is that alternating training's limitation is not merely encoder-level gradient interference but rather structural bias in the shared classifier that becomes entrenched early and persists even after encoder decoupling. The analogy to class imbalance — where early-dominance creates path-dependent bias — provides a useful conceptual lens. While the analogy is not formally proven, it productively motivates a concrete solution (freezing the classifier) that empirically works. The observation that a frozen, pre-biased classifier with lightweight LoRA adapters can outperform a jointly optimized one is practically valuable and somewhat counterintuitive.

## Suggestions

- Strengthen the theoretical section by either (a) providing formal convergence analysis showing when the modality-class imbalance analogy holds, or (b) downgrading the language from "theoretical framework" to "conceptual analogy with empirical support."
- Add robustness experiments: show performance degradation curves as β and r deviate from optimal values, and provide practical selection heuristics.
- Provide computational cost comparisons (wall-clock time, GPU memory) in the main paper.
- Include variance estimates (standard deviation across seeds) in all result tables.

## Score and Decision

The paper presents a well-designed and empirically validated method for an important problem. The framework is clean, the ablation is thorough, and the results are consistently positive. However, the theoretical contribution is overstated, and the significant hyperparameter sensitivity raises concerns about robustness and practical generalization. These issues prevent me from rating it higher, but the solid empirical contribution and clear problem motivation place it above a reject.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>