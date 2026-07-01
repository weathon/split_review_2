## Summary

This paper proposes Pctx, a personalized context-aware tokenizer for generative recommendation (GR). Unlike existing static tokenization methods that assign fixed semantic IDs to items based solely on item features, Pctx incorporates a user's historical interactions to generate different semantic IDs for the same item under different user contexts. The method uses an auxiliary model (DuoRec) to encode user context, clusters these context representations, fuses them with item features, and applies RQ-VAE for quantization, along with strategies to balance personalization and generalizability. Experiments on three Amazon Review datasets show improvements of up to 8.9% in NDCG@10 over non-personalized baselines.

## Strengths

- **Novel and well-motivated problem formulation**: The paper identifies a genuine limitation of existing GR tokenization—the implicit universal similarity assumption enforced by static semantic IDs—and provides a clear, intuitive motivation (Figure 1) for why personalization in tokenization matters. The observation that the same item can be interpreted differently by different users is compelling and practically relevant.

- **Comprehensive methodological design addressing key challenges**: The paper explicitly identifies two core challenges (C1: adaptive tokenization based on personalized context; C2: balancing generalizability and personalizability) and designs specific components to address each. The multi-faceted approach—context representation encoding, clustering, redundant ID merging, data augmentation, and multi-facet generation—shows careful consideration of the trade-offs involved.

- **Strong empirical results with thorough ablation**: The method consistently outperforms all baselines across three datasets and four metrics, with statistically significant improvements. The ablation study (Table 3) is particularly thorough, systematically isolating the contribution of each component (context source, clustering, ID merging, data augmentation, multi-facet generation) and providing clear insights into why each matters.

## Weaknesses

### Major

- **Limited evaluation scope relative to the claimed contribution**: The paper evaluates on only three Amazon Review categories (Instrument, Scientific, Game), all with similar sparsity (~99.96%) and average sequence length (~8-9). The claim of being "the first personalized action tokenizer in GR" would be substantially strengthened by evaluation on datasets with different characteristics (e.g., longer sequences, different domains like news or social media, datasets with explicit user intent labels). The current evaluation does not demonstrate how the method generalizes beyond a narrow setting.

- **The personalization mechanism is indirect and potentially fragile**: The method does not directly condition tokenization on the current user's history at inference time. Instead, it pre-computes cluster centroids from training data and assigns the closest centroid's semantic ID. This means the "personalization" is mediated through a pre-trained auxiliary model (DuoRec) and static clustering, rather than being dynamically computed. The paper does not adequately discuss failure cases where a user's history at inference time does not match any training cluster centroid, or how the method handles cold-start users with very short histories.

- **Dependence on a separately trained auxiliary model**: The method requires training a DuoRec model (or similar) to obtain context representations, which adds significant complexity and computational overhead. The paper does not analyze this cost or discuss whether the benefits justify it in practical deployment scenarios. The ablation shows that using SASRec instead of DuoRec degrades performance, but the paper does not explore whether simpler alternatives (e.g., directly using item embeddings from the GR model itself) could work with appropriate modifications.

### Minor

- **The case study (Figure 4) is illustrative but not quantitatively validated**: While the StarCraft II example is intuitive, the paper does not provide any quantitative evidence that the different semantic IDs actually correspond to different user intents (e.g., by showing that users with similar histories tend to get the same semantic ID, or by evaluating downstream recommendation quality conditioned on the assigned semantic ID). The claim of "explainability" is asserted but not demonstrated.

- **The multi-facet generation mechanism is not clearly distinguished from standard beam search**: The paper describes multi-facet generation as a contribution, but it appears to be standard beam search applied to a model that can output multiple semantic IDs for the same item. The novelty here is unclear, and the paper does not compare against alternative decoding strategies or analyze the diversity of the generated paths.

### Trivial

- The paper uses "Pctx" as the method name but also uses "PCTX" in the title, which is a minor inconsistency.

## Nice-to-Haves

- An analysis of computational cost (training time, inference latency, memory usage) compared to baselines would help practitioners assess the practical trade-offs.
- A discussion of how the method handles items that appear in very different contexts (e.g., an item that is both a gift and a personal purchase) and whether the clustering can capture such multi-modal distributions.
- An exploration of whether the personalized semantic IDs can be used for other downstream tasks beyond next-item prediction, such as user profiling or intent detection.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Expand the evaluation to include datasets with different characteristics (longer sequences, different domains, explicit user intent labels) to demonstrate the generalizability of the approach.
- Provide a quantitative analysis of the semantic IDs' quality, such as measuring intra-cluster coherence of user histories that map to the same semantic ID, or showing that users with similar histories tend to receive the same personalized semantic ID for the same item.
- Discuss the computational overhead of the auxiliary model and clustering step, and provide guidance on when the personalization benefits justify the additional complexity.

## Score and Decision

The paper presents a novel and well-motivated approach to a genuine limitation in generative recommendation. The method is carefully designed with clear reasoning for each component, and the empirical results are strong and well-ablated. However, the evaluation is limited to three similar datasets, and the personalization mechanism is indirect, relying on pre-computed clusters from a separately trained model. These limitations prevent the paper from being a strong accept, but the core contribution is solid and the paper is clearly above the acceptance threshold.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>