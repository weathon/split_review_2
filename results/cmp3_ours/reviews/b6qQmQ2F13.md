Now let me write the final consolidated review.

## Summary

This paper presents a systematic empirical study of memory–accuracy trade-offs for deploying reasoning models under fixed memory budgets. Through ~1,700 configurations across three model families (Qwen3 0.6B–32B, DeepSeek-R1-Distill, OpenReasoning-Nemotron), four benchmarks, three weight precisions, varied token budgets, parallel scaling, and KV cache compression, the authors find that optimal deployment strategies are scale-dependent — models with effective size below ~8-bit 4B benefit from prioritizing larger weights, while larger models benefit from longer generations. The key finding contradicts the scale-agnostic "4-bit is always optimal" narrative from prior non-reasoning model work.

## Strengths

- **Well-motivated and timely research question.** The paper clearly establishes why reasoning models differ from non-reasoning ones (KV cache dominates memory rather than weights, with a 1.8× ratio for Qwen3-4B at 32k tokens), cleanly motivating why prior conclusions do not automatically transfer.

- **Systematic, large-scale experimental design.** The sweep covers ~1,700 configurations across three model families (Qwen3 0.6B–32B, DeepSeek-R1-Distill, OpenReasoning-Nemotron), four benchmarks (AIME25, GPQA-Diamond, LiveCodeBench, MATH500), three weight precisions with multiple quantization schemes (GPTQ, AWQ, FP8), token budgets from 2k to 30k, group sizes up to 16, and two KV compression families (eviction via R-KV/StreamingLLM and quantization via HQQ). This is genuinely comprehensive for an empirical study.

- **Non-trivial, actionable findings.** The central result — that the memory-optimal strategy flips at a scale-dependent threshold — contradicts the established "4-bit is universally optimal" prescription and provides concrete deployment guidance (e.g., Finding 2: task-dependent precision sensitivity). These are exactly the kind of guidelines practitioners need.

- **Generalization checks across model families.** Validating key findings on DeepSeek-R1-Distill and OpenReasoning-Nemotron (Figures 6, 16) substantially strengthens the claim that the findings are not artifacts of the Qwen3 family.

- **Pareto-frontier framing.** Presenting results as Pareto frontiers (Figures 1–5, 8–9) is the correct analytical approach for multi-objective trade-offs and avoids cherry-picking individual configurations.

## Weaknesses

### Major

- **Internal inconsistency in Finding 5's threshold.** The paper states Finding 5's threshold inconsistently across locations. The introductory summary (line 49) and the end of the introduction (line 41) state "effective size smaller than an 8-bit 4B model," while the body (line 211) and formal Finding 5 box (line 221) state "smaller than an 8-bit 8B model." These thresholds differ by roughly 2× (~4.2 GB vs. ~8.9 GB). The abstract (line 9) correctly hedges. Furthermore, Findings 1 and 3 consistently use the 8-bit 4B threshold, and line 41 (end of intro) also claims Finding 5's threshold is 8-bit 4B. The evidence in Figure 9 supports the 8-bit 8B threshold (the 4B 16-bit model at ~7.49 GB shows eviction clearly outperforming quantization, which would not be "small" under the 4.2 GB threshold). The paper never acknowledges or explains the discrepancy. If the thresholds genuinely differ for different trade-offs (weight-vs-token vs. eviction-vs-quantization), that is itself an interesting finding that should be discussed. If it is an error, the current presentation is confusing.

- **No statistical uncertainty reported.** All accuracy values are point estimates without confidence intervals or variance measures. With 32 generations per instance at temperature 0.6 (8 for KV compression), sampling variability is non-trivial. This matters most for (a) determining Pareto frontier membership near the threshold, where noise could shift the reported boundary by one model size, and (b) the relative ordering of eviction vs. quantization strategies for small models (Figure 9), where differences near the frontier could be within noise. The core qualitative finding (scale-dependent trade-off exists) is robust, but the precision of *where* the threshold lies is overstated.

### Minor

- **Finding 2 rests primarily on one knowledge benchmark.** The claim that "4-bit weights are broadly memory-optimal for knowledge-intensive tasks" is supported mainly by GPQA-Diamond. One benchmark is thin ground for a general principle. This is acknowledged as a limitation but weakens the generality of the finding.

- **The conclusion reverts to raw parameter count.** The paper carefully distinguishes "effective size" (parameters × bits per weight) from raw parameter count throughout (line 73), but the conclusion (line 225–227) says "models under the 8B size" — conflating the two concepts. This is a minor but noticeable regression in precision.

- **Protocol ambiguity for accuracy computation.** Line 91 says "accuracy averaged over 32 generations per instance and sample" — it is unclear whether this is pass@1 estimation via independent sampling or some other aggregation. The parallel scaling experiments separately specify majority voting (line 159), implying the default is not majority voting, but this should be stated explicitly.

### Trivial

None.

## Nice-to-Haves

- A table reporting accuracy and total memory for key Pareto-optimal configurations would improve reproducibility and practical utility, complementing the figures.
- A deeper mechanistic discussion of *why* the threshold exists (e.g., showing accuracy vs. token budget per model size) would strengthen the paper.
- Discussion of the potential confound that small models may produce less diverse generations for parallel scaling with majority voting.

## Removed Points

These points from the input review are flagged to be removed, treat them with caution:

1. **Lines 23–27 characterization of prior work** — Minor clarification about Dettmers & Zettlemoyer's scope. The paper's characterization is fair for its purpose.
2. **Activation memory not discussed (lines 69–73)** — Scope creep. The paper scopes to weights + KV cache, which is standard for inference-focused studies.
3. **Hard-to-verify numbers from figures (lines 111–113)** — Figures are an acceptable presentation format for empirical results; tables would be a nice addition but their absence is not a weakness.
4. **Parallel scaling confound (lines 159–163)** — Moved to Nice-to-Haves as a speculative mechanism question, not a demonstrated flaw.
5. **Missing related works** — Removed per policy.
6. **Reproducibility nitpicks about undisclosed hyperparameters** — The paper provides sufficient detail for a study of this scale; full training logs would be impractical.
7. **Formatting/style nitpicks** — Removed per policy.
8. **Strength: addresses important problem** — Generic; removed per policy.

## Novel Insights

The reviews surface one genuinely novel observation beyond the paper's own contributions: the threshold for Finding 5 (KV eviction vs. quantization, stated as 8-bit 8B in the body) may genuinely differ from the threshold for Findings 1 and 3 (weight-vs-token allocation, 8-bit 4B). The paper's introductory framing implies a unified threshold but the evidence and inconsistent presentation suggest otherwise. Whether this reflects a genuine phenomenon (different trade-offs having different tipping points) or an error is worth clarifying. The reviews do not provide additional analysis beyond flagging the tension.

## Suggestions

1. **Resolve the threshold inconsistency** as the highest-priority fix: either correct lines 41/49 to match the body (8-bit 8B for Finding 5), or if the thresholds genuinely differ across trade-offs, explicitly acknowledge and explain why.
2. **Add confidence intervals or bootstrap estimates** for accuracy near the threshold boundary to assess the reliability of the reported threshold.
3. **Clarify the accuracy computation protocol** (pass@1 vs. alternative aggregation) in one sentence.
4. **Add at least one additional knowledge benchmark** (e.g., MMLU-Pro) to strengthen Finding 2's generality.
5. **Replace "models under the 8B size"** in the conclusion with the paper's established "effective size" terminology.

## Score and Decision

**Calibration anchors considered:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| Inference Scaling Laws (VNckp7JEHn.md) | 5.75 | Narrow | Similar empirical study of inference trade-offs; accepted with weaknesses about limited task scope. This paper is more comprehensive but has a more notable error (threshold inconsistency). |
| Cost of Scaling Down (ldJXXxPE0L.md) | 6.00 | Narrow | Empirical study of pruning effects on LLM capabilities; accepted. Comparable in nature and quality. |
| Inference Optimal VLMs (6VhDQP7WGX.md) | 5.80 | Bracket | Empirical trade-off study for VLMs; accepted. This paper covers more factors and model families. |
| IntelLLM (4QWPCTLq20.md) | 3.00 | Bracket | KV cache compression method; rejected due to limited novelty and evaluation issues. Not comparable — this paper is an empirical study, not a method paper. |
| Scaling Laws for Precision (wg1PCg3CUP.md) | 8.00 | Bracket | Strong scaling law paper with formal theory and thorough experiments. This paper lacks the theoretical framework to reach this tier. |

**Round 1 bracket:** 5.5 – 6.5 (based on comparison with Inference Scaling Laws at 5.75 and Cost of Scaling Down at 6.00).

**Final score:** 6.0

**Rationale:** The paper makes a genuine contribution through its systematic empirical study of a timely and practical problem. The findings are actionable and contradict established wisdom. However, the internal inconsistency in Finding 5's threshold is a concrete error that weakens the paper's coherence, and the absence of any uncertainty quantification limits the precision of the claims. These are fixable issues, and with corrections the paper would be stronger. The score reflects a solid borderline accept: the contribution is real but the presentation has a notable flaw that needs resolution.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>