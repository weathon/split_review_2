## Summary

This paper proposes GoalRank, a one-stage generator-only ranking framework that challenges the prevalent two-stage Generator–Evaluator (G-E) paradigm. The authors prove that a sufficiently large generator-only model can achieve strictly smaller approximation error to the optimal ranking policy compared to any finite mixture of small generators combined with an evaluator. They derive a group-relative optimization principle to train such a model practically, using a reward model to construct a reference policy and minimizing KL divergence to it. Extensive offline experiments on public benchmarks and large-scale online A/B tests demonstrate that GoalRank consistently outperforms state-of-the-art methods and exhibits clear scaling laws.

## Strengths

- **Solid theoretical foundation.** Theorem 1 establishes that for any finite (Multi-)Generator–Evaluator family, a generator-only model exists with strictly smaller approximation error to the optimal ranking policy, and the error decreases as the model grows. This provides a principled justification for pursuing one-stage large rankers over multi-stage pipelines.

- **Strong and comprehensive empirical validation.** Offline experiments on ML-1M, Amazon-Book, and industrial datasets show GoalRank outperforming all baselines by substantial margins (e.g., +17.12% H@6 on ML-1M, +25.39% H@6 on Industry). The paper also validates scaling laws—GoalRank's performance improves steadily from 1M to 0.1B parameters while baselines plateau. The online A/B test in a production system with over 500M DAU demonstrates consistent gains across all business metrics and full deployment.

- **Clear ablation studies.** The paper systematically examines the effect of group size \(|\mathcal{B}|\) and reward model bias, showing that GoalRank is robust to both and that performance is optimal with moderate group sizes (8–20). This gives practical guidance for deploying the method.

## Weaknesses

### Major

1. **Potentially unfair comparison against G-E baselines.** The paper states "all baselines share exactly the same evaluator (reward model) as GoalRank." For methods like PIER and NAR4Rec, using a fixed reward model as the evaluator rather than their own trained evaluator could disadvantage them, as those baselines' original evaluators are specifically designed for the list selection task. This is not clearly explained, and the baselines may not be operating at their full potential.

2. **Theoretical result relies on soft mixture evaluator.** Theorem 1 is proven for a policy space \(\mathcal{C}_m^k\) that uses convex combinations of generators (soft mixture), while practical G-E systems typically use hard selection (one-hot \(\omega\)). The paper claims the soft-mixture space "strictly contains the policy class realized by hard selection," but the proof may depend on the convex nature of the space. It is unclear whether the result holds for the hard-selection evaluators actually used in practice, and the paper does not address this gap.

### Minor

- The group-relative optimization principle (Eq. 4–5) closely resembles distillation from a reward model, similar to techniques used in RLHF (e.g., DPO) and knowledge distillation. While the application to ranking with explicit group construction is novel, the core optimization technique is not entirely new.

- The bias robustness experiment (Table 3) injects isotropic Gaussian noise, which does not capture the structured systematic biases that reward models exhibit in practice (e.g., favoring popular items or certain categories). A more realistic bias simulation would strengthen the claim.

### Trivial

- The scaling experiment (Figure 3) would benefit from a description of which architectural dimensions (width, depth, heads) were varied. This would help confirm that GoalRank's advantage does not stem from different scaling strategies applied to baselines vs. GoalRank.

## Nice-to-Haves

- A computational cost comparison (inference latency, FLOPs, memory) between GoalRank's single large model and the MG-E setting with many generators and an evaluator.
- Release of the implementation and training code (already promised) to support reproducibility.

## Novel Insights

Beyond the paper's own contributions, the key insight is that the two-stage G-E paradigm has an inherent representational limitation: the convex hull of small generators cannot approximate all optimal ranking policies, while a single larger generator (due to its greater capacity and nonlinearity) can. This provides a theoretical explanation for the diminishing returns observed when scaling the number of generators and justifies focusing on scaling a single ranker instead. The group-relative optimization principle offers a practical way to train this ranker using a potentially biased reward model, where grouping ensures that reward order is approximately preserved, enabling distillation without needing an exact unbiased reward.

## Suggestions

1. **Clarify the evaluator usage in G-E baselines.** If the reward model replaced the baselines' native evaluators, please add an experiment comparing GoalRank against PIER/NAR4Rec with their original evaluators to ensure a fair comparison.
2. **Discuss hard-selection evaluators.** Explain whether the theoretical result (Theorem 1) extends to hard-selection evaluators or what modifications would be required. If the proof does not cover hard selection, acknowledge this limitation and provide justification that soft-mixture is a reasonable approximation or upper bound.
3. **Add computational cost analysis.** Include a table comparing inference time and model size for GoalRank vs. MG-E (3, 20, 100 generators) to help practitioners assess the trade-offs.

## Score and Decision

MY FINAL SCORE: <score>8</score>  
MY FINAL DECISION: <decision>Accept</decision>