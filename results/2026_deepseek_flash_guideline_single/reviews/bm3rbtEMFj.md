Now I have sufficient calibration data. Let me produce the final consolidated review.

## Summary

ELMUR proposes a transformer architecture augmented with per-layer external memory embeddings managed by a Least Recently Used (LRU) update rule using replacement or convex blending, with bidirectional cross-attention between token and memory tracks. Evaluated via imitation learning/behavior cloning on T-Maze, POPGym (48 tasks), and MIKASA-Robo (visual robotic manipulation), it achieves 100% success on T-Maze corridors up to 1M steps and clear gains on several MIKASA-Robo tasks.

## Strengths

1. **Strong T-Maze retention.** ELMUR achieves 100% success on T-Maze corridors up to 1 million steps while all baselines degrade (Figure 3). The 100,000× extension beyond the attention window is a clean, concrete demonstration of the LRU memory mechanism's ability to retain information across extreme horizons. The generalization heatmap (Figure 4) showing seamless transfer across training/validation lengths further reinforces this result.

2. **Clear gains on visual robotic manipulation.** On RememberColor3-v0 (0.89 vs. 0.65 for RATE) and TakeItBack-v0 (0.78 vs. 0.42), ELMUR shows substantial improvements on tasks with visual observations, continuous actions, and sparse rewards. These are non-trivial robotic tasks closer to realistic settings than synthetic benchmarks.

3. **Well-specified architecture.** Algorithms 1 and 2, Equations 1–8, and the description of the memory track, token track, relative bias, and LRU mechanism provide sufficient detail for implementation. The design choices are clearly motivated.

4. **Informative ablation study (Table 3, Figure 6).** The ablations clarify which components drive performance: per-layer memory and LRU are critical; relative bias and MoE-FFN contribute little. This honesty helps the community understand where the method's value lies. The scaling analysis of memory size \(M\) relative to required segments \(N\) (Figure 6c-d) is particularly useful.

## Weaknesses

### Fatal
None.

### Major

1. **Framing mismatch: "RL problems" vs. IL evaluation.** The title claims "Long-Horizon RL Problems" and the abstract invokes the "RL paradigm," but the method is trained purely via supervised imitation learning/behavior cloning. Section 3 states: "Training is supervised, minimizing the error between predicted and demonstrated actions." The paper explicitly excludes online RL baselines (Section 5.1: "We do not compare with online RL baselines, since they assume interactive data collection with exploration, yielding incomparable training budgets"). While the paper does acknowledge IL in the introduction ("how can we equip IL policies with efficient long-term memory"), the title and abstract consistently overclaim scope. The pasta-cooking robot example in the introduction describes an exploration/discovery problem that the method never faces. This is a substantive framing issue—the paper should reposition itself as a memory-augmented IL architecture rather than claiming to solve "RL problems."

2. **Unexplained statistical inconsistency between Table 1 and Table 3 on RememberColor3-v0.** Table 1 reports ELMUR achieving 0.89 ± 0.07 (3 runs, 100 evaluation episodes). Table 3 reports the "Baseline ELMUR" ablation achieving 1.00 ± 0.00 (3 runs, 20 evaluation episodes). If the underlying success probability were ~0.89, obtaining 20/20 successes across three independent runs (60/60 total) is statistically implausible under standard binomial sampling (\(p \approx 0.0009\)). The ablation section notes it uses 20 episodes rather than 100, but this alone does not resolve the contradiction. The authors must disclose what configuration difference (different \(\lambda\), \(M\), segment length, or task variant) accounts for this discrepancy. As presented, this undermines trust in both tables.

3. **Inconsistency in MIKASA-Robo task count.** The abstract and introduction consistently state "21 out of 23 tasks" (lines 9, 27). The caption of Table 1 says "See results for all **32** MIKASA-Robo tasks in Appendix, Table 8." The main paper shows results for only 4 tasks. This is a clear reporting discrepancy: if there are 23 tasks, the caption is wrong; if 32, the abstract and introduction are incomplete. The authors must resolve this.

### Minor

4. **Modest POPGym aggregate gains.** On the aggregate "All (48)" metric, ELMUR scores 10.4 vs. RATE at 9.5—roughly 9% relative improvement. On the 15 "Reactive" tasks, ELMUR (9.2) is essentially tied with DT (9.3) and RATE (9.1). The paper's claim of "ranking first on 24 of 48 tasks" is a ranking, not a statistical comparison. For a method whose central claim is long-horizon memory, one might expect larger advantages on a benchmark specifically designed to test memory. The improvement is genuine but modest.

5. **Theoretical analysis (Section 4) is elementary and contributes little.** Proposition 1 restates the exponential decay of a convex combination—a direct algebraic consequence of the update rule. Proposition 2 proves that convex combinations of bounded vectors stay bounded—trivially true. The half-life and effective horizon formulas follow immediately. No analysis is provided of information capacity, interference between stored items, retrieval accuracy, or any non-obvious property. The contribution statement ("formal guarantees on forgetting, retention horizons, and stability") overstates the substance. This does not harm the empirical contribution, but the section should either be expanded with genuine insight or removed/reduced.

6. **Missing GTrXL baseline.** Gated Transformer-XL (GTrXL) is a standard backbone for POMDP RL that uses gating and recurrence. Including it would strengthen the comparison set. The current baseline set (RATE, DT, DMamba, BC-MLP, BC-LSTM, CQL, DP) is reasonable but omits this relevant architecture.

### Trivial
None.

## Nice-to-Haves

- Report per-task confidence intervals or significance tests (e.g., paired bootstrap) on POPGym to support the "first on 24 of 48" claim statistically.
- Include training time, memory usage, and FLOPs comparisons across methods beyond the ms/step figure.
- Extend the T-Maze evaluation to require recalling multiple cues or associating cues with different contexts, which would better stress the memory system beyond single-bit recall.
- Drop the MoE-FFN or clearly justify it—the ablation shows replacing it with a standard MLP preserves accuracy.

## Removed Points

These points were flagged for removal; treat them with caution:
- **Criticism about appendix-deferred details** (hyperparameters in Table 7, full MIKASA-Robo results in Table 8, per-task POPGym results in Table 5). Removed because the appendix was stripped by the parser and exists in the original submission. The paper states these are in the appendix.
- **Criticism about missing online RL baselines.** Removed because the paper explicitly scopes this out with a clear justification ("incomparable training budgets"). This is a legitimate scoping choice.
- **Criticism about missing real-robot experiments.** Removed per the paper's scope justification.
- **Criticism that T-Maze is not challenging enough because RATE/BC-MLP maintain ~0.7 at 1M steps.** ELMUR achieves 100% while baselines are at ~70%; this is a meaningful gap. The critic's point about the 100,000× multiplier deriving from a small context window (L=10, S=3) is factually correct but reflects the paper's own framing and does not invalidate the result.
- **Strength about "addressed an important problem"** — removed as generic and superficial.
- **Several minor/overstated claims from the harsh critic about MoE being "unnecessary complexity"** — the ablation shows MoE→MLP preserves accuracy, and the paper notes this. Whether to simplify is a design choice, not a weakness.

## Novel Insights

The primary novel insight emerging from the review is the statistical tension between Tables 1 and 3. If the "Baseline ELMUR" ablation is meant to use the same configuration as the main evaluation, the 0.89 vs. 1.00 discrepancy on RememberColor3-v0 is deeply unlikely and undermines confidence in both tables. If the ablation uses a different configuration (different \(\lambda\), \(M\), segment length), this must be transparently disclosed. Beyond this, the reviews do not surface insights beyond the paper's own contributions.

## Suggestions

1. **Fix the framing.** Change the title from "Long-Horizon RL Problems" to "Long-Horizon Imitation Learning" or "Decision Making under Partial Observability" to accurately reflect the evaluation setting.
2. **Resolve the 0.89 vs. 1.00 inconsistency.** Explicitly disclose any configuration differences between Table 1 and Table 3 for RememberColor3-v0 (different \(\lambda\), \(M\), segment length, or task variant).
3. **Harmonize the MIKASA-Robo task count.** Ensure consistency between the abstract ("21 out of 23 tasks") and the Table 1 caption ("all 32 tasks").
4. **Either expand Section 4 with meaningful analysis** (capacity bounds, interference analysis) or drop the theoretical claims.
5. **Add GTrXL as a baseline** if feasible, or discuss its absence.
6. **Report per-task significance tests on POPGym** to strengthen the "first on 24 of 48" claim.

---

**Calibration Report**

Retrieved anchors (all rounds):

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/c4w7WVs1z7.md` (RATE) | 4.75 | 1,2 | Closest baseline; ELMUR has stronger architecture and better results but has reporting inconsistencies RATE didn't have |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/It4KL6XnPq.md` (Foundation Policies with Memory) | 3.00 | 1 | Also evaluates memory on POPGym; ELMUR's architecture is more novel and results are stronger |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/FhbZ1PQCaG.md` (Think Before You Act) | 5.75 | 1,2 | Similar domain (memory-augmented DT); cleaner reporting but less novel architecture |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/wYJII5BRYU.md` (DHTM) | 5.75 | 2 | Temporal memory for POMDPs; accepted. Cleaner reporting |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/324fOKW1wO.md` (SimDT) | 3.33 | 1 | Imitative decision transformer for driving; weaker results |

**Round 1 bracket**: [4.0, 6.0]

**Round 2 narrowing**: Compared against RATE (4.75) and Think Before You Act (5.75). ELMUR has a more novel architecture than RATE and better T-Maze results, but the reporting inconsistencies (0.89 vs 1.00, 23 vs 32) are specific problems that RATE did not face. The paper sits between these two anchors—stronger methodologically than RATE but with unresolved factual discrepancies that prevent it from reaching the 5.75 level.

**Final score**: 5.0

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>