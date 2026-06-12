## Summary
DemoGrasp proposes a simple yet effective framework for universal dexterous grasping that formulates each grasp attempt as editing a single demonstration trajectory via a single-step MDP. An RL policy learns to modify the wrist pose (where to grasp) and hand joint angles (how to grasp) in the demonstration, then the edited trajectory is replayed open-loop. A flow-matching vision policy is trained on successful rollouts for sim-to-real transfer. The method achieves 95% success on DexGraspNet, 84.6% average across six unseen datasets with multiple embodiments, and 86.5% on 110 unseen real-world objects.

## Strengths
- **Elegant and simple formulation**: Restricting the RL policy to edit a demonstration in a compact SE(3) + delta-joint action space with a single-step decision horizon is a genuinely clever design. It reduces the exploration burden from high-dimensional, long-horizon RL to a low-dimensional, single-shot optimization, enabling training with a minimal reward (binary success + collision penalty). This dramatically simplifies reward engineering compared to prior work (UniDexGrasp++, UniGraspTransformer, ResDex).

- **Exceptionally thorough experimental evaluation**: The paper evaluates across 7+ object datasets (DexGraspNet, YCB, DGA, EGAD, Omni6DPose, ModelNet40, VisualDexterity), 6 robotic embodiments (5 multi-fingered hands + 1 parallel gripper), both state-based and vision-based settings, 110 unseen real-world objects, cluttered scenes, language-conditioned grasping, multiple camera configurations, and multiple ablation dimensions. This is among the most comprehensive evaluations in the dexterous grasping literature.

- **Strong real-world results including previously unsolved challenges**: Achieving 95.3% on normal objects and 71.1% on small/thin objects in tabletop settings is significant—the paper correctly notes that small/thin object grasping has remained challenging for prior sim-to-real methods. The extension to cluttered scenes and language-guided grasping further demonstrates practical utility.

- **Well-designed ablations that provide genuine insight**: The sampling vs. RL comparison (Table 5), the action-space decomposition (Table 8), the demonstration quality study (Table 9), and the training set size analysis (Table 7) each illuminate important aspects of the method. The finding that hand DoF editing provides only +2% gain while wrist rotation provides +13% (Table 8) is a revealing empirical observation about the structure of grasping.

- **Cross-embodiment generality without hyperparameter tuning**: Applying the same framework across 6 different hands (including arm-mounted configurations) and achieving >90% on training objects and 84.6% average on unseen datasets demonstrates genuine universality rather than overfitting to a particular embodiment.

## Weaknesses
### Fatal
None.

### Major
- **Open-loop execution after the edit limits dexterous correction**: Once the editing parameters are chosen, the edited demonstration is replayed open-loop. This means the RL policy cannot correct mid-execution if the grasp is failing. While the vision-based action-chunking policy provides some closed-loop behavior, the fundamental RL formulation commits to a trajectory upfront. This may limit performance on objects requiring active re-grasping or reactive adjustments. The paper should acknowledge this limitation more explicitly and discuss when it might fail.

- **Incomplete baseline comparison in cross-embodiment setting**: In Table 2 (Allegro+UR5), the only baseline is RobustDexGrasp, and for all other embodiments (Table 10 / Figure 3), no baselines are reported at all. Given that the paper emphasizes cross-embodiment generalization as a key contribution, the absence of baseline comparisons for most embodiments weakens this claim. The community cannot assess whether the strong cross-embodiment results are due to the method or simply favorable test conditions.

- **Dependence on a successful demonstration without discussion of acquisition**: The method requires a successful grasp demonstration for a specific object, which must be obtained beforehand. While Table 9 shows robustness to demonstration choice, the paper does not discuss how this demonstration should be obtained in practice for new setups, or what happens if the demonstration is suboptimal (e.g., only partially successful). The 3.88% demonstration replay success rate for "big obj. + side" suggests that some demonstrations barely work at all as baselines—more analysis of how RL overcomes this would be valuable.

### Minor
- **Performance gap on DGA dataset**: Across tables, DGA consistently shows the lowest success rates (e.g., 65.62% in Table 7 with 175 training objects, vs. 97%+ on VisualDexterity and EGAD). The paper should discuss what makes DGA challenging and whether this represents a genuine limitation.

- **Limited analysis of vision-based policy failure modes**: The gap between state-based (95.2%) and vision-based (92.2%) on DexGraspNet training objects (Table 1) and the dramatic failure of depth-based policies on small objects (Table 6) deserve more detailed analysis. What visual features does the policy struggle with?

### Trivial
None.

## Nice-to-Haves
- Training efficiency comparison (wall-clock time, environment interactions) against baselines to quantify the computational advantage of the single-step MDP formulation
- Failure mode analysis for real-world experiments with representative failure examples
- Discussion of how the approach would extend to more complex manipulation tasks beyond grasping (e.g., in-hand manipulation, tool use)

## Novel Insights
The central insight that demonstration editing can be formulated as a single-step MDP is genuinely novel and reframes the dexterous grasping problem. Rather than exploring in the full action space over long horizons (as in standard RL), the policy operates in a compact space of trajectory modifications. The empirical finding that this compact editing space suffices for universal grasping—combined with the observation that wrist DoFs dominate hand DoFs in importance (Table 8)—suggests that the "where to grasp" problem is harder than the "how to grasp" problem, and that a single demonstration's hand-closing pattern transfers remarkably well across objects. The demonstration quality robustness result (Table 9) further suggests that the RL objective is well-behaved despite the multi-modal nature of successful grasps, likely because the single-step formulation avoids the compounding errors that plague long-horizon RL.

## Suggestions
- Add baseline comparisons for other embodiments beyond Allegro+UR5 to substantiate the cross-embodiment claims
- Include a brief discussion on how to acquire the initial demonstration automatically (e.g., via motion planning, scripted sequences, or human teleoperation) and the sensitivity to demonstration quality
- Report training efficiency metrics (wall-clock time, samples needed) compared to baselines
- Add failure mode analysis with representative examples from real-world experiments

## Assessment
This is a strong paper. The core idea is simple, novel, and well-motivated. The experimental evaluation is remarkably comprehensive and convincing, spanning simulation and real world, multiple embodiments and datasets, and thorough ablations. The real-world results on small/thin objects represent genuine progress. The weaknesses (open-loop limitation, incomplete baselines for cross-embodiment) are real but do not invalidate the contribution—they represent natural limitations and opportunities for follow-up work.

MY FINAL SCORE: 8.0
MY FINAL DECISION: Accept