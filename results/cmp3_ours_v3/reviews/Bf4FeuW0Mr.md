## Summary

DemoGrasp proposes a method for universal dexterous grasping that edits a single demonstration trajectory along two interpretable axes: wrist SE(3) transformation for "where to grasp" and hand joint deltas for "how to grasp." This is formulated as a single-step MDP, reducing a high-dimensional, long-horizon RL problem to a compact optimization solvable with a simple binary success + collision penalty reward. The method achieves strong results across simulation benchmarks (95% on DexGraspNet), six hand embodiments, cross-dataset generalization, and real-world tests on 110 objects including small/thin items that have been challenging for prior work.

## Strengths

1. **Clever formulation that converts a hard exploration problem into a tractable one.** The core idea — editing a single demonstration along two interpretable axes — is simple and well-motivated (Section 2.2). The demonstration already encodes a complete approach-grasp-lift trajectory; the policy only needs to discover modifications that make it succeed for a given object. This reduces the effective action space from an 18+ DoF × T-timestep trajectory to a roughly 9-dimensional single-step output.

2. **Consistently strong empirical results across multiple axes.** DemoGrasp outperforms UniGraspTransformer by ~5% on DexGraspNet (Table 1), matches or exceeds RobustDexGrasp on 4/5 cross-dataset tests (Table 2), generalizes to 6 different hand embodiments without hyperparameter tuning (Figure 3), and achieves 86.5% success on 110 real-world objects (Table 3).

3. **Clean reward design.** The binary success + collision penalty (Eq. 3) is notably simpler than the multi-term reward functions used by baselines. The trick of randomly disabling collision detection in half the environments to allow beneficial hand-table contact for thin objects is elegant and demonstrably effective.

4. **Strong sim-to-real evidence.** Real-world evaluation on 110 objects with randomized poses and positions is substantial. The 71.1% on thin/small objects addresses a genuinely difficult regime where prior dexterous grasping work struggled. The camera configuration ablation (Table 6) showing that RGB outperforms depth for thin objects is practically informative.

5. **Robustness to demonstration quality.** Table 9 shows that even when the original demonstration has only 3.88% replay success (big object + side approach), the learned policy achieves >95%, demonstrating the method does not overfit to the demonstration but uses it as a scaffold for exploration.

## Weaknesses

### Major

None.

### Minor

1. **The cross-embodiment comparison with RobustDexGrasp (Table 2) is uncontrolled.** The paper acknowledges RobustDexGrasp was "trained on different object datasets" and claims this is fair "since both aim at universal grasping over arbitrary objects" (line 148). Different training distributions can produce different zero-shot test performance even if both methods are equally capable. Table 2 is suggestive of strong cross-dataset generalization but does not constitute a controlled method comparison. The comparison should be framed primarily as a cross-dataset generalization result.

2. **The "dexterous" contribution is quantitatively marginal.** Table 8 shows that adding hand joint angle editing (Δq) improves the training-set success rate from 94.22% to 96.24% — a ~2% gain over wrist-only editing. The paper acknowledges this (lines 230-231) and provides qualitative evidence (Figure 4). However, there is no quantitative robustness metric (e.g., perturbation resistance, lift stability) demonstrating that the hand DoFs produce meaningfully different grasps. The paper's positioning as a dexterous grasping contribution is partially at odds with its own data showing dexterous DoFs contribute little to raw success rate.

3. **The cluttered-scene real-world evaluation rests on a small basis.** The real-world cluttered grasping results (Table 4) are based on 10 cluttered scenes (line 175). Even with 5-8 objects per scene, the statistical basis is limited. Given that the abstract and conclusion highlight these results, and the 82-84% success rates are impressive, a larger evaluation would strengthen the extensibility claims.

4. **No statistical significance or variance reporting.** The paper does not report confidence intervals or standard errors for success rates. For real-world results (Table 3), where each object is tested for 5 trials, per-category rates have wide confidence intervals (e.g., 60% on 10 tools has roughly 26-88% 95% CI). This is common practice in the field but adding variance information would strengthen the empirical claims.

### Trivial

1. **Equations (1) and (2) have notational ambiguities.** The interpolation mechanism in Eq. (2) uses a scalar-vector division notation that is unclear about dimensionality. The authors should clarify with explicit dimensionality.

## Nice-to-Haves

- **Failure analysis.** A taxonomy of failure modes (e.g., specular surfaces, particular geometries) would strengthen the practical contribution.
- **Runtime/computation reporting.** The paper does not report inference speed for the ViT + flow-matching policy, which matters for real-world deployment.
- **Quantitative robustness metrics for dexterity.** A perturbation-resistance or lift-stability metric would substantiate the value of hand DoFs beyond the 2% success-rate gain.

## Removed Points

The following point from the input review is removed per filtering rules:

- **"Baseline comparison on DexGraspNet is not apples-to-apples"** — Removed per hard rule: the asymmetry in evaluation protocol favors the baselines (fixed positions for baselines vs. randomized 50cm×50cm for DemoGrasp). The paper transparently acknowledges this difference (lines 131-132) and intentionally tests itself under harder conditions.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add confidence intervals or variance bars to the real-world results (Table 3).
2. Include a quantitative robustness metric (e.g., perturbation resistance) to substantiate the value of hand DoF editing.
3. Expand the cluttered-scene real-world evaluation to at least 30-50 scenes.
4. Clarify the notation in Equations (1) and (2).

## Score and Decision

**Score: 7.5**
**Decision: Accept**

**Calibration summary:**

| Paper | Path | Avg Score | Round | Comparison |
|---|---|---|---|---|
| ResDex (MoE Dexterous Grasping) | BUj9VSCoET.md | 7.0 (8,6,8,6) | Bracketing | Sim-only dexterous grasping, 88.8% on DexGraspNet, no real-world. DemoGrasp has broader evidence (real-world on 110 objects, cross-dataset, 6 embodiments) and higher sim performance. |
| Cross-Embodiment Dex Grasping | twIPSx9qHn.md | 5.0 (6,6,3) | Bracketing | Limited real-world, mixed reviews. DemoGrasp substantially stronger in both breadth and depth of evaluation. |
| DexTrack (Neural Tracking Controller) | ajSmXqgS24.md | 6.25 (8,3,6,8) | Bracketing | Mixed reviews, presentation concerns. DemoGrasp has clearer methodology and broader evaluation. |
| Data Scaling Laws in Imitation Learning | pISLZG7ktL.md | 8.0 (8,8,8,8) | Narrowing | Unanimous 8s, massive-scale study with 40k demos + 15k real-world rollouts. DemoGrasp has narrower scope but genuine contribution; comparison issues prevent reaching this tier. |
| Thin-Shell Object Manipulations | KsUh8MMFKQ.md | 8.0 (8,8,8,8,8) | Narrowing | Unanimous 8s, differentiable simulation platform. Elite-tier paper. |
| Geometry-aware RL for Manipulation | 7BLXhmWvwF.md | 8.0 (8,8,8,8) | Narrowing | Unanimous 8s, exceptional paper. |

Round 1 bracket: [7.0, 8.0]. Final score 7.5, reflecting a strong paper with a novel core contribution and broad empirical validation, held back from the 8+ tier by the uncontrolled comparison elements and the quantitatively marginal dexterity contribution.

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>