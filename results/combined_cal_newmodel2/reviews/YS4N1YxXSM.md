Now I have all the calibration data I need. Let me produce the final review.

**Round 1 bracket**: Based on comparison with FlexPrefill (8.00), HASA (5.00), and LazyLLM (5.00), I placed QUOKA between 6 and 8 (above HASA/LazyLLM, below FlexPrefill).

**Narrowing**: Comparing against Cascading KV Cache (6.00), OmniKV (6.00), and HiP (6.25), QUOKA has stronger empirical results and more novel core insight but drag from the flawed Theorem 1. Final score: 6.5.

Anchors used across rounds:
1. **FlexPrefill** (8.00) — cleaner theoretical framing, similar topic, accepted 8/8/8/8
2. **HASA** (5.00) — limited novelty, rejected 5/5/5
3. **LazyLLM** (5.00) — hyperparameter sensitivity, mixed reviews (3/6/5/6)
4. **Cascading KV Cache** (6.00) — accepted 6/6/6/6, weak baselines concern
5. **OmniKV** (6.00) — accepted 6/6/6/6, practical serving integration concerns
6. **HiP** (6.25) — accepted 6/8/5/6, reliance on attention locality assumption

Now writing the final review:

## Summary
QUOKA presents a training-free, hardware-agnostic sparse attention method for accelerating LLM prefill under chunked prefill. ...

## Strengths
...

## Weaknesses
### Major
- Theorem 1 issue

### Minor
- KV cache ambiguity
- Math500 claim
- No variance
- Overhead breakdown

### Trivial
- None

Then score 6.5, decision Accept.**Calibration Summary:**

**Round 1 — Bracketing**: Retrieved anchors across all score bands. Most topically relevant:
- **FlexPrefill** (8.00, accept 8/8/8/8): clean theory, strong experiments, accepted
- **HASA** (5.00, reject 5/5/5): limited novelty, rejected
- **LazyLLM** (5.00, mixed 3/6/5/6): hyperparameter sensitivity, rejected  

Initial bracket: QUOKA sits between 5.00 and 8.00 — above HASA/LazyLLM (stronger novelty and results), below FlexPrefill (cleaner theory).

**Round 2 — Narrowing**: Retrieved mid-range anchors 6.00–6.25:
- **Cascading KV Cache** (6.00): accepted 6/6/6/6, weak baselines concern
- **OmniKV** (6.00): accepted 6/6/6/6, serving integration concerns
- **HiP** (6.25): accepted 6/8/5/6, reliance on attention locality

QUOKA's highest-strength favorabilities (15.31, 14.99) exceed all mid-range anchors' best items, but the Theorem 1 weakness (favorability -3.25) is a genuine negative not present in FlexPrefill (8.00, whose weakest item is +0.56). This places QUOKA clearly above the 5–6 cluster but below the 8-level benchmark.

**Final score**: **6.5** / **Accept**

---

## Summary

QUOKA proposes a training-free, hardware-agnostic sparse attention method for LLM chunked prefill. Its core idea is a geometric observation: queries with low cosine similarity to the mean query account for most key interactions, while near-mean queries concentrate on a small shared key set. QUOKA leverages this by (1) retaining only the most informative queries (low cosine-similarity to the mean) and (2) subselecting keys with high cosine similarity to those queries. The method is validated on Needle-In-A-Haystack, RULER, LongBench, and Math500 across Llama3, Qwen3, SmollM, and GPT-OSS model families, achieving near-dense accuracy with large margins over existing sparse attention baselines, along with 3–7× latency speedups.

## Strengths

- **A genuinely novel empirical observation about query geometry (Section 3.1, Figure 2).** The paper identifies that queries with low cosine similarity to the mean query interact with more keys while near-mean queries concentrate on a small shared set. This observation is clearly presented, appears to be novel, and is the well-motivated core that drives the method. [favorability=15.31]

- **Very strong accuracy results at high sparsity across multiple benchmarks.** On RULER (Table 1) at 32k context with B_SA=1024, QUOKA scores 57.01 on Llama3.2-3B versus 31.73 for SampleAttn and 31.14 for SparQ — roughly an 80% relative improvement. On LongBench (Table 3), QUOKA achieves 0.945 normalized accuracy at B_SA=512 versus 0.738 for the next-best method. These large and consistent margins hold across five model families. [favorability=14.99]

- **Training-free and hardware-agnostic design.** The method uses only standard linear algebra operations (cosine similarity, mean, top-k, gather), making it compatible with FlashAttention and deployable on CPUs and consumer GPUs without custom CUDA kernels — a genuine practical advantage. [favorability=7.32]

- **Thorough baseline comparison and ablation.** The paper compares against four sparse attention baselines (SampleAttention, LessIsMore, SparQ, Loki) across multiple models and budget settings. The ablation study (Section 4.5) examines B_SA, B_CP, and N_Q, showing graceful degradation, and additional ablations in the appendix isolate the contributions of query subselection, cosine scoring, and max-aggregation. [favorability=12.39]

## Weaknesses

### Major

- **Theorem 1 does not provide the theoretical justification the paper claims and contains notation issues.** The theorem introduces q₀ and q^* without clearly distinguishing them; q^* appears undefined in the bound. It provides an upper bound on CosSim(M_Q, q^*) that does not obviously connect to the selection criterion S_q = -CosSim(M_Q, q^*). The paper claims the theorem shows that "queries attending strongly to keys produce large selection scores," but an upper bound does not establish this — it neither proves tightness nor relates the bound expression to the actual selection decision. The empirical evidence in Figure 2 is the real contribution. Since the paper's contribution is fundamentally empirical, the theorem as presented creates a misleading impression of formal rigor without delivering it. The paper would be stronger by either dropping the theorem or replacing it with a clear statement of the empirical geometric finding. [favorability=-3.25]

### Minor

- **Ambiguity about KV cache management across chunks (Section 3.4).** When QUOKA selects a subset K^*, V^* from the accumulated [K_i | K_{<i}], it is unclear whether the dropped keys are discarded from the cache permanently or retained for future chunks but simply not used in the current chunk's attention. The phrase "reducing the KV budget" suggests truncation, but the accuracy results do not depend on this distinction. A single clarifying sentence would resolve the ambiguity. [favorability=5.85]

- **The claim of surpassing dense attention on Math500 (Section 4.4) is stated without caveats.** The paper reports that QUOKA "in some cases even surpasses the accuracy of dense attention" but offers no discussion of possible explanations (variance from the small 500-example set, beneficial regularization from sparsity, or chunked-prefill baseline degradation). This claim appears in both Section 4.4 and the Conclusion. Adding a brief qualification would prevent potential overinterpretation. [favorability=4.90]

- **No measures of variance for accuracy benchmarks.** All RULER and LongBench results are point estimates. While single-run evaluation is standard practice in this subfield and the margins over baselines are large enough that statistical significance is likely, confidence intervals or multiple-run statistics would strengthen confidence, particularly for the Math500 result. [favorability=3.96]

- **Selection overhead is not broken out from attention time.** The reported speedups are net measurements (including all selection overhead), so they are not misleading. However, a breakdown showing selection time vs. attention time for a representative configuration would help readers understand where costs lie, especially at smaller B_SA and B_CP settings where overhead may be proportionally larger. [favorability=7.92]

### Trivial

None.

## Nice-to-Haves

- Report absolute latencies (in ms) alongside speedups for a few representative settings.
- Add a brief intuitive explanation of the pre-aggregation trick (Section 3.3) in plain language.

## Removed Points

These points are flagged to be removed; treat them with caution.
- "The 88% claim in abstract lacks context" — The paper's budget settings are specified throughout; the abstract reports one representative setting.
- "Cosine similarity is overstated as a proxy for softmax" — The paper frames it as a "proxy" (not an equivalent) and provides empirical evidence (Table 9) showing it improves over dot product.
- "No absolute latency numbers" — Relative speedups are standard in this literature and make comparisons hardware-agnostic.
- "Section 2.2 generation discussion is tangential" — This is standard context-setting for a sparse attention paper.
- Various formatting nitpicks and claims about missing appendix content (the parser strips appendices).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Drop or substantially rewrite Theorem 1.** The empirical geometric observation (Figure 2) is the actual contribution; the theorem as written does not provide rigorous grounding and risks misleading readers. A concise statement of the empirical finding suffices.
2. **Clarify the KV cache management protocol** — state explicitly whether non-selected keys are retained in the cache between chunks or discarded.
3. **Add a brief caveat to the Math500 dense-surpassing result** (e.g., "this may reflect variance or beneficial regularization from sparsity").
4. **Provide a selection-time vs. attention-time breakdown** for at least one representative configuration.

---

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>