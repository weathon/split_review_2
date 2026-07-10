Now I have a clear picture. Let me produce the final consolidated review.

## Summary

This paper proposes R-HORIZON, a method to construct multi-step reasoning problems by composing existing single-problem benchmarks with explicit sequential dependencies (the answer to problem i becomes a key numeric input to problem i+1). Using this approach, the authors build a benchmark spanning math, code, and agentic tasks and evaluate 26 large reasoning models (LRMs), finding substantial performance degradation as reasoning horizon increases. They further use R-HORIZON data for reinforcement learning and show that training with composed data improves both multi-horizon and single-problem performance. Diagnostic analyses (error types, reflection patterns, thinking-budget allocation) provide insight into why models fail.

## Strengths

- **Breadth of evaluation is genuinely impressive.** 26 LRMs evaluated across math (MATH500, AIME24, AIME25, AMC23), code (LiveCodeBench), and agentic tasks (WebShaper), with multiple horizon lengths per task. Table 3 alone provides a substantial empirical resource for the community.

- **The RL training finding is practically interesting and non-obvious.** Table 1 shows that training with composed data (n=2, n=4) improves performance not only on composed tasks but also on single-problem benchmarks (e.g., AIME24: 65.4 vs. 57.9 for n=1 training). This has direct implications for training data construction and suggests composition helps develop more robust reasoning.

- **The diagnostic analyses go beyond reporting accuracy drops.** Error-type analysis (Figure 5), effective reasoning length (Figure 6), reflection analysis (Figure 7), and thinking-budget allocation (Figure 8) diagnose *why* models fail — problem-reasoning errors dominate, reflection is localized rather than long-range, and models front-load their thinking budget. This diagnostic depth separates a useful benchmark from a simple leaderboard.

- **Problem framing is well-motivated.** The paper identifies a genuine gap: existing benchmarks test isolated single-horizon problems, while real-world use cases require sustained reasoning across interdependent steps (agents, multi-step planning). The connection to limitations in both evaluation and training is clearly drawn.

## Weaknesses

### Major

- **Impossible accuracy value in the main evaluation table (Table 3, line 157).** Qwen3-32B on MATH500 with n=4 shows **127.6%** accuracy, which is mathematically impossible for an accuracy metric. This entry is clearly erroneous — it could be a data corruption, answer-extraction bug, or parsing artifact. An evaluation table containing an impossible value undermines confidence in the evaluation pipeline and raises questions about whether similar errors affect other entries. The authors must audit the full table, correct or explain this value, and document the reliability of their answer-extraction pipeline. (Note: the same model name "Qwen3-32B" appears twice in the table with different values — lines 157 and 162 — which also needs clarification.)

### Minor

- **RL training comparison is confounded by unequal data quantity (Table 1).** The comparison of "Naive Training Data (n=1)" with "w/ composed queries (n=2)" does not control for the total number of atomic problems seen during training. Each n=2 training sample contains 2 atomic problems, so for the same number of training steps the n=2 condition sees approximately twice as many unique atomic problems. The headline improvement on single-problem benchmarks (+7.5 on AIME24) could partly reflect increased data exposure rather than the compositional structure per se. While the n=4 condition sometimes underperforms n=2 (suggesting composition quality matters beyond data quantity), a proper control matching total atomic problems across conditions is needed to isolate the benefit of composition.

- **o4-Mini on WebShaper is a counterexample to the "consistent degradation" claim (Table 3, line 179).** o4-Mini on WebShaper: 43.7% (n=1) → 87.6% (n=2) → 84.4% (n=3) → 70.3% (n=4) → 61.4% (n=5). Accuracy increases dramatically from n=1 to n=2, directly violating the stated claim of "consistent degradation trends across different model and task categories." The paper mentions that many trained reasoning models have lost tool-calling ability, but this does not explain why o4-Mini's n=2 performance is roughly double its n=1 performance. While the overall degradation pattern holds across most model-task combinations, this counterexample weakens the claim of universality and warrants explicit discussion.

- **No discussion of limitations.** The paper lacks a limitations section. Several are worth explicitly acknowledging: (a) the composition mechanism uses a simple linear shift function, which is artificial compared to real-world dependencies; (b) the evaluation is zero-shot only with no few-shot or in-context learning baseline; (c) the WebShaper results suggest that the composition method may not transfer cleanly to non-math tasks; (d) all results are on English-language math/reasoning benchmarks. Acknowledging these would strengthen the paper's framing and help readers assess scope.

### Trivial

None.

## Nice-to-Haves

- Add partial credit metrics (e.g., average sub-problem accuracy or n-1 accuracy) alongside all-or-nothing scoring to disentangle cascading failures from independent per-problem failures.
- Provide a cost/runtime analysis to substantiate the repeated qualitative claim of being "low-cost."
- Report variance or confidence intervals for the RL training results (Table 1, Figure 4).

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Expected accuracy metric is "mathematically invalid."** REMOVED. The product of independent pass rates is a standard null baseline used for comparison — it estimates what accuracy would be if composition had no effect. The gap between actual and expected accuracy shows the cost of interdependence. This is a valid and informative comparison, not a flawed metric. The reviewer's assertion that actual accuracy is "strictly less than" the product is not mathematically guaranteed either.
- **All-or-nothing scoring conflates failure modes.** REMOVED from core weaknesses; the paper already provides detailed error-type analysis (Figure 5) and ablation studies (Appendix D) that address this concern.
- **No variance/statistical significance.** MOVED to Nice-to-Have. Single-run evaluation for 26 models across large benchmarks is standard practice in this field.
- **Model M for key variable extraction not specified.** REMOVED; this detail is likely in the appendix (which was stripped by the parser).
- **"Overthinking" circularity in framing.** REMOVED as too minor to merit inclusion.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Audit the evaluation table for the 127.6% entry and any other parsing or extraction errors. Document the answer-extraction pipeline's failure rate.
- Run the RL experiment with a control that matches total atomic problems seen (e.g., use twice as many n=1 training steps or twice as many n=1 data points) to disentangle composition from data quantity.
- Add a limitations section and explicitly discuss the o4-Mini WebShaper counterexample.

## Score and Decision

**MY FINAL SCORE: 7.0**

**MY FINAL DECISION: Accept**

The paper makes a substantial and well-motivated contribution: a practical method for constructing multi-horizon reasoning tasks, an impressively broad evaluation across 26 LRMs, diagnostic analyses that provide genuine insight into failure modes, and RL training results with practical implications. The weaknesses are real but addressable — the 127.6% value in the evaluation table is the most concerning, but it is best explained as a data-entry or parsing error that can be corrected, and the overall degradation trends are independently supported by the rest of the table. The RL data-quantity confound weakens but does not invalidate the training result, and the o4-Mini counterexample is a single exception in a large empirical study. With the data quality issue resolved and the confound discussed, the paper's contributions merit acceptance.