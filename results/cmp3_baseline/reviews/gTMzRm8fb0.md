## Summary

This paper challenges the prevailing two-stage (Multi-)Generator–Evaluator ranking paradigm by theoretically proving that a single larger generator-only model can achieve strictly smaller approximation error to the optimal ranking policy, and that this error decreases with model size. Building on this insight, the authors introduce a group-relative optimization principle that uses a reward model trained on real user feedback to construct a reference policy, enabling effective training of large generator-only rankers. The proposed framework, GoalRank, is validated through extensive offline experiments on public benchmarks and large-scale online A/B tests, consistently outperforming state-of-the-art methods and exhibiting clear scaling laws.

## Strengths

- **Strong theoretical foundation.** Theorem 1 provides a rigorous proof that for any finite mixture of small generators with an evaluator, there exists a single larger generator-only model with strictly smaller KL divergence to the optimal ranking policy, and the error vanishes as model size grows. This directly motivates the generator-only paradigm and is a novel contribution.
- **Practical training principle.** The group-relative optimization (Equation 4–5) offers a tractable way to train a large generator using a biased reward model, with theoretical justification via an evidence upper bound. The method is robust to reward model bias, as shown in ablation studies.
- **Comprehensive empirical validation.** Offline experiments on three datasets (ML-1M, Amazon-Book, Industry) show large and consistent improvements over strong baselines (e.g., +17% H@6 on ML-1M, +25% H@6 on Industry). Scaling experiments on a 0.1B-parameter dataset confirm that GoalRank benefits from increased capacity while baselines saturate. Large-scale online A/B tests on a platform with over half a billion daily active users demonstrate statistically significant gains across all business metrics.
- **Clear exposition and well-motivated research questions.** The paper is clearly written, with a logical flow from theoretical analysis to practical algorithm to experimental validation.

## Weaknesses

### Fatal
None.

### Major
- **The theoretical optimal policy is defined via entropy-regularized reward maximization (Equation 1).** While this is a reasonable surrogate, the practical relevance of Theorem 1 depends on how well this regularized target aligns with true user utility. The paper does not discuss the gap between this target and the actual ranking objective in real systems, nor does it provide guarantees on the quality of the reference policy derived from a biased reward model beyond robustness to controlled noise.

### Minor
- **Scaling comparison fairness.** In Figure 3, GoalRank is scaled by increasing model capacity (hidden dimensions, layers, heads), while MG-E is scaled by increasing the number of generators. These are different scaling dimensions, and the paper does not report parameter counts for each method at each scale. A fairer comparison would control for total parameter count or computational cost.
- **Generator architecture not specified in main text.** The paper states the framework is model-agnostic, but the experiments likely use a specific architecture (e.g., transformer). A brief description of the generator used in the main experiments would improve reproducibility and clarity.
- **Evidence upper bound derivation is vague.** The paper mentions deriving an evidence upper bound of the optimization objective (Section 3.2) but does not present the derivation or even a sketch in the main text. The connection between this bound and the group-relative reference policy is asserted rather than explained.

### Trivial
- Online improvements are small in absolute percentage (e.g., 0.149% App Stay Time), though this is typical for large-scale systems and the results are statistically significant.

## Nice-to-Haves

- Provide a sketch of the evidence upper bound derivation in the main text to strengthen the theoretical motivation for the group-relative objective.
- Report parameter counts for all methods in the scaling experiments to ensure a fair comparison.
- Discuss the choice of auxiliary policies in the group construction (e.g., why those specific heuristics/lightweight models) and whether the method is sensitive to this choice.

## Novel Insights

Beyond the paper’s own contributions, the key insight is that the widely adopted two-stage Generator–Evaluator paradigm may be fundamentally suboptimal compared to a single, sufficiently large generator, both in terms of approximation error and scaling behavior. This challenges the conventional wisdom that explicit evaluation over multiple candidate lists is necessary for high-quality ranking, and suggests that investing in a single large model with a proper training objective (group-relative optimization) can be more effective than engineering complex multi-generator pipelines.

## Suggestions

- Clarify the scaling comparison by including a table of parameter counts for each method at each scale in Figure 3.
- Add a brief description of the generator architecture used in the experiments (e.g., transformer with self-attention) in Section 4.1.2 or Appendix D.2.
- Provide a short intuitive explanation of the evidence upper bound in Section 3.2 to help readers understand why group-relative normalization is justified.

## Score and Decision

**Score:** 8  
**Decision:** Accept

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>