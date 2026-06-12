## Summary

This paper introduces the Aligned Scoring Rule (ASR), a method for designing proper scoring rules for textual information elicitation that are optimized to align with human preferences (e.g., instructor scores). Building on the Elicitation^GPT framework of Wu & Hartline (2024), the authors formulate a convex optimization problem over separate scoring rules to minimize the mean squared error between the proper scoring rule and a reference score. Experiments on peer grading datasets demonstrate that ASR achieves significantly better alignment with instructor and LLM-Judge scores compared to non-aligned baselines while maintaining provable properness guarantees.

## Strengths

- **Novel and well-motivated problem formulation**: The paper addresses a genuine tension in textual elicitation—the need for both provable truthfulness (properness) and alignment with human preferences. The idea of optimizing a proper scoring rule to match a reference score is a natural and valuable contribution that bridges mechanism design and practical deployment.

- **Clean theoretical framing**: The optimization problem (Program 2) is clearly stated, and the convexity result (Corollary 3.4) is correctly identified. The reduction to a finite-dimensional convex problem over six variables per dimension is elegant and makes the approach computationally tractable.

- **Strong empirical results**: The experimental results in Table 1 show substantial improvements over baselines. ASR achieves Pearson correlations of 0.717 and 0.705 against instructor and LLM-Judge scores respectively, compared to 0.294 and 0.328 for the best non-aligned baseline (EGPT-AV). The nearly-identity linear fit in Figure 4 provides compelling visual evidence of alignment.

- **Practical significance**: Peer grading is a concrete, high-impact application where both truthfulness and alignment matter. The paper demonstrates that the approach works on real classroom data across 22 assignments, lending credibility to the practical utility of the method.

## Weaknesses

### Major

1. **Limited evaluation of properness preservation**: The paper claims ASR maintains properness by construction (since it optimizes over the space of proper scoring rules), but there is no empirical validation that the learned scoring rule actually satisfies the properness constraints on held-out data. Given that the optimization is solved approximately via gradient descent, it would be valuable to verify that the learned rule does not violate properness constraints in practice, especially near the boundary of the feasible region.

2. **No comparison with non-proper baselines**: The paper only compares against proper baselines (constant score, EGPT-AV, EGPT-MV). A natural question is: how much alignment is "lost" by enforcing properness? Comparing ASR against a non-proper regression model (e.g., a linear model or neural network trained to predict reference scores directly from the same features) would quantify the cost of the properness constraint and strengthen the motivation for the approach.

3. **Limited discussion of the "know-it-or-not" assumption**: Assumption 2.2 (that posterior beliefs are either 0, 1, or the prior) is a strong restriction. The paper justifies it based on observations from the peer grading dataset, but does not provide evidence for how common or limiting this assumption is. If agents can have more nuanced beliefs (e.g., 70% confidence), the ternary report space may be insufficient, and the properness guarantees may not hold for the actual belief distributions.

### Minor

1. **The reference scores themselves are not validated**: The paper uses instructor scores and LLM-Judge scores as "ground truth" for alignment, but does not discuss the reliability or inter-rater agreement of these scores. If the reference scores are noisy or biased, aligning to them may not be desirable.

2. **Limited analysis of the optimization's sensitivity**: The convex optimization has only 6m variables (where m is the number of summary points), but the paper does not discuss how the solution depends on the number of training samples per assignment, the choice of optimization algorithm, or convergence criteria.

3. **The interpretability claim is not empirically evaluated**: The paper claims that ASR is interpretable because the convexity of single-dimensional scores can identify important rubric points, but this is only demonstrated via a case study in the appendix. A more systematic evaluation of interpretability (e.g., comparing identified important dimensions with human intuition) would strengthen this claim.

### Trivial

- The paper uses "know-it-or-not" in Definition 2.3 but "know-it-or-know" in the algorithm description; this is a minor inconsistency.

## Nice-to-Haves

- An ablation study showing how performance varies with the number of summary points m would be informative.
- A discussion of how the approach could be extended to continuous report spaces (beyond the ternary {0,1,⊥} space) would broaden the applicability.
- A comparison with the differentiable economics approach (Dütting et al., 2024) using neural network function approximators, as mentioned in the related work, would be a natural extension.

## Novel Insights

The paper's core insight is that proper scoring rules for textual elicitation can be optimized to match arbitrary reference scores while maintaining truthfulness, by solving a convex optimization over the space of separate scoring rules. This is a principled way to convert non-proper human or LLM judgments into proper scoring mechanisms. The observation that the optimization is convex (and thus tractable) for separate scoring rules but not for max-over-separate rules is a technically useful distinction that guides practical implementation.

## Suggestions

- Add an empirical validation that the learned ASR satisfies properness constraints on held-out data, perhaps by checking the inequalities in Definition 2.5 on a test set.
- Include a comparison with a non-proper baseline (e.g., a linear regression trained on the same features) to quantify the alignment cost of the properness constraint.
- Provide more details on the optimization procedure: number of gradient descent steps, learning rate, initialization, and how the boundedness constraint (sum of scores in [0,1]) is enforced.

## Score and Decision

The paper makes a clear, well-motivated contribution to an important problem (aligning proper scoring rules with human preferences for textual elicitation). The theoretical framing is sound, the empirical results are strong, and the practical relevance is evident. The major weaknesses—lack of empirical properness validation and absence of non-proper baselines—are addressable and do not invalidate the core contribution. The paper is a solid contribution to the intersection of mechanism design and LLM-based evaluation.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>