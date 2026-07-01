## Summary

This paper presents a large-scale empirical study (1,700+ configurations) of memory-accuracy trade-offs for reasoning models. It finds that optimal memory allocation is scale-dependent: for small models (effective size below ~4.2 GB for weight-vs-generation decisions), memory is better spent on larger weights; for large models, it is better spent on longer generations or parallel sampling. The paper also examines KV cache compression, showing eviction generally outperforms quantization for smaller models while both are competitive for larger ones.

## Strengths

1. **Timely and practically motivated problem.** The paper correctly identifies that reasoning models have fundamentally different memory profiles (KV cache dominates) than non-reasoning models, and rigorously tests whether prior memory-optimization advice transfers. This gap is genuine and the reformulation around memory rather than FLOPs is well-motivated.

2. **Large-scale systematic exploration.** The study spans ~1,700 configurations across three model families (Qwen3, DeepSeek-R1-Distill, OpenReasoning-Nemotron), four benchmarks, multiple weight precisions, token budgets up to 30k, parallel scaling up to 16 samples, and two KV cache compression families. This is a substantial empirical effort.

3. **Non-obvious scale-dependent findings.** The central result — that smaller models benefit from allocating memory to weights while larger models benefit from longer generations — is genuinely informative. The finding that this same threshold determines when parallel scaling becomes worthwhile (Finding 3) and when eviction beats quantization (Finding 5) adds practical value.

4. **Validation across model families and quantization schemes.** The paper checks that main Qwen3 results hold for DeepSeek-R1-Distill and OpenReasoning-Nemotron, and replicates key experiments with AWQ and FP8 quantization. This increases confidence the findings are not artifacts of a single architecture or quantization algorithm.

## Weaknesses

### Fatal

None.

### Major

1. **Internal inconsistency in the Finding 5 threshold (8-bit 4B vs. 8-bit 8B).** The enumerated findings at the end of the introduction (line 49) and the introductory summary (line 41) state that KV cache eviction is better than quantization for models with effective size **below 8-bit 4B**. However, the detailed Section 5 body text (lines 211, 217) and the formal Finding 5 statement (line 221) consistently state the threshold as **8-bit 8B**. These differ by a factor of 2 in effective size (~4.2 GB vs. ~8 GB). A practitioner reading different parts of the paper would receive different recommendations. The paper must resolve this contradiction — either by determining the correct threshold and unifying the language throughout, or by explicitly acknowledging that the eviction-vs-quantization threshold genuinely differs from the weight-vs-generation threshold (4B) and explaining why.

2. **The governing threshold (~4.2 GB / 8-bit 4B) is treated as a universal numerical guideline without discussing its provenance.** The threshold used for Findings 1 and 3 directly corresponds to the Qwen3-4B model at 8-bit — one specific model in one family. The paper does not discuss what architectural parameters determine this threshold (e.g., ratio of KV cache to weight memory, model capability saturation per parameter), whether it generalizes numerically (as opposed to qualitatively) to other families, or how practitioners should estimate it for their own models. The cross-family validation (DeepSeek-R1-Distill, OpenReasoning-Nemotron) confirms the *qualitative pattern* of a scale-dependent shift, but does not validate the specific ~4.2 GB value. The conclusion (line 227) notes the inflection point "may change," but the findings are stated as crisp numerical thresholds throughout. This weakens the "principled guidelines" the paper claims.

### Minor

1. **No uncertainty quantification.** The paper reports accuracy averaged over 32 generations per instance (line 91) and 8 generations for KV cache experiments (line 185), but never reports confidence intervals, standard errors, or statistical significance. Many comparisons involve close configurations on Pareto frontiers (e.g., 8B-8bit vs 14B-4bit in Figure 1). Without error bars, the reader cannot assess whether configurations near the frontier are genuinely distinguishable or within noise. Adding bootstrap confidence intervals for the key Pareto plots is straightforward given the available generations and would substantially strengthen the empirical support for categorical claims.

2. **The latency claim on line 111 overreaches the paper's evidence.** The paper states that certain configurations "are also faster because end-to-end latency is dominated by the token budget, making the choice to increase the model's effective size strictly dominant." This claim about speed being "strictly dominant" goes beyond what a memory-focused analysis can support without detailed latency profiling, and the referenced Appendix C.1 is unavailable for verification. The paper should either present the supporting evidence in the main text or weaken the claim.

3. **The PRM evaluation (Section 4.1) is based on a single verifier.** The paper states that "the external verifier is consistently memory-inefficient" based on ActPRM-X (7B). A single 7B PRM may not represent the full space of verifier-based methods (smaller PRMs, LoRA-adapted verifiers, learned verifiers without separate forward passes). The claim is somewhat stronger than the evidence supports, though the Limitations section does partially acknowledge this.

4. **Finding 4 ("Weight quantization alone is not sufficient") is a weak headline.** The finding that KV cache compression further improves the frontier beyond weight-only compression is nearly inevitable — compressing an additional memory component will naturally expand the frontier. The real substantive contribution on KV cache compression is Finding 5 (which strategy and when). Merging Findings 4 and 5 would be clearer.

### Trivial

1. **Table 1 shows identical KV cache sizes for Qwen3-0.6B and Qwen3-1.7B** (both 0.21, 1.92, 3.20 GB at the same token budgets). This may be correct if the models share the same layer count and KV head dimensions, but the paper does not note this, and the reader may find it suspicious. A brief explanation would help.

## Nice-to-Haves

- Add bootstrap confidence intervals to key Pareto frontier plots (Figures 1, 5, 8).
- Discuss what architectural parameters (layer count, head dimension, hidden dimension ratio) determine the effective-size threshold, to help practitioners extrapolate to new models.
- Include one additional knowledge-intensive benchmark (e.g., MMLU-Pro) to strengthen the task-specific Finding 2.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Grammar/style nitpick about abstract phrasing "8-bit 4B parameters":** This is a minor wording issue; removed per formatting-nitpick rule.
- **Introduction framing about 32B 8-bit vs 32B 4-bit being misleading:** This is a subjective interpretation of a pedagogical example; the example is not misleading and is consistent with the paper's framework of effective size.
- **Criticism about Finding 4 being "tautological":** While Finding 4 is not surprising, calling it "tautological" is inaccurate — it is non-obvious that KV cache compression still helps significantly after aggressive weight quantization. The criticism is overstated.
- **"Missing related work":** Removed per instructions (cannot confirm existence of missing works).
- **Speculative concerns about the appendix's content:** Any claims about what the appendix "may" or "may not" contain are removed as unverifiable.
- **General reproducibility nitpicks about undisclosed hyperparameters:** Removed per hard rules; the paper provides adequate experimental detail for an empirical study of this scale.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Resolve the Finding 5 threshold immediately.** Determine whether 8-bit 4B or 8-bit 8B is the correct threshold for the eviction-vs-quantization trade-off. If the correct threshold is 8B (as the body text suggests), update the enumerated findings and intro summary accordingly. If the correct threshold is 4B, correct the body text. Either way, if the eviction-vs-quantization threshold genuinely differs from the weight-vs-generation threshold, explain this explicitly — it would actually be an interesting additional finding, not an embarrassment.

2. **Add bootstrap confidence intervals to at least Figures 1, 5, and 8.** With 32 generations per instance, these are straightforward to compute and would significantly strengthen the paper's empirical credibility.

3. **Soften the presentation of the threshold's generality.** Instead of stating "models effectively smaller than 8-bit 4B" as a universal rule, note that this value was observed empirically in the Qwen3 family and may shift with architecture. The cross-family results confirm the qualitative pattern, which is already valuable.

4. **Either present the latency evidence in the main text or weaken the "strictly dominant" claim** on line 111 to avoid overclaiming.

## Score and Decision

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>