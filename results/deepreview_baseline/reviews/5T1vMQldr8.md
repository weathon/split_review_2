## Summary

This paper introduces SPOT (Subgoal-based Preference Optimization Through Attention Weight), a method that mitigates reward extrapolation errors in offline preference-based RL. SPOT uses attention weights from a Preference Transformer to identify critical states (subgoals) in preferred trajectories, trains a Conditional Variational Autoencoder (CVAE) to generate subgoals conditioned on state-action pairs, and shapes the reward based on cosine similarity between the next state and the predicted subgoal. This regularization constrains policy learning toward in-distribution states, reducing reward estimation errors. Experiments on D4RL, Robosuite, and Meta-World benchmarks show that SPOT achieves competitive or superior performance compared to several baselines, with lower variance and better query efficiency.

## Strengths

- **Clear motivation and problem framing**: The paper addresses a well-recognized challenge in offline PbRL—reward extrapolation due to distribution shift—and provides a principled approach that leverages attention-based subgoal discovery to constrain policy learning.
- **Novel integration of attention-guided subgoal extraction with CVAE generation**: The idea of using attention weights from the Preference Transformer to identify subgoals, and then learning a generative model to produce contextually relevant subgoals for unlabeled data, is original and well-motivated.
- **Comprehensive empirical evaluation**: The paper evaluates SPOT against seven baselines across three distinct benchmark families (D4RL locomotion, Robosuite manipulation, Meta-World). The experiments include ablation studies on the top-K% percentile, reward shaping methods and weight sensitivity, extrapolation error analysis, query efficiency, and a qualitative case study—covering multiple angles to validate the approach.
- **Strong average performance and reduced variance**: SPOT achieves the highest average score (78.82) across all tasks and notably reduces average standard deviation compared to the baseline Preference Transformer (13.80→7.76), indicating more stable learning.

## Weaknesses

### Major

1. **Potential circularity in extrapolation error analysis (Section 5.3)**: The extrapolation error is computed as the absolute difference between the predicted reward and “human-labeled rewards from the dataset as proxy ground truth.” Since the same Preference Transformer (PT) output (attention weights and reward estimates) is used both to define subgoals and to compute the error, and the subgoal-guided reward shaping is applied to the same reward model, the improvement shown in Figure 2 may partly reflect that the error measure is correlated with the shaping signal. Moreover, the source of these “human-labeled rewards” is ambiguous—if they are the true environment reward (e.g., from D4RL), they are not human-labeled; if they are derived from preferences, the analysis may be circular. This weakens the claim that SPOT directly reduces extrapolation error rather than simply biasing the policy toward states that yield smaller error according to the same model.

2. **Incremental improvement over the backbone Preference Transformer**: SPOT builds directly on PT (attention weights, reward model). The average performance gain over PT is about 4% (78.82 vs. 74.76). While consistent, the improvement is modest, and it is not fully disentangled from the effect of adding a generic in-distribution reward shaping term. The novelty lies in the subgoal discovery mechanism, but the paper does not conclusively show that the subgoal-specific component (CVAE + similarity) is critical beyond any smoothness or conservative regularizer.

3. **Limited evaluation of alternative offline RL algorithms and base learners**: All experiments use IQL as the core offline RL algorithm. It is unclear whether the benefits of SPOT generalize to other offline RL methods (e.g., CQL, BCQ). The method’s dependence on IQL may limit its applicability.

### Minor

- The qualitative case study (Figure 3) is illustrative but subjective. It would be strengthened by quantitative metrics (e.g., prediction accuracy of subgoals) or comparison with random subgoal extraction.
- The hyperparameter \(\lambda\) is fixed to 1.0 for all main experiments, yet the ablation shows performance can vary significantly with \(\lambda\) (e.g., cosine similarity on hopper-m with \(\lambda=1.0\) gives 97.36 vs. 44.28 with \(\lambda=-0.5\)). The paper does not provide guidance on how to set \(\lambda\) in practice or whether the optimal value depends on the task.
- The query efficiency experiments (Table 4) compare SPOT only against PT. A comparison with other methods (e.g., DTR, IPL) under reduced query budgets would strengthen the claim.

### Trivial

- Figure 1 caption is repeated in the parsed text, but this is a format artifact and not a paper flaw.

## Nice-to-Haves

- Provide a more rigorous analysis of why the subgoal-based shaping reduces extrapolation error, e.g., by showing that the CVAE-generated subgoals lie within the training distribution compared to random state samples.
- Include experiments with noisy preference labels to test robustness, as noted in the limitations.

## Novel Insights

None beyond the paper’s own contributions: the use of attention weights from a preference model to extract subgoals, and the subsequent conditioning with a CVAE for reward shaping, is the main novel insight. The paper does not introduce a fundamentally new understanding of extrapolation error beyond confirming that proximity to training subgoals reduces it.

## Suggestions

- Clarify the definition of “human-labeled rewards” used in the extrapolation error analysis. If they are environment ground-truth rewards, state this explicitly; if they are derived from preferences, discuss the potential confound.
- Add an ablation that replaces the CVAE with a simpler baseline (e.g., random subgoals or a fixed set of training subgoals) to isolate the contribution of the learned generative model.
- Consider testing SPOT with a different offline RL backbone (e.g., CQL) to demonstrate generalizability.
- Discuss strategies for tuning \(\lambda\) when ground-truth rewards are unavailable.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>