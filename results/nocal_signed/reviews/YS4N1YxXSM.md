Now let me compose the final review.

## Summary

QUOKA proposes a training-free, hardware-agnostic sparse attention method for chunked prefill in LLM inference. The key insight is that queries with low cosine similarity to the mean query interact most broadly with keys and contribute most to the attention distribution. The method uses three steps — query subselection (keeping only the most informative queries), cosine-similarity scoring, and max-aggregation — to reduce the active KV cache, achieving substantial speedups (up to 5× on A100, 7× on CPU) while maintaining near-dense accuracy across multiple benchmarks.

## Strengths

- **Clean, well-motivated design.** The core observation (Figure 2c: correlation of 0.737 between query–mean cosine similarity and max attention weight) is empirically grounded and leads to a natural three-step method using only standard linear algebra. This makes QUOKA genuinely portable across hardware without custom kernels — a clear practical advantage over kernel-level sparse attention methods.

- **Evaluation across diverse model families.** The paper tests on 6 models spanning standard (Llama3, Qwen3), MoE (Qwen3-30B-A3B), and NoPE (GPT-OSS-20B) architectures, strengthening the claim of cross-architecture generalization.

- **Latency benchmarking on CPU and consumer GPU.** Unlike many sparse attention papers that report only on A100 GPUs, QUOKA provides results on Intel Xeon CPU and RTX 2080 GPU, directly supporting the claimed target of resource-constrained deployment.

## Weaknesses

### Fatal
None.

### Major

1. **No variance or error bars on any accuracy benchmark.** Accuracy results on RULER, LongBench, and NIAH are reported as single numbers with no measure of uncertainty. Latency experiments are averaged over 100 trials (per Section 4.6), but accuracy results have no equivalent treatment. This is especially problematic given that QUOKA sometimes exceeds the dense baseline — without variance information the reader cannot assess whether these are meaningful differences or evaluation noise.

2. **Performance gaps over baselines are very large and unexplained.** On RULER (Table 1) at 16k with Llama3.2-3B, QUOKA scores 70.90 vs. SampleAttn at 48.31 (a ~23 point gap). At 32k the gap grows to ~25 points. The paper attributes this to better aggregation but provides no controlled ablation that isolates the effect of query subselection from the different aggregation function (max vs. average). Without diagnostic analysis, it is unclear which component drives the improvements, and the magnitude raises questions about whether the baselines are optimally configured for the chunked-prefill setting.

3. **Unexplained >1.0 normalized scores against the dense baseline.** On Smollm3 in Table 3, QUOKA achieves normalized scores of 1.03 (B_SA=2048) and 1.028 (B_SA=1024), meaning it outperforms dense attention by 2.8–3%. Since a sparse method that drops most KVs should not systematically beat the optimal dense baseline, this requires explanation. The paper mentions a similar phenomenon for Math500 only in passing, but does not address it for LongBench at all.

4. **LongBench reported only as normalized relative scores.** Table 3 reports "relative scores compared to the dense baseline (where 1.0 indicates no accuracy drop)." Without absolute numbers, the reader cannot tell whether QUOKA's 0.945 represents genuinely good performance (e.g., 94.5% of a strong 90% baseline) or merely smaller degradation from a weak baseline (e.g., 94.5% of a weak 60% baseline). The dense baseline itself operates under chunked prefill, which is not the standard evaluation protocol for these benchmarks.

### Minor

5. **Figure 4 caption is internally contradictory.** The caption states that "Full (c) show[s] lower accuracy" than QUOKA on NIAH. Since "Full" is the dense attention baseline (which under chunked prefill should be mathematically equivalent to standard full attention and thus the accuracy upper bound), this claim is either an evaluation issue or a labeling error. No explanation is provided in the paper.

6. **Theorem 1 uses undefined notation.** The theorem introduces a fixed query q₀ and key k, then transitions to an undefined symbol q^* (lines 145 and 149 in the main text). The claimed formal connection between the bound and the query subselection rule cannot be followed as written.

7. **SnapKV and KeyDif appear in Table 1 but are not described in the baselines section.** The Sparse Attention Baselines section (Section 4) only discusses SampleAttention, LessIsMore, SparQ, and Loki. SnapKV and KeyDif appear without introduction or implementation details, which makes the evaluation table feel ad-hoc.

### Trivial

8. **Empty cell in Table 1.** The QUOKA entry for GPT-OSS-20B at 32k is blank with no explanation.

## Nice-to-Haves

- Report absolute LongBench scores alongside (or instead of) the normalized relative scores.
- Add a controlled ablation that varies only the query selection criterion (uniform vs. cosine-dissimilarity) while keeping scoring and aggregation fixed.
- Clarify Figure 4: explain how "Full" dense attention can show lower accuracy than QUOKA, or correct the caption if it is mislabeled.

## Removed Points

These points from the input review were removed with justification:
- **"Ablation claims cannot be verified (appendix missing)"** — Removed per guidelines: the parser strips appendix sections from all papers; they exist in the original submission.
- **"Algorithm 2 not shown in main text"** — Same reason as above.
- **"Implausibly large gaps suggest deliberate baseline misconfiguration"** — The speculative claims about deliberate misconfiguration and systematic evaluation errors are unsubstantiated. The core observation (large gap without diagnostic analysis) is kept as Major weakness #2.
- **"Loki anomalous data point (Table 3, Smollm3)"** — This is a baseline anomaly, not a weakness of the paper's own method.
- **"Source code not included"** — The critic noted this but called it acceptable; not a weakness.
- **All typos/formatting-related criticisms** — Removed per guidelines (parser artifacts).

## Novel Insights

None beyond the paper's own contributions. The reviewer observations (large unexplained gaps, missing error bars, relative-only reporting) are standard evaluation concerns, not novel analytical insights.

## Suggestions

1. Add error bars or multi-seed runs to all accuracy benchmarks.
2. Explain the >1.0 normalized scores on LongBench — either as evaluation noise, an artifact of chunked prefill degrading the dense baseline, or a genuine phenomenon.
3. Add a controlled ablation isolating the query selection strategy from the aggregation function.
4. Define q^* in Theorem 1 and clarify the logical chain from the bound to the subselection rule.
5. Describe SnapKV and KeyDif in the baselines section or remove them from the table if they cannot be described.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>