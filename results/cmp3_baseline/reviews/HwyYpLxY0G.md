## Summary

This paper proposes the Aligned Scoring Rule (ASR), a method for designing proper scoring rules for textual information elicitation that are aligned with human preferences. The authors build on the ElicitationGPT framework (Wu & Hartline, 2024) and optimize over the space of separate scoring rules to minimize MSE between the proper scoring rule and a reference score (e.g., instructor score or LLM-Judge score). Experiments on peer grading datasets show that ASR outperforms baselines in alignment metrics while maintaining provable properness.

## Strengths

- **Novel and well-motivated problem formulation**: The paper identifies a genuine gap—proper scoring rules for text may not align with human preferences—and proposes a principled optimization framework to bridge this gap. This is a natural and important extension of the ElicitationGPT framework.
- **Clean theoretical framing**: The optimization over separate scoring rules is convex (Corollary 3.4), which is a nice theoretical property that makes the approach computationally tractable and interpretable. The connection to automated mechanism design is well-drawn.
- **Empirical results are convincing**: The ASR significantly outperforms baselines (EGPT-AV, EGPT-MV, constant) on MSE, Pearson, and Spearman correlation. The nearly-identity linear fit in Figure 4 is a strong visual demonstration of alignment.
- **Interpretability**: The separate scoring rule structure allows identification of important rubric dimensions, which is a practical advantage over black-box approaches.

## Weaknesses

### Fatal
None.

### Major
- **The "properness" guarantee relies on the non-inverting oracle assumption (Definition 3.1), which is not empirically validated.** The paper states that ElicitationGPT is proper if the QA oracle is non-inverting, but provides no empirical evidence that the LLM-based QA oracle used in experiments satisfies this condition. Given that LLMs are known to have various biases and can make systematic errors, this is a significant gap. Without validation, the core claim of "provably proper" scoring in the experimental setting is unsubstantiated.
- **The evaluation does not test properness empirically.** The paper evaluates alignment (MSE, correlation) but never tests whether the ASR actually incentivizes truthful reporting in practice. A proper scoring rule is defined by its incentive properties, yet the experiments only measure alignment with reference scores. The paper would be significantly stronger with a behavioral experiment or simulation showing that agents maximize expected score by reporting truthfully under ASR.
- **The dataset is small and limited.** 22 assignments, each with 6-8 submissions and 6-8 peer reviews, yields a very small total sample (516 reviews across two classes). This raises concerns about the statistical significance of results and generalizability. The paper does not report confidence intervals or statistical significance tests for the main results in Table 1.

### Minor
- **The "Know-it-or-not" assumption (Assumption 2.2) is restrictive and not well-justified.** The paper states that in their dataset, textual reports either express a state being 0 or 1, or have no information. This is a strong assumption that limits the generality of the approach. It is not clear how the method would extend to settings where agents can express graded uncertainty (e.g., "70% confident").
- **The paper does not discuss the computational cost of the optimization or the LLM queries.** Given the small dataset, this may not be a bottleneck, but for practical deployment, the cost of running summarization and QA oracles on every review could be substantial.
- **The paper does not compare against a simple baseline of directly using the LLM-Judge score as the scoring rule.** While the LLM-Judge score is not proper, it would be informative to see how much alignment is lost by enforcing properness.

### Trivial
- The paper uses "know-it-or-not" in Definition 2.3 and Assumption 2.2, but the term is not standard and could be confused with "know-it-all." The term "ternary report" or "uncertainty-aware" might be clearer.

## Nice-to-Haves
- An ablation study showing the effect of the number of summary points m on alignment quality.
- A simulation or behavioral experiment demonstrating that agents indeed maximize expected score by reporting truthfully under ASR.
- Confidence intervals or bootstrapped standard errors for the metrics in Table 1.

## Novel Insights

The paper's key insight is that proper scoring rules for text can be optimized for alignment with human preferences while maintaining truthfulness, by solving a convex optimization over separate scoring rules. This bridges the gap between the theoretical literature on proper scoring rules and the practical need for aligned evaluation in LLM-based systems. The observation that the optimization is convex (Corollary 3.4) is a nice theoretical contribution that makes the approach practical.

## Suggestions

- **Validate the non-inverting oracle assumption empirically.** Run a small experiment where you compare the LLM's QA output against human annotations for a subset of reviews to estimate the probability of inversion. If the assumption holds, report the empirical inversion rate. If it does not, discuss the implications for properness.
- **Add an empirical test of properness.** For example, simulate an agent with different beliefs and verify that the expected score is maximized by truthful reporting under ASR. This would directly support the claim that ASR is proper in practice.
- **Report confidence intervals or bootstrapped standard errors for Table 1.** Given the small dataset, this is essential for assessing the reliability of the results.
- **Discuss the limitations of the "know-it-or-not" assumption more thoroughly.** How would the method generalize to settings where agents can express graded uncertainty? This is important for broader applicability.

## Score and Decision

The paper addresses a well-motivated and timely problem, proposes a clean and theoretically grounded solution, and provides empirical evidence that the approach works on real peer grading data. The main weaknesses are the lack of empirical validation of the non-inverting oracle assumption and the absence of any empirical test of properness. However, these are common limitations in the literature on LLM-based elicitation, and the paper's core contribution—optimizing proper scoring rules for alignment—is sound and novel. The small dataset is a concern, but the results are consistent and the method is principled. I lean toward acceptance.

MY FINAL SCORE: 6.0score</score>
MY FINAL DECISION: Accept</decision>