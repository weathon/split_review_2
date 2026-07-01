## Summary

This paper empirically studies memory-accuracy trade-offs for reasoning models, where KV cache can dominate over weights — a fundamentally different regime from non-reasoning models. Through 1,700+ configurations across model size (0.6B–32B), weight precision (4/8/16-bit), token budgets (2k–30k), parallel sampling (G=1–16), and KV cache compression (eviction and quantization), the paper finds that the memory-optimal strategy is scale-dependent: models with effective size below ≈8-bit 4B benefit from allocating memory to larger weights over longer generation, while larger models benefit from the opposite. The core finding — that the optimal strategy flips at a threshold determined by effective model size — is practically useful and well-supported by evidence.

## Strengths

- **Timely, well-motivated research question.** The paper correctly identifies that KV cache memory can dominate weight memory for long-generation reasoning models (e.g., Qwen3-4B 4-bit: 2.49 GB weights vs. 4.42 GB KV cache at 32k tokens), fundamentally shifting engineering trade-offs. Framing this as a memory allocation problem is practically motivated and concretely justified.
- **Comprehensive experimental scope.** The study spans 1,700+ configurations across model size, weight precision, token budget, parallel sampling, and two KV compression families, with three model families (Qwen3, DeepSeek-R1-Distill, OpenReasoning-Nemotron) and four benchmarks (AIME25, MATH500, LiveCodeBench, GPQA-Diamond). This breadth provides strong evidence that core findings are not artifacts of a single architecture.
- **Actionable, clearly articulated findings.** The five stated findings are concrete enough to guide deployment decisions. The central observation — that the memory-optimal strategy flips at a threshold determined by effective model size — is a genuinely useful principle. Pareto frontier analysis throughout makes trade-offs visually interpretable.
- **Cross-validation across model families.** Key results are replicated on DeepSeek-R1-Distill (Figures 5–6) and OpenReasoning-Nemotron (Appendix), lending credibility beyond the primary Qwen3 family.

## Weaknesses

### Fatal
None.

### Major

- **Threshold inconsistency between Finding 5 and the paper's summary.** The summary list (line 49) states Finding 5 as: "*KV cache eviction provides a better memory-accuracy trade-off than KV cache quantization for models with an effective size smaller than an **8-bit 4B model**.*" However, the body of Section 5 (lines 211, 221) consistently states the threshold as an **8-bit 8B model** (~8.94 GB, more than double the ~4.19 GB of 8-bit 4B). The paper does not acknowledge or explain this discrepancy. A practitioner reading the summary would receive a substantively different recommendation than one reading the detailed analysis. This must be resolved: if both thresholds are correct, the paper must explain why the eviction-vs-quantization crossover point differs from the weight-vs-KV-cache allocation crossover point; if one is an editing error, it must be corrected.

### Minor

- **KV cache values in Table 1 are identical across different model sizes without explanation.** Qwen3-0.6B and Qwen3-1.7B share identical KV cache footprints (0.21 GB at 2k tokens, 1.92 GB at 18k tokens), and Qwen3-4B and Qwen3-8B share identical values. KV cache size depends on architectural parameters (layers, KV heads, head dimension) that typically differ across model sizes. While there may be a valid architectural explanation (e.g., shared attention configurations), the paper should state the reason explicitly to avoid raising concerns about data integrity.
- **The external verifier analysis (Section 4.1) evaluates only one specific PRM (ActPRM-X, 7B, 13.28 GB).** The paper acknowledges this as a "limited evaluation" (Section 7), but the wording ("using an external verifier such as PRM is memory-inefficient") could be read more broadly than the evidence supports. A smaller verifier (e.g., 1B or 3B) with lower overhead might change the trade-off, especially for larger base models. The claim should be scoped down or additional verifier sizes should be tested.
- **No statistical variance or confidence intervals for accuracy measurements.** Results are reported as averages over 32 generations (serial) or 8 generations (KV compression experiments), but variance is absent. The reader cannot assess whether differences between configurations on the Pareto frontier are meaningful or within noise. This is especially relevant for threshold claims where small differences determine frontier membership.
- **Generalizability of absolute GB thresholds beyond Qwen3 is unclear.** While Section 7 acknowledges this, the thresholds (8-bit 4B, 8-bit 8B) are presented as concrete guidance throughout the main text without quantifying the uncertainty around them. Different architectures at the same effective size may behave differently due to differences in layer count, head dimension, or activation distributions. The paper would benefit from more prominently qualifying the architecture-specific nature of the precise threshold values.

### Trivial
None.

## Nice-to-Haves

- Include error bars or confidence intervals for accuracy measurements.
- Test with smaller verifiers (e.g., 1B or 3B PRMs) to strengthen the external verifier analysis.
- Explore whether the findings on 4-bit weight quantization for mathematical reasoning hold under alternative 4-bit methods beyond GPTQ, AWQ, and FP8 (e.g., QuIP#, AQLM, or finer group sizes).
- If the eviction-vs-quantization threshold genuinely differs (8-bit 8B) from the weight-vs-KV allocation threshold (8-bit 4B), discuss why this asymmetry arises — e.g., eviction's fixed-memory-ceiling behavior may benefit medium-sized models more than quantization does, pushing the crossover higher.

## Removed Points

- **Criticism that the 4-bit weight quantization claim is overstated due to using a single method:** Removed because the paper validates with AWQ and FP8 (Appendix C.2) and reports "nearly identical memory-accuracy curves." The paper has reasonable cross-validation for its claims.
- **Generic scope-creep criticisms** (e.g., requests for more models or quantization methods beyond the already extensive 1,700+ configuration space): These were either addressed by the paper's existing experiments or exceed reasonable expectations for a single paper.
- **Criticism about the memory cost model (Equation 1) omitting overhead:** Removed because the paper uses measured values (Table 1) and Appendix B contains exact equations. The simplified equation is for conceptual framing, not accounting.

## Novel Insights

The reviews surface one genuinely novel observation beyond the paper's own contributions: the threshold inconsistency between Finding 5 and the summary. If the 8-bit 8B threshold in Section 5 is correct and the 8-bit 4B in the summary is an error, then the eviction-vs-quantization crossover point being at a higher effective size than the weight-vs-KV allocation crossover point is itself an interesting finding. This would suggest that eviction's fixed-memory-ceiling behavior is advantageous over quantization even at moderately larger model sizes, pushing the trade-off boundary outward. The paper currently does not discuss this asymmetry or its potential implications.

## Suggestions

1. **Resolve the threshold inconsistency** between the summary (8-bit 4B) and Section 5 (8-bit 8B). If both are correct, explain why the eviction-vs-quantization decision has a higher crossover point. If one is an error, correct it.
2. **Add an explicit note to Table 1** explaining why 0.6B/1.7B and 4B/8B models share identical KV cache footprints (or correct the values if erroneous).
3. **Add error bars or confidence intervals** for accuracy measurements, or at minimum acknowledge their absence and discuss potential impact on threshold claims.
4. **Scope the external verifier claim** more precisely (e.g., "the specific PRM we evaluated" rather than "using an external verifier such as PRM").
5. **Quantify the transitional region** around the stated thresholds rather than presenting them as sharp boundaries.

---

## Calibration Anchors

| Anchor | Path | Avg Score | Round | Comparison |
|--------|------|-----------|-------|------------|
| IntelLLM (KV cache compression) | 4QWPCTLq20.md | 3.00 | 1 | Reject-level KV compression method; less comprehensive scope than this paper |
| PrefixQuant (LLM quantization) | vw0NurJ7UX.md | 3.00 | 1 | Reject-level quantization method; narrow focus compared to this paper's breadth |
| KVTQ (ternary KV cache) | eZAlb8fX5y.md | 4.40 | 1 | Reject; novelty concerns, similar topic but different contribution type |
| Running Huge Context Windows | pG820nmDvy.md | 4.67 | 1 | Reject; top-k attention with speed concerns, less rigorous empirically |
| **Inference Scaling Laws** | VNckp7JEHn.md | **5.75** | 2 | **Most similar anchor** — empirical study of compute-optimal inference trade-offs; narrower scope (math only, 2 model families); scored Accept with mixed reviews (6,3,6,8). Our paper has broader scope but a clear inconsistency issue. |
| **Cost of Scaling Down** | ldJXXxPE0L.md | **6.00** | 2 | Empirical study of pruning effects on LLM capabilities; similar contribution type (empirical findings). Our paper has more comprehensive scope but a concrete inconsistency. |
| HeadKV (head-level KV compression) | FJFVmeXusW.md | 6.50 | 1 | Accept; method paper with strong results, minor weaknesses. Higher novelty but narrower scope than this paper. |
| Scaling Laws for Precision | wg1PCg3CUP.md | 8.00 | 1 | Strong accept; comprehensive scaling laws study, no significant weaknesses. Higher bar than this paper. |

**Round 1 bracket:** 4.0 – 7.0  
**Round 2 narrowing:** The most similar empirical studies ("Inference Scaling Laws" at 5.75 and "Cost of Scaling Down" at 6.00) provide the best anchors. Our paper has broader experimental scope than both, but carries a concrete internal inconsistency that the anchors do not. Score 6.0 reflects a solid empirical contribution with a fixable but real flaw.

**MY FINAL SCORE: <score>6.0</score>**
**MY FINAL DECISION: <decision>Accept</decision>**