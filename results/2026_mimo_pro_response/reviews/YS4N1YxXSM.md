Now I have enough calibration data. Let me finalize the review.

**Calibration analysis:**

**Round 1 bracket: 6.5–8.0**

Key anchors retrieved:
- FlexPrefill (8.00) — closest topical match, sparse attention for prefill, all 8s
- StreamingLLM (7.50) — efficient streaming with attention sinks
- Training-Free Activation Sparsity (7.50) — training-free inference speedup
- ZETA (7.00) — top-k attention via Z-order curves
- Radar (6.60) — training-free dynamic token selection
- HShare (6.80) — hierarchical KV sharing
- Selective Attention (6.75) — parameter-free attention improvement
- D2O (5.80) — dynamic KV cache optimization
- OmniKV (6.00) — KV cache selection for long context
- LazyLLM (5.00) — rejected, dynamic token pruning for prefill

**Round 2 narrowed bracket: 7.0–7.5**

QUOKA has stronger empirical margins (10–25 points on RULER) than most 6–7 range papers and broader hardware portability than FlexPrefill. However, its theorem is more suggestive than FlexPrefill's theoretical grounding, and latency is measured on only one model for TTFT. These balance out to place QUOKA just below FlexPrefill.

## Summary

QUOKA is a training-free, hardware-agnostic sparse attention algorithm for accelerating LLM inference during chunked prefill. The core insight is that queries with low cosine similarity to the mean query are the most influential for key selection; by prioritizing these queries and scoring keys via cosine similarity, QUOKA achieves near-dense accuracy while reducing KV pairs by up to 88%. The paper reports up to 5× attention speedup on NVIDIA GPUs, ~7× on CPUs, and 3× TTFT reduction, evaluated across 6 model families and 4 benchmarks.

## Strengths

- **Large, consistent accuracy margins over all baselines across multiple benchmarks and models**: Table 1 shows QUOKA achieving 57.01 on RULER at 32k for Llama3.2-3B vs. 31.73 for SampleAttn (next-best), with comparable margins across all 5 models. Table 3 shows 0.945 vs. 0.738 (28% relative improvement) on LongBench for Llama3.2-3B at B_SA=512 — these are among the largest margins reported for any sparse attention method in this space.

- **Novel query-geometry observation with empirical and theoretical support**: The insight that queries with low cosine similarity to the mean query attend broadly is validated by Figure 2c (correlation of 0.737 between S_q and max_k(A)), PCA visualization (Figure 2b), and Theorem 1 providing a geometric bound. This is a genuinely new angle compared to prior methods that treat queries homogeneously.

- **Hardware portability with real latency measurements across three distinct platforms**: Figure 5 reports measured speedups on NVIDIA A100 (~5× attention speedup), Intel Xeon CPU (~7×), and NVIDIA RTX 2080 (~5-6×). This is enabled by using only standard linear algebra operations (Algorithm 1), directly addressing portability limitations of kernel-level sparse attention methods.

- **Strong accuracy retention at 25% KV budget across 6 models**: Table 2 shows ≤3% accuracy loss at 25% compression ratio across all tested models including an MoE variant (Qwen3-30B-A3B), demonstrating practical scalability.

- **Efficient GQA pre-aggregation trick**: The linearity-based pre-aggregation (Section 3.3) reduces computation and memory by a factor of the number of KV groups, making the method especially efficient on modern GQA architectures.

- **Graceful degradation under parameter sweeps**: Tables 11-12 show <3% accuracy drop even with N_q = (1/16)B_CP, providing deployment flexibility across diverse hardware constraints.

## Weaknesses

### Fatal

None.

### Major

- **Missing GPT-OSS-20B / 32k entry in Table 1**: The QUOKA row for GPT-OSS-20B at 32k context length is blank (line 213 ends with `<b>57.79</b> |  |`), while all baselines report values for this setting. Since GPT-OSS-20B is one of the six evaluated models, this gap leaves one model-length combination unreported for the primary benchmark. The authors should either include the data or explain its absence.

### Minor

- **Theorem 1's connection to the scoring rule is suggestive rather than rigorous**: Theorem 1 provides a per-key, per-query geometric bound (Eq. 5), but the paper frames it as "formalizing" the selection criterion. The leap from "low CosSim(M_Q, q) is consistent with strong attention for a specific key-query pair" to "this scoring minimizes approximation error in Eq. (4)" is not formally proven. The heuristic works well empirically (Figure 2c, r=0.737), but the framing should be softened.

- **>1.0 normalized LongBench scores on Smollm3 are unexplained**: Table 3 shows QUOKA achieving 1.03 and 1.028 at B_SA=1024 and 2048 on Smollm3 (exceeding the dense baseline). If sparse attention acts as implicit regularization and improves over dense attention, this is a noteworthy finding that strengthens the paper — but only if acknowledged and discussed rather than left implicit.

- **Key ablation evidence deferred to appendix**: The cosine similarity vs. dot product ablation (Table 9) and Math500 generation results (Table 8) directly support stated contributions. Table 9 justifies the core scoring mechanism and Table 8 supports the claim of outperforming generation-specific methods. Both should be in the main text.

- **No variance/confidence intervals reported**: On synthetic benchmarks (NIAH, RULER) where prompt sampling could introduce variance, at least one standard deviation or range would strengthen the evidence.

### Trivial

- The "88% fewer key-value pairs" claim in the abstract maps to B_SA=1024 on ~8K context, but this configuration is not explicitly stated.

## Nice-to-Haves

- Latency evaluation on at least one additional model (e.g., Llama3.2-3B) to confirm speedups are architecture-independent beyond Qwen3-4B.
- A brief overhead analysis quantifying the wall-clock cost of the cosine similarity and top-k operations relative to the attention savings.
- An ablation comparing QUOKA against a kernel-level method under chunked vs. non-chunked prefill to empirically support the claim that kernel-level methods lose efficiency under chunked prefill.

## Removed Points

These points are flagged to be removed, treat them with caution.

- (No points were removed after filtering; all weaknesses survived scrutiny against the paper text.)

## Novel Insights

The paper's central insight — that queries with low cosine similarity to the mean query are the most influential for key selection — is genuinely novel and well-supported by both geometry (PCA visualization, Theorem 1) and empirical correlation (Figure 2c, r=0.737). This differs from prior work which treats queries homogeneously or selects based on per-query attention patterns. The observation that sparse attention can sometimes exceed dense attention accuracy (LongBench Smollm3) is also noteworthy, though the paper does not discuss it.

## Suggestions

- Move Tables 8 and 9 into the main text; they directly justify core claims.
- Discuss the >1.0 LongBench scores briefly — this could strengthen the contribution.
- Soften Theorem 1's framing to "motivated by" rather than "formalized through."
- Report at least one variance metric for RULER/NIAH results.
- Include the missing GPT-OSS-20B / 32k data or explain its absence.

## Reporting

**All retrieved anchors across rounds:**

| Paper | Avg Score | Round | Comparison |
|-------|-----------|-------|------------|
| FlexPrefill | 8.00 | 1,2 | Most topically similar; sparse prefill. QUOKA has larger margins, more hardware coverage, but weaker theory |
| StreamingLLM | 7.50 | 2 | Attention sinks, different focus but same inference optimization space |
| Training-Free Activation Sparsity | 7.50 | 2 | Training-free approach, complementary topic |
| Transformer-VQ | 7.33 | 2 | Linear-time attention via vector quantization, different approach |
| ZETA | 7.00 | 2 | Top-k attention method, methodological comparison |
| HShare | 6.80 | 1 | KV sharing for decoding. QUOKA has stronger margins |
| Selective Attention | 6.75 | 2 | Parameter-free attention modification |
| Radar | 6.60 | 2 | Training-free dynamic token selection. QUOKA has larger and more consistent margins |
| SharedContextBench | 6.50 | 2 | Long-context benchmarking paper |
| D2O | 5.80 | 1 | KV cache optimization. QUOKA clearly stronger |
| OmniKV | 6.00 | 1 | KV cache selection. QUOKA has larger margins |
| LazyLLM | 5.00 | 1 | Rejected, token pruning for prefill. QUOKA much stronger |
| IntelLLM | 3.00 | 1 | KV cache compression, reject-tier |
| Running Huge Context | 4.67 | 1 | KV pruning, reject-tier |
| SimLayerKV | 5.25 | 1 | Layer-level KV reduction, mid-tier |

**Bracketing:** Round 1 bracket was 6.5–8.0. Round 2 narrowed to 7.0–7.5 based on comparison with FlexPrefill (8.00, stronger theory, similar accuracy), Radar (6.60, weaker margins), and HShare (6.80, narrower evaluation). QUOKA's consistently large empirical margins (10–25 points on RULER over all baselines, 10–20%+ on LongBench), novel query-geometry insight, and three-platform hardware portability place it near the top of the 7.0–7.5 range. The missing table entry, suggestive (not rigorous) theorem, and deferred ablation tables prevent a higher score.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>