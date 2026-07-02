### Summary

This paper examines sparse recovery in a heterogeneous noise setting, where measurements come from sources with varying noise levels. Specifically, the authors establish sample size requirements for both information-theoretic and algorithmic recovery, introducing the "Price of Quality" to describe the trade-off between high- and low-quality samples. They analyze the LASSO in the agnostic setting and find that its recovery threshold is independent of individual noise levels, depending only on the average noise level. These results provide the first conditions for sparse recovery with mixed-quality data, highlighting key differences between information-theoretic and algorithmic thresholds in adapting to data quality variations.

### Soundness

3

### Presentation

3

### Contribution

2

### Strengths

- The paper is well-written and easy to follow.
- The problem is well-motivated, and the authors provide a thorough review of existing work.
- The authors offer a comprehensive analysis of the "Price of Quality" in both agnostic and informed settings, which is interesting and novel.

### Weaknesses

#### Some Related Works


#### comment

 - The authors should discuss the practical implications of this work. While the setting is interesting and novel, it is unclear how it applies to real-world applications. Providing examples of where this model could be useful would enhance the paper’s relevance.

- The paper could benefit from exploring alternative algorithms beyond LASSO for this specific setting. While LASSO is a popular choice, other methods, such as those employing weighted $\ell_2$ loss to account for varying noise levels, might be more suitable. A comparison of these algorithms would add value.

- The assumption of binary signals ($\beta^* \in \{0, 1\}^p$) is quite restrictive. In practice, signals often take real values, and this binary constraint may limit the model’s applicability. Expanding the analysis to real-valued signals would make the results more broadly relevant.

### Suggestions

The paper would significantly benefit from a more thorough discussion of its practical applications. While the theoretical analysis is sound, the current presentation leaves the reader wondering about the real-world scenarios where this model would be relevant. For instance, the authors could explore how their framework applies to problems in sensor networks, where some sensors might have higher precision than others, or in crowdsourcing settings, where data from different contributors might have varying levels of quality. Providing concrete examples, even if simplified, would help to bridge the gap between the theoretical results and practical utility. Furthermore, a discussion of the limitations of the model in specific applications would also be valuable. For example, how would the model perform if the noise distributions are not precisely Gaussian, or if the noise levels are not known a priori? Addressing these questions would greatly enhance the paper's impact.

Expanding the analysis beyond the LASSO algorithm is crucial for a more comprehensive understanding of the problem. While LASSO is a widely used method, it may not be optimal in the presence of heterogeneous noise. The authors should consider exploring algorithms that explicitly account for the varying noise levels, such as weighted $\ell_2$ loss methods, where the weights are inversely proportional to the noise variances. A comparative analysis of these algorithms, both theoretically and empirically, would provide valuable insights into the performance trade-offs. Specifically, it would be interesting to see how the performance of LASSO compares to these alternative methods in terms of recovery accuracy and robustness to noise. Furthermore, the authors could investigate whether there are specific conditions under which LASSO is guaranteed to perform optimally, or if there are other algorithms that are more robust to variations in noise levels. This would provide a more nuanced understanding of the algorithmic aspects of the problem.

Finally, the assumption of binary signals is a significant limitation that needs to be addressed. While this assumption simplifies the analysis, it greatly restricts the applicability of the results. In many real-world scenarios, signals can take any real value, and the binary constraint is not realistic. The authors should explore how their results can be extended to the case of real-valued signals. This would likely require a more sophisticated analysis, but it would significantly broaden the scope of the paper. One possible approach would be to consider a more general signal model where the non-zero entries of the signal are drawn from a distribution over the real numbers. This would allow the authors to analyze the performance of their methods in a more realistic setting. Furthermore, it would be interesting to investigate whether the "Price of Quality" concept still holds in the real-valued signal setting, and if so, how it is affected by the distribution of the signal values.

### Questions

Please refer to the weaknesses.

### Rating

5

### Confidence

4

**********