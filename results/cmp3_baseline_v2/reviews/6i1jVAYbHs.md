## Summary

The paper proposes **AtlasKV**, a parametric framework for augmenting LLMs with very large knowledge graphs (up to billion triples) under tight GPU memory constraints (under 20 GB VRAM). AtlasKV has two main components: (1) **KG2KV**, which transforms each KG triple \((h, r, t)\) into query-key-value (QKV) data by masking an entity and rewriting the relation into a noun, producing diverse training data; and (2) **HiKVP**, a hierarchical key-value pruning algorithm that clusters keys and prunes them during inference to achieve sub-linear time and memory complexity. Experiments on three OOD datasets show improved knowledge grounding accuracy and generation relevance compared to KBLaM and in-context learning, while the memory projection indicates that 1B triples can be handled within 20 GB VRAM.

## Strengths

- The problem is important: scaling parametric knowledge injection to billion-scale KGs with low memory is a practical and timely challenge for LLM augmentation.
- The combination of KG2KV (data-side innovation) and HiKVP (algorithmic-side innovation) is clever and well motivated. The observation that KG triples can be naturally decomposed into Q-K-V strings is insightful and leverages the structure of KGs.
- HiKVP’s hierarchical pruning is a non-trivial extension of the KBLaM paradigm, converting linear complexity to sub-linear complexity while preserving accuracy. The memory projection (Figure 4) convincingly shows dramatic savings over KBLaM.
- The OOD evaluation design (Enron, ATLAS-CC-QKV, ATLAS-Pes2o-QKV) is more challenging than the standard settings and the results (Table 3, Figure 5) demonstrate clear improvements over both KBLaM and ICL in grounding accuracy and generation relevance.

## Weaknesses

### Major

1. **Billion-scale claim is only supported for memory, not for task performance.** The paper claims “end-to-end augmentation with billion-scale KGs”, but the accuracy and generation evaluations are limited to subsets of up to \(10^4\) triples. It is unclear whether the method maintains high knowledge grounding accuracy and generation quality when the KG has \(10^9\) triples. Without task-level evidence at larger scales, the central scalability claim remains partially unsubstantiated.

2. **Unfair comparison with KBLaM due to different training data.** AtlasKV is trained on the KG2KV-generated ATLAS-Wiki-QKV dataset, while KBLaM is trained on its original Synthetic dataset. As the authors themselves note, the KG2KV data is much more diverse. Consequently, the observed superiority (Table 3) could be primarily due to the training data, not the method itself. A controlled experiment (e.g., training KBLaM on the same ATLAS-Wiki-QKV data, or training AtlasKV on Synthetic) is essential to attribute the gains.

3. **Generation quality evaluation does not include full AtlasKV with HiKVP.** Figure 5 only reports GPT-4o scores for “AtlasKV w/o HiKVP”. Since HiKVP is a core component that prunes keys, it is critical to show that pruning does not substantially degrade generation relevance. Without this, the read cannot assess the utility of the full system.

4. **Insufficient baseline coverage.** The only parametric baseline is KBLaM; non-parametric baselines are limited to ICL and a memory complexity comparison with RAG and CAG. No comparisons with modern graph-based RAG systems (e.g., GraphRAG, LightRAG, \(\mathrm{E}^2\) GraphRAG) or with other parametric knowledge injection methods (e.g., MemDec) are provided. For a paper claiming superiority over both paradigms, the baseline set is too narrow.

5. **Missing technical details that affect reproducibility.** The KG2KV process uses an LLM to “rewrite the relation into its noun word” – which LLM, prompt template, and temperature are used? The hierarchical clustering (UMAP + GMM) parameters are not specified. Training hyperparameters (learning rate, batch size, optimizer, etc.) are relegated to the appendix; at least the key choices should appear in the main text. These omissions weaken the paper’s reproducibility.

### Minor

- The diversity ratio in Table 1 is not precisely defined (“unique enquiry attributes divided by the total number of triples”) – it would be clearer to define what constitutes a unique enquiry attribute and how it is counted.
- In Figure 4, the “In-context learning” baseline assumes placing all triples verbatim in the context, which is not a feasible policy for billion-scale KGs; this extrapolation should be explicitly justified.
- The paper claims “training-free adaptation to new knowledge”, but after initial training, new triples still need to be encoded via KG2KV and the sentence encoder; this is not truly training-free but inference-only, which is acceptable but the phrasing could be more precise.

## Nice-to-Haves

- Evaluate accuracy on larger KG subsets (e.g., \(10^5\) or \(10^6\) triples) to provide direct evidence that the method scales in performance, not just in memory.
- Run a controlled experiment where KBLaM is trained on the same ATLAS-Wiki-QKV data to disentangle effect of method vs data.
- Report generation relevance scores for full AtlasKV (with HiKVP) to quantify the cost of pruning.
- Compare with a strong non-parametric RAG baseline (e.g., GraphRAG or LightRAG) on the same OOD datasets.

## Novel Insights

Beyond the paper’s own contributions, the key insight is that the relational structure of KGs \((h, r, t)\) can be directly mapped to the Q-K-V format used in attention layers, where the masked entity serves as the value and the remaining context (other entity + relation) forms the key. This mapping naturally produces highly diverse question–key pairs without requiring manual schema design, and it avoids the token cost of synthesizing full question–answer pairs from unstructured text. Combined with hierarchical pruning, this suggests that structured knowledge graphs are a particularly well-suited source for parametric memory injection in LLMs, offering both scalability and generalization.

## Suggestions

- Perform an experiment on a large-scale KG (e.g., 1M triples from ATLAS) to report grounding accuracy; if exact evaluation is infeasible, sample a set of queries and measure retrieval precision.
- Include a controlled variant where KBLaM is trained on the same KG2KV data to isolate the contribution of the AtlasKV training procedure.
- Report generation quality and grounding accuracy for AtlasKV with HiKVP at varying top‑k settings, not just for the ablation without pruning.
- Add a comparison with a state‑of‑the‑art graph RAG method (e.g., LightRAG or GraphRAG) to contextualize the results against non‑parametric approaches.

## Score and Decision

MY FINAL SCORE: <score>4</score>  
MY FINAL DECISION: <decision>Reject</decision>