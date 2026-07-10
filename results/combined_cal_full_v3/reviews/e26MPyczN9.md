Now let me write the final consolidated review.

## Summary

This paper re-evaluates claims from the programmatic RL literature that programmatic policies generalize better than neural policies in out-of-distribution (OOD) settings. Through experiments on TORCS, KAREL, and PARKING, the authors show that much of the reported gap arises from experimental confounds (reward misspecification, observation design) rather than representational differences. The paper then introduces an expressivity/discoverability framework and makes a theoretically grounded positive contribution: constant-memory neural architectures (feedforward, fixed-size RNNs) cannot represent solutions whose working memory grows with input size (e.g., BFS in pathfinding), while programmatic representations can. A proof-of-concept with FUNSEARCH synthesizing BFS on a modified KAREL maze illustrates this.

## Strengths

- **Memory-capacity argument (Sections 4.4 and 5).** The paper makes a clean theoretical case that constant-memory models cannot represent solutions whose working memory scales with input size, such as breadth-first search (Θ(|V|) frontier+visited set). This is grounded in an information-theoretic lower bound (Ω(log|V|) bits just to index a vertex) and supported by references to known empirical limitations of LSTMs (Weiss et al., 2018). This identifies a genuine class of problems where programmatic representations have an in-principle advantage.

- **KAREL wall-following insight (Section 4.2, Figure 3).** The observation that partial observability helps OOD generalization in maze tasks because it forces the agent to learn local heuristics (follow-the-wall) rather than memorizing global layouts is genuinely interesting and somewhat counterintuitive. Table 2 shows PPO with a_{t-1} achieving 1.00 return on 100×100 mazes for StairClimber, Maze, TopOff, and FourCorner, matching or exceeding LEAPS.

- **Expressivity/discoverability framework (Definitions 2–3).** These definitions provide a useful vocabulary for diagnosing why a particular comparison might be misleading. The observation that prior work "inadvertently evaluated programmatic and neural representations that satisfied expressivity, and discoverability was controlled for the search in the programmatic space, but not in the neural space" (Section 1) is a fair diagnosis of a recurring pattern.

## Weaknesses

### Major

- **TORCS re-evaluation compares asymmetric conditions.** The central TORCS comparison pits NDPS trained with the original reward (β=1.0, historical data from Verma et al. 2018) against DRL trained with a modified cautious reward (β=0.5, new runs). These are different training objectives. The paper's claim that "once we replaced the original reward function with a safer one... neural policies matched programmatic ones in generalization" is based on this asymmetric comparison. Additionally, DRL generalization rates are computed only over the subset of seeds that completed training (13/30 for G-TRACK-1, 4/15 for AALBORG), introducing selection bias—the 17/30 seeds that failed to complete a lap on the training track are not represented in the generalization results. No variance is reported for NDPS lap times, making it impossible to assess statistical significance. The paper would be substantially strengthened by running both NDPS and DRL under identical conditions (same β, same seed count, same evaluation protocol).

### Minor

- **FUNSEARCH proof-of-concept is thin.** The paper's central positive claim—that programmatic representations provide an inherent advantage for problems requiring instance-scaling memory—rests on a single experiment: three runs of FUNSEARCH on one custom wall-sparse KAREL maze, all succeeding. No neural baseline is provided to empirically demonstrate that fixed-capacity models fail on this task (the theoretical argument is sound, but the paper markets this as a "proof-of-concept" experiment rather than a theoretical exercise). Three successful runs are not statistically meaningful for demonstrating robust capability.

- **PARKING results are inconclusive.** Table 3 shows PSM and DQN achieving nearly identical test success rates (0.16 vs 0.18 with overlapping confidence intervals). The paper acknowledges this ("PARKING is a challenging domain for both types of representation"), but the section does not clearly advance either the re-evaluation narrative or the memory-capacity thesis. The asymmetric sample sizes (30 PSM vs 15 DQN) are noted but not explained.

- **LSTM failure in KAREL is not ablated.** The paper attributes PPO with LSTM's poor performance (0.00 on 100×100 for StairClimber and Maze) to the model being "more complex to train" without an ablation that holds the observation space fixed while varying the model architecture. This is a plausible explanation but is not investigated.

### Trivial

- None beyond the minor points above.

## Nice-to-Haves

- Run NDPS with β=0.5 to enable a controlled comparison with DRL(β=0.5).
- Add a neural baseline (LSTM or transformer) to the FUNSEARCH experiment to empirically demonstrate failure on the wall-sparse maze.
- Report standard deviations or confidence intervals for NDPS results in Table 1.
- Clarify why sample sizes differ between PSM (30 seeds) and DQN (15 seeds) in the PARKING experiments.

## Removed Points

These points from the input review are removed with justification:

- **KAREL observation-space conflation (original Issue 2):** REMOVED because the paper does specify LEAPS's observation space through the DSL in Figure 2(a), whose perception functions (frontIsClear, leftIsClear, rightIsClear, markersPresent, noMarkersPresent) are inherently local/partially observable. The critic's concern that LEAPS may have used a fully observable grid is speculative and unsupported by the paper.

- **FUNSEARCH depends on a 30B neural LM (part of original Issue 3):** REMOVED because this misunderstands program synthesis—FUNSEARCH uses an LLM as a search tool over program space; the output is a program. The neural/programmatic boundary in synthesis is not a meaningful criticism of the paper's thesis.

- **The wall-sparse maze (Figure 7) not shown:** REMOVED because the appendix (including figures) was stripped by the extraction pipeline; it exists in the original submission.

- **Missing related works citations:** REMOVED per review policy (reviewers cannot verify existence of uncited works).

- **Formatting, typo, and style nitpicks:** REMOVED per review policy.

## Novel Insights

The key tension that emerges from the reviews is that the paper's two claims—negative (re-evaluation showing confounds) and positive (memory-capacity as the true differentiator)—operate at different levels of evidentiary support. The negative claim is suggestive but undermined by asymmetric experimental conditions (TORCS) and thin evidence (PARKING). The positive claim is theoretically rigorous (information-theoretic lower bound, connection to known LSTM limitations) but empirically thin (3 runs of a single experiment). This asymmetry is itself an interesting finding: the paper makes its strongest contribution when it stops trying to disprove prior claims and instead constructs a principled argument for when programmatic representations genuinely matter.

## Suggestions

1. **Strengthen the core theoretical contribution.** Foreground the memory-capacity analysis (Section 5) as the paper's primary contribution and treat the re-evaluation (Section 4) as a motivating discussion rather than a central experimental result. The theoretical argument is the paper's strongest asset.
2. **Run a controlled TORCS experiment.** Train NDPS with β=0.5 and compare OOD generalization under identical conditions. This would either validate or qualify the paper's confound claim.
3. **Add a neural failure experiment for FUNSEARCH.** Demonstrate empirically that an LSTM or transformer policy fails on the wall-sparse maze, to complement the theoretical argument.

## Score and Decision

**Score calibration anchors:**

| Path | Avg Score | Round | Itemized | Comparison |
|---|---|---|---|---|
| `/home/wg25r/split_review_opus_repro/.../NGVljI6HkR.md` | 3.67 | R1 | Yes | Directly comparable topic (programmatic policies in KAREL), but that paper lacked a novel theoretical contribution beyond the empirical comparison. The current paper has stronger theory but weaker experimental control in parts. |
| `/home/wg25r/split_review_opus_repro/.../MpA6HMD7Wq.md` | 3.00 | R1 | Yes | Similar framing (symbolic vs black-box generalization), but that paper had severe presentation issues and limited baselines. Current paper is stronger across all dimensions. |
| `/home/wg25r/split_review_opus_repro/.../It4KL6XnPq.md` | 3.00 | R1 | Yes | Memory-augmented RL policies. Less directly comparable but shares the memory+generalization theme. Current paper has a more novel theoretical argument. |
| `/home/wg25r/split_review_opus_repro/.../lUWf41nR4v.md` | 4.50 | R2 | Yes | Programmatic RL paper with similar methodological depth. Current paper has a stronger theoretical foundation but thinner empirical validation. |
| `/home/wg25r/split_review_opus_repro/.../R6klub5OXr.md` | 5.25 | R2 | Yes | Closest structural match—a re-evaluation/analysis paper combining theory and empirical study. Current paper has a more novel theoretical insight but less extensive and less rigorous empirical work. |
| `/home/wg25r/split_review_opus_repro/.../fvTaoyH96Z.md` | 2.33 | R1 | No | Environmental generalization in RL. Lower quality; current paper is substantially stronger. |

**Bracket from Round 1:** 4–6. The paper is clearly stronger than NGVljI6HkR (3.67) due to its theoretical contribution, but does not reach the 6+ tier because the headline re-evaluation claim is weakened by asymmetric experimental conditions.

**Narrowing in Round 2:** Comparing against R6klub5OXr (5.25) and lUWf41nR4v (4.50): the current paper's strengths (memory-capacity argument, favorability 9.41; wall-following insight, favorability 9.09) are stronger than those of the 4.50 anchor and comparable to the 5.25 anchor. The current paper's weaknesses (TORCS asymmetry at 3.66, FUNSEARCH thinness at 1.91) are moderately negative but not catastrophically so—unlike the -1.26 to -5.13 range seen in the 5.25 anchor. This positions the paper above 4.50 and near 5.25.

However, the TORCS asymmetry is a structural issue that cuts at the paper's headline claim, and the FUNSEARCH experiment lacks an empirical neural failure baseline. These prevent the paper from reaching the 6+ borderline-accept range. The paper's genuine theoretical contribution (memory-capacity analysis) and the KAREL wall-following insight are contributions worth preserving.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>