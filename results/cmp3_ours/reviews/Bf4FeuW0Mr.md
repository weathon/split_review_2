## Summary

DemoGrasp proposes a framework for universal dexterous grasping that reformulates the problem as editing a single demonstration trajectory. The policy outputs SE(3) wrist transformations and delta hand joint angles (editing parameters) in a single step, after which the edited trajectory is replayed open-loop. This turns a long-horizon RL problem into a near-contextual-bandit problem with compact action space. The method achieves strong results: 95% state-based and 92% vision-based on DexGraspNet with Shadow Hand, 84.6% average across 6 unseen datasets and 6 hand embodiments, and 86.5% real-world success on 110 objects including small/thin items.

## Strengths

- **Novel and elegant formulation.** The core insight—search over edits to a single demonstration rather than over low-level actions—is non-obvious and effectively transforms a high-dimensional exploration problem into a much simpler one. The connection between "where to grasp" (wrist edit) and "how to grasp" (hand joint edit) is well-motivated.
- **Strong empirical results across multiple axes.** The method achieves 95% state-based / 92% vision-based on 3.4K DexGraspNet objects, surpassing UniGraspTransformer by 4–5%. Cross-embodiment results (84.6% average across 6 hands on unseen datasets, trained on only 175 objects) and real-world results (86.5% on 110 objects, 71.1% on small/thin objects) are compelling.
- **Minimal reward engineering.** The reward is simply binary success × binary no-collision (with a clever trick to permit finger-table contact in half the environments), notably simpler than the dense reward functions used in prior work, yet achieves SOTA.
- **Well-designed ablations.** Ablations cover RL vs. sampling (Table 5, 19% gap), contribution of each action-space component (Table 8), training set size (Table 7, 175 objects nearly sufficient), demonstration quality robustness (Table 9), and camera configurations (Table 6). These go beyond box-ticking and actually support the paper's claims.

## Weaknesses

### Fatal

None.

### Major

- **Open-loop vs. closed-loop comparison in state-based setting (Table 1).** DemoGrasp's state-based RL policy operates in a single step: it observes the initial state, outputs editing parameters, and the edited trajectory is replayed open-loop without further feedback. The baselines (UniDexGrasp, UniDexGrasp++, UniGraspTransformer) learn closed-loop policies that receive state observations at each timestep and adjust actions continuously. This is a fundamentally different control paradigm, and the paper does not acknowledge this architectural difference when presenting Table 1. The vision-based comparison (where DemoGrasp's flow-matching policy is closed-loop) is fairer and still shows clear improvement (92% vs 88.9%), but by a smaller margin. The paper should discuss whether the advantage stems from the editing formulation, the open-loop simplification, or both.

- **Uncontrolled baseline evaluation protocols.** The paper states (line 131) that "the baseline methods do not randomize object initial positions, whereas our method is trained and tested with a large reset region of 50cm × 50cm." This means the numbers in Table 1 reflect different evaluation protocols, not a controlled experiment. Similarly, the RobustDexGrasp comparison in Table 2 acknowledges "trained on different object datasets." The paper argues these differences make DemoGrasp's task harder, which is plausible, but the lack of controlled comparison weakens the precision of claims like "surpasses previous state-of-the-art methods by a large margin." The real-world results and ablations independently support the method's value, but the main simulation comparisons should be more carefully framed.

### Minor

- **Terminological imprecision: "single-step MDP" vs. contextual bandit.** The formulation (Section 2.3) is technically a contextual bandit (single action, single terminal reward), not an MDP. Calling it a "single-step MDP" is imprecise; a 1-step horizon MDP would still involve an intermediate state transition. This doesn't affect the method's validity but over-claims the generality of the reformulation.

- **Potential numerical issue in Equation (2).** The hand-pose interpolation involves elementwise division by `(q*_{T_lift} - q*_0)`. If any hand joint has the same angle at both the open and grasp poses, this would cause division by zero. In practice most joints change, but this edge case is unaddressed.

### Trivial

None.

## Nice-to-Haves

- A controlled experiment retraining/evaluating baselines under the same 50cm × 50cm position randomization used for DemoGrasp would substantially strengthen the comparison.
- A failure-mode analysis (what causes the remaining failures on small/thin objects: geometry, vision, or execution?) would be valuable for future work.
- An ablation isolating why the single-step editing formulation outperforms closed-loop baselines (is it easier exploration, avoidance of compounding errors, or the editing parameterization itself?) would strengthen the theoretical contribution.

## Removed Points

These points are flagged to be removed, treat them with caution:
- **Criticism about missing RL algorithm / architecture details in main text** (Harsh Critic's "Missing Parts #2"): The reviewer notes that the main text does not specify the RL algorithm or network architecture, saying these are "presumably in the appendix." Since the appendix is stripped by the parser and these details exist in the original submission, this criticism is removed per the parser-strip rule.
- **Criticism about failure analysis not being included** (Harsh Critic's "Missing Parts #1"): This is a suggestion for additional analysis, not a weakness in the presented work. The paper provides extensive evaluation and is not deficient for not including failure analysis.
- **Criticism about the "open-loop to closed-loop gap" analysis** (Harsh Critic's "Missing Parts #3"): Similarly a suggestion for additional decomposition, not a weakness. Already captured in Nice-to-Haves.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Explicitly acknowledge the open-loop vs closed-loop architectural difference when presenting the state-based comparison, and discuss its implications for interpreting the results.
- Frame the single-step formulation as a contextual bandit (or "single-decision formulation") rather than a "single-step MDP" for terminological precision.
- Add a brief note in the main text about the numerical edge case in Equation (2) and how it is handled.

## Calibration Report

**Round 1 bracket:** [6.5, 8.5] — based on comparison with directly relevant papers.

**Anchor papers retrieved across rounds (all rounds):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `BUj9VSCoET.md` (ResDex: Efficient Residual Learning with MoE for Universal Dexterous Grasping) | 7.0 | 1,2 | Most directly comparable. Sim-only evaluation, 88.8% on DexGraspNet. DemoGrasp is clearly stronger: higher success rate (95%), real-world experiments, broader evaluation, simpler formulation. |
| `twIPSx9qHn.md` (Cross-Embodiment Dexterous Grasping with RL) | 5.0 | 1 | Related topic but weaker: 80% on YCB, limited real-world, fewer hands. DemoGrasp is much stronger. |
| `VEdeDd13gx.md` (ManiBox) | 5.25 | 1 | Simpler grasping (parallel gripper), rejected. DemoGrasp is substantially stronger. |
| `ajSmXqgS24.md` (DexTrack) | 6.25 | 1 | Different focus (tracking control). DemoGrasp has broader evaluation and stronger results. |
| `meRCKuUpmc.md` (PIDM/Seer) | 7.5 | 2 | Manipulation pre-training, different sub-area. Comparable quality of contribution. |
| `pISLZG7ktL.md` (Data Scaling Laws) | 8.0 | 1,2 | Very strong unanimous Accept. DemoGrasp is not quite at this level due to comparison fairness concerns. |
| `KsUh8MMFKQ.md` (Thin-Shell Manipulations) | 8.0 | 1,2 | Different sub-area, but excellent paper. DemoGrasp is comparable in scope and rigor. |

**Narrowing:** The paper is clearly stronger than ResDex (7.0) — the most directly comparable dexterous grasping paper. It is comparable to PIDM/Seer (7.5). The comparison fairness issues keep it below the unanimous-8.0 tier.

**Final score:** 7.5 — strong Accept. The method makes a genuine contribution, the evaluation is broad and convincing, and the weaknesses (comparison framing issues) are addressable without invalidating the core claims.

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>