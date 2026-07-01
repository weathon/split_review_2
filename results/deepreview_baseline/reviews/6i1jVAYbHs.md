## Summary

The paper proposes **AtlasKV**, a parametric method to augment large language models (LLMs) with billion-scale knowledge graphs (KGs) using very little GPU memory (claimed <20GB VRAM for 1B triples). It introduces **KG2KV** to convert KG triples into query-key-value (QKV) training data, and **HiKVP** (hierarchical key-value pruning) to achieve sub-linear time and memory complexity at inference. Experiments compare AtlasKV with KBLaM and in-context learning on OOD evaluation datasets, reporting higher knowledge grounding accuracy and GPTScore while using less GPU memory.

## Strengths

- **Relevant problem**: Augmenting LLMs with large-scale structured knowledge under tight memory budgets is practically important.
- **Novel combination of ideas**: Converting KG triples into QKV data and applying hierarchical pruning to reduce complexity is a creative synthesis of existing concepts (KBLaM, hierarchical clustering).  
- **Clear writing and methodology**: The paper is well-structured, the figures are helpful, and the technical details (complexity analysis, pruning steps) are explained in a readable way.

## Weaknesses

### Fatal

- **Core claim of billion-scale capability is unsupported by empirical evidence**. The paper repeatedly states AtlasKV can handle 1B triples in <20GB VRAM, but the experiments only evaluate knowledge grounding up to 1 000 triples (Table 3) and memory usage is shown only in a plot that appears to be extrapolated (Figure 4 – no measurement description, no data points below 10⁴ triples, no actual run for 10⁹). No end-to-end experiment on a billion-scale KG is provided, making the central scalability claim unverified.
- **Missing comparisons with state-of-the-art scalable RAG methods**. The paper mentions `E²` GraphRAG and LinearRAG in related work but does not compare against them or any other method that claims to handle large KGs efficiently. Only KBLaM and ICL are used as baselines, which are not the most competitive for this setting.

### Major

- **Inference latency and throughput are not evaluated**. The paper focuses on memory usage and accuracy but never reports actual wall-clock time, latency, or throughput for HiKVP. The hierarchical pruning involves multiple CPU–GPU transfers, which could introduce significant overhead; this is not discussed.
- **Training data construction quality is not rigorously assessed**. The KG2KV pipeline requires rewriting relations into noun words via an LLM; the paper does not evaluate the accuracy of this rewriting or its impact on downstream performance. The “diversity ratio” in Table 1 is computed on unspecified datasets, making the comparison with the “Synthetic” method questionable.
- **Limited scale of grounding experiments**: The largest KG size for accuracy experiments is only 10³ triples (Table 3). This does not demonstrate that the method works at scales approaching billions, even with HiKVP.

### Minor

- **Ablation study on entity types** is performed only on a variant without HiKVP, so the effect of entity type in the full AtlasKV pipeline is unclear.
- The paper claims “training-free adaptation to new knowledge” for the parametric paradigm, but AtlasKV still requires training the KG-specific query/projection heads on some data. The distinction between “training-free” and “not retraining the base LLM” could be clarified.

### Trivial

- Some figures (e.g., Figure 1) have unclear dollar-sign icons and lightning bolt icons that are not explained in the caption.
- Equation numbers are inconsistent (Equation 3–11 are used, but the reference to Equation 2 for KBLaM uses `(2)` while later equations are `(3)` etc., minor formatting).

## Nice-to-Haves

- Provide an actual experiment on a KG with at least 10⁶ or 10⁷ triples to validate the memory and accuracy claims at scale.
- Report inference time (latency per token) and total wall-clock time for the full HiKVP pipeline, including CPU–GPU transfer costs.
- Compare with graph-based RAG methods (e.g., `E²` GraphRAG, LinearRAG) on the same OOD benchmarks.

## Novel Insights

None beyond the paper’s own contributions. The observation that KG triples naturally decompose into Q-K-V strings is sensible, and the idea of using hierarchical pruning with top-k selection to achieve sub-linear scaling is a straightforward application of known techniques to the rectangular attention setting. The paper does not reveal a deep or unexpected insight.

## Suggestions

- Run the full method on a KG with at least 10⁶ triples and report accuracy and memory usage. This is necessary to substantiate the primary claim.
- Include runtime/latency measurements to show that the sub-linear complexity translates into practical speed.
- Compare with a state-of-the-art scalable RAG method, such as `E²` GraphRAG or LinearRAG, to establish clear advantages.
- Evaluate the quality of the KG2KV relation rewriting automatically (e.g., using human annotation or a separate metric) to ensure the training data is faithful.

## Score and Decision

**Score**: 3 (reject)

**Decision**: Reject

The paper addresses a timely problem and has a reasonable idea, but the central claim of handling billion-scale KGs in 20GB VRAM is not empirically supported. The experiments are limited to very small KG sizes (≤10³ triples) for accuracy evaluation, and the memory plot appears extrapolated without measurement details. Critical baselines (modern scalable RAG methods) are missing. Without stronger empirical evidence, the contribution cannot be validated.

MY FINAL SCORE: 3</score>
MY FINAL DECISION: Reject</decision>