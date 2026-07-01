## Summary
This paper introduces AdaBoN, a prompt-adaptive strategy for Best-of-N alignment that allocates inference-time compute more efficiently across batches of prompts. The method uses a two-stage algorithm: an initial exploratory phase estimates the reward distribution for each prompt using a small budget, followed by a greedy allocation of the remaining budget based on estimated marginal gains. The authors evaluate AdaBoN across 12 LM-RM pairs and 50 batches from three datasets, showing consistent improvements over uniform allocation and competitiveness against uniform allocations with 20% larger budgets.

## Strengths
- **Practical and well-motivated problem**: The paper addresses a genuine inefficiency in Best-of-N sampling—the uniform allocation of compute across prompts of varying difficulty—which has clear practical relevance for deployment scenarios with latency and budget constraints.
- **Comprehensive empirical evaluation**: The study covers 12 LM-RM pairs, 3 datasets, and 50 batches per setting, providing robust evidence for the method's effectiveness. The use of multiple metrics (BWR, EST) and ablations over batch size and budget strengthens the claims.
- **Simplicity and model-agnostic nature**: AdaBoN requires no auxiliary model training, works out-of-the-box for any LM-RM combination, and has minimal hyperparameter tuning (only the exploration budget d). This makes it highly practical and reproducible.
- **Latency-aware design**: The two-stage approach minimizes latency by allowing parallelization of LM calls, which is a practical concern often overlooked in adaptive methods.

## Weaknesses
### Fatal
None.

### Major
- **Limited novelty relative to Damani et al. (2024)**: The core problem formulation and the two-stage allocation framework are very similar to Damani et al. (2024). The main claimed differences are: (1) using KDE instead of a learned auxiliary model, (2) focusing on a different regime (small K, large B), and (3) broader evaluation. While these are valid contributions, the methodological novelty is incremental. The paper would benefit from a clearer articulation of what fundamentally new algorithmic insight is being introduced beyond the choice of distribution estimator.
- **No comparison with the most directly related method**: The authors explicitly state they cannot compare with Damani et al. (2024) due to implementation difficulties and computational cost. While the reasoning is understandable, the lack of any empirical comparison—even on a smaller scale or with a simplified version—weakens the claim that AdaBoN is a superior approach. The paper would be stronger with at least a small-scale comparison or a theoretical argument for why the KDE-based approach should outperform the learned model approach in the small-K, large-B regime.

### Minor
- **The choice of d=0.75B is somewhat arbitrary**: While the authors show that this choice works well across experiments, the exploration budget consumes 75% of the total budget, leaving only 25% for adaptive allocation. This raises the question of whether the gains come primarily from the exploration phase itself rather than the adaptive allocation. A more detailed analysis of the trade-off between exploration and exploitation would strengthen the paper.
- **The EST metric definition has a subtle issue**: The EST sums BWTR over N from 1 to infinity, but in practice is capped at 2B. The interpretation as "expected survival time" assumes that BWTR is monotonically decreasing in N, which is not guaranteed. The paper would benefit from clarifying this assumption and discussing potential violations.
- **The paper claims AdaBoN "minimizes latency" but only requires "two calls to the base LM"**: This is somewhat misleading—while the number of *sequential* calls is two, the total number of LM queries is still BK (the same as uniform). The latency advantage is about parallelization, not total compute reduction.

### Trivial
- The paper uses "BWR" and "BWTR" which are very similar acronyms and could be confused. Consider renaming one for clarity.

## Nice-to-Haves
- An analysis of how the quality of the KDE estimate (e.g., via Wasserstein distance to the true distribution) varies with the exploration budget d, and how this correlates with final BWR performance.
- A discussion of the computational overhead of the Monte Carlo estimation step (Line 3 of Algorithm 2) and how it scales with K and B.
- An investigation of whether the method's performance depends on the specific choice of Gaussian kernel versus other nonparametric density estimators.

## Novel Insights
None beyond the paper's own contributions. The key insight—that reward distributions for LM-RM pairs are smooth and can be estimated with simple nonparametric methods, enabling effective adaptive allocation—is well-demonstrated but not deeply surprising given the existing literature on reward distribution properties.

## Suggestions
- Provide a small-scale comparison with Damani et al. (2024), even if limited to one LM-RM pair and one dataset, to empirically validate the claimed advantages of the KDE-based approach.
- Include an analysis of the sensitivity to the exploration budget d, showing the trade-off between estimation quality and remaining budget for adaptation.
- Clarify the latency argument: explicitly state the number of sequential LM calls versus total LM calls, and discuss scenarios where this distinction matters (e.g., on-device vs. server-side inference).

## Score and Decision
The paper addresses a practical and well-motivated problem with a simple, effective solution and provides a thorough empirical evaluation. However, the methodological novelty is incremental relative to existing work, and the lack of any empirical comparison with the most directly related method weakens the contribution. The paper is solid and would be a useful addition to the literature, but it does not rise to the level of a top-tier acceptance.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>