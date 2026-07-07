Now I have enough to finalize the review.

**Round 1 bracket: 6–8**, anchored by FlexPrefill (8.0, very similar topic — dynamic sparse attention for LLM prefill, all-accept across reviewers). QUOKA's empirical breadth is stronger than FlexPrefill's and its hardware-agnostic novelty is clear. However, the algorithm description ambiguity and missing full-attention baseline in Table 1 are real presentation gaps. These push slightly below 8.0. **Final bracket: 6.5–7.5 → score 7.0**.

---

## Summary
QUOKA is a training-free, hardware-agnostic sparse attention algorithm for LLM prefill under chunked prefill. It selects representative queries by cosine dissimilarity from the mean query, scores keys via cosine similarity, and aggregates over queries (max) and GQA groups (mean, with a pre-aggregation trick that reduces cost by the GQA ratio). Experiments span five model families (including MoE and NoPE variants), three hardware platforms, and four long-context benchmarks, showing near-lossless accuracy at 25% KV budget and up to 5× attention speedup.

## Strengths
- **Novel geometric observation grounded empirically (Section 3.1, Figure 2c):** Queries with low cosine similarity to the mean query have higher max attention scores (correlation 0.737 on the shown head) and attend more broadly to keys. This provides a distinct and well-motivated selection criterion compared to uniform sampling (SampleAttention).
- **Pre-aggregation via GQA linearity is a concrete efficiency contribution (Section 3.3):** Normalizing Q and K before scoring allows averaging normalized queries across GQA groups due to linearity of the mean and the outer product QK^T. This reduces scoring cost by a factor equal to the GQA ratio — large in modern models like Qwen3 and GPT-OSS — and is cleanly implementable.
- **Unusually broad validation:** Table 1 covers five model families (Llama3, Qwen2.5, Qwen3, SmolLM3, GPT-OSS) including MoE-FFN and NoPE variants; Table 2 provides direct comparison against full attention across six models; latency measured on A100, RTX 2080, and Intel Xeon CPU.
- **Table 2 (QUOKA at 25% budget vs. full attention on RULER) is credible and strong:** At most ~3-point absolute degradation across all models and lengths up to 32k — the most honest and interpretable experiment in the paper.
- **Table 3 LongBench margins are large and robust:** QUOKA achieves 0.945 normalized accuracy at budget 512 vs. best baseline (SampleAttention) at 0.738 for Llama3.2-3B-Instruct; >20-point margin persists across all four model families and all three budgets.

## Weaknesses

### Fatal
None.

### Major
- **Algorithm description is ambiguous about non-selected queries.** Algorithm 1 lines 1–4 overwrite Q with the top-N_Q subselected queries (`Q ← gather(topk(-S_Q, N_Q), Q)`) and then outputs K*, V* from this reduced Q. The algorithm as written does not state that all B_CP original queries attend to K*, V* in the downstream attention call. A reader implementing Algorithm 1 literally would silently drop B_CP − N_Q queries, producing corrupted hidden states. Section 3.4 says "the resulting subset of keys and values is then passed to the attention computation for that chunk," but does not clarify whether all original queries receive output. Table 2's near-lossless RULER results confirm the implementation is correct (interpretation: N_Q queries are used only for KV *scoring*, then all B_CP queries attend to K*, V*), but this must be stated explicitly in Algorithm 1 or its surrounding text. The Reproducibility Statement claims the method is "straightforward to implement" — this claim is undermined by this gap.

- **Full attention baseline absent from Table 1.** Table 1 (RULER, B_SA=1024) shows QUOKA at 57.01 on Llama 32k but no full attention column. Without it, readers cannot judge whether 57 represents near-lossless performance or severe degradation. Table 2 shows full attention at ~76 on the same model at 32k (under the 25% budget condition), but uses a different budget setup. The fixed-budget Table 1 needs a reference column for correct interpretation.

### Minor
- **Theorem 1 scope is overstated.** Theorem 1 (Eq. 5) proves a bound on CosSim(M_Q, q*) under the precondition CosSim(M_Q, k) < 0 — that the mean query is negatively correlated with key k. This precondition is not guaranteed in general and is not verified empirically. Furthermore, the theorem bounds CosSim(M_Q, q*), not max_k(A) — the connection to "queries with low S_q attend to more keys" requires an additional argument that is absent. The empirical evidence in Figure 2c is more convincing than the theorem; the paper should characterize Theorem 1 as a geometric intuition rather than a proof of the selection criterion's correctness.

- **Motivating observation from a single layer/head (Figure 2).** The core evidence (S_q vs. max_k(A) correlation) is shown for "Llama 3.2-3B-Instruct, layer 0 head 11" only. Layer 0 is atypical in most transformers (processes raw embeddings before any cross-layer context). Showing this correlation across early, middle, and late layers would substantially strengthen the motivating premise.

- **"Surpasses dense attention" claim on Math500 (Section 4.4, Section 6) should be attributed to noise.** A sparse approximation cannot systematically outperform exact attention on a reasoning benchmark in expectation. The observed cases (also visible in Table 3 where Smollm3 at budgets 1024 and 2048 shows normalized accuracy >1.0) are sampling variance, and the paper should say so plainly rather than highlighting them as results.

### Trivial
None.

## Nice-to-Haves
- Extending the chunk size sweep (Table 11 ablates B_CP for QUOKA alone) to also plot accuracy for SampleAttention across chunk sizes would directly demonstrate when and why QUOKA's selection criterion provides advantages over uniform sampling as chunking structure changes — the paper's central narrative.
- Explicitly stating in Section 4.6 that the reported speedup figures are end-to-end attention module time (including the QUOKA selection step overhead) rather than just the downstream attention call.
- Extending Figure 2c to show S_q vs. max_k(A) across a representative sample of layers would validate that the motivating geometric observation is not layer-0-specific.

## Removed Points
*These points are flagged to be removed, treat them with caution.*

- **Comparison fairness / inflated margin (Harsh Critic §2):** The critic argues that the large margins in Tables 1 and 3 partially reflect putting baselines in a hostile setting (chunked prefill) they were not designed for. Removed because: the paper's explicit contribution is a method for chunked prefill, and evaluating all methods in the chunked prefill setting is the correct evaluation. The asymmetry favors the baselines in a hostile setting — not an inflated advantage for QUOKA. Per filtering rules, comparisons that disfavor the baseline in an unfair setting are not a weakness.

- **Missing kernel-based methods from accuracy tables:** The critic notes that Lai et al. 2025, Zhang et al. 2025, Jiang et al. 2024 are not compared in accuracy tables. The paper justifies exclusion via portability arguments and compares to them as related work in Section 5. Removed as reasonable scope management.

- **Sink-token artifact analysis:** The critic suggests max-aggregation over queries may be dominated by sink-token queries. Figure 2c explicitly excludes the sink token. No specific evidence of the problem is identified in the paper. Removed as speculation.

- **Strength (broad applicability claim):** The claim that QUOKA "applies to generation" via Math500 is generic and partially contradicted by the verified "surpasses dense" noise issue. Retained only in weakened form above.

## Novel Insights
The asymmetric aggregation design in Section 3.3 — max over queries but mean over GQA groups — is motivated by empirical tail-distribution differences (Figure 3) and supported by ablations (Tables 9, 10). Combined with the pre-aggregation trick (normalizing Q/K before scoring allows averaging across GQA groups via linearity), this yields an architecture-aware efficiency gain that is underappreciated in related work. The identification that query geometry (cosine dissimilarity from the mean) is a better proxy for KV relevance than uniform sampling in multi-query settings is the paper's most transferable insight and could inform future work on query-dependent sparse attention beyond chunked prefill.

## Suggestions
- **Algorithm 1:** Add a line after line 12 or a textual note explicitly stating that K*, V* are used as inputs to a dense attention kernel applied to the *original full set* of B_CP queries (not just the N_Q selected ones). This resolves the algorithm ambiguity without any change to the method.
- **Table 1:** Add a "Full Attention" reference row to make QUOKA's absolute scores interpretable in isolation.
- **Theorem 1:** Revise the surrounding text to characterize the theorem as supporting geometric intuition rather than proving the selection criterion's optimality. Alternatively, add an empirical check that the precondition CosSim(M_Q, k) < 0 holds in representative heads.
- **Math500 / LongBench>1.0 results:** Add a sentence explicitly attributing these to sampling variance.

---

## Score and Decision

**Anchor papers and comparison:**

| Paper | Path | Avg Score | Round | Comparison |
|---|---|---|---|---|
| FlexPrefill (sparse attention for LLM prefill) | OfjIlbelrT.md | 8.0 | R1 | Most topically similar; QUOKA has comparable novelty, broader hardware/model coverage, but larger algorithm-description gap |
| Partial Contexts (long-context training+inference) | TrKRpaOk8y.md | 6.4 | R1 | Lower score; QUOKA's contributions are cleaner and more hardware-agnostic |
| OmniKV (dynamic context selection) | ulCAPXYXfa.md | 6.0 | R1 | Similar scope; QUOKA's empirical breadth and accuracy margins are stronger |
| ShadowKV (long-context KV cache throughput) | vHO9mU87dc.md | 6.0 | R1 | Mixed 5–8 scores; QUOKA has cleaner unified method |
| ChunkAttention (KV sharing + chunking) | 9k27IITeAZ.md | 4.5 | R1 | Rejected; weaker contributions |
| HASA (sparse attention for prefill) | Hjk1tWIdvL.md | 5.0 | R1 | Rejected; QUOKA has substantially stronger empirical results and hardware portability |
| IntelLLM (KV cache compression) | 4QWPCTLq20.md | 3.0 | R1 | Rejected; weaker novelty |
| Cascading KV Cache | dSneEp59yX.md | 6.0 | R1 | Borderline accept; QUOKA's method is more principled |

**Round 1 bracket:** 6–8. FlexPrefill at 8.0 is the closest topical anchor and is accepted; QUOKA matches or exceeds it in empirical breadth and hardware-agnostic novelty.

**Narrowing:** The two major weaknesses (algorithm description ambiguity, missing baseline column) are presentation gaps, not methodological flaws — Table 2 proves the method works. These warrant requiring revisions but do not pull the score below acceptance threshold. The geometric observation and GQA pre-aggregation trick are genuine contributions. Placing QUOKA slightly below FlexPrefill (which had a cleaner presentation and no algorithm ambiguity) gives **7.0**.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>