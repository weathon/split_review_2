## Summary

QUOKA proposes a training-free, hardware-agnostic sparse attention method optimized for chunked prefill. The core insight is that queries with low cosine similarity to the mean query interact more broadly with keys and contribute more to the attention output. By subselecting these "informative" queries and scoring keys via cosine similarity, the method reduces the effective KV cache size. Empirically, QUOKA shows large and consistent margins over baselines: at B_SA=1024 on 32k sequences (RULER), it scores 57.01 vs 31.73 for the next best method on Llama3.2-3B, and on LongBench it maintains near-dense normalized accuracy (0.945–0.998 at B_SA=512) while baselines drop to 0.7–0.86. Latency speedups of 3–7× are demonstrated across A100, RTX 2080, and Intel Xeon hardware.

## Strengths

1. **Geometric insight is well-motivated and empirically grounded.** The observation that queries farther from the mean query attend more broadly (Figure 2a) is geometrically intuitive. The PCA visualization (Figure 2b) and the correlation between S_q and max_k(A) (r=0.737, Figure 2c) provide concrete supporting evidence.

2. **Accuracy results show large and consistent margins over baselines.** On RULER (Table 1) at 32k with B_SA=1024, QUOKA achieves 57.01 on Llama3.2-3B vs 31.73 for SampleAttention — a gap of nearly 2×. On LongBench (Table 3), QUOKA at B_SA=512 achieves 0.945 vs 0.738 for SampleAttention. These margins hold across six model families and both synthetic and realistic benchmarks.

3. **Hardware portability is convincingly demonstrated.** The method relies only on standard linear algebra (mean, cosine similarity, top-k gather), compatible with FlashAttention and deployable without custom kernels. Latency results on Intel Xeon CPU (Figure 5c) and RTX 2080 GPU (Figure 5d) validate this claim concretely.

4. **Broad model coverage strengthens generality claims.** Experiments span six model families (Llama3, Qwen2.5, Qwen3, SmollM3, Qwen3-30B-A3B MoE, GPT-OSS) including RoPE, NoPE, and MoE variants.

## Weaknesses

### Fatal
None.

### Major

1. **Theorem 1 contains an undefined symbol and does not provide meaningful theoretical grounding.** The theorem (lines 143–148) introduces q^* without definition — the setup defines q_0 and k, then bounds CosSim(M_Q, q^*). The variable q^* is never specified; it is unclear whether q^* = q_0 or refers to a different quantity. This notational gap makes the theorem unverifiable. More fundamentally, the bound is a purely algebraic consequence of the cosine law; it restates the selection criterion rather than justifying it, and its connection to post-softmax attention logits is not established. The paper presents this theorem as formal justification ("This can be formalized through the following theorem"), but it adds no theoretical substance. **Fix or remove this theorem.**

2. **The claim that QUOKA surpasses dense attention is reported without explanation, undermining credibility.** On Smollm3 LongBench (Table 3), QUOKA achieves normalized scores of 1.03 and 1.028 — exceeding the dense baseline by ~3%. On Math500, the paper states QUOKA "in some cases even surpasses the accuracy of dense attention" (Section 4.4). No explanation or hypothesis is offered. Without analysis (is this regularization? evaluation noise? a suboptimal dense baseline?), this result undermines confidence rather than supporting the method. At minimum, confidence intervals are needed; ideally, an explicit discussion of why this occurs (or an acknowledgment that it may be within noise).

### Minor

1. **No variance or statistical significance reported for accuracy results.** All accuracy numbers (Tables 1, 2, 3) are single-point estimates with no confidence intervals or standard deviations. Many comparisons at shorter sequence lengths (Table 1, 4k results) involve small margins, and the >1.0 LongBench results are within a few percent of baseline. The latency experiments are averaged over 100 trials; the same rigor should apply to accuracy.

2. **Empirical evidence for the core geometric observation is from a single layer and head.** Figure 2 shows data from layer 0, head 11 of Llama 3.2-3B-Instruct only. Attention patterns vary substantially across layers and heads. Showing that the correlation between S_q and attention influence holds across multiple layers and heads would substantially strengthen the paper's central claim.

3. **Missing data point in Table 1.** The QUOKA row for GPT-OSS-20B at 32k is empty (line 213). This should be corrected or explained.

4. **Scoring overhead is not broken down from attention savings.** The latency speedups (Figure 5) are reported as end-to-end and module-level, but the fraction of time spent in the scoring/selection step (computing mean query, cosine similarities, top-k) vs the reduced attention computation is not given. This breakdown is important for practitioners deciding when the method is beneficial.

5. **No code release.** The reproducibility statement (Section 8) acknowledges that source code is not included. While the method uses standard operations, faithful reproduction across six baseline methods and six model families would be materially aided by code. This is a practical limitation for a methods paper.

### Trivial

- The claim in Section 1 that pattern-based approaches' "benefits are limited" under chunked prefill due to "dynamic compute graph and KV cache memory bandwidth overhead" is asserted without supporting citation. This does not affect the paper's core contribution.

## Nice-to-Haves

- Include an ablation isolating the contribution of each component (query subselection, cosine similarity scoring, max vs mean aggregation) on the same benchmark and budget in the main text rather than the appendix.
- Adapt generation-oriented baselines (LessIsMore, SparQ, Loki) more carefully to prefill (e.g., using QUOKA's query subselection as a front-end) to verify that QUOKA still wins under a fairer comparison.
- Provide a failure case analysis: when does QUOKA's accuracy degrade beyond 3%? Are there task types or sequence lengths where it performs poorly?
- Specify N_Q and B_SA explicitly in the latency experiment description (Section 4.6).

## Removed Points

- Criticism that Table 9 (cosine similarity vs dot product ablation) is in the appendix and unverifiable. **Removed per rule: parser-stripped appendix content should not be flagged as missing.**
- Criticism that the baseline comparison is "structurally unfair" because generation methods are naively extended to prefill. **Weakened to nice-to-have.** The paper acknowledges this limitation (lines 121–122) and already compares against SampleAttention (designed for prefill). The massive margins in Table 1 make it very unlikely the conclusion would flip under a fairer setup.
- Criticism about missing related works. **Removed per rule: do not mention missing related works without external sources to confirm.**

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Fix (define q^*) or remove Theorem 1 — it currently harms rather than helps the paper's credibility.
2. Add confidence intervals (e.g., 3–5 seeds) for the main accuracy tables, especially for the >1.0 LongBench results.
3. Either explain the >1.0 accuracy phenomenon or flag it as within expected noise.
4. Fill the missing GPT-OSS-20B 32k entry in Table 1.
5. Provide a breakdown of scoring overhead vs attention computation time in the latency experiments.
6. Release source code to aid reproducibility.

---

**Calibration Summary**

All anchor papers retrieved across rounds:

| Path | Avg Score | Round | Comparison to QUOKA |
|---|---|---|---|
| HASA (Hjk1tWIdvL) | 5.00 | R1 | Similar topic (sparse prefill) but requires training; QUOKA stronger |
| SeerAttention (HmwneoGoy9) | 5.25 | R1 | Learned sparsity, requires training & custom kernels; QUOKA stronger |
| Cascading KV Cache (dSneEp59yX) | 6.00 | R1 | Training-free KV management, comparable scope; QUOKA has larger margins |
| SparseRAG (HE6pJoNnFp) | 6.60 | R1 | RAG-focused sparsity; comparable contribution level |
| FlexPrefill (OfjIlbelrT) | 8.00 | R1 | Dynamic sparse prefill; stronger analysis and unanimous scores |

**Round 1 bracket:** 5.5–7.5 (QUOKA is clearly stronger than HASA/SeerAttention, comparable to SparseRAG/Cascading KV Cache, weaker than FlexPrefill)

**Final score anchored** against SparseRAG (6.60) and Cascading KV Cache (6.00): QUOKA has larger empirical margins than both but weaker theoretical framing and missing variance reporting, placing it between them.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>