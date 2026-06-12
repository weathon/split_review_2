## Summary

This paper introduces a formal framework for studying how an algorithmic information mediator (e.g., an LLM) can strategically control the precision of private signals in a sequential social learning setting. The authors characterize optimal policies for both altruistic (welfare-maximizing) and biased (action-inducing) planners, proving convexity of the value function and identifying distinct policy regimes. They validate their theoretical results through LLM-based simulations, showing that LLM planners exhibit emergent strategic behavior that broadly mirrors theoretical predictions while adapting to non-Bayesian agent behavior.

## Strengths

- **Novel integration of control theory with social learning**: The paper bridges a gap between information design and sequential social learning by allowing the planner to dynamically choose signal precision for each agent, rather than fixing a single information structure upfront. This is a meaningful extension over prior work (e.g., Arieli et al. 2022, Wu et al. 2025).

- **Rigorous theoretical characterization**: The convexity proof of the value function (Theorem 2) is technically non-trivial and enables clean characterization of optimal policies for both altruistic and biased planners. The three-phase structure of the altruistic policy and the five-phase structure of the biased policy provide clear, interpretable insights.

- **Empirical validation with LLMs**: The simulation framework using LLMs as both planners and agents is well-designed and goes beyond simple numerical verification. The identification of specific non-Bayesian patterns (NB1-NB3) and the demonstration that LLM planners adapt to these patterns adds significant value.

- **Policy-relevant findings**: The result that even constrained planners (no lying, no cherry-picking, full transparency) can reduce social welfare by 40-50% is striking and has clear implications for AI governance and regulation.

## Weaknesses

### Major

- **Limited scope of the model assumptions**: The binary state, binary action, binary symmetric signal, and homogeneous agent assumptions are quite restrictive. While the authors acknowledge this as a limitation, the paper would be stronger with at least one concrete extension (e.g., the heterogeneous agents result in Appendix D is a start, but it's relegated to the appendix and not fully developed). The claim that "the qualitative nature of our results will continue to hold" for larger state spaces is speculative without formal justification.

- **LLM simulation methodology concerns**: The paper does not specify which LLM model(s) were used (GPT-4? Claude? Llama?), the number of simulation runs, or the statistical significance of the results. The "emergent strategic behavior" claims would be more convincing with multiple LLM models, ablation studies, or at minimum, clear reporting of model versions and hyperparameters. The absence of these details makes reproducibility difficult.

- **Missing quantitative comparison between analytical and LLM policies**: Figure 2b shows a histogram of percentage deviation, but there is no formal statistical test or error metric (e.g., mean absolute error, KL divergence) comparing the LLM policy to the optimal policy. The claim that "the magnitude of the policy deviation is often modest" is qualitative and not rigorously supported.

### Minor

- **The biased planner's cost function asymmetry**: The biased planner incurs cost β(|q_i - p|) for any deviation from baseline, while the altruistic planner only incurs cost for increasing precision above p. This asymmetry makes direct comparison between the two planners' behaviors less clean. A unified cost framework would strengthen the theoretical contribution.

- **Discount factor interpretation**: The discount factor δ is introduced but its role in the theoretical results is not fully explored. The myopic case (δ=0) is characterized, but the general δ case for the biased planner is not explicitly stated in the main theorems.

### Trivial

- The paper uses "herding" and "information cascade" interchangeably, which is standard but could be clarified for readers less familiar with the social learning literature.

## Nice-to-Haves

- A formal comparison of the LLM planner's policy to the optimal policy using a quantitative metric (e.g., L1 distance, regret) with confidence intervals.
- An ablation study showing how the LLM planner's behavior changes with different LLM models or temperature settings.
- A discussion of how the planner's optimal policy changes with different cost functions β(·) beyond the linear case.

## Novel Insights

Beyond the paper's own contributions, a genuinely novel insight is that the optimal biased planner's strategy involves *intentionally obfuscating* signals (decreasing precision below baseline) in certain belief regimes. This is counterintuitive—one might expect a biased planner to always want more precise signals to steer agents—but the analysis shows that when public belief already favors the planner's desired action, reducing precision prevents agents from receiving countervailing private signals that could overturn the favorable cascade. This "strategic ignorance" result has implications for understanding how recommendation systems might subtly manipulate user behavior without explicit deception.

## Suggestions

1. Report the specific LLM model(s), version numbers, temperature settings, and number of simulation runs used in the experiments. Include confidence intervals or error bars on the policy deviation and welfare results.

2. Add a quantitative comparison metric (e.g., mean absolute error, Wasserstein distance) between the LLM planner's policy and the analytically optimal policy, with statistical significance testing.

3. Consider adding a small-scale human subject experiment or citing existing human data to strengthen the claim that LLM agents' non-Bayesian patterns mirror human cognitive biases.

4. Clarify in the main text how the discount factor δ affects the optimal policies for both planner types, beyond the myopic case.

## Score and Decision

The paper makes a solid theoretical contribution by introducing a tractable model of controlled social learning with dynamic signal precision choice, and provides rigorous characterizations of optimal policies. The LLM-based empirical validation is innovative and supports the theoretical findings. However, the restrictive model assumptions and the lack of detailed experimental reporting (LLM model specifics, statistical significance) prevent the paper from being a "strong accept." The core contribution is meaningful and the paper is well-written, but the empirical component needs more rigor to fully substantiate the claims about LLM strategic behavior.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>