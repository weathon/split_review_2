## Summary

This paper introduces CoRAL, a modular neuro-symbolic framework for zero-shot contact-rich robotic manipulation. The system separates the roles of vision (for pose tracking and physical parameter estimation) and LLM (for generating cost functions and contact strategies), then feeds these into an MPPI controller with online adaptation and memory-based experience reuse. Experiments in simulation across six challenging tasks show that CoRAL outperforms end-to-end VLA baselines (OpenVLA, π_0.5) on contact-rich scenarios and approaches the performance of human-expert-designed cost functions, while ablations validate the necessity of each module.

## Strengths

- **Clear problem motivation and well-motivated design**: The paper correctly identifies that current VLA systems struggle with contact-rich manipulation due to their black-box nature and reliance on large tele-operated datasets. The decoupling into vision for perception, LLM for reasoning, and MPPI for reactive control is a principled and well-justified architecture.

- **Strong empirical methodology**: The experimental design is thorough, with six diverse tasks that isolate different challenges (multi-stage reasoning, force control, tool-use), two state-of-the-art VLA baselines, two human-expert cost baselines, and four systematic ablations. The ablation study convincingly demonstrates the contribution of each component, particularly the criticality of the pose estimator and the role separation.

- **Good analysis of failure recovery and explainability**: The paper provides concrete examples of the LLM diagnosing failures (e.g., incorrect friction estimate in the cutting board task, cost weighting in the wall-flip task) and adapting both world model parameters and strategies mid-execution. This goes beyond reporting success rates and shows the system's reasoning capability.

- **Novel contribution to a timely problem**: Integrating LLM-generated cost functions and contact strategies directly into an MPPI controller is a genuinely new approach that grounds high-level reasoning in a formal optimal control problem. The memory unit for reusing past successful plans is a practical touchstone for real-world deployment.

## Weaknesses

### Fatal
None.

### Major

- **Simulation-only evaluation**: All experiments are conducted in MuJoCo/ROBOSUITE. For a framework that claims to handle contact-rich manipulation and emphasizes the sim-to-real gap, the absence of any real-world validation is a significant gap. The reactive control augmentation (Eq. 7) is proposed to address this gap but never demonstrated. This limits confidence in the system's practical applicability.

- **Moderate absolute performance on hardest tasks**: On the most challenging tasks (T1: Push+Pick Board, T6: Flip with Wall), CoRAL achieves only 40% and 70% success rates respectively. While this substantially outperforms VLA baselines, it is still far from reliable deployment. The gap to the human-expert FSM baseline (80% and 90%) indicates considerable room for improvement, and the paper does not discuss whether this gap is inherent or addressable.

- **Computational latency underexamined**: The paper mentions computational latency as a limitation but provides no quantitative analysis. The system uses parallel rollouts of 200 trajectories and calls GPT-4o for online adaptation, which could be slow for real-time control. Given that reactive control is central, understanding the wall-clock time per control cycle and adaptation cycle is essential to assess feasibility.

### Minor

- **Dependence on object models**: The system requires known 3D geometric models (M) as input for FoundationPose. This limits applicability to novel objects for which CAD models are unavailable. The paper does not discuss how this constraint could be relaxed (e.g., via category-level pose estimation).

- **Comparison with VLA baselines is somewhat unfair**: The VLA baselines (OpenVLA, π_0.5) are fine-tuned on LIBERO tasks, while CoRAL uses object models, LLM reasoning, and MPPI—a fundamentally different paradigm. The comparison is informative but not a direct head-to-head on equal footing. The paper acknowledges this implicitly but could frame it more clearly as "different paradigm outperforms standard imitation-learned policies" rather than implying CoRAL is a better VLA.

- **Memory unit benefits are modest**: On T1, memory improves success from 2/10 to 4/10; on T3, from 9/10 to 10/10. The improvement is positive but small, and there is no analysis of how many stored episodes are needed, what retrieval mechanism is used, or whether the LLM-based embedding similarity is robust.

### Trivial
None significant.

## Nice-to-Haves
- Real-world validation on at least one contact-rich task (e.g., pushing or flipping a box with a real Franka arm)
- Ablation varying N_retry (the number of inner-loop failures before triggering adaptation) to understand sensitivity
- Comparison with a variant that uses a learned dynamics model instead of the physics simulator for MPPI rollouts
- Analysis of the types of failures that the online adaptation module cannot recover from

## Novel Insights

Beyond the paper's own contributions, the results provide a concrete demonstration that explicit reasoning about contact strategies and cost structures can dramatically reduce the search complexity for motion planning in contact-rich tasks. The 83.9% reduction in planning steps when the LLM provides contact guidance (Sec. 4.1.4) is striking evidence that "where to make contact" is often more important than precise trajectory optimization in these settings. This suggests that for manipulation with significant contact dynamics, the bottleneck is not trajectory optimization but the combinatorial problem of choosing which surfaces to contact—a problem well-suited for LLM reasoning. The paper also shows that LLMs can correct their own physical parameter estimates through iterative failure feedback, hinting at a capability for "self-correction" that goes beyond standard LLM prompting.

## Suggestions

- Add a clear quantitative breakdown of computational latency: time per MPPI iteration, time per GPT-4o call for adaptation, and total time for a typical episode. This would help readers assess real-time feasibility.
- Consider testing on at least one real-world task to validate the reactive control augmentation and sim-to-real transfer claims. A simple pushing or flipping task with a real Franka arm would significantly strengthen the paper.
- Discuss the generalization to novel objects without CAD models, or add an experiment using category-level pose estimation (e.g., FoundationPose with mesh-free estimation) to show robustness.
- Report confidence intervals or standard errors for success rates across more than 10 trials per task to improve statistical robustness.

## Score and Decision

The paper makes a novel and well-motivated contribution to contact-rich manipulation by cleanly decomposing reasoning, perception, and control, with strong experimental evidence for the importance of each component. The main limitation is the simulation-only evaluation and the still-moderate success rates on the most challenging tasks. The paper is sound, the experiments are thorough, and the writing is clear. The value to the community is real: it provides a concrete blueprint for combining LLMs with optimal control for physically-grounded manipulation.

Given the score distribution guidelines, this paper is above average in quality and should be accepted. I assign 6 (borderline accept) reflecting that the contribution is clear and well-supported, but the lack of real-world validation and moderate performance on hard tasks prevent a higher score.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>