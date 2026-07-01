## Summary

QUOKA proposes a training-free, hardware-agnostic sparse attention method for chunked prefill in LLMs, based on the empirical observation that queries with low cosine similarity to the mean query interact more strongly with more keys. The method works in three stages: (1) subselect the most informative (dissimilar) queries, (2) score keys by cosine similarity with those queries, and (3) aggregate scores via max-over-queries and mean-over-GQA-heads. Experiments across five model families, four benchmarks, and three hardware platforms show consistent accuracy advantages over existing sparse attention methods and substantial speedups (5× attention, 3× TTFT).

## Strengths

1. **Novel and well-supported empirical observation about query geometry (Section 3.1, Figure 2).** The paper identifies that queries with low cosine similarity to the mean query are disproportionately responsible for large attention logits, supported by a correlation of 0.737 between $S_q$ and $\max_k(A)$ (Figure 2c). This observation cleanly motivates the two-stage design (query subselection first, then key subselection using those queries), which differs meaningfully from prior work that averages uniformly over all queries.

2. **Consistent and substantial empirical advantage across models, budgets, and benchmarks.** On RULER (Table 1), QUOKA leads every baseline by 10–20+ points across all model sizes and sequence lengths. On LongBench (Table 3), QUOKA achieves normalized scores of 0.945–1.03 while the next-best method (SampleAttention) peaks at 0.901–0.966. This advantage holds across Llama3, Qwen2.5, Qwen3, SmollM3, and GPT-OSS — five distinct model families from 3B to 20B parameters — demonstrating robustness.

3. **Training-free and hardware-agnostic by design.** QUOKA uses only standard linear algebra (mean, cosine similarity, top-k, gather) with no custom CUDA kernels, making it deployable on CPUs, consumer GPUs, and edge accelerators without reimplementation. The measured speedups (up to 7× on Intel Xeon, 5–6× on RTX 2080, Figures 5c/5d) validate this portability advantage concretely.

4. **Graceful degradation under sparsity (Section 4.5).** The ablation study shows accuracy drops only ~3% even when using less than 12% of original tokens, which is important for practical deployment where the sparsity budget may need to be tuned to available hardware.

## Weaknesses

### Fatal

None.

### Major

1. **Theorem 1 is incoherent and does not provide the claimed formal justification (Section 3.1, lines 143–149).** The theorem introduces $q_0$ and $k$, then bounds $\text{CosSim}(M_Q, q^*)$ where **$q^*$ is never defined**. The surrounding text alternates between $q$, $q_0$, and $q^*$ without clarifying the relationship. Furthermore, the bound's right-hand side ($1 + \alpha_q\beta_q - 0.5\alpha_q^2 - 0.5\beta_q^2$) is *decreasing* in $\beta_q$ when $\alpha_q < 0$ and $\beta_q > 0$ (the assumed regime), which contradicts the claimed intuition that larger $\beta_q$ produces a larger selection score $S_q$. The theorem is presented as a formalization but does not hold up to scrutiny. **This is fixable**: the empirical evidence (Figure 2) independently supports the design choice, so the authors can either provide a correct theorem with all variables properly defined, or simply remove the theorem.

2. **>1.0 normalized accuracy scores are presented without explanation or error bars (Table 3, Section 4.4).** QUOKA achieves normalized scores of 1.03 and 1.028 for Smollm3 on LongBench (Table 3), and the paper claims it "in some cases surpasses the accuracy of dense attention" on Math500 (Section 4.4). If sparse attention (dropping 88% of KVs) outperforms full attention, this requires discussion — possible causes include regularization effects, noise in evaluation, or numerical approximations in the dense FlashAttention baseline. Without variance estimates or a mechanism explanation, these results read as potential measurement artifacts. The paper's core "near-baseline accuracy" claim is reasonable, but the "surpasses dense" claim needs stronger support (error bars or explanatory discussion).

### Minor

3. **Missing data point in Table 1.** The QUOKA row for GPT-OSS-20B at sequence length 32k is blank (line 213), while all baselines have entries. The authors should clarify whether this is a formatting artifact or a genuinely missing result.

4. **No variance or error bars on any accuracy result.** All tables report point estimates without confidence intervals, standard deviations, or significance tests. Given that some comparisons hinge on 1–3% differences (e.g., QUOKA vs. full attention in Table 2), it is difficult to assess whether these gaps are meaningful. This is especially important for interpreting the >1.0 scores.

5. **Adaptation of baselines to the prefill setting is not described.** The paper notes that methods like SparQ and Loki were designed for single-query generation and that "naively averaging such proxies across multiple queries in a prefill chunk often degrades accuracy" (line 282), but does not describe how these baselines were actually extended to the multi-query prefill setting. The authors should clarify the extension procedures used.

6. **Overhead of the scoring step is not quantified.** The method incurs an $O(N_Q \cdot T \cdot d)$ cost for query subselection and cosine similarity scoring before the reduced attention. The paper reports end-to-end speedups but does not measure this overhead separately, making it unclear what fraction of prefill time is spent on scoring vs. attention. Direct measurement would strengthen the efficiency claims.

### Trivial

7. Notational inconsistency in Theorem 1 and surrounding text ($q^*$ vs. $q_0$ vs. $q$), which appears to be more than a simple typo since $q^*$ is never defined.

## Nice-to-Haves

- An ablation where QUOKA's dissimilarity-based query subselection (Stage 1) is replaced by uniform random sampling (keeping everything else identical) would directly test whether the geometric selection criterion itself matters, or whether any small query set suffices. This is the single most informative ablation missing from the paper.
- A dedicated limitations section discussing (a) the scoring overhead, (b) that the method reduces KV computation but not KV cache memory, and (c) scenarios where the method might struggle would improve completeness.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"Algorithm 1 Step 8 may incorrectly distribute queries across heads":** The reviewer questioned whether top-k selection distributes queries unevenly across heads. However, top-k is applied per-head over the token dimension, so the reshape in Step 8 is valid. The paper could clarify the dimension but this is not a real flaw.
- **"88% fewer claim is misleading":** The claim straightforwardly states the compression ratio at the chosen operating point. This is a factual description, not misleading.
- **"Baseline comparison unfair because SparQ/Loki use 64-dim projections while QUOKA uses 16 full-dim queries":** These are different methods' inherent design choices. QUOKA's latency advantage (Figure 5) confirms the approach is competitive despite using richer scoring signal. However, the related concern about how baselines were adapted to prefill (point 5 under Minor) is retained.
- **"Missing limitations section":** Absence of a dedicated limitations section is a presentation choice, not a substantive weakness.
- **"Theorem is never used elsewhere":** This is encompassed by the stronger criticism that the theorem is incoherent.

## Novel Insights

None beyond the paper's own contributions. The reviews surface the theorem's incoherence and the unexplained >1.0 scores as issues the authors need to address but do not contribute new observations about the method beyond what the paper already states.

## Suggestions

1. Fix or remove Theorem 1. The empirical evidence (Figure 2) independently supports the design choice, so removal is a clean option.
2. Provide error bars or variance estimates for the main accuracy tables (at minimum for LongBench and RULER comparisons that hinge on small margins).
3. Explain or qualify the >1.0 normalized scores. If these are within noise, say so and report variance. If sparsity acts as a regularizer, discuss the mechanism.
4. Fill in the missing data point in Table 1 or explain the omission.
5. Describe how each baseline was adapted to the prefill setting with multiple queries.
6. Measure the scoring overhead separately and report it alongside end-to-end speedups.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>