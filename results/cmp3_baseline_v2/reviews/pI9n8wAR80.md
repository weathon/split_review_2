## Summary

This paper proposes CoLA (Co-Calibrated Logit Adjustment) for long-tailed semi-supervised learning (LTSSL). The authors identify two key limitations in existing Logit Adjustment (LA) methods: (1) naive frequency counting overestimates head class prevalence due to sample redundancy, causing over-suppression, and (2) the overall adjustment strength is treated as a fixed hyperparameter despite being highly sensitive to the estimated distribution. CoLA addresses these by introducing De-Duplicated Distribution Estimation (DDDE) using effective rank to estimate class distributions, and Logit Meta-Calibration (LMC) which meta-learns the optimal overall adjustment strength on a proxy validation set. The method achieves state-of-the-art results across four benchmarks and six distribution types, supported by a theoretical generalization bound.

## Strengths

- **Novel and well-motivated problem identification**: The paper clearly identifies two genuine limitations in existing LA-based LTSSL methods—over-suppression from sample redundancy and the sensitivity of the overall adjustment strength to distribution estimates. The empirical demonstration in Figure 1b that optimal τ does not correlate monotonically with imbalance ratio is a compelling motivation.

- **Principled technical solution**: The DDDE component using effective rank to estimate de-duplicated class distributions is a clever adaptation of existing ideas (effective number of samples, effective rank) to the LTSSL context. The LMC meta-learning approach for learning τ is well-designed, and the use of a linear LA term (rather than logarithmic) is justified by stability considerations.

- **Strong empirical results**: CoLA achieves state-of-the-art or near-SOTA performance across all 5 distributions on CIFAR-10/100-LT, STL-10-LT, and SIN-127. The improvements are particularly notable on the more challenging CIFAR-100-LT (1+ percentage point gains) and STL-10-LT (up to 1.95% improvement). The ablation studies (Table 4) convincingly demonstrate the individual contributions of both DDDE and LMC.

- **Theoretical grounding**: The generalization bound (Proposition 1) provides a formal connection between the accuracy of distribution estimation (DDDE) and the quality of the learned τ (LMC), showing that a tighter bound requires smaller distribution discrepancy. The convexity analysis in Appendix F further supports the optimization.

## Weaknesses

### Major

- **Limited novelty of individual components**: While the combination is novel, both DDDE (effective rank for de-duplication) and LMC (meta-learning on a proxy set) draw heavily from existing ideas. The effective number of samples concept (Cui et al., 2019) and effective rank (Roy & Vetterli, 2007) are well-established. Meta-learning on a held-out set for hyperparameter optimization is also a standard technique. The paper would benefit from clearer articulation of what is genuinely new beyond the combination.

- **Theoretical analysis is somewhat disconnected from practice**: The generalization bound (Proposition 1) is a standard domain adaptation-style bound with importance weighting. While it formally connects DDDE and LMC, it does not provide actionable guidance (e.g., how to set the bound tightness, or what the Rademacher complexity term means for the specific hypothesis class). The bound's dependence on B (the importance weight bound) is circular—Assumption 4 requires that DDDE does not severely underestimate, but the whole point is that DDDE should improve estimation. The convexity analysis in Appendix F is more practically relevant but is relegated to the appendix.

- **Computational overhead is not thoroughly analyzed**: The DDDE requires computing SVD of feature matrices per class per epoch, and LMC requires constructing a proxy set and performing meta-learning optimization. While Appendix H provides a brief time complexity analysis, there is no empirical runtime comparison with baselines. For a method that claims to be practical, this is a notable omission.

### Minor

- **The linear LA term deviation is under-explained**: The paper states that the linear term (τ·p) is motivated by theoretical insights from (Mor & Carmon, 2025) and avoids numerical instability, but this is not elaborated. Given that the standard LA uses log frequencies, this change is significant and deserves more justification, especially since the ablation study does not compare the linear vs. logarithmic formulation.

- **The warm-up phase for τ is somewhat ad-hoc**: The paper mentions that during warm-up, τ is configured according to ACR, but does not specify how long this phase lasts or how sensitive the method is to this choice. Given that LMC is a core contribution, the reliance on a prior method for initialization is a potential weakness.

### Trivial

- The paper occasionally uses inconsistent notation (e.g., "LMIC" in Section 4 vs. "LMC" elsewhere).

## Nice-to-Haves

- An empirical comparison of the linear vs. logarithmic LA term in the ablation study would strengthen the justification for this design choice.
- A sensitivity analysis of the warm-up duration and the threshold for when LMC begins would improve reproducibility.
- Runtime comparison with baselines (e.g., ACR, Meta-Expert) would help practitioners assess the practical cost of the method.

## Novel Insights

None beyond the paper's own contributions. The key insight—that the two components of LA (class-wise and overall adjustment) interact and must be co-designed—is genuinely useful, but the individual techniques (effective rank for de-duplication, meta-learning for hyperparameter optimization) are adaptations of existing ideas rather than fundamentally new concepts.

## Suggestions

- Provide an empirical comparison of the linear vs. logarithmic LA term in the ablation study to justify the design choice.
- Include a runtime comparison with the most competitive baselines (ACR, Meta-Expert) to demonstrate practical feasibility.
- Clarify the warm-up phase: how many epochs, how sensitive is the method to this choice, and what happens if LMC is applied from the start?

## Score and Decision

The paper makes a solid contribution to LTSSL by identifying and addressing two genuine limitations of existing LA-based methods. The empirical results are strong and consistent across multiple benchmarks and distribution types. The theoretical analysis, while not groundbreaking, provides formal support for the method's design. The main weaknesses are the limited novelty of individual components and the lack of empirical runtime analysis. However, the combination is effective and well-motivated, and the paper is clearly written. This is a solid paper that advances the state of the art in a well-studied problem.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>