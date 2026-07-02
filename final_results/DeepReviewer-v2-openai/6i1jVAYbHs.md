## Summary
This paper presents AtlasKV, a parametric knowledge augmentation method that enables large language models (LLMs) to incorporate billion-scale knowledge graphs (KGs) with very low GPU memory (under 20GB VRAM). The method addresses two key limitations of prior parametric approaches (specifically KBLaM): (1) training data quality, solved by KG2KV which converts KG triples into query-key-value (Q-K-V) training data by masking entities and rewriting relations; and (2) scalability to massive KGs, solved by HiKVP (Hierarchical Key-Value Pruning) which organizes KG embeddings into a three-level hierarchical index and prunes irrelevant entries through sequential top-k selection, achieving sub-linear O(∛M) inference complexity. Experiments on three out-of-distribution datasets (Enron, ATLAS-Pes2o-QKV, ATLAS-CC-QKV) using LLaMA3.1-8B-Instruct show that AtlasKV significantly outperforms KBLaM in attention-based knowledge grounding accuracy (ACC@1/5) and GPT-4o-scored answer relevance, while using orders of magnitude less GPU memory. Ablation studies confirm the contributions of both the KG2KV data pipeline and the mixed entity-type training strategy. The paper addresses a practical and timely problem — efficiently grounding LLMs with structured knowledge at scale — and provides a technically sound solution with clear empirical support. However, several reproducibility gaps (missing implementation details, dataset statistics, baseline parity documentation) and methodological clarifications (memory measurement methodology, complexity phase attribution) need to be addressed before the work can be considered fully rigorous.

## Strengths
1. **Practical and impactful problem.** The paper addresses a real bottleneck in LLM knowledge augmentation: the inability to incorporate billion-scale structured knowledge under realistic GPU memory constraints. The target of <20GB VRAM for 1B triples corresponds to a widely available GPU tier (e.g., RTX 4090, A5000), making the approach practically accessible.

2. **Technically sound dual-component architecture.** The KG2KV + HiKVP decomposition cleanly separates the data-quality challenge from the scalability challenge. KG2KV's insight that KG triples naturally decompose into Q-K-V structures is well motivated and leverages the relational diversity of KGs to improve generalization. HiKVP's hierarchical pruning is a principled extension of KBLaM's rectangular attention to sub-linear complexity.

3. **Strong empirical validation on OOD benchmarks.** The paper evaluates on three out-of-distribution datasets with varying difficulty. On the harder datasets (ATLAS-Pes2o-QKV, ATLAS-CC-QKV), AtlasKV demonstrates large improvements over KBLaM (e.g., +61.8 ACC@1 on $10^2$ triples for ATLAS-Pes2o-QKV), convincingly showing the generalization benefits of KG2KV training data diversity.

4. **Memory efficiency demonstration.** Figure 4 provides compelling visual evidence that AtlasKV maintains near-constant GPU memory (~20GB) as KG size scales from $10^4$ to $10^9$ triples, while KBLaM exceeds 40GB at only $10^5$ triples. This is the paper's strongest practical selling point.

5. **Comprehensive ablation study.** The ablation in Section 5.3 systematically evaluates the contribution of named vs. event entities in the KG2KV pipeline, providing insight into why the mixed training strategy works and what factors drive grounding accuracy.

6. **Training efficiency.** AtlasKV achieves strong results with only 3K training steps using 20K KGKV samples, compared to KBLaM's 20K steps. This training efficiency is a practically meaningful advantage.

## Weaknesses
### W1. Missing reproducibility-critical implementation details (Major)

Several aspects of the KG2KV pipeline and experimental setup are insufficiently specified for reproduction:
- The sentence encoder is only named (all-MiniLM-L6-v2) in the experiment section, not in the method description.
- The query prefix generation (number of templates, whether they are fixed or varied per triple, how they are used at inference time) is described only qualitatively.
- The relation rewriting process uses an unspecified LLM; the prompt template is relegated to Appendix H (which is not available in the provided manuscript excerpt).
- Table 3 has empty cells for the KBLaM 20K step condition on Enron (10^3 triples), and the column headers "10^3 Triples" could be more clearly labeled as "Number of KG Triples at Evaluation Time."
- The "zero-shot" baseline is not operationally defined.

**Impact:** These gaps reduce the paper's reproducibility and make it difficult for practitioners to implement AtlasKV independently.

**Fix:** Add a dedicated reproducibility subsection or table in the main text that specifies: sentence encoder model and output dimension, number and format of query prefixes, inference-time query construction strategy, the LLM and prompt used for relation rewriting, and a clear operational definition of each baseline.

---

### W2. Memory measurement methodology needs clarification (Major)

The GPU memory results in Figure 4 are a central contribution, but the methodology is not fully transparent:
- It is unclear whether the reported memory includes the LLM backbone weights (~16GB for LLaMA3.1-8B in FP16), the KG embedding storage, the KV cache, and the intermediate activations — or only the incremental cost of the KG augmentation.
- AtlasKV's ~20GB at 1B triples is only ~5GB above zero-shot's ~15GB. If the model weights dominate, the incremental cost of the KG is small but the absolute numbers need a breakdown.
- ICL is shown at <20GB even at 10^9 triples, which is unrealistic — ICL with billion-scale context would exceed any practical GPU memory. The figure should clarify the feasible range for ICL.

**Impact:** Without a memory breakdown, readers cannot determine which component dominates memory usage or how the method would scale to larger models or deeper hierarchies.

**Fix:** Provide a memory budget table showing: model weights, root-layer KG keys (GPU), intermediate/leaf keys (CPU), KV cache, and activations. Disambiguate which phase (precomputation vs. inference) the complexity expressions in Table 2 refer to.

---

### W3. Attention-based ACC@1/5 metrics may be misinterpreted (Major)

The knowledge grounding accuracy (ACC@1/5) measures whether the KG-part post-softmax attention scores at layer 15 assign highest weight to the correct triple. This is a **direct metric of attention-based retrieval quality** but is not equivalent to end-task accuracy (e.g., QA correctness). The paper's narrative could lead readers to over-interpret these as task-level accuracies. The GPTScore (Figure 5) partially addresses this by measuring answer relevance, but only for the w/o HiKVP variant across limited KG sizes (10^2 to 10^4 triples).

**Impact:** The claim "AtlasKV achieves significantly higher Top-1 and Top-5 accuracy than KBLaM" is accurate for the defined metric, but the practical significance for downstream tasks is inferred rather than directly measured.

**Fix:** Explicitly state that ACC@1/5 measures knowledge grounding (attention-based triple retrieval), not downstream task accuracy. Add at least one end-to-end evaluation (e.g., KGQA accuracy) to bridge this gap, or clearly bound the claims to attention-based grounding.

---

### W4. CPU-GPU data transfer latency is not considered (Major)

HiKVP requires three rounds of data transfer per attention layer per decoding step: (1) CPU→GPU for root keys, (2) GPU→CPU for root, CPU→GPU for inter keys, (3) GPU→CPU for inter, CPU→GPU for leaf keys and values. For L=32 layers, this means 96 PCIe transfers per decoding step. Each transfer involves at least k_R·S·D parameters (root: ~128·100·768 ≈ 10M floats ≈ 40MB) per layer. The total I/O latency could dominate the computational savings from sub-linear FLOP complexity, especially for autoregressive decoding where this cost is incurred at every step.

**Impact:** The claimed sub-linear complexity may not translate to proportional wall-clock speedup, which is the practically relevant metric for deployment.

**Fix:** Add wall-clock latency measurements for end-to-end inference, and discuss the I/O bottleneck. Consider alternative designs such as prefetching or pipelined transfer.

---

### W5. Novelty comparison is deferred (Retrieval-Disabled Mode)

Due to the absence of external paper search in this run (Retrieval-Disabled Mode), a systematic novelty comparison against prior parametric knowledge augmentation methods (beyond KBLaM) and graph-based RAG methods could not be conducted. The paper claims "superior effectiveness and scalability compared to ICL, KBLaM, and RAG methods," but the comparison set is limited. Methods such as MemDec, CAG, and various graph-based RAG approaches are mentioned in related work but not quantitatively compared. The clustering strategy (UMAP + GMM) is commonly used in existing work (Sarthi et al., Zhang et al., Huang et al.), and the paper's differentiation from these should be explicitly articulated.

**Impact:** Without external literature verification, the novelty position of AtlasKV relative to the full landscape of LLM-KG augmentation methods cannot be fully adjudicated.

**Fix:** Perform a systematic literature comparison (recommended for revision). Explicitly state what is genuinely novel vs. an engineering extension of existing ideas. Acknowledge the overlap with prior hierarchical retrieval methods and clearly articulate the differentiation.

---

### W6. Evaluation scope is limited to one backbone and one metric type (Minor)

All experiments use LLaMA3.1-8B-Instruct as the backbone with all-MiniLM-L6-v2 as the sentence encoder. The behavior of AtlasKV with larger LLMs (e.g., 70B, Mixtral) or different sentence encoders (e.g., sentence-T5, BGE) is unknown. The GPTScore evaluation uses GPT-4o as the judge without reporting the scoring prompt, inter-rater agreement, or potential biases (verbatim overlap, length preference). On the harder datasets, AtlasKV w/o HiKVP achieves far higher scores than KBLaM, but the absolute GPTScore values (near 1.0 for small KG sizes) suggest ceiling effects.

**Impact:** Generalizability to other model families and the robustness of the GPT-based evaluation are not established.

**Fix:** Add results with at least one additional backbone LLM (e.g., Mistral-7B, LLaMA2-7B). Report the GPT scoring prompt and a sample of scored outputs. Consider adding human evaluation or a standard KGQA benchmark.

---

### W7. Missing limitations discussion (Minor)

The paper lacks a dedicated limitations section. Practical limitations include: the one-time cost of KG2KV preprocessing (relation rewriting via LLMs), the hyperparameter sensitivity of UMAP/GMM clustering, the assumption that KG entrypoint diversity is sufficient for OOD generalization, and the lack of evaluation on factual accuracy benchmarks (e.g., QA, fact-checking).

**Impact:** The absence of a limitations discussion weakens the paper's scientific completeness and may lead to overestimation of the method's readiness for deployment.

**Fix:** Add a limitations subsection explicitly addressing: (1) preprocessing cost of KG2KV, (2) dependency on clustering quality, (3) evaluation scope constraints, and (4) conditions under which AtlasKV may underperform (e.g., very small KGs, domains with sparse relations).

---

### W8. Symbol overloading and notation issues (Minor)

The symbol L is used for both the number of attention layers (Section 3.2) and the total sequence length in Equation (7). The variable $\text{logits}_{k_{gl}}$ in Equations (10)-(11) is reused for both inter-layer and leaf-layer computation with different meanings. The notation $\text{logits}_{\bar{s}_{k_{gl}}}$ in Equation (11) is not defined in the text.

**Impact:** These notation issues reduce readability and may cause confusion during implementation.

**Fix:** Replace L in Equation (7) with T or N_seq. Use distinct variable names for inter-layer logits (logits_inter) and leaf-layer logits (logits_leaf). Define all subscripts in the mathematical notation.

## Score
**Final Score: 7/10**

**Rationale:** The score prioritizes research value and novelty as primary dimensions, followed by validity/soundness and reproducibility.

**Research Value (high weight): 7/10.** The problem — scaling parametric KG augmentation to billion-scale under memory constraints — is practically important and timely. The proposed solution (HiKVP's sub-linear hierarchical pruning) offers a clear improvement over KBLaM's linear complexity and is demonstrated convincingly in memory usage. However, the research value is partially limited by the evaluation scope: only one backbone LLM (8B), one sentence encoder, and attention-based metrics rather than end-task accuracy. The KG2KV pipeline, while effective, is an adaptation of existing ideas (triple-to-text conversion, relation rewriting) rather than a fundamentally new paradigm.

**Novelty: 6/10.** The combination of hierarchical clustering with top-k pruning for attention-based knowledge injection is novel relative to KBLaM. However, the individual components (UMAP + GMM clustering, hierarchical index, top-k pruning) are well-established techniques adapted from existing work. The differentiation from prior hierarchical retrieval methods (Sarthi et al., Huang et al.) is not explicitly articulated. Systematic literature verification was deferred due to Retrieval-Disabled Mode, so this score should be re-evaluated after a full comparison. KG2KV's triple-to-QKV conversion is a practical contribution but shares conceptual similarity with existing KG-to-text approaches.

**Validity/Soundness: 7/10.** The experimental design is generally sound: three OOD datasets, comparison against a strong baseline (KBLaM), and ablation studies. Major concerns that prevent a higher score include: (1) unclear memory measurement methodology (Figure 4), (2) CPU-GPU transfer latency not addressed, (3) ACC@1/5 as attention-based (not task-level) metrics may be misinterpreted, (4) missing variance/confidence intervals, (5) several reproducibility gaps in implementation details.

**Reproducibility: 5/10.** The method description is missing several critical details (query prefix specification, inference-time query construction, relation rewriting LLM, dataset statistics). The appendix (prompt templates, additional results) is referenced but not available in the provided manuscript excerpt. The approach is implementable by an expert reader familiar with KBLaM, but the current description does not meet the standard for independent reproduction.

**Overall:** AtlasKV is a solid systems-oriented contribution with a clear practical advantage (memory efficiency) and strong empirical support on the chosen metrics. The main technical weaknesses are the missing memory measurement breakdown, the CPU-GPU I/O bottleneck not being discussed, and several reproducibility gaps. The paper would benefit from end-task validation (e.g., KGQA) and a broader comparison set. I recommend the paper for acceptance with minor revisions, contingent on adding the missing reproducibility details and addressing the memory measurement methodology.