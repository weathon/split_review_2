## Summary

QubitCache proposes a KV-cache compression method that partitions tokens into preserved (~15%, stored as full K,V pairs) and non-critical (~85%, whose K,V pairs are discarded). For non-critical tokens, attention patterns from the initial forward pass are encoded via quantum amplitude encoding (simulated classically with 9-qubit circuits) into static probability distributions. During inference, attention over these tokens uses pre-computed, query-independent weights from quantum measurements, combined with interpolated value vectors. The method achieves 7× memory reduction.

## Strengths

- **Well-motivated problem diagnosis.** The paper correctly identifies that existing token-eviction methods (H2O, ScissorHands) make binary keep/drop decisions that sever relational structure between evicted and retained tokens, which is particularly harmful for multi-hop reasoning. This diagnosis is grounded in cited prior work on attention sparsity (Michel et al., 2019; Jaszczur et al., 2021; Choromanski et al., 2020).

- **Informative ablation study (Table 4).** The ablation cleanly separates the contribution of attention-based critical token selection from the quantum encoding component. The finding that removing critical tokens causes a catastrophic 20.4% drop (0.491 → 0.391) while removing the quantum encoding causes only a 3.9% drop (0.491 → 0.472) honestly reveals where the method's actual leverage comes from, even if this undercuts the central novelty claim.

- **Broad evaluation across models and benchmarks.** The paper tests across Llama-3-8B, Mistral-7B, Phi-4-mini, Qwen2-7B, DeepSeek-Coder-7B, and scales to Llama-70B and Qwen-30B. Seven benchmarks span language modeling, multi-hop QA, summarization, and document understanding.

## Weaknesses

### Major

- **Query-independent attention for 85% of tokens is not acknowledged.** Equation (2/7) presents the soft-attention term over non-critical tokens as if it were standard query-dependent attention. In reality, pⱼ(ψ) is computed from pre-computed quantum states encoding aggregated attention from the *initial forward pass* (Equations 3–5). These weights do not change based on the current query during autoregressive generation. The method replaces dynamic attention over 85% of the sequence with static importance-sampling weights determined at prefill time. The paper never discusses this fundamental departure from standard transformer attention, nor does it analyze scenarios — such as multi-hop reasoning where later queries assign high attention to initially peripheral tokens — where this static weighting would fail. This is not a resolvable omission; it is a core design limitation.

- **Central performance claims are not supported by the paper's own data.** Two specific claims are contradicted:
  - *15-25% improvement on multi-hop reasoning.* Checking Table 1 (HotpotQA), improvements over the *strongest* baseline per model are: 1.6% (Llama-8B), 3.6% (Mistral-7B), 4.9% (DeepSeek-Coder), 5.3% (Phi-4-mini), and 8.8% (Qwen2-7B). The 15-25% figure holds only against the weakest baselines (e.g., H2O or StreamingLLM), not against competitive ones (ScissorHand, GEAR).
  - *92-97% performance retention.* On HotpotQA with Mistral-7B: Full KV = 0.566, QubitCache = 0.459, which is 81.1% retention — well below the 92% floor. The claim appears averaged across easier tasks, masking larger degradation on harder benchmarks.

- **No runtime or latency analysis is reported.** QubitCache simulates 9-qubit quantum circuits per segment, per layer, per head at inference time. The paper mentions "gate fusion, parallel segment encoding, and adaptive shot allocation" as optimizations and claims "minimal latency overhead" (line 216), but provides zero wall-clock time, tokens-per-second, or any latency measurement. This is a critical omission for a method that adds substantial per-step computation compared to simple token-selection heuristics, and it makes the method's practical viability unassessable.

- **Baseline performance is implausibly low on several model-benchmark pairs.** DeepSeek-Coder + ScissorHand on PG19 achieves F1=0.018 (9.3% of Full KV's 0.193). Phi-4-mini + H2O on Contract achieves Acc=0.200 (38.2% of Full KV's 0.523). DeepSeek-Coder + ScissorHand on PIQA achieves Acc=0.661 (70.6% of Full KV's 0.936). These are far below what published baselines typically achieve. The paper states "consistent protocols" but does not specify whether compression ratios / token retention rates were equalized across methods — a standard practice in compression evaluation. This raises concerns that baselines were not properly tuned per model.

### Minor

- **The quantum encoding provides marginal benefit and the framing is overclaimed.** Table 4 shows Full QubitCache (F1=0.491) vs. No Quantum (F1=0.472), a 3.9% relative improvement. The actual working component is the attention-based critical token selection heuristic (20.4% drop when removed). The paper also claims "logarithmic compression beyond classical information-theoretic limits" (abstract, Section 3.2), but the entire implementation is classical simulation storing 512 complex amplitudes per segment — there is no realized quantum compression benefit. The memory savings come from discarding 85% of K,V pairs, which is a token-eviction strategy, not a quantum one.

- **"First framework" claim is contradicted by the paper's own citations.** The abstract claims QubitCache is "the first framework recognizing that attention patterns between tokens constitute the primary information carrier." Yet the paper cites Michel et al. (2019), Jaszczur et al. (2021), and Choromanski et al. (2020), all of which analyze attention patterns as primary information carriers. This claim should be removed.

- **Key hyperparameter choices are unjustified.** The balance parameter λ = √(|ℐₚ|/N) (line 120) is presented without any analysis or ablation justifying the square-root form. The threshold sₘᵢₙ for critical token selection is mentioned (Section 3.4) but never given a value or explained how it is determined (fixed, adaptive, or tuned per model).

- **The memory advantage over GEAR is marginal.** Table 3 shows QubitCache at 0.55 GB (7.0×) vs. GEAR at 0.59 GB (6.7×) — a 0.04 GB difference. The O(log N) term in QubitCache's complexity is negligible compared to the O(L × H × 0.15S × D) term from preserved tokens. The paper frames this as a decisive advantage.

- **No statistical significance reported.** No error bars, confidence intervals, or multiple-run statistics are provided. Some differences in Table 1 are small (e.g., Mistral-7B PG19: QubitCache 0.121 vs GEAR 0.117) and may not be significant.

### Trivial

- The figure caption for the quantum circuit (Figure 2) defines αᵢ = 2 arctan(√(w_right/w_left)) but w_right and w_left are never defined in the main text.

## Nice-to-Haves

- A cleaner ablation replacing the quantum encoding with an explicitly stored probability vector of the same dimension would isolate whether the quantum formalism provides any practical advantage or is purely cosmetic.
- Runtime/latency analysis comparing QubitCache against baselines is essential for assessing practical viability.
- Equalizing compression ratios across methods would make baseline comparisons fairer and more interpretable.
- Analysis of how the static weighting performs at longer context lengths (32K+ tokens) where the query-independent assumption becomes more problematic.

## Removed Points

These points were raised by the harsh critic but are removed for the following reasons:

1. **"The method does not compress the KV cache — it replaces attention with static weights" (framed as the most fundamental problem):** The core criticism (query-independent weights for 85% of tokens) is retained under Major Weaknesses. However, the claim that the method "does not compress the KV cache" is inaccurate — it achieves 7× memory reduction by storing only 15% of K,V pairs plus compact quantum state representations. Compression does occur; the issue is what happens to the compressed information, not whether compression occurs.

2. **"The theoretical proof is claimed but does not appear in the main body":** Removed because the appendix (which may contain the proof) was stripped by the PDF parser. Per system instructions, weaknesses about missing appendix content are not chargeable to the authors.

3. **Missing related works / insufficient related work coverage:** Removed per instructions — I cannot confirm the existence or non-existence of related works from external knowledge, and the instruction explicitly forbids mentioning missing related works.

4. **Formatting, style nitpicks, and parser artifact complaints:** Removed as these are either parser issues, not author errors, or are too minor to include.

## Novel Insights

None beyond the paper's own contributions. The reviews surface a consistent pattern: the paper has a genuinely reasonable high-level idea (preserving attention-informed importance weights for evicted tokens rather than discarding them entirely) but oversells it with unwarranted quantum framing, unsupported performance claims, and missing evaluation dimensions (latency, equalized baselines). The ablation study paradoxically undermines the core novelty claim by showing the quantum component contributes only 3.9% while the token-selection heuristic drives the performance.

## Suggestions

1. **Honestly describe the method.** The abstract, introduction, and method sections should clearly state that for ~85% of tokens, QubitCache uses static, pre-computed attention weights determined at prefill time — not query-dependent attention. Drop the "beyond classical information-theoretic limits" claim and the "first framework" novelty claim.

2. **Report performance against the strongest baseline per model, not the weakest,** when making comparative claims (e.g., the 15-25% figure).

3. **Provide runtime/latency measurements.** Without them, the method's practical viability is unassessed. Report tokens-per-second, wall-clock time per step, and memory bandwidth utilization.

4. **Investigate and fix the suspicious baseline numbers** (DeepSeek-Coder + ScissorHand at F1=0.018 on PG19, etc.). Either correct the configuration or explain the discrepancy and show that the baselines were properly tuned.

5. **Equalize compression ratios across methods** or clearly state the retention rates used for each baseline. The current comparison (QubitCache at 7×, baselines at 2×) conflates the retention rate and the reconstruction quality.

6. **Report statistical significance** (error bars over multiple runs, or at minimum the number of runs).

7. **Provide ablation or justification for λ = √(|ℐₚ|/N)** and specify the sₘᵢₙ threshold value.

## Calibration Report

**Round 1 bracket:** 2.5 – 4.0

**Anchors retrieved across all rounds:**

| Paper | Avg Score | Round | Comparison |
|-------|-----------|-------|------------|
| IntelLLM (4QWPCTLq20.md) | 3.00 | R1 | Eviction-based KV compression, rejected. Less ambitious claims, more honest execution. QubitCache has broader evaluation but more fundamental flaws. |
| Not All Heads Matter (FJFVmeXusW.md) | 6.50 | R1 | Head-level allocation, accepted. Thorough evaluation including latency. QubitCache has more novelty in concept but weaker execution. |
| Don't Discard (CRQ8JuQDEd.md) | 5.00 | R1 | Mixed-precision, rejected for limited novelty. Sound method but incremental. QubitCache has more novelty but more severe flaws. |
| PyramidKV (jZVNmDiU86.md) | 5.60 | R1 | Dynamic compression, rejected. QubitCache underperforms relative to this anchor. |
| QJL (xHPVGmLXjd.md) | 3.50 | R2 | 1-bit quantization, rejected for limited evaluation. QubitCache is comparable. |
| LSH-E (0ZcQhdyI3n.md) | 3.83 | R2 | LSH-based eviction, rejected. Mixed reviews. QubitCache's problems are more fundamental. |
| KVTQ (eZAlb8fX5y.md) | 4.40 | R2 | Ternary quantization, rejected. Mixed scores. |

The paper falls below the accepted papers (6.5+) and below the stronger rejected papers (4-5 range) due to the combination of overclaimed results, missing evaluation dimensions, and the fundamental design issue of unacknowledged query-independent weighting. It is most comparable to IntelLLM (3.00) and QJL (3.50) — papers with substantive flaws that prevented acceptance.

MY FINAL SCORE: <score>3.0</score>
MY FINAL DECISION: <decision>Reject</decision>