## Summary

This paper studies how to aggregate answers from multiple LLMs beyond majority voting by leveraging higher-order information. The authors propose two algorithms: Optimal Weight (OW), which uses first-order information (agent accuracies) and is proven Bayesian optimal under conditional independence, and Inverse Surprising Popularity (ISP), which uses second-order information (correlations between agents) and is shown theoretically to have higher expected advantage than majority voting, which in turn outperforms the standard surprising popularity rule. Experiments on synthetic data, UltraFeedback, MMLU, and a real-world healthcare dataset (ARMMAN) demonstrate consistent improvements over majority voting.

## Strengths

- **Novel adaptation of information aggregation theory to LLM multi-agent setting.** The paper formalizes the LLM aggregation problem with random label shuffling and derives principled aggregation rules, bridging a gap between classic information aggregation literature and modern LLM applications.
- **Theoretical comparison of ISP, MV, and SP.** Theorem 2 provides explicit expressions for the expected advantage differences, giving a clear theoretical ranking (ISP > MV > SP) that is empirically validated.
- **Extensive empirical evaluation.** Experiments span synthetic data, two standard LLM benchmarks (UltraFeedback, MMLU), and a real-world healthcare dataset (ARMMAN), using multiple model families. The results consistently show improvements over majority voting, with statistical significance tests reported.
- **Practical estimation methods for unsupervised settings.** The paper proposes OW-L and OW-I to estimate accuracies from second-order information without ground-truth labels, making the Bayesian optimal aggregator applicable in realistic scenarios.

## Weaknesses

### Major

- **Theoretical results are on advantage functions, not accuracy.** The paper proves that ISP has higher expected *advantage* than MV, and MV higher than SP, but does not establish that higher advantage translates to higher accuracy. The advantage function is a proxy; without a formal link, the core theoretical claim ("ISP outperforms MV") is not fully supported. The experiments show accuracy gains, but the theory is incomplete.
- **OW's Bayesian optimality requires true accuracies, which are unavailable.** The practical methods (OW-L, OW-I) are heuristics that estimate accuracies from second-order information. No theoretical guarantees are provided for these estimated-weight variants, so the optimality property does not carry over to the actual deployed algorithms. The paper would benefit from analysis of how estimation error affects aggregation performance.
- **Conditional independence assumption is strong and likely violated in practice.** While the paper mentions relaxing this assumption in the appendix, the main theoretical results rely on it. The experiments may violate this assumption (e.g., questions of varying difficulty), but the paper does not analyze robustness to violations or quantify how much the assumption matters.

### Minor

- **Baselines are limited.** The paper compares only against majority voting and surprising popularity. Other natural baselines such as confidence-weighted voting, softmax-based aggregation, or simple averaging of log-probabilities are not considered, making it unclear how much of the gain is due to the specific proposed methods versus any weighted aggregation.
- **The advantage of ISP over MV diminishes as K increases** (Theorem 2 shows Θ(1/K) gap). The paper acknowledges this but does not discuss practical implications or provide guidance on when ISP is most beneficial.
- **Estimation of second-order information requires many samples.** The paper assumes "negligible cost" but does not analyze sample complexity or provide practical guidelines for how many questions are needed for reliable estimation.

### Trivial

- The paper uses "first-order information" to mean accuracies and "second-order information" to mean conditional probabilities between agents. This terminology is reasonable but could be clarified earlier.

## Nice-to-Haves

- A direct theoretical comparison of expected accuracy (not just advantage) between ISP and MV would strengthen the paper significantly.
- Analysis of how violations of conditional independence affect the theoretical guarantees would be valuable.
- Comparison against additional aggregation baselines (e.g., confidence-weighted voting, Borda count) would better contextualize the improvements.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Provide a theoretical or empirical link between advantage and accuracy to justify the main claim that ISP "outperforms" MV.
- Include experiments with more diverse model ensembles (e.g., varying number of agents, different model families) to test generalizability.
- Discuss the sample complexity of estimating second-order information and provide practical recommendations for minimum dataset size.

## Score and Decision

**Score:** 6  
**Decision:** Borderline Accept

The paper makes a solid contribution to multi-agent LLM aggregation by introducing theoretically motivated algorithms that consistently outperform majority voting in experiments. However, the theoretical gap between advantage and accuracy, and the heuristic nature of the practical OW variants, prevent a stronger recommendation. The work is above the ICLR median and offers value to the community, but the core theoretical claims are not fully substantiated.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>