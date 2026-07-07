## Summary
COREctifier proposes a "Rectified RL" (RRL) paradigm for Neural Combinatorial Optimization, where partial segments of policy-generated trajectories are probabilistically replaced with high-quality segments from reference solutions during training. The method operates at three hierarchical levels — batch, instance, and sub-instance — and is positioned as a general plug-in framework that can be applied on top of existing RL-based NCO backbones (POMO, MatNet, AM). Experiments across TSP, ATSP, PCTSP, CVRP, and KP show consistent and often substantial improvements over vanilla RL baselines and, notably, over SL-based heatmap methods on several settings, with a prominent reduction in the scalability gap at TSP-500.

## Strengths

- **Well-motivated problem and intuitive solution.** The paper clearly diagnoses the two core RL4CO bottlenecks (sparse/delayed rewards and vanishing advantage signal at local optima) and the proposed rectification mechanism directly addresses both: injected expert segments boost the reward of a small fraction of trajectories, restoring a meaningful advantage signal that guides the policy out of local optima.

- **Comprehensive experimental evaluation.** The benchmark covers 5 COPs, sizes ranging from 50 to 500 nodes/items, both synthetic and real-world distributions (TSPLIB, CVRPLIB), and comparisons against RL-based, SL-based, unsupervised, and meta-learning methods — a notably broader scope than most prior RL4CO papers. The 89.8% reduction in TSP-500 performance drop vs. prior RL methods is a striking empirical result.

- **Demonstrated generality.** The method is successfully applied to three different RL backbones (POMO, MatNet, AM) and to a combinatorial task that is not a routing problem (KP), supporting the plug-in claim. Training curves (Figs. 3–4) clearly show the benefit over vanilla RL and IL across tasks.

- **Diversity and advantage analysis (Fig. 6).** The entropy and advantage distribution plots convincingly explain *why* the method works mechanistically, not just that it works numerically.

## Weaknesses

### Fatal
None identified.

### Major

1. **Theoretical validity of the gradient update.** The core policy gradient loss (Eq. 11–12) computes ∇_θ log π_θ(τ'|G) · A(τ'), where τ' contains actions that were *not* sampled from π_θ — they were replaced by expert actions a*. The standard REINFORCE derivation requires that the trajectory τ is sampled from the current policy π_θ. Using a mixture trajectory τ' (part policy, part expert) introduces an off-policy discrepancy: the log-probability term includes log π_θ(a*|s), which the policy did not choose. The paper does not provide a theoretical justification for why this update is still a valid or approximately unbiased gradient estimator, nor does it discuss potential bias/variance trade-offs. This is the most important open question for the soundness of the method.

2. **Data requirements are understated relative to baselines.** CORectifier requires near-optimal labeled solutions (Concorde for TSP-100, LKH-3 for ATSP, HGS for CVRP). The compared "vanilla RL" baselines use *no* such data. The paper does discuss this but frames it as a minor cost. A clearer analysis of how much labeled data is needed, and how performance degrades with less or lower-quality data, would be essential for practitioners assessing the method's practical cost (beyond the brief Remark 2 in Section 4.3).

3. **KP results classification inconsistency.** Table 9 classifies CORectifier as "SL+G" for KP, while everywhere else it is classified as "RL+G." This is not explained in the main text. It is unclear whether a different training pipeline was used for KP, undermining the claim that RRL is the method being evaluated.

### Minor

1. **Ablation table values (Table 6) appear to be from a different configuration.** The TSP-50 objectives in the ablation over segment length (5.770, 5.778, 5.799…) are all substantially worse than the main TSP-50 result (5.697 in Table 1). If the ablation uses a different shorter training run, this should be stated explicitly, as it limits interpretability.

2. **Scalability at large scales remains behind SL methods.** On TSP-500, even CORectifier (N=128) achieves 4.024% drop vs. COExpander's 0.837% (Table 1). The paper acknowledges this, but the framing ("first step") merits a stronger analysis of *why* the gap persists and what would be needed to close it.

3. **Hyperparameter sensitivity and cosine scheduling add complexity.** The method introduces p_batch, p_inst, α, β, and four cosine annealing schedules, each with their own T_max — a total of ~12 hyperparameters. While the sensitivity study in Fig. 5 and Table 6 suggests relative robustness, the overall configuration burden is non-trivial and not fully analyzed across all tasks.

### Trivial
None worth listing.

## Nice-to-Haves
- A formal analysis (or at least a discussion with citations) of the off-policy bias introduced by mixed-trajectory gradient updates, perhaps drawing on importance weighting or DAgger-style theoretical frameworks.
- A data efficiency curve: how does performance scale with the number of labeled instances in G*? This would be very informative for practitioners.
- Clarification of the KP training paradigm (why "SL+G" classification).

## Novel Insights
The key insight of operating expert guidance at the *sub-trajectory* level — extracting multiple overlapping segments from a single labeled instance rather than treating each instance as a monolithic label — is genuinely novel in the NCO context. This "segment reuse" dramatically improves label efficiency: a single reference tour for TSP-100 can generate O(M) distinct guiding signals with varying starting positions and lengths, each creating a high-advantage anchor trajectory in the training batch. This reframing of expert data as a source of decomposable local signals rather than global templates offers a principled bridge between IL's data efficiency and RL's constraint-aware flexibility.

## Suggestions
- Address the theoretical gap: provide an argument (even informal) for why including log π_θ(a*|s) in the gradient for replaced steps does not corrupt learning. One possible framing is that the method is implicitly doing importance-weighted off-policy learning; another is that the gradient contribution of the replaced steps acts as a mild imitation loss regularizer. Either interpretation should be made explicit.
- Report the size of G* (number of labeled training instances) for each task, and test performance as |G*| varies from very small to large, to characterize data efficiency.
- Clarify the KP experiment setup and correct or justify the "SL+G" label.
- In Table 6, specify whether the ablation uses fewer training epochs or different seeds, so the numbers can be properly contextualized relative to Table 1.

## Score and Decision
The paper addresses a real and important bottleneck in RL-based NCO, proposes an intuitive and well-implemented solution, and backs it up with unusually broad empirical evidence. The primary theoretical concern — whether the gradient update with mixed trajectories is valid — is not fatal in practice (the strong results speak for themselves) but is a genuine soundness gap that the authors should address. The requirement for labeled data is a real constraint but is acknowledged and does not invalidate the contribution. Overall, this is a solid, above-average contribution to the NCO field.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>