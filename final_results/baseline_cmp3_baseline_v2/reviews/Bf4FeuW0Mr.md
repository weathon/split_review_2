## Summary

The paper proposes DemoGrasp, a framework for learning universal dexterous grasping policies from a single demonstration. The key idea is to reformulate the task as a single-step Markov Decision Process where the policy edits the demonstration trajectory by modifying the wrist pose (determining *where* to grasp) and hand joint angles (determining *how* to grasp), rather than exploring in the full low-level action space. This dramatically reduces exploration complexity, enabling training with a simple binary success reward plus collision penalty. The learned state-based policy is then distilled into a vision-based flow-matching policy via imitation learning on rendered rollouts for sim-to-real transfer. Extensive experiments show state-of-the-art results on DexGraspNet (95% success with Shadow Hand), strong cross-dataset and cross-embodiment generalization (84.6% average on six unseen datasets across six embodiments), and successful zero-shot real-world deployment on 110 unseen objects including small/thin items (86.5% overall, 71.1% on thin objects).

## Strengths

1. **Novel and elegant problem formulation.** The demonstration-editing approach combined with a single-step MDP is a conceptually clean way to mitigate the exploration challenges of high-dimensional, long-horizon multi-task RL. It removes the need for complex reward shaping, curriculum learning, or multi-stage pipelines required by prior work.

2. **Strong empirical results across multiple axes.** DemoGrasp achieves state-of-the-art on the large-scale DexGraspNet benchmark (95.2% state-based, 92.2% vision-based), outperforming UniGraspTransformer by 4-5%. It also demonstrates broad generalization: zero-shot transfer to unseen datasets (84.6% average across six datasets), to six different robotic embodiments without hyperparameter tuning, and to real-world grasping of 110 unseen objects including challenging small and flat items.

3. **Simplicity and ease of use.** The framework requires only a single demonstration, a binary reward, and standard RL—no complex reward engineering, dense shaping terms, privileged contact observations, or iterative distillation processes. The same approach works across different hands, arms, and object sets, suggesting practical accessibility for the robotics community.

4. **Addresses a long-standing challenge in tabletop dexterous grasping.** The ability to grasp previously challenging small and thin objects (71.1% real-world success) by permitting minimal robot-table contact where beneficial is a meaningful advance over prior work that either avoids tabletop setups entirely or fails on such objects.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor
1. **Limited real-world baseline comparisons.** While the paper provides extensive simulation comparisons against UniDexGrasp, UniDexGrasp++, and UniGraspTransformer, the real-world experiments lack a direct comparison with a prior method under the same conditions. The claim of being "to our knowledge, the first to grasp previously unseen small, thin objects" is supported by qualitative statements about prior work but not by quantitative head-to-head real-world baselines.

2. **The single-step MDP formulation is open-loop for the grasping phase.** After the policy selects the editing parameters, the entire edited demonstration is replayed open-loop. While the vision-based policy uses action chunking for closed-loop control, the core RL policy does not reason about feedback during the grasp execution. This could limit robustness to dynamic perturbations or object slip in more challenging scenarios.

### Trivial
None.

## Nice-to-Haves
- A deeper analysis of failure cases in real-world experiments, especially for thin and small objects.
- Comparison against a recent method that also targets tabletop dexterous grasping with sim-to-real (e.g., RobustDexGrasp) in real-world tests, if such a comparison is feasible.
- Discussion of the computational cost of training: number of RL steps, wall-clock time, and how the single-step formulation compares to multi-step methods in terms of training efficiency.

## Novel Insights
The key insight is that a single grasping demonstration encodes transferable motion patterns, and by restricting policy exploration to a low-dimensional editing space (SE(3) wrist transform + delta hand pose) within a one-step horizon, the multi-task exploration burden collapses. This reveals a general design principle: for tasks with a well-defined behavioral template (approach, grasp, lift), strong universal policies can be learned without dense rewards or long-horizon RL, contradicting the common belief that dexterous manipulation inherently requires complex reward shaping and hierarchical frameworks. The demonstration that a binary success-collision reward suffices when exploration is properly constrained is both surprising and practically valuable.

## Suggestions
- For future work, consider extending the formulation to allow the policy to select among multiple demonstrations or to adapt the trajectory online after the initial edit, combining the single-step efficiency with closed-loop robustness.
- Release the trained demonstrations, editing parameters, and vision-based checkpoints to facilitate reproducible baselines for the community.

## Score and Decision
Score: 9.0  
Decision: Accept

MY FINAL SCORE: <score>9.0</score>
MY FINAL DECISION: <decision>Accept</decision>