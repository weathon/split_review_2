## Summary
This paper introduces QUOKA, a training-free and hardware-agnostic sparse attention method designed to accelerate the prefill stage of LLM inference under chunked prefill. The key insight is that queries with low cosine similarity to the mean query interact more strongly with more keys and contribute most to final attention logits. QUOKA leverages this by first subselecting representative queries based on cosine dissimilarity, then scoring and subselecting keys using cosine similarity, achieving near-baseline accuracy while using 88% fewer key-value pairs and delivering up to 5× attention speedup on GPUs and 7× on CPUs.

## Strengths
- **Novel and well-motivated approach**: The paper identifies a genuine limitation of existing query-dependent sparse attention methods (designed for single-query generation, not multi-query prefill) and provides a principled solution based on query geometry. The observation that low cosine-similarity queries are the most informative is both novel and empirically validated.
- **Strong empirical results across diverse settings**: QUOKA consistently outperforms multiple strong baselines (SampleAttention, SparQ, Loki, LessIsMore) across four benchmarks (NIAH, RULER, LongBench, Math500) and five model families (Llama3, Qwen2.5, Qwen3, SmolLM, GPT-OSS). The improvements are substantial (10-20% on RULER, near-baseline on LongBench) and hold across varying sparsity budgets.
- **Hardware agnosticism and practical deployability**: By relying on standard linear algebra operations rather than custom CUDA kernels, QUOKA is portable across heterogeneous hardware (Nvidia GPUs, Intel CPUs, consumer GPUs). This is a significant practical advantage over kernel-level sparse attention methods.
- **Comprehensive ablation and analysis**: The paper provides thorough ablations on key hyperparameters (B_SA, B_CP, N_Q), demonstrating graceful degradation under increasing sparsity. The empirical analysis of query-key geometry (Figure 2) and the justification for max vs. mean aggregation (Figure 3) are well-supported.

## Weaknesses
### Fatal
None.

### Major
- **Theoretical justification is weak and potentially misleading**: Theorem 1 attempts to formalize the query subselection criterion, but the bound appears vacuous or incorrectly derived. The theorem states that if CosSim(k, q_0) = β_q > 0 and CosSim(M_Q, k) = α_q < 0, then CosSim(M_Q, q*) ≤ 1 + α_q β_q - 0.5α_q² - 0.5β_q². However, the right-hand side can easily exceed 1 (e.g., α_q = -0.5, β_q = 0.5 gives 1 - 0.25 - 0.125 - 0.125 = 0.5, but α_q = -0.1, β_q = 0.9 gives 1 - 0.09 - 0.005 - 0.405 = 0.5, while α_q = -0.9, β_q = 0.1 gives 1 - 0.09 - 0.405 - 0.005 = 0.5). More critically, the theorem does not actually prove that low CosSim(M_Q, q*) queries are the ones that attend strongly to keys—it only provides an upper bound. The paper's core claim that "queries with lower cosine similarity to the mean query attend to the majority of keys" is supported empirically but the theoretical grounding is insufficient and the theorem as stated does not convincingly connect to the selection criterion. The proof is relegated to the appendix (which is stripped), making it impossible to verify.

- **Missing comparison to important baselines**: The paper does not compare against StreamingLLM (Xiao et al., 2024), H2O (Zhang et al., 2024), or other KV cache eviction methods that are also training-free and hardware-agnostic. While the paper notes that eviction is "complementary," these methods are directly applicable to the same problem setting and represent a natural baseline. Additionally, the paper does not compare against any pattern-based sparse attention methods (e.g., Block-Sparse Attention) that could be adapted to chunked prefill, even if they require custom kernels.

- **Limited analysis of computational overhead**: The paper reports speedups but does not provide a detailed breakdown of where time is spent in QUOKA's three-stage pipeline (query subselection, cosine similarity scoring, aggregation). The overhead of computing cosine similarity between all queries and all keys (even after subselection) could be significant, especially for large KV caches. The paper claims sub-quadratic complexity but does not provide a formal complexity analysis or empirical profiling of the selection overhead vs. the attention computation itself.

### Minor
- **The paper claims "near-baseline accuracy" but some results show non-trivial degradation**: On RULER with B_SA=1024 (Table 1), QUOKA achieves 57.01 on Llama3.2-3B at 32k length vs. the full attention baseline (not shown in that table but presumably higher). While QUOKA outperforms baselines, the absolute accuracy drop from full attention is not always reported, making it hard to assess the "near-baseline" claim quantitatively.
- **The Math500 results (Table 8) are mentioned but not shown in the main paper**: The paper states "Table 8" but the table is not included in the provided content. This makes it impossible to evaluate the claim that QUOKA "surpasses the accuracy of dense attention" in some cases.
- **The paper does not discuss the impact of chunk size B_CP on the effectiveness of query subselection**: When chunks are very small (e.g., B_CP = 2), the number of queries available for subselection is limited, potentially reducing the benefit of the query selection step.

### Trivial
- The paper uses "subsection" and "subselection" inconsistently (should be "subselection").
- Figure 1 caption is repeated three times.

## Nice-to-Haves
- A comparison against a simple baseline that randomly selects KV pairs (to isolate the benefit of the query/key selection strategy from the benefit of sparsity itself).
- An analysis of how QUOKA's performance varies across different layers of the transformer (e.g., early vs. late layers), since attention sparsity patterns are known to vary by depth.
- A discussion of how QUOKA interacts with quantization or other compression techniques commonly used in edge deployment.

## Novel Insights
The paper's core insight—that queries with low cosine similarity to the mean query are the most informative for key selection during prefill—is genuinely novel and well-supported by empirical analysis. This observation provides a principled way to reduce redundancy in multi-query settings, which is a key limitation of existing query-dependent sparse attention methods. The use of cosine similarity (rather than dot product) as a stable, bounded proxy for attention relevance is also a practical contribution that improves selection quality.

## Suggestions
1. Strengthen the theoretical justification: either provide a more rigorous theorem that directly connects the selection criterion to attention approximation error, or reframe the theoretical contribution as an empirical observation with heuristic justification.
2. Add comparisons to StreamingLLM, H2O, or other training-free KV cache eviction methods that are applicable to the same setting.
3. Include a complexity analysis and empirical profiling of the selection overhead vs. attention computation to demonstrate that the overhead is indeed sub-quadratic and does not dominate the speedup.
4. Report absolute accuracy of the full attention baseline alongside QUOKA's results in all tables to support the "near-baseline" claim quantitatively.

## Score and Decision
The paper presents a novel, well-motivated, and empirically strong method for accelerating LLM prefill. The results are convincing across multiple benchmarks, models, and hardware platforms. The main weaknesses are the weak theoretical justification and the missing comparison to important baselines, but these do not invalidate the core contribution. The paper is clearly written, the experiments are thorough, and the method is practical and deployable. I recommend acceptance.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>