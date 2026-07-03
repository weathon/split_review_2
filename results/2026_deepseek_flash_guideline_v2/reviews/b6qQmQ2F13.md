Now I have full verification. Let me finalize the review.

The inconsistency is clearly confirmed: the abstract (line 9), intro (lines 41, 49), and Findings 1/3 (lines 45, 47, 121, 163) all say "8-bit 4B" (~4.19 GB), while Section 5 body (lines 211, 217, 221) consistently says "8-bit 8B" (~8.94 GB). The abstract explicitly claims "this scale threshold also determines... whether KV cache eviction outperforms KV quantization" — but if Section 5's 8-bit 8B is the intended threshold, then it is NOT the same threshold as the 8-bit 4B used for Findings 1 and 3.

Let me also verify the effective size table values to be precise about the difference.

From Table 1: 8-bit 4B = 4.19 GB; 8-bit 8B = 8.94 GB. The difference is roughly 2.1×, not a minor rounding issue.

Now I'll write the final review.

## Summary
2-3 sentence summary of the paper's contribution.

This empirical study investigates memory-accuracy trade-offs for reasoning models under fixed memory budgets, examining model size, weight precision, token budget, parallel scaling, and KV cache compression. It demonstrates that the common 4-bit prescription fails for reasoning models and identifies a scale-dependent threshold governing when to prioritize weights vs. tokens, when parallel scaling helps, and when KV eviction beats quantization. The study spans 1,700+ configurations across three model families and four benchmarks.

## Strengths
- **Demonstrates that 4-bit weight quantization fails for reasoning models**: Provides concrete Pareto-dominance evidence contradicting prior universal prescriptions. For example, the 8B model in 8-bit consistently outperforms the 14B model in 4-bit (Figure 1), and the 32B model in 4-bit is strictly dominated by the 14B model in 8-bit (Section 4).

- **Introduces "effective size" as a unifying organizational concept**: Shows that a single quantity (N × P_W) correlates with the threshold where memory allocation strategy should shift across three independent axes — weight-vs-token allocation, parallel scaling efficiency, and KV compression method choice. This is a non-trivial empirical regularity.

- **First systematic comparison of KV cache eviction vs. quantization for reasoning models under a unified memory budget**: Prior work studied each compression method in isolation; this paper provides a direct head-to-head comparison (Figures 8–9) establishing different regimes of advantage (Findings 4–5).

- **Extensive experimental scope with cross-family validation**: Over 1,700 configurations across 6 model sizes, 3 weight precisions, 8 token budgets, up to 16 parallel samples, and two KV compression families, with key findings replicated on DeepSeek-R1-Distill and OpenReasoning-Nemotron.

- **Robustness checks across quantization schemes**: Replicates key experiments with AWQ and FP8, reporting nearly identical memory-accuracy curves (Appendix C.2).

- **Empirical evaluation of PRMs under memory constraints**: Shows a 7B Process Reward Model adds 13.28 GB fixed overhead rarely recouped in accuracy gains (Section 4.1, Figure 7).

## Weaknesses

### Fatal
None.

### Major
- **Threshold inconsistency between abstract/intro and body for Finding 5**: The abstract (line 9), intro (lines 41, 49 — Finding 5 list), and Findings 1/3 consistently use "8-bit 4B" (~4.19 GB) as the threshold. However, Section 5 body (lines 211, 217) and Finding 5 statement (line 221) consistently use "8-bit 8B" (~8.94 GB) — a difference of roughly 2.1×. The abstract explicitly claims "this scale threshold also determines... whether KV cache eviction outperforms KV quantization," asserting a unified threshold for all three phenomena. If the body's 8-bit 8B is correct, then the eviction-vs-quantization threshold differs from the weight-vs-token threshold (8-bit 4B), contradicting this headline claim. If the intro's 8-bit 4B is correct, then multiple passages in Section 5 need correction. Either way, the inconsistency undermines a central narrative and must be resolved.

- **No statistical uncertainty or variance reported**: The paper reports point estimates of accuracy averaged over 32 generations per instance (8 for KV experiments) at temperature 0.6 without any confidence intervals, standard errors, or variance measures. For an empirical study making comparative claims (e.g., "the 1.7B model in 8-bit with a 6k token budget outperforms the 0.6B model in 8-bit with an 18k token budget," line 111), the absence of uncertainty quantification makes it impossible to assess whether observed differences are meaningful or within noise. This is a significant methodological gap for a study whose main output is comparative statements.

### Minor
- **The "effective size" concept conflates parameter count and precision in ways the paper itself documents**: Finding 2 shows that 4-bit vs. 8-bit are not interchangeable at the same effective size — higher precision matters for mathematical reasoning regardless of parameter count. This creates tension between the paper's central organizational device (grouping configurations by effective size) and its own finding that task-dependent precision sensitivity cuts across effective-size groupings. The qualitative direction is likely robust, but the precise threshold numbers should be treated as approximate.

- **Limited knowledge benchmark coverage for the task-dependence claim**: Finding 2 (task-dependent optimal precision) rests on a single knowledge benchmark (GPQA-Diamond) against math/code benchmarks. The finding is plausible but would benefit from additional knowledge benchmarks.

- **Missing hardware specifications**: The paper does not specify GPU type or computational budget for the 1,700+ configurations, hindering reproducibility.

### Trivial
None.

## Nice-to-Haves
- **Budget-forced token quality control**: The paper uses budget forcing (injecting "Wait" prompts) to extend generations but does not analyze whether forced extensions degrade in quality compared to naturally long generations. A control experiment comparing budget-forced generations at a model's natural length to natural generations at that length would strengthen the conclusions.
- **PRM finding caveat**: The conclusion that external verifiers are "memory-inefficient" rests on a single 7B verifier (ActPRM-X). Smaller PRMs or self-verification might shift this conclusion. The paper acknowledges this but could qualify the finding more explicitly.

## Removed Points
These points were raised by reviewers but removed after verification:

- **"The parallel scaling comparison generates vastly more total tokens"** (Harsh Critic): Removed because the paper correctly frames parallel scaling as a memory comparison under batched inference (KV cache grows with G), which is the appropriate framing. The paper explicitly states this is about memory efficiency under fixed budgets, not per-token efficiency.
- **"Effective size is a fundamental framing flaw"** (Harsh Critic): Demoted to Minor. The paper is clear that effective size is a coarse organizational device, and Finding 2 explicitly documents the task-dependent precision sensitivity that creates the tension. The qualitative conclusions survive.
- **"Missing appendix content / proofs"**: Removed per rules — appendix content is stripped by the PDF parser and exists in the original submission.
- **Strength Finder claims about the problem being "important"**: Removed as generic/superficial; kept only concrete, paper-specific strengths.

## Novel Insights
The threshold inconsistency between the intro (8-bit 4B) and body (8-bit 8B) for Finding 5 is more than a typo — it raises the substantive question of whether the thresholds for weight-vs-token allocation, parallel scaling, and eviction-vs-quantization genuinely coincide. The body's evidence suggests they may not (8-bit 4B vs 8-bit 8B differ by ~2×), which would make the paper's claim of a "unified scale threshold" an overstatement. This ambiguity needs resolution regardless of which number is correct.

## Suggestions
1. **Resolve the threshold inconsistency**: Reconcile the 8-bit 4B vs 8-bit 8B numbers for Finding 5 across abstract, intro, and body. If the threshold genuinely differs from Findings 1/3, state this explicitly and discuss why; if it's a typo, correct all occurrences.
2. **Add uncertainty quantification**: Provide confidence intervals, error bars, or at minimum report variance with a discussion of which differences are likely meaningful.
3. **Acknowledge the limitations** of the "effective size" concept more explicitly, given Finding 2's task-dependent precision sensitivity.
4. **Include hardware specifications** (GPU type, runtime) to aid reproducibility.

## Score and Decision

Calibration was attempted via `calibration_search` but the corpus was inaccessible due to systemic file-path errors. I proceed with my own calibrated judgment.

Based on the ICLR scale (1=strong reject, 3=reject, 4=borderline reject, 6=borderline accept, 8=accept, 10=strong accept), I assess this paper as follows:

The paper has genuine contributions — it convincingly demonstrates that 4-bit quantization fails for reasoning models, provides a large-scale empirical characterization of scale-dependent trade-offs, and offers practically useful guidelines. The experimental scope is impressive and the cross-family validation strengthens the findings.

However, two issues prevent full confidence. The threshold inconsistency (8-bit 4B vs 8-bit 8B) is not a minor typo — it directly affects the paper's headline claim about a "unified scale threshold" governing multiple phenomena. The complete absence of statistical uncertainty quantification is a significant methodological gap for an empirical study built on comparative claims. Both issues are fixable, but in their current form they weaken the evidentiary foundation.

The paper is therefore at the borderline — solid contributions held back by fixable but meaningful flaws. A score of 4 (borderline reject) reflects that the paper needs substantive corrections before acceptance, but the core contribution is real and the path to improvement is clear.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>