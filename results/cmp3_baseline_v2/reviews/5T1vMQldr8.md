## Summary

This paper proposes SPOT (Subgoal-based Preference Optimization Through Attention Weight), a method for offline preference-based RL that uses attention weights from the Preference Transformer to identify subgoals in preferred trajectories. A CVAE is trained to generate subgoals conditioned on state-action pairs, and the cosine similarity between the next state and predicted subgoal is used as an auxiliary reward shaping signal to mitigate reward model extrapolation errors. Experiments on D4RL, Robosuite, and Meta-World benchmarks show that SPOT achieves higher average performance than several existing offline PbRL methods.

## Strengths

- The idea of extracting subgoals from preference data using attention mechanisms is intuitive and well-motivated by the structure of preference transformer rewards.
- The integration of CVAE to generate contextually relevant subgoals for unlabeled trajectories is technically sound and addresses the challenge of mapping subgoals to new states.
- The experimental evaluation is comprehensive, covering locomotion and manipulation tasks with multiple baselines, and demonstrates improved average performance and lower variance compared to prior methods.
- The query efficiency analysis (Table 4) provides an interesting additional benefit, showing that SPOT maintains performance even with fewer preference queries.

## Weaknesses

### Fatal

- **The central claim of mitigating reward model extrapolation errors is not properly supported.** The paper defines extrapolation error as the absolute difference between predicted reward and ground truth reward, but the analysis in Figure 2 appears to compare the final augmented reward (model reward + shaping) for SPOT against the model reward alone for PT. Since SPOT does not modify the reward model itself—only adds a shaping term—the reward model's own extrapolation error is unchanged. The lower "extrapolation error" shown for SPOT is simply a reflection of the shaping signal correlated with ground truth, not evidence that the reward model's distribution-shift errors have been reduced. This flaws the core motivation and framing of the paper. The title and abstract consistently state that SPOT mitigates reward extrapolation errors, but the evidence provided conflates two different quantities.

### Major

- It is unclear whether all baseline methods were trained using the same offline RL algorithm (IQL) or whether the numbers are taken from original papers that may use different algorithms (e.g., SAC). If the latter, the performance comparisons may be confounded by differences in the policy optimization backbone rather than the preference learning component.
- The ablation studies (Top-K%, reward shaping methods, lambda selection) are performed on only 2 environments each, limiting the generalizability of the conclusions drawn.
- The paper does not report statistical significance tests (e.g., confidence intervals) for the main results in Table 1, making it difficult to assess whether the performance improvements are robust.

### Minor

- The qualitative case study in Section 5.4 (Figure 3) is illustrative but lacks quantitative verification of the claimed "one timestep forward-looking" behavior.
- The oracle baseline performance on some tasks (e.g., hopper-medium-expert: 62.10) appears lower than typical offline RL values reported in the IQL paper (~91.5), raising questions about the experimental setup (e.g., data subsampling, preference labeling protocol).
- The paper does not discuss computational overhead or training time of the added CVAE component.

### Trivial

- Reference [Christiano et al. 2017a] and [Christiano et al. 2017b] appear to be the same paper listed twice.
- Some equations (e.g., Eq. 3) contain subscript inconsistencies.

## Nice-to-Haves

- A formal analysis or proof sketch showing how subgoal-based reward shaping reduces reward model extrapolation error (as opposed to just adding a correlated signal).
- Experiments on more Meta-World tasks to strengthen the manipulation evaluations.
- Investigation of robustness to noisy or inconsistent preference labels, as acknowledged in the limitations.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Reframe the paper around "reward augmentation with preference-derived subgoals" and clearly distinguish between reward model errors and overall reward signal quality. The current claim of "mitigating reward extrapolation errors" is misleading based on the presented evidence.
- Clarify the baseline evaluation protocol: explicitly state whether all methods use the same offline RL algorithm (IQL) and report the source of the numbers.
- Provide a separate analysis of the reward model's own extrapolation error (without shaping) to support any claims about the reward model itself.
- Include hyperparameter sensitivity analysis for lambda and Top-K% across all main domains.
- Add error bars and confidence intervals (e.g., 95% CI) for the main results to quantify statistical significance.

## Score and Decision

Given the fatal flaw regarding the misinterpretation of extrapolation error mitigation—the core contribution of the paper is not properly validated—the paper does not meet the bar for acceptance. The technical idea and experimental results are still of interest, but the central claim is unsupported and would require significant revision. Therefore, the recommendation is reject.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>