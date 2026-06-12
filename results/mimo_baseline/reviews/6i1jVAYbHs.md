## Summary

AtlasKV proposes a parametric method to augment LLMs with billion-scale knowledge graphs using minimal GPU memory. It introduces KG2KV, which naturally converts KG triples into query-key-value data for improved training diversity and generalization, and HiKVP, a hierarchical key-value pruning algorithm that achieves sub-linear O(M^{1/3}) complexity, enabling integration of 1B triples within 20GB VRAM.

## Strengths

- **Elegant KG2KV insight with strong empirical support.** The observation that KG triples (h, r, t) naturally decompose into Q-K-V data is genuinely clever. Table 1 quantifies the diversity advantage: 7.864% vs 0.003% diversity ratio and 165.7 vs 349.9 average token cost compared to synthetic methods. This translates directly into improved generalization on hard OOD datasets (ATLAS-Pes2o-QKV, ATLAS-CC-QKV) where KBLaM fails dramatically (e.g., 0.0% vs 16.4% Top-1 accuracy at 1K triples on ATLAS-Pes2o-QKV).

- **Impressive scalability results.** Figure 4 convincingly demonstrates that AtlasKV maintains ~20GB VRAM even at 1B triples, while KBLaM exceeds 40GB at just 100K triples. The theoretical sub-linear complexity analysis (Table 2) is well-justified and the hierarchical pruning pipeline in Figure 3 is clearly presented.

- **Comprehensive evaluation design.** The paper evaluates across three OOD datasets of varying difficulty, multiple KG sizes (10^0 to 10^4 triples), and both knowledge grounding accuracy and GPT-scored answer relevance. The inclusion of "AtlasKV w/o HiKVP" cleanly separates the contributions of KG2KV and HiKVP. The ablation study (Table 4) on entity types provides useful design insights.

- **Efficiency of training.** Only 3K training steps achieve strong performance, compared to 20K steps reported for KBLaM, suggesting the KG2KV data construction significantly improves training efficiency.

## Weaknesses

### Fatal

None.

### Major

- **Significant accuracy degradation from HiKVP.** Table 3 shows that HiKVP causes substantial drops in knowledge grounding accuracy. On ATLAS-Pes2o-QKV at 10^1 triples, Top-1 accuracy drops from 72.7% to 52.2% (a 20.5-point absolute drop). At 10^0 triples, it drops from 47.3% to 16.4%. These are large degradations that undermine the core claim of "maintaining high knowledge grounding accuracy during inference time." The paper claims the specific heads have "capabilities to conduct fuzzy retrieval at different layers of semantic granularity," but this explanation is insufficient given the magnitude of the drops, especially at smaller KG sizes where the pruning pressure should be minimal.

- **Limited downstream task evaluation.** The evaluation metrics are knowledge grounding accuracy (Top-1/Top-5) and GPT-scored answer relevance, but there is no evaluation on standard QA benchmarks (e.g., FreebaseQA, WebQuestionsSP, or similar). Knowledge grounding accuracy alone does not demonstrate that the injected knowledge actually improves the LLM's ability to answer questions correctly. The GPTScore evaluation is a step in this direction but uses a somewhat non-standard evaluation protocol.

- **Evaluation only up to 10^4 triples with no demonstrated billion-scale task performance.** While the paper convincingly shows 20GB VRAM at 1B triples (Figure 4), all accuracy results in Table 3 and all GPTScore results in Figure 5 only go up to 10^3–10^4 triples. There is no accuracy or quality evaluation at 10^5, 10^6, or 10^9 triples. The gap between the memory proof-of-concept and demonstrated task performance is significant, especially since at the largest evaluated size (10^4), HiKVP already degrades accuracy substantially.

- **Small evaluation sample sizes with no statistical significance testing.** Table 3 uses only 100 samples per dataset. With binary accuracy metrics, 95% confidence intervals for a 72.7% result would be approximately ±8.8 percentage points, meaning many of the reported differences (especially at smaller KG sizes) may not be statistically significant. No confidence intervals or significance tests are provided.

### Minor

- **Fixed top-k settings without sensitivity analysis.** The top-k values (128, 64, 16) appear to be fixed without systematic exploration. The paper mentions Appendix B.4.1 covers different settings, but the main paper should at least summarize whether these are optimal and how sensitive performance is to these choices.

- **Sentence encoder not discussed at scale.** The UMAP dimensionality reduction and GMM clustering pipeline requires processing all M key embeddings. For 1B triples, this pre-computation cost and the storage of all key embeddings are not discussed. This could be a practical bottleneck.

- **Missing comparison with graph-based RAG baselines.** The related work discusses E² GraphRAG, LinearRAG, RAR, and KnowGPT, but none are included as baselines. While some may not be directly comparable, at least E² GraphRAG or LinearRAG could serve as comparisons for the scalability argument.

### Trivial

None beyond typical formatting artifacts from PDF extraction.

## Nice-to-Haves

- An analysis of how HiKVP's accuracy/efficiency trade-off varies with different cluster sizes S or numbers of hierarchical layers (the paper fixes 3 layers).
- A breakdown of wall-clock inference latency, not just VRAM, compared to KBLaM and ICL/RAG methods.
- Discussion of the offloading latency when keys/values are transferred between CPU and GPU in HiKVP's three steps.

## Novel Insights

The key novel insight is the natural alignment between KG triple structure (head-relation-tail) and the Q-K-V structure of self-attention, and the empirical demonstration that this alignment yields dramatically higher training data diversity than synthetic methods (7.864% vs 0.003%). This is a genuine conceptual contribution that could inform future work on structured knowledge integration. The hierarchical pruning approach, while inspired by retrieval-augmented methods, is novel in its application to the key-value injection paradigm and provides a concrete path to billion-scale parametric knowledge augmentation.

## Suggestions

- Add evaluation on standard QA/KBQA benchmarks at scale to demonstrate that knowledge grounding translates to improved answer quality.
- Provide accuracy results at larger KG sizes (≥10^5 triples) to close the gap between the scalability demonstration and quality evaluation.
- Include error bars and significance tests for all reported metrics given the small evaluation sample sizes.
- Explicitly discuss and quantify the accuracy-efficiency trade-off introduced by HiKVP across different configurations.

## Score and Decision

The paper presents a genuinely novel and well-motivated approach to scaling parametric knowledge augmentation for LLMs. The KG2KV insight is elegant and well-supported, and the scalability results are impressive. However, the significant accuracy degradation from HiKVP, the lack of downstream task evaluation, and the disconnect between demonstrated scalability (1B triples) and evaluated quality (up to 10^4 triples) are substantial weaknesses. The paper is a solid contribution but would benefit from more rigorous evaluation before acceptance at a top venue.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>