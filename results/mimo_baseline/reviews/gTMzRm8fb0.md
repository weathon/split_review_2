## Summary

The paper proposes GoalRank, a generator-only ranking framework for recommender systems that challenges the prevailing two-stage Generator-Evaluator (G-E) paradigm. The authors (1) prove theoretically that a sufficiently large generator-only model can achieve strictly smaller approximation error to the optimal ranking policy than any finite multi-generator-evaluator system, (2) derive a group-relative optimization principle using a reward model to construct reference policies for training, and (3) validate the approach through offline experiments on public benchmarks and large-scale online A/B tests on a platform with over half a billion daily active users.

## Strengths

- **Strong theoretical motivation with formal guarantees.** Theorem 1 rigorously proves that for any k-mixture (α,β)-bounded policy space, there exists a larger generator-only policy space with strictly smaller KL approximation error to the optimal policy, and that this error vanishes as model size grows. This provides a principled foundation for the generator-only paradigm.

- **Compelling online A/B test results.** GoalRank was deployed on a production short-video platform serving 500M+ daily active users, showing statistically significant improvements across all business metrics (App Stay Time +0.149%, Watch Time +0.197%, Effective Views +1.212%, Comments +0.802%) over the production MG-E baseline. This is strong evidence of real-world impact.

- **Clear scaling law demonstration.** Figure 3 shows that GoalRank's performance improves steadily from 1M to 0.1B parameters, while baselines (DNN, RankMixer, PIER, MG-E) show much weaker scaling. This empirically validates the theoretical prediction and is practically valuable for deployment decisions.

- **Comprehensive experimental evaluation.** The paper evaluates across 4 datasets (2 public, 2 industrial), 10+ baselines spanning all three paradigms (G-only, G-E, MG-E), multiple metrics, ablation studies on group size and reward bias, and online A/B tests. The evaluation is thorough and well-designed.

- **Practical robustness analysis.** Tables 2 and 3 demonstrate that GoalRank is robust to suboptimal group sizes and reward model bias, with even λ=0.5 noise degrading performance only modestly while still outperforming all baselines.

## Weaknesses

### Fatal
None.

### Major

- **Loose connection between theory and practice.** Theorem 1 proves existence of a better generator-only model by requiring width ≥ kα+n, which is essentially a universal approximation argument. The paper then pivots to group-relative optimization (Section 3.2–3.3) without a tight theoretical bridge explaining why this specific training procedure realizes the theoretical advantage. The derivation of the evidence upper bound and the group-relative construction are reasonable, but the theoretical result does not directly motivate or constrain the training algorithm. This makes the theory feel more like post-hoc justification than a driving design principle.

- **Group construction depends on auxiliary models, undermining the "generator-only" claim.** The practical effectiveness of GoalRank relies on an auxiliary set of ranking policies M (including heuristic methods and lightweight neural models) to construct diverse list groups B_u. This means GoalRank is not truly a standalone generator-only system during training—it requires a portfolio of other models to generate the reference signal. The paper should more clearly acknowledge this dependency and discuss its implications for the "generator-only" framing.

### Minor

- **The MG-E baseline comparison is somewhat asymmetric.** GoalRank uses a reward model trained on user feedback plus auxiliary policies for group construction, while MG-E baselines use multiple generators with the same evaluator. The MG-E approach scales by adding generators, while GoalRank scales by increasing model capacity. These are fundamentally different scaling strategies, and the comparison, while fair in parameter count, doesn't fully isolate whether the gains come from the training objective, the model architecture, or the scaling approach.

- **The group-relative optimization is conceptually similar to existing preference learning methods.** The reference policy construction (Equation 4) is essentially a softmax over normalized rewards within a group, which is closely related to DPO-style preference learning and REINFORCE with baseline. The paper would benefit from a more explicit discussion of how this differs from or improves upon these established approaches in the recommendation context.

### Trivial
None.

## Nice-to-Haves

- A comparison of GoalRank's training cost versus MG-E at equivalent performance levels would help practitioners understand the efficiency tradeoff.
- Analysis of how GoalRank handles distribution shift or cold-start users, where the reward model may be less reliable.
- Discussion of the computational cost of the auxiliary policy set M during training.

## Novel Insights

The paper's most novel insight is the empirical demonstration that generator-only models exhibit significantly stronger scaling behavior than multi-generator-evaluator systems in the ranking domain. While the theoretical result (Theorem 1) is a formalization of a universal approximation argument, the practical finding that this theoretical advantage manifests as clear scaling laws in real recommendation systems—and that a group-relative training objective can effectively unlock this advantage—is genuinely valuable. The online deployment results, showing that a single large generator can fully replace a production multi-generator-evaluator system with hundreds of candidate lists, provide a compelling proof point for the broader trend toward unified, end-to-end recommendation models.

## Suggestions

- Tighten the theory-practice connection by either (a) showing that the group-relative objective is a direct consequence of the approximation error analysis, or (b) providing a separate theoretical analysis of the training procedure's convergence properties.
- Add a dedicated discussion section comparing group-relative optimization with DPO and other preference learning methods, clarifying what is specific to the recommendation setting.
- Provide more detail on the auxiliary policy set M and ablate its contribution to understand how much of GoalRank's performance depends on this component.

## Score and Decision

The paper presents a well-motivated framework with strong empirical validation, particularly the online A/B tests at massive scale and the scaling law demonstration. However, the theoretical contribution, while well-formalized, is somewhat expected (universal approximation argument) and loosely connected to the practical training procedure. The methodological novelty of group-relative optimization is moderate given its similarity to existing preference learning approaches. The practical impact is the paper's strongest asset.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: Accept