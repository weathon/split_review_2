## Summary

This paper conducts a large-scale empirical study (~1,700 configurations) investigating how to optimally allocate memory across model size, weight precision, token budget, parallel scaling, and KV cache compression for reasoning models. The central finding is that the memory-optimal strategy is scale-dependent: for models with effective size below ~8-bit 4B, prioritize weight capacity; above that threshold, prioritize test-time compute. The paper provides concrete, actionable thresholds for practitioners.

## Strengths

1. **Extensive and well-organized experimental design.** The paper spans over 1,700 configurations across three model families (Qwen3 0.6B–32B, DeepSeek-R1-Distill, OpenReasoning-Nemotron), four benchmarks (AIME25, MATH500, GPQA-Diamond, LiveCodeBench), and multiple compression techniques (GPTQ, AWQ, FP8 for weights; HQQ for KV quantization; R-KV and StreamingLLM for eviction). The scope is ambitious but the paper manages it coherently.

2. **Actionable findings with clear thresholds.** Unlike many empirical studies that report only qualitative trends, this paper provides concrete thresholds (e.g., effective size of 8-bit 4B ≈ 4.2 GB) that translate directly into deployment decisions for practitioners. This concreteness is valuable.

3. **Honest limitation section.** The paper acknowledges its choices (focus on Qwen3, limited verifier evaluation, small set of quantization schemes) without claiming more generality than the experiments support.

## Weaknesses

### Fatal
None.

### Major

1. **Absence of uncertainty quantification for comparative claims.** The paper reports pass@1 accuracy for each configuration but provides **no error bars, confidence intervals, or measures of statistical significance anywhere**. This is a significant gap for a paper whose central claims are inherently comparative—e.g., "the 1.7B model in 8-bit with a 6k token budget outperforms the 0.6B model in 8-bit with an 18k token budget" (Section 4, line 111) and "the 32B model in 4-bit is strictly dominated by both the 14B model in 8-bit and the 8B model in 16-bit" (Section 4, line 135). Without variance estimates, particularly on AIME25 (only 30 problems, accuracy averaged over 32 generations per instance), the reader cannot assess whether the differences driving the Pareto frontier analysis are real or within noise. The "strict dominance" claims require statistical confidence the current data does not provide. This concern is amplified in Section 5, where the KV cache compression experiments use only 8 averaging runs per instance (line 185) versus 32 in Section 4.

2. **Internal inconsistency in Finding 5's threshold.** The Introduction (line 49, bullet point 5) states: *"KV cache eviction provides a better memory-accuracy trade-off than KV cache quantization for models with an effective size smaller than an **8-bit 4B** model."* However, Section 5's body text (line 211) and Finding 5 (line 221) both state the threshold as **8-bit 8B**. These differ by a factor of ~2× in effective size (4.2 GB vs. 8.94 GB per Table 1), which would place different models into the "eviction-preferred" category. This inconsistency undermines the reliability of the paper's central practical recommendations.

### Minor

3. **Framing oversimplifies distinct thresholds.** The abstract (line 9) states "this scale threshold also determines when parallel scaling becomes memory-efficient and whether KV cache eviction outperforms KV quantization," implying a single threshold governs all findings. In reality, Findings 1 and 3 use the 8-bit 4B threshold, while Finding 5 uses 8-bit 8B. These are different thresholds for different phenomena, and the unified "scale-dependent trade-off" framing over-claims the unity of the findings.

4. **Potential confound in Finding 2's task-dependent claim.** Finding 2 attributes the difference between 4-bit being memory-optimal (GPQA-Diamond) versus suboptimal (AIME25, LiveCodeBench) to "knowledge-intensive" vs. "mathematical reasoning/code generation." However, GPQA-Diamond is multiple-choice (4 options), while AIME25 requires exact answer generation. Multiple-choice benchmarks are inherently more robust to quantization error because the model only needs to rank a few options, whereas exact-answer generation requires precise numerical outputs. The paper does not control for this answer-format confound, though the pattern across MATH500 (free-response math) and LiveCodeBench partially mitigates the concern.

5. **"Strictly dominant" claim needs qualification.** The paper argues that increasing model size is "strictly dominant" (Section 4, line 111) because end-to-end latency is dominated by token budget (Appendix C.1). This assumes single-device inference; with model parallelism (common for 32B+ models), the latency equation changes and the dominance claim would need qualification.

### Trivial
- Table 1 shows identical KV cache memory (0.21 GB at 2k tokens) for Qwen3-0.6B and Qwen3-1.7B despite a 3× parameter difference. A brief explanation would help.
- Section 5's reduction to 8 averaging runs (from 32 in Section 4) is mentioned but not justified.

## Nice-to-Haves
- Add bootstrap confidence intervals or similar uncertainty estimates to all accuracy plots, especially for Pareto frontier comparisons.
- Resolve the Finding 5 threshold discrepancy and explicitly state which threshold applies to which phenomenon.
- Discuss whether the task-type finding (Finding 2) could be influenced by answer format (multiple-choice vs. free-response).
- Qualify the "strictly dominant" latency claim for model-parallelism scenarios.

## Removed Points
*These points were flagged for removal; treat them with caution.*

- **"The effective size concept conflates two sources of weight memory"** — The critic argued that the paper does not test whether models with the same effective size but different composition behave equivalently. However, the paper explicitly discusses this (Section 4: "the 8B model in 8-bit consistently outperforms the 14B model in 4-bit"), and the entire framing acknowledges that effective size alone is not determinative. Removed as the paper already addresses this nuance.
- **"No discussion of per-problem accuracy variance"** — This is a narrower instance of the uncertainty quantification concern already covered in Weakness 1. Removed as redundant.
- **Formatting and style nitpicks** — Removed per review guidelines (parser artifacts, not author errors).
- **Related-work omissions** — Removed per review guidelines (cannot verify completeness without external sources).

## Novel Insights

The most interesting observation emerging from the reviews is that the paper's two different thresholds (8-bit 4B for Findings 1/3 and 8-bit 8B for Finding 5) tell a more nuanced story than the unified "scale-dependent" framing suggests. Rather than a single inflection point, there appear to be at least two distinct phase transitions: one governing the weights-vs-tokens and serial-vs-parallel trade-offs (~4 GB), and another governing the KV eviction-vs-quantization choice (~9 GB). This layered structure is potentially more informative than a single threshold, and the paper would benefit from making this multiplicity explicit.

## Suggestions
- Fix the Finding 5 threshold inconsistency between the Introduction (8-bit 4B) and Section 5 (8-bit 8B). If the two thresholds are genuinely different for different phenomena, state this explicitly.
- Add uncertainty quantification (bootstrap confidence intervals or standard errors) to all accuracy plots, particularly for the Pareto frontier comparisons. This is important because the paper's core contribution is comparative.
- Clarify in the abstract that different findings may operate at different effective-size thresholds rather than a single unified threshold.
- Discuss the potential answer-format confound in Finding 2 (multiple-choice vs. free-response) and consider adding a multiple-choice math benchmark in future work.
- Qualify the "strictly dominant" latency claim to acknowledge model-parallelism scenarios.

**Calibration Anchors** (all rounds):

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/3xjc9PhEPd.md` (Empirical Guidelines for Deploying LLMs) | 4.75 | R1 | Similar empirical/guidelines paper but rejected for common-sense findings; current paper has more novel, non-trivial findings |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/6VhDQP7WGX.md` (Inference Optimal VLMs) | 5.80 | R1 | Similar empirical trade-off study with scaling insights, accepted despite weaknesses; current paper is similarly structured and substantive |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/wg1PCg3CUP.md` (Scaling Laws for Precision) | 8.00 | R1 | Stronger unified theoretical framing with extensive validation; current paper lacks similar theoretical unification |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/2veex1oOtc.md` (MQuant) | 5.75 | R1 | Rejected for insufficient technical contribution; current paper's contribution is the systematic study itself, which is more novel |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/pG820nmDvy.md` (Running Huge Context Windows) | 4.67 | R1 | Rejected for failing to demonstrate practical speed; current paper doesn't have this issue |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/pXIbcRPxWR.md` (Supervised CoT) | 2.50 | R1 | Weak empirical support and poor presentation; current paper is substantially stronger |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/8QTpYC4smR.md` (Systematic Review of LLMs) | 1.00 | R1 | Survey paper with no novel contribution; not comparable |

**Round 1 bracket:** 5.5–7.0 (between the Accepted empirical trade-off studies at 5.80 and the strong theoretical work at 8.00, but above the rejected guidelines paper at 4.75)

**Final score determination:** The paper's empirical scope is genuinely impressive and its findings are non-trivial and actionable, placing it clearly above the 4.75 rejected paper. It is comparable in nature and quality to the Accepted 5.80 VLM paper, with both making empirical trade-off characterizations. However, the uncertainty quantification gap and the Finding 5 threshold inconsistency prevent it from reaching the 7+ range. Score is set at 6.0.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>