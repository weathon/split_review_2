Now I have sufficient calibration data. Let me compile the final review with anchor comparisons.

## Summary
QUOKA is a training-free, hardware-agnostic sparse attention method for accelerating LLM prefill under chunked prefill. It exploits the geometric observation that queries with low cosine similarity to the mean query attend most broadly to keys, using this to select representative queries and then score/subselect KVs per chunk. Evaluated on NIAH, RULER, LongBench, and Math500 across 6 model families, it shows 20-25+ point accuracy margins over baselines and 3–7× speedups across A100, RTX 2080, and Intel CPUs.

## Strengths
- **Novel geometric observation with strong empirical support**: The paper identifies that queries with low cosine similarity to the mean query interact most broadly with keys. Figure 2c shows r=0.737 correlation between dissimilarity score S_q and max_k(A); Figure 2b provides PCA visualization showing high-S_q queries lie closer to the key cluster. This is a genuinely new insight compared to prior sparse attention methods (SampleAttention, SparQ, Loki) that treat queries homogeneously.

- **Substantially stronger accuracy than all baselines across benchmarks and models**: On RULER (Table 1), QUOKA achieves 57.01% at 32k on Llama3.2-3B while the next-best (SampleAttention) gets 31.73% — a 25+ point gap. On LongBench (Table 3), QUOKA maintains 0.945–1.028 normalized accuracy at B_SA=512, while baselines range 0.384–0.765. These margins are consistent across all 6 model families tested (Llama3.2, Qwen2.5, Qwen3-4B, Qwen3-30B-A3B, SmolLM3, GPT-OSS-20B).

- **Cross-hardware portability validated on 3 distinct platforms**: Tests on A100 (enterprise GPU), RTX 2080 (consumer GPU), and Intel Xeon CPU (Figure 5). QUOKA achieves ~5× attention speedup on A100, 5–6× on RTX 2080 and CPU. This is a direct consequence of using standard linear algebra operations rather than custom CUDA kernels, and distinguishes QUOKA from kernel-level sparse attention methods.

- **Minimal accuracy degradation under high sparsity**: Table 12 shows only ~3% drop even with N_Q = (1/16)B_CP. The claim of <3% drop with <12% of original tokens (Section 4.5) is directly evidenced by LongBench and RULER results at low budgets.

- **Elegant pre-aggregation trick for GQA architectures**: Section 3.3 explains that by normalizing Q and K before scoring, the mean across GQA KV groups can be computed cheaply via linearity, reducing computation by a factor equal to the number of KV groups.

## Weaknesses

### Fatal
None

### Major
- **Missing data point in headline Table 1**: In Table 1 (RULER, B_SA=1024), the QUOKA row has an empty entry for GPT-OSS-20B at 32k tokens (line 213: `| <b>79.19</b> | <b>73.40</b> | <b>57.79</b> |  |`). All competing baselines have values for this cell (e.g., SampleAttn=30.42, SparQ=15.20, LessIsMore=20.11). This is the longest evaluation length for the largest model tested — a particularly important data point. Its absence is unexplained.

### Minor
- **Theorem 1 formalization is loose**: The variable q* appears in the bound (Eq. 5, line 145) but is never defined in the theorem statement — only introduced in the informal interpretation below (lines 147-149). The connection from the geometric bound to the practical algorithm ("retain queries most dissimilar from the mean") is asserted rather than rigorously derived. The empirical evidence (Figures 2b, 2c with r=0.737 correlation) more convincingly supports the method than the theorem does. This doesn't invalidate the contribution but the formalization should be sharpened or reframed.

- **"Better-than-dense" phenomenon left unexplained**: In Table 3, QUOKA on SmolLM3 with B_SA∈{1024, 2048} achieves normalized scores of 1.03 and 1.028 — outperforming dense attention by ~3%. Section 4.4 also notes this for Math500. This is a potentially significant finding (sparsity as beneficial regularization) but is noted as an achievement without analysis. Which tasks benefit? Is this consistent across runs? Is the dense comparison baseline using chunked prefill or not?

- **SnapKV and KeyDif appear in Table 1 without introduction**: The baseline descriptions (line 187) describe SampleAttention, LessIsMore, SparQ, and Loki, but SnapKV and KeyDif appear in Table 1 (lines 207-208) without any description. They should be briefly described when they first appear.

### Trivial
- **NIAH evaluation limited to single model**: Section 4.1 evaluates NIAH only on Llama3.2-3B-Instruct with B_SA=2048, while RULER and LongBench cover multiple models. This is a minor completeness concern.

## Nice-to-Haves
- A systematic analysis of how the query-geometry observation varies across layers and heads would strengthen the foundational claim. Figure 2 shows one layer, one head of one model.
- Math500 results are referenced (Table 8) but the table is in the appendix. Since "in some cases even surpasses the accuracy of dense attention" is a key claim, at least a summary should appear in the main text.

## Removed Points
These points are flagged to be removed, treat them with caution:
- The harsh critic's concern about Theorem 1 being "fatal" or "structural" is demoted — while the formalization is loose, the empirical evidence independently supports the method and the proof exists in the appendix. This is treated as a Minor weakness above.
- The harsh critic framed the "better-than-dense" phenomenon as an "evidential gap" suggesting unfair comparison; however, this is more accurately an unexplored opportunity rather than a weakness. The paper's core claims don't depend on explaining this.

## Novel Insights
The paper's genuinely novel contribution is the geometric observation about query-key relationships: queries cosine-dissimilar from the mean query are the ones that dominate attention logits. This is supported by r=0.737 correlation (Figure 2c) and leads to a principled query selection criterion that outperforms uniform sampling (SampleAttention) by 20-25 points on RULER. The practical consequence — that a simple training-free algorithm using standard linear algebra can substantially outperform kernel-level sparse attention methods across heterogeneous hardware — is a meaningful advance for efficient LLM inference.

## Suggestions
- Fill in or explain the missing GPT-OSS-20B/32k entry in Table 1.
- Sharpen Theorem 1 by defining q* in the theorem statement or reframing as "Motivating Observation."
- Add brief descriptions of SnapKV and KeyDif when they first appear in results.
- Analyze the "better-than-dense" phenomenon — this could be the most interesting finding in the paper.

## Reporting

**Anchors retrieved across all rounds:**

| Paper | Avg Score | Round | Comparison |
|-------|-----------|-------|------------|
| FlexPrefill: Context-Aware Sparse Attention for Prefill | 8.00 | 1 | Most similar topic — sparse attention for prefill, training-free. QUOKA shows larger margins over baselines and more comprehensive evaluation (6 models, 4 benchmarks, 3 hardware platforms). |
| OmniKV: Dynamic Context Selection | 6.00 | 1 | Training-free KV cache method, but focused on memory offloading rather than prefill speed. QUOKA achieves stronger latency results and broader benchmarking. |
| Cascading KV Cache | 6.00 | 1 | Training-free KV cache for context extension. Weaker baselines (mainly StreamingLLM). QUOKA has much stronger experimental validation. |
| VL-Cache: Sparsity-Aware KV Compression for VLMs | 6.00 | 1 | KV cache compression for VLMs. Different domain but similar spirit. QUOKA more focused and better validated. |
| Identify Critical KV Cache (Output Perturbation) | 5.75 | 1 | Theoretical KV cache analysis. Scored 5-6, incremental contribution. QUOKA has a more novel core insight and stronger results. |
| Running Huge Context Windows on Tiny GPUs | 4.67 | 1 | Sparse attention for long context. Rejected. QUOKA is substantially more thorough. |
| ChunkAttention | 4.50 | 1 | Efficient attention with chunking sharing. Rejected. Different focus but QUOKA is stronger. |
| KV Prediction for TTFT | 4.50 | 1 | TTFT reduction via auxiliary model. Rejected (3-5). QUOKA is training-free and shows stronger results. |
| LSH-E: LSH for KV Cache Compression | 3.83 | 1 | KV compression using cosine dissimilarity (similar geometric intuition). Rejected (1-6). QUOKA has a much stronger formulation and evaluation. |
| IntelLLM: KV Cache Compression | 3.00 | 1 | KV cache compression. Rejected. QUOKA is clearly stronger. |
| MixAttention | 2.00 | 1 | Inference-friendly architecture. Rejected. Not directly comparable. |
| PrefixQuant | 3.00 | 1 | Quantization method. Not directly comparable. |
| Cut Cross-Entropy | 8.50* (accidentally in 1.5-3.5 band) | 1 | Different topic (loss computation). Score 8.5 is misleading for comparison purposes. |

**Round 1 bracket:** Between 6.5 and 8.0. QUOKA clearly outperforms papers scored 4-6 (KV Prediction at 4.5, LSH-E at 3.83, OmniKV at 6.0) in terms of experimental thoroughness, baseline margins, and cross-hardware validation. FlexPrefill (8.0) is the closest comparison — both are training-free sparse attention for prefill — but QUOKA has stronger empirical margins and more comprehensive evaluation, while FlexPrefill has a more sophisticated dynamic adaptation mechanism. QUOKA's missing GPT-OSS-20B/32k entry in Table 1 and loose theorem prevent a clean 8.0.

**Final score:** 7.5. QUOKA is a strong paper with a novel geometric insight, large empirical margins, and practical cross-hardware validation. It is clearly above the 6.0 papers (OmniKV, Cascading KV) and approaches FlexPrefill (8.0) in quality. The missing table entry and loose theoretical formalization keep it from 8.0, but the core contribution — the cosine-dissimilarity observation leading to a simple, effective, portable sparse attention method — is well-supported and significant.

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>