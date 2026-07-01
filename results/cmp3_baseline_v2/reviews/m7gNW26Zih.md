## Summary

This paper addresses language-based audio retrieval using a dual-encoder architecture. It proposes three complementary techniques: (i) soft-label distillation from an ensemble of pretrained retrieval teachers to handle non-binary audio-caption correspondences, (ii) LLM-based caption augmentation (back-translation and LLM-driven mix for mixed audio), and (iii) an auxiliary classification task guided by unsupervised caption clustering. Experiments on the CLOTHO dataset report mAP@16 improvements over a contrastive baseline, with the best single model reaching 46.6 and a weighted ensemble reaching 48.8 on the development test split.

## Strengths

- **Clear problem and practical motivation**: The paper tackles an important task (language-based audio retrieval) and identifies a realistic issue—that caption-audio correspondences are often non-binary—motivating the soft-label approach.
- **Reproducible augmentation pipeline**: The LLM-based caption augmentation is described with specific techniques (back-translation, LLM mix) and dataset sizes (50,000 new pairs), making it easy to replicate.
- **Thorough ablation design**: The controlled system variants (SID 1–5 in Table 1) allow isolating the effect of distillation, augmentation, and clustering across three different audio backbones.
- **Strong ensemble results**: The weighted ensemble across configurations achieves the best reported scores, demonstrating that the individual components offer complementary strengths.

## Weaknesses

### Fatal

None.

### Major

- **Limited novelty**: The three components are individually well-known (ensemble distillation, LLM-based data augmentation, cluster-based classification). Their combination is straightforward and does not introduce conceptually new learning principles or theoretical insights.
- **Cluster guidance provides no consistent improvement**: In Table 2, adding cluster supervision (SID 4 and 5) yields marginal or negative gains compared to the already augmented model (SID 3). For EAT and BEATs, clustering *hurts* mAP@16. The paper acknowledges “mixed gains” but this directly undermines the claimed contribution of cluster-guided alignment.
- **No comparison to prior state-of-the-art**: The paper does not benchmark against any existing methods on standard test splits (e.g., CLOTHO evaluation set or AudioCaps test set). Without such comparisons, it is impossible to judge whether the proposed system advances the field. The single evaluation-set number (mAP@16=0.421) is given without context.
- **Reliance on a proprietary LLM**: GPT-4o is used for augmentation, and the paper does not provide a fallback with an open-source model. This limits reproducibility, especially for a venue like ICLR.

### Minor

- **Hyperparameter selection not justified**: The weight λ₂=0.05 for the cluster-loss is fixed without any sensitivity analysis. No ablation on the number of clusters, the clustering algorithm, or the effect of the pseudo-label noise is provided.
- **Missing dataset diversity**: All fine-tuning and re-fine-tuning are done only on CLOTHO. It is unclear whether the gains transfer to other audio-retrieval benchmarks (e.g., AudioCaps).
- **Single-run results**: No error bars or statistical significance measures are reported, though raw numbers may be deterministic given the training setup.
- **Gap between dev test and evaluation set**: The large drop from 48.83 (mAP@16 on dev test) to 0.421 (on evaluation) is not discussed, leaving questions about generalization and potential overfitting.

### Trivial

None.

## Nice-to-Haves

- An open-source clustering alternative (e.g., k-means on Sentence-BERT embeddings) to compare against BERTopic.
- A small-scale human evaluation of the LLM-mixed captions to validate their quality.
- Ablation on the temperature τ in the distillation loss.

## Novel Insights

None beyond the paper’s own contributions—the combination itself does not yield a new understanding of why soft-label distillation or cluster guidance work for audio retrieval, nor does it reveal surprising failure modes.

## Suggestions

- Provide a direct comparison with published baselines (e.g., Koepke et al. 2022, Primus et al. 2024, or the DCASE 2024 leaderboard) on the same evaluation splits. This is critical to establish the practical value of the proposed system.
- Either strengthen the empirical evidence for cluster guidance (e.g., show that it helps specifically under high correspondence ambiguity with a dedicated experiment) or remove the claim that it is a core contribution.
- Include experiments on AudioCaps to demonstrate cross-dataset generalization.
- Report sensitivity of the final ensemble weights to show stability of the grid search.

## Score and Decision

- **Originality**: 2 (largely incremental)
- **Quality**: 4 (solid engineering but weak empirical support for core novelty)
- **Clarity**: 5 (well-structured but thin on analysis)
- **Significance**: 3 (useful component combination but no benchmark-topping results or new insights)

MY FINAL SCORE: 4score  
MY FINAL DECISION: Rejectdecision