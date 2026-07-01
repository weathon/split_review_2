## Summary

TSPulse introduces a family of ultra-light pre-trained models (1M parameters) for time-series diagnostic tasks. It proposes a pre-training framework that combines masked reconstruction with explicit disentanglement across representation spaces (time vs. frequency) and abstraction levels (fine-grained vs. semantic), producing three complementary embedding views (temporal, spectral, semantic). The model also includes lightweight post-hoc fusers (MHT, TSLens) and a hybrid masking strategy. Experimental results on anomaly detection, classification, imputation, and similarity search show strong performance improvements over larger models, often with 10–100× fewer parameters and CPU-friendly deployment.

## Strengths

- **Compact and efficient design** – The 1M parameter model is drastically smaller than competitors like MOMENT (40M) and UniTS (10M+), while achieving competitive or better results across multiple tasks. This enables GPU-free deployment and near-instant CPU inference.
- **Novel disentanglement framework** – Explicitly learning separate temporal, spectral, and semantic embeddings within a unified pre-training objective is a clear advance over existing approaches that entangle these signals. The sensitivity analysis (Table 2) convincingly shows that each embedding type responds differently to perturbations, confirming the desired disentanglement.
- **Comprehensive evaluation** – The paper evaluates on four diagnostic tasks across 75+ datasets, including the TSB-AD leaderboard (anomaly detection), UEA (classification), LTSF (imputation), and custom similarity search benchmarks. Ablation studies isolate the contribution of each component.
- **Strong zero-shot transfer** – In anomaly detection, TSPulse (ZS) outperforms all trained models on TSB-AD; in imputation, zero-shot performance exceeds many fine-tuned baselines. This demonstrates genuine transferability without target-task training.

## Weaknesses

### Fatal

None.

### Major

1. **Misleading claim about imputation gains against statistical methods.** Figure 6 shows “Interpol” (likely linear interpolation) achieving a mean MSE of 0.039, while TSPulse (ZS) achieves 0.074. The paper states “Compared to statistical interpolation methods, TSPulse shows 50%+ gains,” which is contradicted by the reported numbers. This error undermines the credibility of the zero-shot imputation results. At best, TSPulse (ZS) is worse than a simple interpolation baseline; the claim should be clarified or corrected.

2. **Overstated zero-shot imputation performance in context.** The paper focuses on gains over MOMENT and UniTS (which are themselves weak at imputation), but does not frame its results against the simple and often effective baseline of interpolation. The strong claim “+50% on imputation” (abstract, intro) refers to zero-shot vs. MOMENT/UniTS, not vs. statistical methods—but the text conflates these comparisons. A clearer, more honest positioning is needed.

3. **Similarity search evaluation is synthetic and non-standard.** The retrieval setup generates queries by applying augmentations to indexed samples, so ground truth is trivially known. While this tests embedding robustness, it does not replace standard time-series retrieval benchmarks (e.g., UCR-based nearest neighbor tasks). The claim of “+25% on similarity search” should be validated on established protocols.

4. **Classification gains are modest and comparisons may not be fully fair.** TSPulse (FT) achieves 0.733 mean accuracy vs. VQShape (0.701), a 5% relative improvement. However, TSPulse uses task-specialized pre-training (reweighted loss objectives) and a dedicated fuser (TSLens), while baselines are general-purpose pre-trained models. The comparison against data-specific methods (TS2Vec, T-Rep) is more relevant, but the advantage over them is also small (5–12%). The paper claims “+5–16% improvements,” which reaches 16% only when compared to the weakest baseline (TCSS at 0.652).

5. **Missing important baselines in some tasks.** For imputation, the paper does not compare with recent large pre-trained models like TimesNet (though TimesNet is not pre-trained on 1B samples, it is a strong supervised baseline). For similarity search, only MOMENT and Chronos are compared; no lightweight embedding-based retrieval models are included. On anomaly detection, the TSB-AD leaderboard includes many methods, but the paper omits some recent deep AD models that might be more competitive.

### Minor

- The architecture description is detailed but somewhat complex; the diagram (Figure 2) is difficult to parse at the resolution provided.
- The hybrid masking strategy is presented as a key contribution, but the ablation shows a 79% drop without it—this is expected in the hybrid mask evaluation setting, but a separate evaluation on block-masking (Appendix) shows it still beats baselines. The paper could clarify that hybrid masking is mainly beneficial for realistic missing patterns.
- The TSLens module is described as a “post-hoc fuser,” but it is trained end-to-end with the decoder during fine-tuning, not truly post-hoc. The terminology is slightly misleading.
- Some formatting and typographical errors are present (e.g., “In-addition,” “Multi-Variate”), but these do not affect technical soundness.

### Trivial

- The paper uses both “0.074” and “0.07” for the same number in different locations.
- The reference to Appendix 18 should be Appendix A.18.

## Nice-to-Haves

- Include a standard time-series retrieval benchmark (e.g., UCR nearest neighbor classification) to validate similarity search claims more rigorously.
- Provide per-dataset results with standard deviations for classification and anomaly detection to assess statistical significance.
- Compare against lightweight non-pre-trained methods (e.g., simple CNN classifiers, statistical anomaly detectors) on the same footing.
- Report CPU inference latency for the full anomaly detection pipeline (including multi-head triangulation), not just similarity search.
- Clarify the relationship between register tokens and semantic embeddings—specifically, how many register tokens are used and whether they are shared across channels.

## Novel Insights

None beyond the paper’s own contributions: the joint disentanglement of temporal, spectral, and semantic embeddings in a single pre-trained model is the core insight. The sensitivity analysis (Table 2) provides useful empirical evidence that the three embedding types behave as intended.

## Suggestions

- Correct the imputation comparison: clearly state that TSPulse (ZS) underperforms simple interpolation but outperforms MOMENT and UniTS by wide margins. Reframe the “+50%” claim consistently.
- Add standard retrieval benchmarks (e.g., similarity search on UCR datasets with a held-out query set) to strengthen the similarity search evaluation.
- Include error bars or significance tests for the main results (especially classification and anomaly detection) to demonstrate that improvements are statistically reliable.
- Provide a table of per-dataset classification accuracies for all methods on the UEA archive to allow readers to judge consistency.

## Score and Decision

The paper’s core contribution—a compact, disentangled pre-training framework for time-series diagnostic tasks—is novel and well-motivated. The experimental scope is broad and the model is impressively efficient. However, the major weaknesses—particularly the inaccurate comparison against interpolation in imputation and the synthetic retrieval evaluation—significantly weaken the paper’s claims. These issues must be resolved for the paper to meet the acceptance bar.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>