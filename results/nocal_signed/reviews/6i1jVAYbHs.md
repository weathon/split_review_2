Now let me write the final consolidated review.

## Summary

The paper proposes AtlasKV, a parametric method for augmenting LLMs with billion-scale knowledge graphs (KGs) using two components: (1) **KG2KV**, which converts KG triples into Q-K-V training data by leveraging the natural triple structure, and (2) **HiKVP**, a hierarchical key-value pruning algorithm that reduces time and memory complexity from linear to cube-root in the number of triples. The method aims to enable KG augmentation within 20GB VRAM without external retrievers or retraining.

## Strengths

- **KG2KV is a clever and well-motivated data construction technique (Section 4.1, Table 1).** The insight that KG triples naturally decompose into Q-K-V structures — aligning with the self-attention computation — is genuinely useful. The diversity ratio comparison (7.864% vs 0.003% over synthetic) and average token cost reduction (165.7 vs 349.9) are concrete and meaningful.

- **The scalability problem is accurately diagnosed (Sections 1, 3.2, Table 2).** The paper clearly identifies that KBLaM's linear O((M+N)·N·D) complexity is a bottleneck for real-world KG scales, and the cube-root complexity target is a genuine improvement.

- **The ablation of entity types (Table 4, Section 5.3) is well-designed.** Isolating named entities vs. event entities in KG2KV and showing that both contribute strengthens internal validity.

## Weaknesses

### Major

- **RAG superiority is claimed but no actual RAG method is evaluated.** The abstract and introduction claim superiority over RAG methods, but the experiments use in-context learning (ICL) as a proxy — which is not the same as an actual RAG system with a trained retriever and indexed corpus. No RAG method (e.g., E² GraphRAG, LinearRAG, or a standard dense-retrieval RAG pipeline) is tested on accuracy or latency. Since the paper's positioning heavily contrasts AtlasKV with RAG, this is a significant evidential gap.

- **No runtime or latency data for scalability claims.** The paper's title and central claim concern billion-scale KG augmentation in 20GB VRAM, but only GPU memory usage is reported (Figure 4). No wall-clock time, per-query latency, or throughput measurements are provided. For a scalability paper, the absence of empirical runtime data is a critical omission.

- **The primary accuracy metric measures attention alignment, not task performance.** Table 3 reports whether the correct KG triple receives the highest post-softmax attention weight at layer 15. This measures attention to the right knowledge, not whether the model generates the correct answer. GPTScore (Figure 5) partially addresses this, but relies on GPT-4o-as-judge and is reported only for AtlasKV w/o HiKVP (not the full pruned model). Standard KGQA end-to-end metrics are absent.

- **The comparison against KBLaM conflates data and method effects.** KBLaM is trained on Synthetic data while AtlasKV is trained on ATLAS-Wiki-QKV (constructed via KG2KV). The paper never trains KBLaM on ATLAS-Wiki-QKV data, so the large performance gap in Table 3 cannot be attributed solely to the AtlasKV architecture — it may be driven by the superior data quality of KG2KV, which is itself a confounded variable. A control experiment (same data, different methods) is needed.

### Minor

- **The evaluation setup asymmetrically disadvantages KBLaM.** KBLaM is trained on Synthetic data but evaluated on KG2KV-constructed datasets (ATLAS-Pes2o-QKV, ATLAS-CC-QKV) whose format differs from its training data. This may explain some of its poor performance beyond any inherent method limitation.

- **The parameterized AtlasKV (128-64-16) with HiKVP is not shown in Figure 5.** Only AtlasKV w/o HiKVP (the unpruned version) appears in the GPTScore comparison, making it hard to assess whether HiKVP preserves generation quality.

- **The LLM used for KG2KV relation rewriting is not specified.** The paper states relations are rewritten "through LLMs" (Section 4.1) but does not name the model or estimate the cost of processing 1B triples.

- **Training sample selection is underspecified.** The paper mentions 20K training samples from ATLAS-Wiki (5.9B edges) but does not describe how they are selected.

## Nice-to-Haves

- Evaluate on standard KGQA benchmarks (WebQSP, CWQ) with end-to-end metrics.
- Include MemDec and CAG as additional parametric baselines for accuracy.
- Report how accuracy varies with training set size to support the claim that "we do not need such large scale KGKV pairs in the tuning process."

## Removed Points

These points are flagged to be removed; treat them with caution.

- Criticism that "requires no external retrievers" is misleading because AtlasKV uses a sentence encoder — REMOVED: a frozen sentence encoder is not a "retriever" in the RAG sense; the distinction is standard.
- Criticism about the prompt template being in the missing appendix — REMOVED per hard rule (parser strips appendix content).
- Criticism that Figure 4 shows "theoretical projections, not actual profiling" — REMOVED as speculative; the paper states experiments ran on a single 48GB GPU.
- Criticism about missing "Limitations" section — REMOVED: the paper has Ethics and Reproducibility statements.
- Criticism about the 3-layer justification being "tautological" — REMOVED: the choice is principled (∛M clusters per layer).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Train KBLaM on ATLAS-Wiki-QKV data (or AtlasKV on Synthetic data) to isolate data effects from architectural effects.
2. Report wall-clock latency and per-query throughput for the 1B-triple setting.
3. Add at least one standard KGQA benchmark with end-to-end accuracy metrics.
4. Evaluate at least one actual RAG method (not just ICL as proxy) on the same benchmarks.
5. Specify the LLM used for relation rewriting and the training sample selection strategy.
6. Include the pruned AtlasKV (128-64-16) in Figure 5.

## Score and Decision

The paper's core ideas (KG2KV data construction, HiKVP scaling) are genuinely novel and well-motivated. The KG2KV insight alone is a contribution worth developing. However, the experimental evaluation has several significant gaps that prevent the paper from supporting its strongest claims. RAG superiority is asserted but never tested. Scalability in the title lacks runtime verification. The primary metric measures attention, not task performance. And the central comparison against KBLaM is confounded by different training data. These gaps are fixable, but as submitted the evidence does not match the claims.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>