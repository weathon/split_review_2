## Summary

This paper proposes DemoGrasp, a framework for universal dexterous grasping that starts from a single demonstration and adapts it to novel objects by editing the wrist pose (where to grasp) and hand joint angles (how to grasp). The key innovation is formulating this editing task as a single-step MDP, which dramatically reduces the exploration burden and eliminates the need for complex reward shaping. The RL policy is trained in simulation, and a vision-based flow-matching policy is distilled from its successful rollouts for sim-to-real deployment. Results show SOTA performance on DexGraspNet (95.2% state-based, 92.2% vision-based), strong cross-embodiment generalization (84.6% across six unseen datasets), and successful real-world grasping of 110 unseen objects including small/thin items that have challenged prior work.

## Strengths

- **Novel and well-motivated formulation (Section 2.2–2.3).** The idea of decomposing grasping into *where* (SE(3) wrist transformation) and *how* (delta joint angles) via demonstration editing, then formulating this as a single-step MDP, is genuinely clever. The compact action space and single-step horizon eliminate the need for complex reward engineering — the policy uses only binary success plus a collision penalty (Equation 3). The core insight that a single demonstration encodes transferable approach-squeeze-lift patterns is clearly articulated and backed by Table 9, which shows that virtually any successful demonstration yields comparable final performance.

- **State-of-the-art simulation results with meaningful margin (Table 1).** On DexGraspNet with the Shadow Hand, DemoGrasp achieves 95.2% (state-based) and 92.2% (vision-based), surpassing UniGraspTransformer by 4–5 points. The generalization gap between training and unseen categories is only ~1%. Notably, baselines train/test without position randomization while DemoGrasp uses a 50cm × 50cm reset region, making the comparison *conservative* in DemoGrasp's favor.

- **Cross-embodiment and cross-dataset generalization evidence (Section 3.3).** Training on only 175 objects and generalizing to six unseen datasets across five different hand embodiments (including a parallel gripper) with an average 84.6% success rate is substantively impressive. The method does not overfit to a specific hand morphology.

- **Real-world results on challenging objects (Table 3).** 95.3% on 110 unseen normal-sized objects is strong. More importantly, the paper addresses the underexplored problem of small/thin objects in tabletop settings (68.3% for flat/thin, 76.7% for small), which prior work struggles with. The reward design that probabilistically disables table-collision detection (Section 2.3) is a principled solution for flat objects.

- **Thorough ablation study (Section 3.5).** The paper ablated alternative approaches (sampling+BC vs. RL in Table 5), isolated the contribution of each action-space dimension (Table 8), tested demonstration quality robustness (Table 9), and verified that 175 training objects suffice (Table 7). This goes beyond typical ablation scope.

## Weaknesses

### Fatal
None.

### Major
- **No variance or confidence intervals for simulation results (Tables 1, 2, 5, 7, 8).** All success rates are reported as point estimates without standard deviations or confidence intervals. Grasping success is stochastic due to object pose randomization and physics noise. While the margins over baselines are large enough (4–5%) that the ranking is unlikely to change, the absence of variance reporting limits the precision of SOTA claims. For the primary benchmark (Table 1), reporting mean ± std over 3–5 random seeds is expected.

### Minor
- **Real-world cluttered-scene evaluation is small (Section 3.4, 10 scenes).** The paper reports 82% and 84% success rates on 10 cluttered scenes with 5–8 objects each. With roughly 8–9 successes out of 10 trials, a single failure shifts the rate by 10 percentage points. The simulation cluttered-scene results are also reported without variance. This does not invalidate the contribution, but the language-conditioned grasping results should be interpreted as preliminary.

- **Vision-based policy is trained via imitation learning, not RL (Section 2.4).** The closed-loop vision policy is trained by behavior cloning (flow-matching on the RL policy's successful rollouts). This means it never benefits from RL's corrective trial-and-error in the vision domain, and its ability to recover from out-of-distribution states is limited. The strong real-world results partially mitigate this concern, but the ~3% gap between state-based (95.2%) and vision-based (92.2%) on DexGraspNet conflates sim-to-real domain gap with the regression from RL to imitation learning. The paper does not discuss this design trade-off.

- **Post-lift trajectory simplification is not discussed as a limitation (Section 2.2).** After T_lift, the hand pose is held constant and the end-effector follows a fixed vertical lift. This is a deliberate simplification for tabletop grasping, but it would fail for objects requiring lateral or rotational motion during extraction (e.g., pulling a tool from a tight holder). The paper scopes to tabletop settings but does not explicitly state this limitation.

- **Collision-disable fraction (50%) is presented without justification or sensitivity analysis (Section 2.3).** The paper randomly disables table-collision detection in half the environments. While this design is reasonable, no ablation explores whether 50% is optimal or whether the method is robust to this hyperparameter (e.g., 0%, 25%, 75%, 100%).

- **Baselines not tested under the same position-randomization condition.** The paper correctly notes that baselines do not randomize object positions. However, running the best baseline (UniGraspTransformer) with the same 50cm × 50cm position randomization used for DemoGrasp would provide a cleaner comparison and more rigorously establish the spatial generalization advantage.

### Trivial
None.

## Nice-to-Haves

- Report inference speed / computational cost for the vision policy, which would be useful for real-world deployment considerations.
- Retrain RobustDexGrasp on the same 175-object training set used by DemoGrasp for a cleaner comparison in Table 2 (the paper acknowledges the distribution mismatch).
- A sensitivity analysis on the collision-disable fraction would clarify robustness to this hyperparameter.

## Removed Points

These points are flagged to be removed — treat them with caution.

- **Vision implementation details deferred to appendix (action chunk horizon, flow steps, ViT variant).** The paper states "Further implementation details are provided in Appendix E." Since the appendix was stripped by the PDF parser and exists in the original submission, this is not a valid criticism of the authors' submission.
- **Suggestion to replace RL with residual RL.** This is speculative and not a concrete weakness — the paper already demonstrates a working method with strong results.
- **Generic "inference speed not reported" framed as weakness.** Moved to Nice-to-Haves.

## Novel Insights

The reviewer raises a genuinely useful observation beyond the paper's own contributions: the comparison in Table 1 is asymmetric in DemoGrasp's favor (baselines without position randomization vs. DemoGrasp with 50cm × 50cm randomization). This means the reported margin likely *understates* DemoGrasp's spatial generalization advantage — a point the paper mentions but the reviewer correctly frames as strengthening the result rather than weakening it. No other novel insights emerge beyond the paper's own contributions.

## Suggestions

1. Add multi-seed statistics (mean ± std over 3–5 seeds) to Table 1, and ideally to the other main results tables, to ground the SOTA claims statistically.
2. Test UniGraspTransformer under the same 50cm × 50cm position-randomization condition to isolate the spatial generalization advantage.
3. Expand the real-world cluttered-scene evaluation to 30–50 scenes for more reliable conclusions.
4. Explicitly discuss the post-T_lift trajectory simplification (fixed vertical lift, static hand pose) as a limitation in the main text.
5. Include a brief sensitivity analysis for the collision-disable fraction, or add a note justifying the 50% choice.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>