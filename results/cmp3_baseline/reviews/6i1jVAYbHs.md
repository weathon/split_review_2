## Summary
The paper proposes AtlasKV, a parametric method to augment large language models with very large knowledge graphs (KGs) using very little GPU memory (e.g., <20GB VRAM for 1B triples). The core innovations are KG2KV, which naturally converts KG triples into Q-K-V training data, and HiKVP, a hierarchical key-value pruning algorithm that reduces inference time/memory complexity from linear in the KG size to sub-linear (cube root). Experiments on OOD KGQA datasets show that AtlasKV achieves higher knowledge grounding accuracy and answer relevance than KBLaM and other baselines, while dramatically reducing GPU memory usage.

## Strengths
- **Novel combination of KG2KV and HiKVP**: The KG2KV pipeline provides a principled way to convert structured KG triples into Q-K-V tuples that align with the attention mechanism, solving the training data diversity issue. The HiKVP algorithm is clever and well-motivated, reducing memory and time complexity from linear to sub-linear in the number of triples.
- **Strong empirical results on OOD datasets**: AtlasKV consistently outperforms KBLaM (often by large margins) on three OOD datasets (Enron, ATLAS-CC-QKV, ATLAS-Pes2o-QKV) across various KG sizes. The ablation study clearly validates the contributions of both KG2KV and the cooperative use of named/event entities.
- **Convincing memory scaling analysis**: Figure 4 provides a clear visual demonstration that AtlasKV’s GPU memory cost stays nearly flat (around 20GB) while KBLaM, ICL, and RAG methods grow linearly or quadratically, supporting the claim of billion-scale feasibility under low VRAM.
- **General approach**: The method is training-free for new KGs after initial training, does not require external retrievers, and is not limited to a specific KG format, which adds practical value.

## Weaknesses
### Fatal
None.

### Major
1. **Lack of empirical grounding accuracy at the claimed billion-scale**: The paper consistently advertises the ability to handle 1B triples in 20GB VRAM, but all accuracy/relevance experiments (Table 3, Figure 5) are conducted on at most 10<sup>4</sup> triples. While the memory scaling plot is credible, there is no evidence that the method maintains high knowledge grounding accuracy when scaled to 1B triples. The pruning strategy (HiKVP) may introduce significant accuracy degradation at very large scales due to coarse clustering, but this is not evaluated.
2. **None** (but this is a major gap that weakens the core claim).

### Minor
1. **Comparison with KBLaM may be partially unfair**: KBLaM is designed for general KBs (text strings), not specifically for KGs, and uses synthetic Q-K-V data with limited diversity. AtlasKV’s KG2KV is a natural advantage for KG tasks. The paper does not include a baseline where KBLaM is also trained on KG2KV-style data (which would isolate the benefit of HiKVP over rectangular attention).
2. **Reliance on a third-party LLM (GPT-4o) for relevance scoring** is not a standard benchmark; using GPT-4o as an evaluator introduces potential bias and irreproducibility. While GPTScore is a plausible metric, the paper could have included a human evaluation or task-specific metrics for stronger validation.

### Trivial
- Some notation in the equations is slightly overloaded (e.g., $\bar{\mathbf{k}}_I$ appears both as the selected inter-layer keys and as the pruned set), but the description is still understandable.

## Nice-to-Haves
- A benchmark or simulation showing grounding accuracy vs. KG size beyond 10<sup>4</sup> (e.g., up to 10<sup>6</sup> or 10<sup>7</sup>) would greatly strengthen the billion-scale claim.
- Analysis of the trade-off between pruning aggressiveness (top-\(k\) values) and accuracy at different KG scales.
- Code release (the paper promises it but the appendix is missing) would improve reproducibility.

## Novel Insights
The paper introduces two clean, complementary ideas: (i) leveraging the inherent structure of KG triples to create Q-K-V data that mimics the attention mechanism, and (ii) using hierarchical clustering to prune key-value pairs in a sub-linear fashion while preserving retrieval accuracy. The observation that increasing the diversity of enquiry attributes (via KG relations) improves OOD generalization is a concrete takeaway for future work on parametric knowledge injection. The training dynamics (the model learns to “retrieve” rather than “memorize” after a certain step) is intriguing but not deeply analyzed; it could inspire new regularization strategies.

## Suggestions
1. **Provide empirical grounding results for at least 10<sup>5</sup>–10<sup>6</sup> triples** to bridge the gap between the memory plot and actual accuracy. If GPU memory is a constraint, consider reporting on smaller scales with projected degradation curves.
2. **Add a baseline where KBLaM is trained on the same KG2KV data** to isolate the contribution of HiKVP over rectangular attention.
3. **Use a deterministic evaluation metric** (e.g., exact match or F1 on a standard KGQA dataset) in addition to GPTScore to improve reproducibility.
4. **Discuss limitations of HiKVP**: how does the choice of cluster size (cube root) impact accuracy vs. scale? What is the optimal top-\(k\) search strategy?

## Score and Decision
**Score**: 6 (borderline accept)  
**Decision**: Reject  

**Rationale**: The paper presents a technically sound and interesting method with clear practical potential. The two main innovations (KG2KV and HiKVP) are well-motivated and yield strong results on moderate-scale experiments. However, the core claim of “billion-scale augmentation” is not empirically validated for knowledge grounding accuracy. Without evidence that the method retains high accuracy when actually applied to millions or billions of triples, the paper’s most prominent selling point remains unsubstantiated. The experiments are otherwise thorough, and the method is likely to be useful for smaller scale KG integration, but for the full claim, the evidence is incomplete. A revision that includes larger-scale accuracy results could move this toward acceptance.

MY FINAL SCORE: <score>6</score>  
MY FINAL DECISION: Reject