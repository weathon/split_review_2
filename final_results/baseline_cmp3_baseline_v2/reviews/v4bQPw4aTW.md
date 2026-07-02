## Summary
This paper proposes AdaBoN (Adaptive Best-of-N), a two-stage inference-time alignment method that adaptively allocates sampling budgets across a batch of prompts based on estimated reward distributions. The initial exploratory stage uses a small budget per prompt to estimate reward distributions via kernel density estimation, then a second stage greedily allocates the remaining budget across prompts to maximize cumulative reward. The authors evaluate their method on 12 LM-RM pairs across three datasets, showing consistent improvements over uniform budget allocation.

## Strengths
- **Well-motivated practical problem**: The paper addresses a genuine limitation of Best-of-N sampling - its computational inefficiency from uniform allocation across prompts of varying difficulty. The problem is clearly framed and relevant for deployment scenarios like on-device inference.
- **Simple and practical solution**: The two-stage approach is straightforward, model-agnostic, and requires no auxiliary training. The use of Gaussian KDE with Scott's rule for bandwidth selection makes implementation trivial. The method handles latency well by being parallelizable into only two rounds of LM calls.
- **Comprehensive empirical evaluation**: The authors evaluate across 12 LM-RM pairs (4 LMs × 3 RMs), 3 datasets, and 50 batches per configuration, providing robust statistical evidence. The introduction of BWR and EST metrics appropriately captures the meaningful aspects of performance comparison.

## Weaknesses

### Major
- **Unclear practical significance of gains**: The median BWR values in Table 1 (0.54-0.62) are only modestly above 0.50. While statistically significant across 50 batches, it is unclear whether a 4-12% win rate improvement translates to meaningful practical savings given the overhead of the two-stage procedure and Monte Carlo estimation. The paper would benefit from a concrete cost-benefit analysis showing wall-clock time or FLOP savings.

- **Limited baselines and comparisons**: The authors only compare against uniform allocation. While they justify not comparing to Damani et al. (2024) due to implementation challenges, this severely limits the paper's contribution assessment. There is no comparison to other adaptive test-time compute approaches, no ablation on the greedy allocation versus simpler heuristics, and no comparison to simply using a smaller uniform budget.

- **The exploration budget choice is critical but not thoroughly studied**: The key hyperparameter d = 0.75B means that 75% of the budget is allocated to the exploration stage, leaving only 25% for adaptive allocation. This seems like a very conservative split that limits the potential gains from adaptivity. The tuning results in the appendix (Table 3) show that performance is relatively insensitive to d, but this also means the adaptive component may be contributing modestly.

### Minor
- **The empirical setting may favor the method**: The choice of K=5, B=120 with d=0.75B means that after exploration (d=90 per prompt), only 30 samples per prompt remain for adaptive allocation across 5 prompts (150 total). The gains from redistributing 150 samples may be inherently limited, and the results are consistent with this interpretation.

- **Missing analysis on when adaptivity helps most**: The paper does not analyze what properties of a batch drive AdaBoN's success. Are certain reward distribution characteristics (e.g., high variance, multi-modality) predictive of larger gains? Such analysis would strengthen the practical guidance for practitioners.

### Trivial
- The EST definition bounds the sum to 2B, which means the maximum observable EST is around 240 (2×120), but the reported values cluster around 148-153, providing limited resolution for differentiation.

## Nice-to-Haves
- A comparison to other simple adaptive strategies (e.g., allocating remaining budget proportional to observed variance or to the maximum observed reward) would help isolate the benefit of the KDE-based approach.
- An analysis of how the Monte Carlo sample size m=1024 affects the quality of the V_ij estimates and downstream allocation quality would be useful for practitioners.

## Novel Insights
The paper's key insight is that reward distributions for LMs are sufficiently smooth and learnable from small samples that a simple KDE-based estimator, combined with a greedy allocation procedure, can outperform uniform budget allocation across diverse LM-RM pairs. This finding is empirically validated across 12 model pairs, suggesting that the structure of reward distributions in language model alignment has useful statistical properties that can be exploited for computational efficiency. The paper also contributes the methodological insight that effective adaptive allocation can be achieved with minimal latency overhead (only two rounds of LM calls), which is a practical consideration often overlooked in the adaptive compute literature.

## Suggestions
- Provide an analysis of wall-clock time or total FLOPs comparing AdaBoN to uniform allocation, including the overhead of Monte Carlo estimation and KDE fitting.
- Add experiments with smaller exploration budgets (e.g., d = 0.3B or d = 0.5B) to better understand the regime where the adaptive component has more room to operate.
- Characterize which types of batches (e.g., high variance in reward distributions across prompts) benefit most from AdaBoN.

## Score and Decision

The paper addresses a well-motivated problem, proposes a simple and practical solution, and provides reasonably thorough empirical evaluation. However, the modest gains (median BWR 0.54-0.62), the lack of comparison to other methods, and the conservative exploration budget (75% allocated to exploration) limit the contribution's significance. The paper represents incremental but solid progress on an important practical problem.

MY FINAL SCORE: 5.0score</score>
MY FINAL DECISION: Rejectdecision</decision>