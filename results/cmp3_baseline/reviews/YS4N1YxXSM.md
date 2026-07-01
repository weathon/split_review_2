## Summary

QUOKA is a training-free, hardware-agnostic sparse attention method designed to accelerate the prefill stage of LLM inference under chunked prefill. The key insight is that queries with low cosine similarity to the mean query interact more strongly with a larger set of keys and contribute most to the final attention logits. QUOKA first selects a small set of such representative queries, then uses cosine similarity between those queries and all keys to subselect the most relevant KV pairs before feeding them into a dense attention kernel. Experiments on Needle-In-A-Haystack, LongBench, RULER, and Math500 show that QUOKA achieves near-baseline accuracy while providing up to 5× attention speedup and 3× time-to-first-token reduction on GPUs, and up to 7× speedup on CPUs, using 88% fewer KV pairs per attention evaluation.

## Strengths

- **Novel and well-motivated observation**: The paper identifies that queries with low cosine similarity to the mean query are the most influential in attention, and leverages this geometry to perform query subselection. This is a clean, intuitive insight that is empirically validated (Figure 2) and supported by a theoretical bound (Theorem 1).
- **Strong empirical results across diverse settings**: QUOKA consistently outperforms existing sparse attention methods (SampleAttention, SparQ, Loki, LessIsMore, SnapKV, KeyDif) on LongBench, RULER, and NIAH across multiple model families (Llama3, Qwen3, SmollM, GPT-OSS) and sequence lengths up to 32k. The accuracy degradation is minimal even at high sparsity (e.g., <3% drop with 12% of tokens).
- **Practical speedups on heterogeneous hardware**: The method achieves significant latency reductions on NVIDIA A100, RTX 2080, and Intel Xeon CPUs, demonstrating hardware portability. The speedups scale with sequence length, which is critical for long-context applications.
- **Training-free and compatible with standard kernels**: QUOKA uses only standard linear algebra operations and can be combined with optimized dense kernels like FlashAttention, avoiding the need for custom CUDA kernels. This makes it easy to deploy across different platforms.
- **Thorough ablation studies**: The paper systematically ablates key hyperparameters (B_SA, B_CP, N_Q) and design choices (cosine similarity vs. dot product, max vs. mean aggregation), confirming the robustness of the method.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor
- **Theoretical justification is limited**: Theorem 1 provides a bound on the cosine similarity between the mean query and a query that attends strongly to a key, but the bound involves unknown quantities (α_q, β_q) and the proof is relegated to the appendix. The theorem does not directly guarantee that the selected queries are the most informative; it only shows a necessary condition. The empirical evidence is strong, but the theoretical grounding could be tightened.
- **Potential overhead of query subselection**: The method requires computing cosine similarity between all queries in a chunk and the mean query, then selecting top-k. While this is O(B_CP) per chunk, the paper does not fully analyze the overhead relative to the attention savings, especially for small chunk sizes. The speedup plots (Figure 5) show net gains, but a breakdown of the overhead would strengthen the paper.
- **Occasional super-baseline accuracy**: On some settings (e.g., SmollM3 on LongBench with B_SA=2048, accuracy 1.028), QUOKA exceeds the dense baseline. The paper does not discuss this phenomenon; it may be due to noise or a regularization effect of sparsity. A brief comment would improve clarity.

### Trivial
- The paper states "up to nearly a 7× speedup on Intel Xeon CPUs" in the abstract, but Figure 5c shows speedups up to about 5× for QUOKA at 60k tokens. The 7× claim may refer to a different setting or be an overestimate; the numbers should be consistent.

## Nice-to-Haves

- Provide a complexity analysis (FLOPs and memory) for QUOKA in the main text, comparing it to dense attention and other sparse methods.
- Include a discussion of limitations, e.g., scenarios where the query geometry assumption might break (e.g., very early layers or models with unusual attention patterns).
- Release the code to facilitate reproducibility and adoption.

## Novel Insights

Beyond the paper's own contributions, the key insight that query geometry (specifically angular distance from the mean query) can serve as a reliable proxy for attention influence is a novel and potentially transferable idea. This suggests that not all queries in a prefill chunk are equally informative for KV selection, and that a small set of "outlier" queries can guide the selection effectively. This principle could inspire other query-dependent sparsification or caching strategies beyond the specific method presented.

## Suggestions

- Add a brief complexity analysis in Section 3 or 4 to quantify the overhead of query subselection and scoring relative to the attention savings.
- Clarify the discrepancy in the CPU speedup claim (abstract vs. Figure 5c) and ensure all numbers are consistent.
- Discuss the super-baseline accuracy results briefly, e.g., attributing them to noise or a beneficial regularization effect.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>