## Summary
This paper presents a system for language-based audio retrieval built on a dual-encoder architecture enhanced with soft-label distillation from an ensemble of teachers, LLM-driven caption augmentation (back-translation and caption mixing), and cluster-guided auxiliary classification. The authors conduct experiments on the CLOTHO dataset using three audio backbones (PaSST, EAT, BEATs), report their best single model achieving mAP@16 of 46.6, and a weighted ensemble reaching 48.8 on the development test split, with an evaluation set score of 0.421 mAP@16.

## Strengths
- **Comprehensive ablation structure**: The paper systematically ablates distillation, augmentation, and clustering across multiple audio backbones (Table 1, Table 2), allowing the reader to isolate the contribution of each component.
- **Practical ensemble strategy**: The weighted ensemble approach combining multiple system variants and backbones (Table 3) is well-motivated and yields a clear performance gain (mAP@16 48.8 vs. best single model 46.6), demonstrating complementarity among the trained models.
- **Reproducible augmentation pipeline**: The LLM-based back-translation and caption mixing for mixed audio are described with sufficient specificity to be replicated, and the methods (back-translation via Sennrich et al., LLM mix via Wu et al.) are grounded in prior work.
- **Addressing an important problem**: The paper tackles the real issue of non-binary audio-text correspondences in existing retrieval datasets, which is a valid and under-explored challenge.

## Weaknesses
### Fatal
None.

### Major
- **Cluster-guided classification yields negligible or negative gains**: In Table 2, comparing SID 3 (distill + aug, no cluster) to SID 4 (cluster with finetuned embeddings) and SID 5 (cluster with BERTopic), the mAP@16 scores are nearly identical across all backbones (e.g., PaSST: 46.41 → 46.39 → 46.50; EAT: 46.05 → 45.34 → 45.34). The differences are within noise range, and for EAT and BEATs the cluster variants are *worse* than SID 3. The paper acknowledges "mixed gains" but does not squarely address whether the auxiliary classification adds any value given the added complexity and hyperparameter (λ₂) tuning required. The main claim that clustering "contributed to additional performance gains" (Conclusion) is not supported by the data.
- **Distillation and augmentation results are not clearly separated**: Comparing SID 1 (base) to SID 2 (distill only) shows a strong gain (e.g., PaSST mAP@16: 42.08 → 46.62). However, SID 3 (distill + aug) shows no further improvement over SID 2 (PaSST: 46.62 → 46.41; EAT: 45.35 → 46.05; BEATs: 43.89 → 44.66). The paper attributes the gain to distillation and augmentation collectively, but the data suggest the augmentation provides marginal to zero benefit on top of distillation, and may even hurt PaSST. The claim that augmentation "enhance[s] model performance" is overstated.
- **Missing statistical significance or variance reporting**: All results in Table 2 are reported as point estimates without error bars, confidence intervals, or multiple seeds. Given that the differences between many configurations (e.g., SID 3 vs. 4 vs. 5) are extremely small (≤0.2 mAP@10 or mAP@16), it is impossible to assess whether these differences are meaningful or merely noise. Standard practice for retrieval benchmarks includes at least 3 runs with mean and std.

### Minor
- **Limited architectural novelty**: The core contributions (distillation loss, LLM augmentation, clustering-based auxiliary loss) are all adapted from existing work: the distillation follows Primus et al. (DCASE 2024 Task 8), LLM augmentation follows GPT-4o usage (Hurst et al., 2024) and Wu et al. (2024), and the clustering uses BERTopic (Grootendorst, 2022). The novelty lies in their combination for audio retrieval, which is modest but acceptable for a systems paper.
- **Hyperparameter λ₂ fixed without sensitivity analysis**: The auxiliary classification weight λ₂ = 0.05 is fixed across all experiments without any ablation on this value. Given that the cluster loss provides essentially no gain, one might suspect the weighting is suboptimal or that any positive effect is washed out; a sweep would be informative.
- **Table formatting**: Table 3 (ensemble coefficients) is difficult to parse; the column headers are confusing (SID 2 and 3 share a header column, SID 4 and 5 share another). The table would benefit from clear grouping or sub-headers.

### Trivial
- The figure caption in the PDF is repeated twice (once in the figure alt-text and once as normal text).
- The paper states "Limitations include reliance on proprietary LLMs" but the LLM augmentation is not a core claimed contribution that invalidates the results; it is a practical limitation.

## Nice-to-Haves
- Ablation on the number of clusters used for classification to see if the null result is due to granularity.
- Comparison with an alternative, non-clustering-based auxiliary task (e.g., caption classification by random partitioning) to test whether the topic-based clustering is specifically beneficial.
- Evaluation on a second audio retrieval dataset (e.g., AudioCaps) to test generalizability beyond CLOTHO.

## Novel Insights
None beyond the paper's own contributions. The paper is primarily an engineering combination of known techniques applied to audio retrieval. The main takeaway—that soft-label distillation from an ensemble provides the dominant gain, while LLM augmentation and cluster guidance add little—is useful for practitioners, but the paper itself does not highlight this insight.

## Suggestions
- Explicitly discuss the near-zero contribution of the cluster-guided classification and LLM augmentation over distillation alone, and frame the paper's contribution more honestly around the distillation ensemble strategy, which is the only component that clearly works.
- Report results from at least 3 random seeds with mean and standard deviation for all key configurations to establish significance of the small differences.
- Remove or demote the "cluster-guided" claim from the abstract and conclusion unless new evidence (e.g., on high-ambiguity subsets, as hinted in the abstract) convincingly shows a regime where it matters. The abstract states "ablations indicate consistent improvements under high correspondence ambiguity," but no such subset analysis is presented in the main results.

## Score and Decision
**Score**: 4.5

**Rationale**: The paper addresses a relevant problem and provides a reproducible system, but its core claims are not well supported: the cluster-guided and augmentation components show negligible to no improvement over the distillation baseline, and the lack of statistical significance reporting makes the small observed differences uninterpretable. The best contribution—the distilled ensemble—is already largely a replication of Primus et al. (2024) applied to a multi-backbone setting. The paper is borderline because the ensemble result and the systematic comparison of three backbones have practical value, but the contribution is weaker than claimed and the experimental evidence is insufficient to fully validate the proposed method.

MY FINAL SCORE: 4.5score
MY FINAL DECISION: Reject