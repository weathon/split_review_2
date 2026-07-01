Now let me produce the final review.

## Summary

This paper addresses the completeness-efficiency trade-off in state representation for RL-based Dynamic Path Planning (DPP). The authors propose a Dynamics Feature Representation (DFR) framework: (1) a policy attention mechanism that selects top-k shortest paths by static distance to form a task-relevant subgraph, and (2) an n-hop neighborhood method that extracts node-local features from that subgraph. Experiments on three urban road networks compare DQN, GCN+DQN, and PPO with and without DFR, showing that DFR improves performance while reducing feature dimensionality.

## Strengths

- **Hierarchical two-stage decomposition has clear conceptual motivation.** Separating task-relevant filtering (policy attention → W') from agent-centric locality (n-hop → W'') is a sensible design principle for graph-based feature compression. The formalization in Equation 5 (W → W' → W'') captures this cleanly.

- **The ablation study (Figure 6, Section 5.3) provides useful insight into hyperparameter sensitivity.** The heatmap tables for (k, n) combinations across Mean GAP, SR, and CR give concrete evidence of how the two parameters interact. The systematic exploration shows diminishing returns as n increases, which is practical guidance for users.

- **Experiments cover three distinct urban networks and three RL algorithms (DQN, GCN+DQN, PPO), demonstrating generality.** DFR-enhanced models consistently outperform their AD counterparts across all nine algorithm/network combinations. The ablation also shows that n-hop alone (k=-1) can improve performance, disentangling the contribution of each component to some degree.

## Weaknesses

### Major

- **The policy attention mechanism selects subgraphs based on static distance, but DPP is about time-varying traffic costs — the paper provides no analysis validating that distance-based subgraphs retain the information needed for time-optimal routing.** The core idea (Section 4.3) relies on top-k shortest-distance paths to define the "task-relevant" subgraph. Under realistic congestion where short roads are jammed, the optimal detour may use longer-distance edges not in any top-k shortest path. The paper's justification ("distance naturally serves as one of the most fundamental constraints," line 149) is a reasonable intuition but is not backed by any analysis of overlap between distance-based subgraphs and optimal dynamic paths under varying congestion intensities. This is the most significant gap in the paper's evidence — without such validation, it is unclear whether the method's central design choice is beneficial or potentially harmful.

- **The claimed "accelerated convergence" (abstract, contributions line 23) is not demonstrated.** The training curves in Figure 6 (bottom) compare different DFR configurations (varying n, fixed k=0.6) but do not overlay any DFR model against its AD baseline. Convergence acceleration is listed as a core contribution but is entirely unsupported by the reported experiments.

- **Several baselines that would isolate DFR's actual contribution are missing.** The only baseline is AD (all edge weights as a flat feature vector), which has vastly higher input dimensionality — feature compression helping neural network training is well-known. The paper would benefit from: (a) a random-subgraph baseline at the same compression ratio to test whether distance-based selection is better than any compression; (b) comparison with existing DPP-specific state representation methods from the cited literature (e.g., Du et al., 2024a; Lin et al., 2025). (Note: the ablation's k=-1 and n=-1 settings partially address some component ablations, but these missing baselines are more serious.)

### Minor

- **The PSR theoretical grounding (Section 4.2, lines 129–135) is invoked as a "guarantee" but is not substantiated.** PSR requires a representation to predict all future observation probabilities given all action sequences — a stringent condition that DFR makes no effort to verify. The paper states that "grounding DFR in PSR principles thus guarantees that the resulting representations are compact, temporally predictive, and theoretically sufficient" (line 135), but provides no proof or even informal argument connecting DFR's hand-designed feature subset to the PSR condition. This reads as conceptual window-dressing. The paper would be stronger if it acknowledged DFR as a heuristic with empirical justification.

- **Data inconsistency between text and heatmap table for the AD baseline.** The ablation text (line 208) states that the DQN+AD baseline achieves "SR of 0.884 and a Mean GAP of 0.170." The corresponding heatmap entries (lines 226, 236) show Mean GAP=0.176 and SR=0.864. Neither value matches. The discrepancy is small (~4–7% relative) but indicates imprecise reporting.

- **No statistical significance is reported.** Mean GAP, SR, and CR are presented as point estimates without error bars or confidence intervals. Given randomness in source–goal sampling and RL training, the reliability of the reported differences is unclear.

- **The congestion model (Equation 9) assumes spatially uncorrelated random factors per edge per timestep.** Real traffic congestion propagates spatially (e.g., gridlock spreading from a bottleneck), which tends to push optimal detours farther from shortest-distance routes. The uncorrelated model likely makes the problem easier for distance-based attention, since independently random congestion still has substantial overlap with shortest-distance paths. This limitation should be explicitly acknowledged and discussed.

### Trivial

None.

## Nice-to-Haves

- An analysis measuring the overlap between top-k shortest-distance subgraphs and ground-truth optimal dynamic paths under varying congestion regimes would directly validate (or invalidate) the method's core design assumption.
- A random-subgraph baseline at matched compression ratios would help isolate whether distance-based selection specifically — rather than compression in general — drives the performance gains.
- Showing DFR vs. AD convergence curves would substantiate the convergence acceleration claim.
- Consider using Dijkstra's algorithm instead of RL for the static shortest-path subtask, which is exact and inexpensive.

## Removed Points

- **D\* Lite / traditional re-planning algorithm comparison**: The paper explicitly scopes its contribution as investigating state representation within the RL paradigm (footnote 3, line 165: "Our work instead aim to investigate the impact of the DFR framework within the RL paradigm"). Criticizing the absence of non-RL comparisons falls outside the stated scope.
- **"Missing local-only baseline fully absent"**: The ablation study already includes settings equivalent to this (k=-1, n>0 = n-hop without policy attention; k>0, n=-1 = policy attention without n-hop). The critic's specific concern about a local-only baseline is partially addressed by existing data.
- **Generic problem-importance framing**: Removed as not specific to this paper's contribution.
- **"Why use RL for shortest paths instead of Dijkstra" elevated to major**: Demoted to minor/nice-to-have. It is a valid observation but does not threaten the paper's core claims.

## Novel Insights

None beyond the paper's own contributions. The reviews surface a straightforward but important gap — the paper's central design choice (distance-based attention) is not validated against its purpose (time-optimal routing under dynamic congestion) — but this is a critique of the evidence, not a novel insight about the method.

## Suggestions

1. **Validate the distance-based attention assumption.** Compute the overlap between top-k shortest-distance subgraphs and ground-truth optimal dynamic paths under varying congestion intensities (e.g., low, moderate, high β regimes). This is the single most important experiment to establish that DFR's core mechanism actually retains decision-relevant information.
2. **Add missing baselines.** A random-subgraph baseline at matched compression ratios would directly test whether distance-based selection matters. Comparison with existing DPP-specific representation methods (cited in the paper's own related work) would show where DFR sits relative to the state of the art.
3. **Provide DFR vs. AD convergence curves** to support the claimed accelerated convergence.
4. **Correct the data inconsistency** between the text (line 208) and heatmap tables for the AD baseline values.
5. **Add statistical significance reporting** (error bars or confidence intervals) for all main metrics.
6. **Tone down the PSR framing.** Either provide a rigorous argument connecting DFR features to predictive state conditions, or acknowledge DFR as a well-motivated heuristic with empirical support.

## Score and Decision

**Calibration anchors** (from `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/`):

| Path | Avg Human Score | Round | Comparison |
|------|----------------|-------|-----------|
| ZiF1bJ9K6B.md (Learning Coverage Paths with RL) | 4.75 | 1 | More thorough evaluation (classical baselines, ablations), the paper under review has a clearer problem framing but weaker baselines |
| sEv6vHIUnu.md (Structured Predictive Representations in RL) | 4.80 | 1 | Similar overclaiming of theoretical grounding (predictive state representations), comparable evidence level |
| NIhRwzqhUz.md (Learning the Partially Dynamic TSP) | 3.00 | 1 | Narrower contribution, the paper under review is stronger |
| z3L59iGALM.md (Massively Scalable IRL in Google Maps) | 5.25 | 1 | Real-world deployment at Google scale, far more thorough validation; the paper under review has less experimental rigor |
| Pj3ErOxlLo.md (NaviFormer) | 6.00 | 2 | RL path planning with new architecture, more complete evaluation; the paper under review has a significant unaddressed gap in its core design choice |
| TOiageVNru.md (Physics-informed TD Metric Learning) | 6.00 | 2 | Strong theoretical grounding + thorough experiments; the paper under review has weaker theoretical backing and evidence |

**Round 1 bracket:** The paper sits between the 3.0 (reject) and 5.25 (mixed accept) bands — its problem framing and method are better than the 3.0 papers, but its experimental evidence is weaker than the 4.75–5.25 papers due to the unvalidated core design assumption and missing baselines.

**Round 2 narrowing:** Comparing directly to coverage-path-planning (4.75) and structured predictive representations (4.80) papers, the paper under review has a more significant methodological gap (distance vs. cost mismatch) that the other papers do not, pulling it downward.

**Final calibrated score: 4.0**

This paper identifies a genuine problem and proposes a sensible hierarchical framework. However, its core design choice — distance-based attention for a time-cost minimization problem — is insufficiently validated. A core claimed contribution (accelerated convergence) is not shown. The experimental comparison is limited to a single, structurally favorable baseline. These weaknesses collectively prevent the paper from making a convincing case in its current form.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>