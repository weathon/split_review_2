## Summary

This paper presents a large-scale empirical study (1,700+ configurations) of memory–accuracy trade-offs for reasoning models across five factors: model size, weight precision, token budget, parallel scaling (majority voting), and KV cache compression. The core finding is that memory-optimal strategies are scale-dependent and task-dependent: small models (effective size below ~4.2 GB) benefit most from allocating memory to model weights, while large models benefit from longer generation and parallel scaling. The paper further finds that 4-bit weight quantization is optimal for knowledge tasks but not math/code, and that KV cache eviction versus quantization choice also depends on model scale.

---

## Strengths

1. **Scale-dependent findings (Findings 1 and 3) are genuinely novel and non-obvious.** The claim that small reasoning models should prioritize weight capacity over longer generations, while large models should do the opposite, is well-contrary to the intuition that longer chain-of-thought always helps. The supporting evidence (Section 4, e.g., "1.7B-8bit with 6k tokens outperforms 0.6B-8bit with 18k tokens") is concrete and illustrated in Figure 2.

2. **Task-dependent precision finding (Finding 2) is interesting and empirically grounded.** Showing that 4-bit quantization is memory-optimal for GPQA-Diamond but not for AIME25/LiveCodeBench is a practically useful nuance. The contrast between Figures 1/3 (math/code) and Figure 4 (knowledge) is visually compelling.

3. **Systematic scope.** 1,700+ configurations, three model families (Qwen3, DeepSeek-R1-Distill, OpenReasoning-Nemotron), three weight quantization schemes (GPTQ, AWQ, FP8), two KV compression families (eviction and quantization), and four benchmarks. This breadth makes the findings more robust than a narrower study would be.

---

## Weaknesses

### Fatal

None.

### Major

1. **Threshold inconsistency between the summary and Finding 5.** The summary list (bullet 5, line 49) and the introduction (line 41) state that the threshold for when KV cache eviction outperforms quantization is "effective size smaller than an 8-bit **4B** model." However, the actual Finding 5 in Section 5 (lines 211, 221) and the surrounding prose consistently state the threshold as "effective size smaller than an 8-bit **8B** model." From Table 1, 8-bit 4B ≈ 4.19 GB while 8-bit 8B ≈ 8.94 GB — these are materially different thresholds. The abstract (line 9) also implies a single "8-bit 4B" threshold governs all findings including the eviction-vs-quantization choice. This is a factual error in the paper's own terms. The authors must correct the inconsistency and, if the thresholds genuinely differ across findings, acknowledge this explicitly — which would make the paper more informative, not less.

2. **Budget forcing confound unexamined for Finding 1.** The paper uses budget forcing (appending "Wait") to vary token budgets across model sizes. Small reasoning models naturally terminate earlier than large ones, so under budget forcing a larger fraction of their generation is forced (potentially lower-quality) tokens. Finding 1 concludes that longer token budgets are memory-inefficient for small models, but this could partially reflect that forced tokens are lower quality for small models, rather than a genuine interaction between memory allocation strategy and scale. The paper provides no analysis (e.g., fraction of forced tokens per model size, or comparison against naturally long generations from a different method). This weakens the strength of Finding 1's conclusion as stated.

### Minor

3. **Generalizing "knowledge-intensive tasks" from one benchmark.** Finding 2 claims "for knowledge-intensive tasks, 4-bit is broadly memory-optimal," but the evidence comes from a single benchmark: GPQA-Diamond. The paper's other benchmarks (AIME25, MATH500, LiveCodeBench) are math and code, not knowledge. A claim about "knowledge-intensive tasks" in general should be supported by at least a second knowledge benchmark (e.g., MMLU-Pro). As it stands, the finding is really "4-bit is memory-optimal on GPQA-Diamond."

4. **Limited test of the "effective size" hypothesis across N/bit combinations.** The paper defines "effective size" as N × bits_per_weight and claims behavior is "mainly governed" by it, but the threshold (8-bit 4B ≈ 4.2 GB) was derived from Qwen3 models. While R1-Distill and Nemotron are tested, those families offer different N values (1.5B, 7B, 14B) rather than testing whether the *same* effective size from different N/bit ratios (e.g., 2B-16bit vs. 4B-4bit, both ≈4 GB) produces similar behavior. Without such a comparison, it is unclear whether the results are governed by effective size per se or by parameter count and precision as separate factors.

### Trivial

None.

---

## Nice-to-Haves

- **Error bars / confidence intervals.** The paper reports accuracy averaged over 32 generations (dropping to 8 for KV compression experiments) without variance estimates. Since some comparisons between configurations are close, readers cannot assess whether observed differences are within noise. Adding confidence intervals would strengthen the paper's claims.
- **Explicit discussion of the generation-count drop (32 to 8) for KV compression experiments.** The paper should address whether this affects comparability between Sections 4 and 5.
- **Context-dependent KV cache costs.** The KV cache depends on both prompt length and generation length. The paper focuses on generation tokens (2k–30k) but does not discuss how varying prompt lengths across benchmarks affect the total memory footprint.

---

## Removed Points

These points were raised in the input review but are removed after filtering:

- **"Timely and practically important problem" (Strength 1):** Generic; many papers address important problems. Removed per filtering rules.
- **External verifier limited to one model (Section 4.1 critique):** The paper already acknowledges this limitation in Section 7. Not a valid weakness.
- **Section-by-section notes about scope and presentation:** Some notes (e.g., scope of test-time scaling methods) describe the paper's design choices rather than weaknesses.
- **"No error bars" as a standalone weakness:** Moved to Nice-to-Haves — single-run evaluation at scale is the norm for this type of work.
- **Memory model for parallel scaling implicit:** The formula M_total = M_weights + G × M_KV_per_sample is given in line 71; the reviewer's concern is adequately addressed.

---

## Novel Insights

One genuinely novel insight emerges from cross-referencing the reviews with the paper: the threshold inconsistency between the summary (8-bit 4B) and Finding 5 (8-bit 8B) may actually reflect a meaningful empirical fact that the paper obscures by trying to unify all findings under a single threshold. If KV cache compression decisions have a different (roughly double) scale dependency than weight-vs-token allocation decisions, this is itself an interesting finding — it suggests that different memory subsystems have different sensitivity to model capacity. The paper would be stronger by embracing this multiplicity rather than papering over it.

---

## Suggestions

1. **Resolve the threshold inconsistency.** Correct bullet 5 and the abstract to match Finding 5's actual threshold (8-bit 8B), or explain why the same threshold applies and provide evidence. If the thresholds genuinely differ between Findings 1/3 (8-bit 4B) and Finding 5 (8-bit 8B), state this explicitly — it makes the paper more informative.

2. **Analyze the budget forcing artifact.** Measure the fraction of forced tokens per model size and token budget. If forced-token quality varies systematically with model size, either control for it or soften the claim in Finding 1.

3. **Add a second knowledge benchmark or reframe Finding 2.** A single extra benchmark (e.g., MMLU-Pro subset) would substantially strengthen the claim. If infeasible, reframe the finding as specific to GPQA-Diamond.

4. **Add variance estimates or confidence intervals** to the main figures (Figures 1, 4, 5, 8) so readers can assess whether observed differences between configurations are significant.

---

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>