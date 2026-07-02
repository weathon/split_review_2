### Summary

This paper studies how to make robust decisions based on partially calibrated forecasts. The authors consider a decision maker who wants to maximize their expected utility, but they are uncertain about the true conditional distribution of the outcome given the prediction. They model this uncertainty by considering a set of possible conditional distributions that are consistent with the calibration guarantees of the predictor. They then formulate the problem as a minimax optimization problem, where the decision maker tries to maximize their expected utility in the worst-case distribution. They show that the optimal decision rule can be computed efficiently using a convex program. They also show that if the predictor is decision calibrated, then the optimal decision rule is simply the best response to the predictor. They provide experimental results to support their theoretical findings.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

The paper is well-written and clearly explains the problem and the proposed solution. The authors provide a clear motivation for their work and a thorough discussion of the related literature. The theoretical results are interesting and provide a new perspective on the problem of decision-making under uncertainty. The experimental results provide strong evidence for the effectiveness of the proposed approach.

### Weaknesses

#### Some Related Works


#### comment

The paper assumes that the decision maker is risk-neutral and has a linear utility function. This may not be realistic in many applications. It would be interesting to see how the results generalize to other types of utility functions. The paper also assumes that the decision maker knows the set of possible conditional distributions. In practice, this set may be difficult to specify. It would be interesting to see how the results generalize to settings where the decision maker has only partial knowledge of the set of possible distributions. The paper also does not provide a detailed analysis of the computational complexity of the proposed approach. It would be interesting to see how the computational cost scales with the size of the action space and the number of possible conditional distributions.

### Suggestions

The assumption of a linear utility function is a significant limitation, as many real-world decision-making scenarios involve non-linear preferences. For example, a decision-maker might exhibit risk aversion, preferring a certain but smaller reward over a risky but potentially larger one. This could be modeled with a concave utility function. The current framework does not account for such preferences, and it would be valuable to explore how the proposed minimax approach could be adapted to handle non-linear utility functions. This might involve reformulating the optimization problem or using techniques from robust optimization that can handle non-linear objectives. Furthermore, the paper should discuss the implications of this assumption on the practical applicability of the results.

The assumption that the decision-maker has full knowledge of the set of possible conditional distributions is also a strong one. In practice, the decision-maker might only have access to a limited set of information about the possible distributions, or they might have to estimate the set from data. It would be beneficial to investigate how the proposed approach could be adapted to handle situations where the decision-maker has only partial or noisy information about the set of possible distributions. This could involve using techniques from robust statistics or Bayesian methods to model the uncertainty about the set of distributions. The paper should also discuss the sensitivity of the results to the choice of the set of possible distributions and provide guidance on how to choose this set in practice.

Finally, the paper lacks a detailed analysis of the computational complexity of the proposed approach. While the authors mention that the optimal decision rule can be computed efficiently using a convex program, they do not provide a precise analysis of how the computational cost scales with the size of the action space and the number of possible conditional distributions. This is important for assessing the practical feasibility of the approach in large-scale applications. The paper should provide a more detailed analysis of the computational complexity, including the dependence on the number of actions and the size of the set of possible distributions. It would also be helpful to discuss potential ways to improve the computational efficiency of the approach, such as using approximation algorithms or parallel computing techniques.

### Questions

1. How do the results generalize to other types of utility functions?
2. How do the results generalize to settings where the decision maker has only partial knowledge of the set of possible conditional distributions?
3. What is the computational complexity of the proposed approach?

### Rating

6

### Confidence

3

**********