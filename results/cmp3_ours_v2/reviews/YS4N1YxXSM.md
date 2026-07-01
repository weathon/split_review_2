Now I have a clear picture. Let me write the final consolidated review.

## Summary
QUOKA proposes a query-oriented sparse attention method for chunked prefill inference in LLMs. The key insight — that queries with low cosine similarity to the mean query interact more strongly with more keys and matter most for attention — motivates a training-free method that first subselects representative queries, then uses cosine-similarity scoring to pick the most relevant keys. The method achieves 3× TTFT reduction and 5× attention speedup using only standard linear algebra ops, not custom kernels.

## Strengths

1. **Genuinely novel insight for the chunked-prefill setting.** The core observation (Section 3.1) — that queries with low cosine similarity to the mean query contribute disproportionately to attention — is specific to the multi-query prefill case and does not trivially carry over from single-query decode methods. This motivates a non-obvious design (discard near-mean queries), supported by geometric reasoning and an empirical correlation of 0.737 (Figure 2c). This distinguishes QUOKA from methods that naively average across all queries in a chunk.

2. **Strong empirical accuracy across multiple model families and benchmarks.** QUOKA outperforms all baselines by 10–20+ points on RULER at B_SA=1024 (Table 1) and maintains ≥0.945 normalized accuracy on LongBench at B_SA=1024 across four model families, compared to ≤0.929 for the next-best baseline (Table 3). Evaluation covers five model families (Llama3, Qwen2.5, Qwen3, SmollM, GPT-OSS) including MoE and NoPE variants, supporting the generalization claim.

3. **Hardware portability is a genuine differentiator.** QUOKA's reliance on standard linear algebra (cosine similarity, top-k, gather) rather than custom CUDA kernels is a real advantage over pattern-based and kernel-level sparse attention methods. CPU speedups of 5–7× (Figures 5c–5d) demonstrate this concretely, not as a vague architectural claim.

## Weaknesses

### Major

1. **QUOKA matching or exceeding dense-attention baselines in several settings is reported without discussion or explanation.** Table 3 shows normalized scores of 1.03 and 1.028 for Smollm3 at B_SA=1024/2048 — exceeding the dense-attention baseline (1.0). Section 4.4 states QUOKA "in some cases surpasses the accuracy of dense attention." The paper offers no hypothesis for why this occurs (e.g., regularization effect, noise filtering, evaluation artifact, or baseline misconfiguration). This is not a minor omission: without an explanation, the reader cannot assess whether the accuracy comparisons are meaningful or whether the dense baseline is correctly configured for the chunked-prefill setting. While the relative ordering between QUOKA and other sparse methods remains trustworthy, the absolute comparison to dense attention is ambiguous.

2. **Theorem 1 is confusingly presented and does not clearly support the method.** The quantity q* is never defined (only q₀ is introduced in the premise). The bound CosSim(M_Q, q*) ≤ 1 + α_qβ_q − 0.5α_q² − 0.5β_q² simplifies to CosSim(M_Q, q*) ≤ 1 − 0.5(α_q − β_q)², which is an upper bound on a quantity already bounded by 1, making it informative only in extreme cases where |α_q − β_q| is large. The connection from this bound to the selection criterion S_q = −CosSim(M_Q, q*) is not clearly drawn. The paper's empirical motivation (Figure 2) is far more compelling than the theorem; the theorem should either be repaired (define q*, clarify how the bound guarantees S_q is large) or removed.

### Minor

3. **Baseline comparison is tilted toward decode-oriented methods.** SparQ, Loki, and LessIsMore are designed for single-query generation, not multi-query prefill, which disadvantages them. Pattern-based and kernel-level prefill methods (e.g., block-sparse FlashAttention variants, MInference) are excluded on portability grounds. While the portability focus is a legitimate design choice, including a subset of kernel-level prefill methods with a clear discussion of the portability trade-off would strengthen the comparison. Additionally, SnapKV and KeyDif appear only in the RULER table and not in LongBench or latency experiments, making the comparison inconsistent across benchmarks.

4. **The overhead of QUOKA's selection pipeline is not isolated from the reported speedups.** The net speedup (attention savings minus selection overhead) is reported in Figures 5a–5d, but there is no breakdown of where time is spent across the multiple selection steps (mean query computation, cosine similarity, top-k over queries, normalization, pre-aggregation, scoring, top-k over keys, gather). Without this at varying sequence lengths, the reader cannot assess whether the selection overhead becomes a meaningful fraction of total time at shorter contexts or smaller budgets.

### Trivial

5. **N_Q default specification is inconsistent.** The paper states "QUOKA and SAMPLEATTENTION subselect 16 queries at a time" but the ablation section gives N_q = (1/16)B_CP, which for B_CP=128 gives N_Q=8. The default N_Q should be stated clearly.

6. **Figure 2 shows only layer 0, head 11.** While the correlation is clear for this specific case, showing that the pattern holds across layers (especially early vs. late layers) and heads would strengthen the empirical motivation.

7. **GPT-OSS-20B entry at 32k is blank in Table 1.** If it represents a failed/out-of-memory experiment this should be noted.

## Nice-to-Haves

- **Explain why QUOKA exceeds dense attention** in some settings — this could reveal a more interesting finding about sparse attention acting as a denoising regularizer for long-context tasks.
- **Add a latency breakdown** isolating selection overhead from attention savings across sequence lengths.
- **Report variance or significance** for accuracy numbers where margins between methods are small.
- **Include per-layer/per-head analysis** of the query subselection effectiveness to validate that the correlation in Figure 2 generalizes.

## Removed Points

- "Theorem 1 RHS ranges in [−0.5, 2], making the bound vacuous" — The critic's claimed range is incorrect; the RHS 1 − 0.5(α−β)² ranges in [−1, 1] for α,β ∈ [−1,1]. The substantive criticism (undefined q*, unclear connection to selection) is retained in Major Weakness 2 above.
- Missing appendix tables (5, 6, 8, 9, 10, 11, 12) — These are appendix tables stripped by the parser; per evaluation rules, this criticism is removed.
- "Loki shows anomalously low scores for Smollm3" — This is reporting experimental results, not a weakness of the paper.
- "88% fewer KV pairs should be contextualized" — Minor presentation nitpick, removed.
- Missing related works — Cannot be confirmed without external sources.
- Generic reproducibility concerns about hyperparameters / implementation details.

## Novel Insights

The harsh critic's observation that the "exceeding dense attention" phenomenon could be the paper's most interesting finding if explored properly is genuinely novel. The current paper treats it as a throwaway observation; if the authors investigated whether sparse query selection acts as a denoising regularizer (removing queries that attend to shared, uninformative keys), this could strengthen both the paper and the community's understanding of sparse attention. Beyond this, no novel insight emerges beyond the paper's own contributions.

## Suggestions

1. **Address the "exceeding dense attention" cases head-on.** Either (a) explain the phenomenon as a regularizer effect (and add supporting analysis), or (b) acknowledge it as a baseline configuration issue and correct the comparisons. Do not leave it unexplained.
2. **Repair or remove Theorem 1.** If retained, define q*, explicitly connect the bound to S_q being large, and state the specific conditions under which the bound is non-vacuous. If the theorem cannot be sharpened, drop it and rely on the empirical motivation (Figure 2), which is sufficient.
3. **Isolate selection overhead in the speedup results.** Add a breakdown table or figure showing time spent on each step of Algorithm 1 vs. the reduced attention computation.
4. **Clarify the default N_Q** and fix the inconsistency between "16 queries" and N_q = (1/16)B_CP.

## Score and Decision

**Initial bracket (Round 1):** The paper sits between 5.5 and 7.0 after comparing against:
- HASA (5.00, Reject) — weaker novelty, less comprehensive evaluation. QUOKA is clearly stronger.
- LazyLLM (5.00, Reject) — similar framing but weaker accuracy results. QUOKA is stronger.
- HiP (6.25, Accept) — similar training-free approach for prefill, comparable evaluation. QUOKA's query-subselection insight is more novel, but HiP's evaluation is more polished.
- Cascading KV Cache (6.00, Accept) — similar scope and contribution level. Comparable strength.
- OmniKV (6.00, Accept) — similar contribution level with some baseline concerns. Comparable.
- FlexPrefill (8.00, Accept) — stronger presentation and cleaner evaluation. QUOKA is less polished.

**Final score:** 6.0

**Decision rationale:** QUOKA makes a solid contribution with a genuinely novel geometric insight and strong empirical results across diverse models and benchmarks. However, the unexplained cases of exceeding dense attention introduce ambiguity in the evaluation, and Theorem 1 is presented in a confused state that detracts from rather than supports the method. These are addressable issues, and with revisions (explain the dense-attention comparison, repair or drop the theorem, isolate selection overhead) the paper would make a strong contribution to efficient LLM inference.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>