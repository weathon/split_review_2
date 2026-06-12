## Summary
This paper introduces AdaBoN (Adaptive Best-of-N), a prompt-adaptive strategy for allocating inference-time compute in Best-of-N sampling for language model alignment. The method uses a two-stage algorithm: an initial exploration phase estimates the reward distribution for each prompt using a small budget, followed by a greedy allocation of the remaining budget based on estimated marginal gains. The authors evaluate AdaBoN across 12 LM-RM pairs, 3 datasets, and 50 batches of prompts, showing consistent improvements over uniform allocation and competitiveness against uniform allocations with 20% larger inference budgets.

## Strengths
- **Practical and well-motivated problem**: The paper addresses a genuine inefficiency in Best-of-N sampling—the uniform allocation of compute across prompts of varying difficulty—which has real-world implications for latency and computational cost in deployment settings.
- **Comprehensive empirical evaluation**: The study covers 12 LM-RM pairs, 3 datasets, and 50 distinct batches per configuration, providing robust evidence for the method's effectiveness. The inclusion of multiple batch sizes and inference budgets strengthens the claims.
- **Simple, model-agnostic design**: AdaBoN requires no auxiliary model training, works out-of-the-box with any LM-RM combination, and has minimal hyperparameter tuning (only the exploration budget d), making it highly practical for deployment.
- **Novel evaluation metrics**: The Batch Win Rate (BWR) and Expected Survival Time (EST) are well-defined and appropriate for the problem setting, capturing both relative improvement over uniform allocation and computational savings against larger budgets.

## Weaknesses
### Fatal
None.

### Major
- **Limited comparison with existing adaptive methods**: The authors explicitly state they cannot compare with Damani et al. (2024) due to implementation difficulties and computational cost. While the reasoning is understandable, this is a significant gap—the paper claims to address the same problem but provides no empirical evidence that AdaBoN outperforms or is competitive with the most directly related prior work. The paper would be substantially stronger with at least a small-scale comparison or a principled argument for why the comparison is infeasible beyond computational cost.

- **The two-stage design limits adaptivity**: The method commits to a fixed exploration budget d (set to 0.75B in most experiments) and does not dynamically refine estimates during the allocation phase. This means that 75% of the budget is spent before any adaptive allocation occurs, which seems counterintuitive for an "adaptive" method. The paper would benefit from a clearer justification for why this specific split is chosen and whether more fine-grained adaptivity (e.g., sequential allocation with periodic re-estimation) would yield further gains.

- **Assumption of smooth reward distributions may not generalize**: The method relies on Gaussian KDE for reward distribution estimation, which the authors note works well for the continuous, smooth distributions they observe. However, this assumption may fail for discrete reward models, sparse reward signals, or domains where reward distributions are multimodal in ways that KDE cannot capture. The paper acknowledges this as a limitation but does not explore alternative estimation procedures or characterize when KDE might fail.

### Minor
- **The exploration budget d=0.75B is a large fraction of total budget**: Using 75% of the budget for exploration means that the adaptive allocation only affects the remaining 25%. While the results show improvement, the method's "adaptivity" is quite limited in scope. A more aggressive exploration-exploitation trade-off (e.g., d=0.5B or d=0.25B) might yield different insights.

- **Results are presented primarily for K=5, B=120**: While ablations for other K and B values are in the appendix, the main text focuses heavily on a single configuration. The paper would benefit from a more prominent discussion of how performance varies across the full range of hyperparameters.

- **The EST metric caps at 2B**: The authors cap the sum in Equation 5 to 2B, which limits the interpretability of EST values near the cap. For batches where EST approaches 2B, it's unclear whether the true EST might be much higher.

### Trivial
- The paper uses "concave" in quotes in Algorithm 1 but the formal proposition (3.1) proves concavity. The quotes are unnecessary and slightly confusing.

## Nice-to-Haves
- A small-scale comparison with Damani et al. (2024) on a single LM-RM pair and a few batches would significantly strengthen the paper's claims about practical advantages.
- An analysis of when AdaBoN fails (e.g., which types of reward distributions lead to BWR < 0.50) would help practitioners understand the method's limitations.
- A discussion of the computational overhead of the Monte Carlo estimation step (Line 3 of Algorithm 2) and how it scales with batch size and budget would be useful for deployment considerations.

## Novel Insights
The paper's key insight is that reward distributions for LM-RM pairs are smooth and learnable from a small number of samples, enabling effective prompt-adaptive allocation without auxiliary model training. This observation, combined with the two-stage design that minimizes latency, provides a practical bridge between theoretical allocation problems and real-world deployment constraints. The finding that AdaBoN remains competitive against uniform allocations with 20% larger budgets suggests that adaptive allocation can yield meaningful computational savings without sacrificing alignment quality.

## Suggestions
- Add a small-scale comparison with Damani et al. (2024) on a single LM-RM pair and a few batches, or provide a more detailed explanation of why such a comparison is infeasible beyond computational cost.
- Include an analysis of the sensitivity of results to the exploration budget d, perhaps showing BWR as a function of d for a few representative configurations.
- Discuss the computational overhead of the Monte Carlo estimation step and how it scales with batch size and budget.

## Score and Decision
The paper addresses a well-motivated problem with a simple, practical solution and provides a comprehensive empirical evaluation. The main weakness is the lack of comparison with the most directly related prior work, which limits the ability to assess the method's relative merits. However, the paper's contributions—a novel adaptive allocation strategy, new evaluation metrics, and extensive empirical results—are substantial and valuable to the community. The method is clearly presented, reproducible, and has practical implications for deployment.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>