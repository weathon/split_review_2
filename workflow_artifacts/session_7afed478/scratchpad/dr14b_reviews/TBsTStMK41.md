### Summary

This paper addresses the problem of desk-rejection in AI conferences due to per-author submission limits. The authors propose a novel optimization-based approach to minimize unnecessary desk rejections while adhering to submission limits. They model the desk-rejection process as a mathematical optimization problem and develop an efficient algorithm that significantly reduces needless rejections compared to current policies. The method is validated using 11 years of real-world ICLR submission data.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a new optimization framework for desk-rejection policies, offering a fresh perspective on a practical problem in conference management.
2. The proposed algorithm is computationally efficient, making it feasible for large-scale applications.
3. The authors provide a thorough theoretical analysis of their method, including proofs of correctness and time complexity.

### Weaknesses

#### Some Related Works


#### comment

1. The paper lacks empirical evaluation of the proposed method's impact on review quality or overall conference outcomes.
2. The method's effectiveness may depend on the accuracy of the authorship matrix A, which could be incomplete or inaccurate in practice.
3. The paper does not discuss potential ethical implications or biases that could arise from using an optimization-based desk-rejection system.

### Suggestions

The paper's primary weakness lies in its lack of empirical validation regarding the impact on review quality and overall conference outcomes. While the proposed optimization framework is theoretically sound and computationally efficient, the absence of real-world experiments makes it difficult to assess its practical value. Specifically, the authors should have considered conducting simulations or pilot studies using historical conference data to evaluate how their method affects the distribution of reviews per paper, the overall quality of accepted papers, and the diversity of accepted authors. For example, they could have compared the review workload distribution under their method versus the current ID-based system, analyzing metrics such as the number of reviews per paper, the variance in review scores, and the overall satisfaction of reviewers. Furthermore, they could have examined the impact on author diversity by tracking the acceptance rates of different demographic groups under both systems. Without such empirical validation, it remains unclear whether the proposed method truly improves the conference review process or merely shifts the burden in unforeseen ways.

Another significant concern is the reliance on the accuracy of the authorship matrix A. The paper assumes that this matrix is complete and accurate, but in practice, this may not always be the case. Authorship information can be incomplete or incorrect due to various reasons, such as errors in data entry, missing affiliations, or intentional misrepresentation. The authors should have discussed the potential impact of such inaccuracies on the performance of their method. For instance, if a significant number of authors are missing from the authorship matrix, the optimization algorithm might make suboptimal decisions, leading to either unnecessary desk rejections or the acceptance of low-quality papers. The authors could have explored methods to mitigate the impact of incomplete data, such as using probabilistic models or incorporating uncertainty into the optimization framework. Furthermore, they should have discussed the potential for manipulation of the system by authors who are not listed in the authorship matrix, as this could lead to unfair advantages.

Finally, the paper needs to address the potential ethical implications and biases that could arise from using an optimization-based desk-rejection system. While the authors claim that their method is neutral, the optimization process itself could inadvertently amplify existing biases in the submission data. For example, if certain groups of authors are systematically underrepresented in the submission data, the optimization algorithm might learn to deprioritize their submissions. The authors should have conducted a thorough analysis of potential biases and discussed how they could be mitigated. This could involve techniques such as fairness-aware optimization or post-processing adjustments to ensure that the system is equitable for all authors. Furthermore, they should have considered the potential for gaming the system, where authors might strategically modify their submissions to increase their chances of acceptance. A discussion of these ethical considerations is crucial for the responsible deployment of the proposed method.

### Questions

1. How does the proposed method affect the distribution of review workload among reviewers compared to current desk-rejection policies?
2. What measures are in place to prevent authors from gaming the system, such as by strategically adding or removing co-authors?
3. How does the algorithm handle edge cases, such as papers with a large number of authors or authors who are not listed in the authorship matrix?

### Rating

5

### Confidence

3

**********