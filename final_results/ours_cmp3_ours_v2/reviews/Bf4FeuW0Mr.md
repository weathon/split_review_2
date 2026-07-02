Now I have a comprehensive calibration picture. Let me write the final review.

## Summary

DemoGrasp proposes a method for universal dexterous grasping that leverages a single demonstration trajectory. The key insight is that generalization can be decomposed into "where to grasp" (an SE(3) wrist transformation) and "how to grasp" (delta hand joint angles), formulated as a single-step MDP trained with RL on the editing parameters. A vision-based policy is then distilled via flow-matching on successful rollouts for sim-to-real transfer. Results show 95.2% success on DexGraspNet (Shadow Hand), 84.6% average across six unseen datasets on various embodiments, and 86.5% on 110 real-world unseen objects including small/thin items that have challenged prior work.

## Strengths

1. **Clever core idea (Section 2.2–2.3).** The insight that a single demonstration trajectory encodes reusable grasp patterns and that generalization decomposes into SE(3) wrist transformation plus delta joint angles is simple, well-motivated, and technically elegant. The single-step MDP reformulation effectively sidesteps the exploration and credit-assignment problems that plague prior multi-step dexterous grasping RL.

2. **Strong quantitative results on standard benchmarks (Table 1).** On DexGraspNet with the Shadow Hand, DemoGrasp achieves 95.2% (state) and 92.2% (vision), substantially outperforming prior methods including UniGraspTransformer (the previous SOTA). The ~1% generalization gap between training and unseen objects is notable.

3. **Comprehensive ablation study (Section 3.5, Tables 5, 8, 9).** The paper systematically isolates each design choice — RL vs. sampling-based exploration, contribution of each action-space component (translation, rotation, hand joints), effect of demonstration quality, and sufficiency of 175 training objects. The sampling+BC comparison (Table 5) is particularly informative.

4. **Real-world validation on challenging objects (Table 3, Section 3.4).** 110 unseen real-world objects with randomized poses, including small (76.7% success) and flat/thin (68.3% success) items that prior work has struggled with. This is a genuinely difficult and convincing test.

5. **Cross-embodiment generalization (Section 3.3).** Training on one embodiment and transferring to five others (different numbers of fingers, arm-mounted vs. floating) without retuning, with an average of 84.6% on unseen datasets, demonstrates strong generality.

## Weaknesses

### Major

- **Baseline comparisons are not fully controlled, weakening the precision of the "SOTA" claim.** The paper explicitly states (Section 3.2, p.5) that baseline methods "do not randomize object initial positions," while DemoGrasp is trained and tested with a 50cm×50cm spatial randomization. Baseline numbers are taken from published papers and were not re-run under spatially randomized conditions. The paper argues that spatial randomization makes the task *harder* for its method, which is reasonable, but without re-running baselines under identical conditions, the exact margin over prior work is uncertain. This does not undermine the paper's main conclusions (DemoGrasp clearly performs well), but it weakens the precision of the quantitative comparison in Table 1.

### Minor

- **Cross-dataset comparison (Table 2) is informative but not controlled.** The comparison against RobustDexGrasp uses methods trained on different object datasets. While both test on unseen data, zero-shot generalization depends on the training distribution, making this a reference comparison rather than a controlled one. The paper's framing is reasonable but slightly overstated.

- **Equation 2 has an ambiguity in the interpolation ratio.** The hand-joint interpolation involves elementwise division of a vector numerator by a vector denominator. If any joint angle does not change between the initial open pose and the grasp pose (denominator component = 0), the interpolation ratio is undefined. A clarifying note about handling this edge case would be helpful, even if the issue is unlikely in practice.

- **Vision-based policy details deferred to the appendix.** The transition from the state-based RL policy to the closed-loop vision-based policy (Section 2.4) is described very briefly, with key details relegated to Appendix E (which is stripped by the parser). Given that sim-to-real transfer is a primary contribution, the main text would benefit from clarifying: (a) whether the flow-matching policy outputs editing parameters or direct joint-space actions, and (b) how the open-loop editing scheme used during RL training relates to the closed-loop nature of the vision policy.

- **No limitations discussion.** The paper does not discuss failure modes, object categories or scenarios where the method systematically struggles, or the sensitivity of results to the specific demonstration trajectory. A limitations section would strengthen the paper.

- **No statistical variance reported for key results.** All numbers are point estimates. While the large-scale simulation results (3,400+ objects) likely have low variance, real-world results (5 trials per object, 110 objects) and cross-dataset results would benefit from confidence intervals or standard deviations.

### Trivial

None.

## Nice-to-Haves

- An analysis of failure cases — what objects does DemoGrasp systematically fail on and why?
- A brief note on training time and computational cost of the parallel RL setup.
- Clarification on how motion planning to the initial end-effector pose (Section 2.2, step 1) is handled in real-world deployment.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **Criticism about "single-step MDP" framing being imprecise:** The formulation is technically correct — the policy makes one decision per episode, which defines a single-step MDP (a contextual bandit). The terminology is appropriate and not misleading.
- **Criticism about reward design with disabled collision detection:** The critic suggested the policy could "learn to always use collision-allowed environments," but environments are randomly assigned per episode — the policy cannot choose its environment type.
- **Table garbling in Section 3.3:** A PDF extraction artifact where all six embodiments show identical numbers. This is a parser issue, not an author error.
- **"First to grasp" claim in abstract:** The paper qualifies this with "to our knowledge." Generic criticism applicable to any first claim; the paper provides supporting evidence.
- **Missing appendix details:** The parser strips appendix content; these details exist in the original submission.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Re-run the Table 1 baselines under spatially randomized conditions (using publicly released checkpoints if available) to tighten the comparison.
- Add a limitations paragraph discussing failure modes.
- Clarify the vision-based policy's relationship to the editing parameter space in the main text.
- Report confidence intervals or standard deviations for real-world and cross-dataset results.
- Add a note in the text about the edge case in Equation 2's interpolation ratio.

## Score and Decision

### Calibration Anchors

**Round 1 (Bracketing):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `deepreview_13k_calibration/BUj9VSCoET.md` (ResDex) | 7.00 | R1 | Similar topic (universal dexterous grasping on DexGraspNet). ResDex achieves 88.8% with no real-world experiments. DemoGrasp has higher scores (95.2%) and extensive real-world validation. |
| `deepreview_13k_calibration/twIPSx9qHn.md` (Cross-Embodiment Dex Grasping) | 5.00 | R1 | Cross-embodiment dexterous grasping at 80% on YCB. DemoGrasp has broader evaluation, higher scores, and real-world tests. |
| `deepreview_13k_calibration/ajSmXqgS24.md` (DexTrack) | 6.25 | R1 | Dexterous manipulation tracking from human references. DemoGrasp has more comprehensive evaluation and cleaner methodology. |
| `deepreview_13k_calibration/VEdeDd13gx.md` (ManiBox) | 5.25 | R1 | Spatial grasping generalization via sim data. DemoGrasp has broader scope and stronger results. |
| `deepreview_13k_calibration/eJHnSg783t.md` (DIFFTACTILE) | 6.50 | R1 | Tactile simulation, different sub-area. |
| `deepreview_13k_calibration/jNR6s6OSBT.md` (ASID) | 6.75 | R1 | System identification for manipulation. Less directly comparable. |

**Round 1 bracket:** 6.5 – 8.0 (DemoGrasp is stronger than ResDex at 7.0 due to real-world validation and higher simulation scores, but the baseline comparison concern prevents it from reaching the 8+ tier)

**Final score:** 7.5

DemoGrasp presents a genuinely novel and well-executed approach to dexterous grasping. Its core idea (demonstration editing + single-step RL) is elegant, its experimental validation is unusually broad (large-scale simulation, real-world on 110 objects, multiple embodiments, cluttered scenes), and the results are compelling. The main limitation — that baseline comparisons in Table 1 were not run under identical conditions — is transparently acknowledged by the paper and does not undermine the core contribution, but it prevents the evaluation from being fully definitive. The paper should be accepted.

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>