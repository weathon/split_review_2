## Summary

This paper studies how to aggregate answers from multiple LLMs beyond simple majority voting. The authors propose two algorithms: Optimal Weight (OW), which uses first-order information (model accuracies) to achieve Bayesian-optimal aggregation, and Inverse Surprising Popularity (ISP), which leverages second-order information (answer correlations between models) when ground-truth labels are unavailable. The paper provides theoretical guarantees showing both methods provably outperform majority voting under mild assumptions, and validates these claims through simulations and real-world experiments on UltraFeedback, MMLU, and a healthcare dataset (ARMMAN).

## Strengths

- **Strong theoretical foundation**: The paper provides rigorous theoretical analysis, including Bayesian optimality of OW (Theorem 1) and explicit expressions for the expected advantage of ISP over MV and SP (Theorem 2). The theoretical results are clean and well-motivated.
- **Practical relevance**: The problem of aggregating multiple LLM responses is timely and important, especially given the growing use of multi-agent LLM systems. The paper addresses the realistic constraint that ground-truth labels are often unavailable.
- **Novel algorithmic contribution**: ISP is a clever adaptation of the surprisingly popular rule, and the paper provides both theoretical justification and empirical evidence for why this modification is necessary in the LLM setting (as opposed to human crowds).
- **Comprehensive empirical evaluation**: Experiments span synthetic data, standard LLM benchmarks (UltraFeedback, MMLU), and a real-world healthcare application (ARMMAN), demonstrating consistent improvements over majority voting across diverse settings.

## Weaknesses

### Fatal
None.

### Major
- **Conditional independence assumption (Assumption 1) is strong and likely violated in practice**: The paper acknowledges this limitation and claims to extend results to more general settings in Appendix C, but the main theoretical results (Theorems 1-3) all rely on this assumption. Given that LLMs are trained on similar data and may share systematic biases, conditional independence is questionable. The empirical results are encouraging, but the theoretical guarantees are weaker than claimed.
- **The practical estimation of second-order information requires many samples**: Theorem 3 shows that the advantage of ISP over MV degrades as O(1/√M), but the paper does not provide clear guidance on how many samples are needed in practice. The experiments use large datasets (e.g., MMLU has ~14K questions), but many real-world applications may have far fewer unlabeled questions.
- **The comparison between OW-L/OW-I and MV is somewhat unfair**: OW-L and OW-I use the entire dataset to estimate accuracies (via second-order information), while MV is a per-question method. A fairer comparison would be to evaluate MV on a held-out set after using the training set to estimate which model is best, or to compare against a weighted voting scheme that uses held-out validation accuracy.

### Minor
- **The paper claims OW is "Bayesian optimal" but this optimality is with respect to the true distribution P, which is unknown**: In practice, the accuracies x_i must be estimated, and the paper's own experiments use estimated accuracies (OW-L, OW-I). The optimality guarantee does not extend to these practical variants.
- **The presentation of Algorithm 1 has a formatting issue**: The argmax expression appears to be missing a closing parenthesis or bracket, making it slightly unclear.
- **The paper does not discuss computational cost**: While querying LLMs is expensive, the aggregation algorithms themselves have different computational requirements (e.g., OW-L requires solving an optimization problem). A brief discussion of runtime would be helpful.

### Trivial
- The paper uses "surprising popularity" instead of the standard "surprisingly popular" in some places, but this is a minor terminology issue.

## Nice-to-Haves

- An ablation study showing how performance varies with the number of questions M used to estimate second-order information would strengthen the practical guidance.
- A discussion of when majority voting might be preferred despite the theoretical advantages of OW/ISP (e.g., when N is very small or when models are nearly homogeneous).
- An analysis of the robustness of ISP to violations of the conditional independence assumption, perhaps through additional synthetic experiments with correlated agents.

## Novel Insights

The key insight is that the surprisingly popular rule, which works well for human crowds by correcting systematic biases, is actually *worse* than majority voting in the LLM setting because LLMs are generally more capable and exhibit less bias. The paper's inversion of this rule (ISP) is a principled response to this observation. This highlights an important distinction between human and machine aggregation that future work should consider. Additionally, the connection between optimal weighting and the Bradley-Terry model (Corollary 1) provides a theoretical justification for practices already used in LLM post-training.

## Suggestions

- Clarify the practical setting: When would a practitioner have access to enough unlabeled data to estimate second-order information reliably, but not have access to any labeled data for accuracy estimation? This would help readers understand the realistic applicability of ISP vs. OW-L/OW-I.
- Provide guidance on the minimum number of questions M needed for ISP to reliably outperform MV, perhaps through a simple rule of thumb or additional simulations.
- Consider adding a baseline that uses held-out validation accuracy to weight models, to provide a fairer comparison between OW-L/OW-I and methods that use first-order information.

## Score and Decision

The paper makes a solid contribution to an important and timely problem. The theoretical analysis is rigorous, the algorithms are well-motivated, and the empirical results are convincing across multiple datasets. The main concerns are the strength of the conditional independence assumption and the practical estimation requirements, but these are partially addressed through empirical validation and the acknowledgment of limitations. The paper is clearly written and represents a meaningful advance over the current practice of majority voting.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>