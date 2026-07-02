## Summary

QUOKA introduces a training-free, hardware-agnostic sparse attention method for accelerating LLM prefill under chunked prefill. The core insight is that queries with low cosine similarity to the mean query interact more broadly with keys and contribute most to attention outputs. By retaining only these representative queries and using them to subselect the most relevant KV pairs via cosine similarity scoring with max aggregation, QUOKA reduces the effective KV budget while maintaining near-baseline accuracy—achieving up to 5× attention speedup and 3× reduction in time-to-first-token across diverse hardware.

## Strengths

- **Novel geometric insight with strong empirical support.** The observation that low-cosine-similarity queries are more informative and interact with more keys (Figure 2) is well motivated by both empirical evidence (PCA visualization, correlation with max attention) and a theoretical bound (Theorem 1). This is a clean and actionable finding that directly drives the method.

- **Comprehensive and convincing empirical evaluation.** The paper evaluates QUOKA across 5 model families (Llama3, Qwen3, SmollM, GPT-OSS, Qwen3-30B-A3B), 4 benchmarks (NIAH, RULER, LongBench, Math500), multiple budgets (B_SA from 512 to 2048), and multiple hardware platforms (A100, RTX 2080, Intel Xeon). QUOKA consistently outperforms competing sparse attention methods, often by 10–20% on RULER (Table 1) and with near-1.0 normalized accuracy on LongBench (Table 3).

- **Practical hardware agnosticism.** By relying only on standard linear algebra operations (mean, cosine similarity, top-k, gather) rather than custom CUDA kernels, QUOKA is portable to CPUs, consumer GPUs, and edge accelerators—a significant practical advantage over pattern-based or kernel-level approaches. Speedups on CPU (7×) and RTX 2080 (5–6×) demonstrate real cross-platform viability.

- **Thorough ablation and robustness analysis.** The paper systematically ablates B_CP, B_SA, and N_Q (Tables 3, 5, 6, 11, 12), showing graceful degradation under increasing sparsity (less than 3% drop with 12% of tokens) and stable performance across hyperparameter choices. This supports practical deployment under varied hardware constraints.

- **Clean handling of GQA.** The pre-aggregation trick (averaging normalized queries across KV groups before computing scores) is both principled (linearity of mean and outer product) and efficient, reducing computation and memory by the number of KV groups. This is a nice engineering contribution that maintains compatibility with modern architectures.

## Weaknesses

### Major

- **Unexplained cases where sparse attention outperforms dense attention.** On LongBench (Table 3), QUOKA with 1024 budget achieves normalized accuracy >1.0 (1.03 for SmollM3), and on Math500 (Section 4.4) the paper states QUOKA "in some cases surpasses the accuracy of dense attention." On NIAH (Figure 4), the "Full" baseline shows lower accuracy than QUOKA in some regions. These are unusual outcomes for a sparse approximation on retrieval tasks. The paper does not adequately explain why this occurs—whether it is due to chunked prefill degrading the baseline, regularization effects, noise in evaluation, or an implementation issue. Without explanation, these results raise questions about the fairness and correctness of the baseline comparison.

- **Missing analysis of the overhead of KV selection per chunk.** QUOKA applies query subselection, cosine similarity computation, and gather operations for each chunk during chunked prefill. While the latency speedups are impressive for long sequences (30k+ tokens), the overhead-to-benefit ratio at shorter or moderate lengths is not thoroughly discussed. The method may be less efficient or even detrimental at small sequence lengths where the selection overhead is not amortized.

- **No code release.** The reproducibility statement explicitly says "we have not included source code." While the method is described in detail, releasing code is standard practice at ICLR and significantly strengthens reproducibility, especially for comparing against baselines on specific benchmarks.

### Minor

- **Theoretical motivation is suggestive but not rigorously linked to the selection criterion.** Theorem 1 provides a bound on CosSim(M_Q, q*) under specific assumptions about CosSim(k, q_0) and CosSim(M_Q, k). The connection between this bound and the claim that S_q = -CosSim(M_Q, q*) identifies queries that "contribute most to the attention distribution" relies on the empirical correlation in Figure 2c rather than a tight theoretical guarantee. The theorem feels more like a consistency check than a derivation of optimality.

- **Cosine similarity vs. dot-product scoring is insufficiently justified.** The paper argues that cosine similarity is preferable to dot products because it is "scale-dependent and unstable under aggregation" but provides limited theoretical analysis of why L2 normalization preserves the ranking of important KVs better than scaled dot products. The empirical ablation (Table 9, 10% improvement on RULER) is helpful, but a more principled explanation would strengthen the paper.

- **Generality of the geometric observation across layers and heads.** The detailed geometric analysis (Figure 2) is shown for a single layer (layer 0) and a single head (head 11) of Llama 3.2-3B. While the paper validates QUOKA across models, the underlying assumption that query geometry is similar across all layers and heads is not directly verified. Some layers may have different query-key interaction patterns.

### Trivial

- "subsection selection" appears to be a typo for "subselection" (Sections 3.1 and 3.2).

## Nice-to-Haves

- An analysis of failure modes or cases where QUOKA underperforms relative to the dense baseline would strengthen the paper's transparency.
- A study of how the query geometry (S_q distribution) evolves across layers would provide deeper insight into why the method works.
- A discussion of how QUOKA could be combined with KV cache eviction methods (mentioned briefly in related work but not explored) would be a useful direction.
- A breakdown of the overhead cost of each step (query subselection, scoring, gathering) relative to the saved attention cost would help practitioners understand the trade-offs.

## Novel Insights

Beyond the paper's own contributions, the key insight is that not all queries in a prefill chunk are equally informative for determining which KVs matter: queries near the mean query attend mostly to a small common set of keys, while queries far from the mean have broad, differentiated attention patterns. This geometric characterization of query diversity as a signal for representative subsampling is a genuinely useful observation that could inspire other selective computation strategies in transformers beyond attention (e.g., selective FFN activation or selective layer skipping).

## Suggestions

1. **Address the "outperforming dense attention" issue directly.** Provide an explanation for why QUOKA sometimes exceeds full attention accuracy—whether due to chunked prefill artifacts, regularization, or statistical noise. If this is a real effect, discuss its implications. If it is an artifact, correct the presentation.

2. **Release code.** The method is simple to implement, but code release is expected for a methodology paper at ICLR, especially to ensure fair comparison with baselines on standard benchmarks.

3. **Add an overhead analysis.** Include a breakdown of the computational cost of QUOKA's selection steps vs. the saved attention cost as a function of sequence length and chunk size, to help practitioners understand when the method is beneficial.

4. **Clarify the cosine similarity justification.** Provide a more rigorous explanation of why L2 normalization followed by dot product (i.e., cosine similarity) is a better relevance proxy than raw scaled dot products for KV selection under multi-query aggregation.

## Score and Decision

This paper presents a well-motivated, practically valuable method with a clean geometric insight and thorough empirical validation across multiple models, benchmarks, and hardware platforms. The primary concerns—unexplained outperformance of dense attention and lack of code—are significant but not fatal to the core contribution. The paper makes a clear empirical case that QUOKA is effective and efficient.

MY FINAL SCORE: 7.0score</score>
MY FINAL DECISION: Accept</decision>