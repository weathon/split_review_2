### Summary

This paper builds on the work of Wu and Hartline (2024) by optimizing their scoring rules to better align with human preferences. The authors introduce a new scoring rule, ASR, and demonstrate its superior performance in aligning with human preferences compared to previous methods, while maintaining properness.

### Soundness

3

### Presentation

2

### Contribution

3

### Strengths

1. The authors provide a thorough theoretical analysis of their ASR, including proofs of properness and convexity of the optimization problem. This adds credibility to their approach.

2. The experimental results are comprehensive, comparing ASR with multiple baselines on real-world datasets. The use of multiple metrics (MSE, Pearson correlation, Spearman rank correlation) provides a robust evaluation.

### Weaknesses

#### Some Related Works


#### comment

1. The authors assume that the agent's posterior belief distribution is either 0, 1, or the prior. This assumption may be too strong and unrealistic in practice. It is unclear how the method would perform if the agent's posterior beliefs are more nuanced. The paper lacks a discussion on the sensitivity of the results to this assumption, and it's not clear if the method would still be effective with more realistic belief distributions.

2. The authors only evaluate their method on a single dataset. This limits the generalizability of their findings. It is not clear if the performance gains observed would hold across different datasets and domains. The paper should include experiments on diverse datasets to demonstrate the robustness of the proposed method.

3. The paper lacks a detailed analysis of the computational complexity of the proposed method. This is important for practical applications, especially when dealing with large datasets. The paper should provide a clear analysis of the time and space complexity of the ASR, and discuss how it scales with the size of the dataset and the number of summary points.

### Suggestions

The paper should include a more thorough analysis of the assumption that the agent's posterior belief distribution is either 0, 1, or the prior. This assumption is quite restrictive and may not hold in many real-world scenarios. The authors should explore the impact of relaxing this assumption and consider how the method would perform with more nuanced posterior beliefs. For example, they could simulate scenarios where the posterior beliefs are distributed across a range of values, and analyze how this affects the performance of the ASR. A sensitivity analysis would be beneficial to understand the robustness of the method to deviations from this assumption. Furthermore, the authors should discuss the potential limitations of their method when this assumption is violated and suggest possible ways to address these limitations.

To address the limited generalizability of the findings, the authors should conduct experiments on multiple datasets from different domains. This would provide a more comprehensive evaluation of the proposed method and demonstrate its robustness across different settings. The datasets should vary in terms of the size, the nature of the text, and the task at hand. For example, the authors could consider datasets from different areas of peer grading, or even datasets from other domains where text summarization is used. This would help to establish the general applicability of the ASR and provide a more convincing argument for its effectiveness. The paper should also include a discussion of the specific characteristics of each dataset and how they might influence the performance of the method.

Finally, the paper should include a detailed analysis of the computational complexity of the proposed method. This analysis should include both time and space complexity, and should discuss how the complexity scales with the size of the dataset and the number of summary points. The authors should also provide empirical results on the running time of the method on different datasets. This information is crucial for practitioners who want to use the method in real-world applications. The paper should also discuss the potential bottlenecks of the method and suggest possible ways to improve its efficiency. A clear understanding of the computational complexity is essential for assessing the practical feasibility of the proposed method.

### Questions

1. How sensitive is the performance of ASR to the choice of hyperparameters? Can you provide a sensitivity analysis?

2. Have you explored the possibility of using more expressive models for the scoring rule? What are the potential benefits and drawbacks?

3. How does your method perform when the quality of the LLM-generated summary points is poor? Have you conducted any robustness checks?

### Rating

6

### Confidence

3

**********