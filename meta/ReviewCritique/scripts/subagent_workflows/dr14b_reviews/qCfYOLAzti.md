### Summary

The paper addresses the issue of spurious unlearning in LLM unlearning, where models may still generate semantically related variants of target responses even after unlearning. The authors propose a bootstrapping framework that incorporates model beliefs into the unlearning objective to mitigate this issue. The framework is instantiated at both the token level (BS-T) and the sequence level (BS-S), and it is shown to outperform state-of-the-art baselines in terms of achieving a better balance between forgetting and retention.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a novel bootstrapping framework for LLM unlearning that effectively mitigates the squeezing effect and spurious unlearning.
2. The paper provides a comprehensive analysis of the limitations of existing unlearning methods and introduces a new evaluation metric (LLaJ) that aligns more closely with human judgment.
3. The paper includes extensive experiments on diverse benchmarks and model families, demonstrating the effectiveness of the proposed bootstrapping framework.
4. The paper provides a theoretical analysis of how the bootstrapping framework reshapes gradient dynamics and mitigates the squeezing effect.

### Weaknesses

#### Some Related Works


#### comment

1. The paper could benefit from a more detailed discussion of the computational overhead introduced by the bootstrapping framework, particularly BS-S, which involves sampling and augmenting unlearning data. The analysis should include a breakdown of the time complexity associated with each step of the algorithm, such as the sampling process, the calculation of token-level and sequence-level probabilities, and the actual unlearning updates. Furthermore, the paper should explore the scalability of the proposed method when dealing with large-scale unlearning tasks, including the memory requirements and the potential for parallelization.
2. The paper primarily focuses on the TOFU benchmark, and while it includes results on MUSE and WMDP, a broader range of datasets and unlearning scenarios could further strengthen the empirical validation of the proposed method. Specifically, the paper should consider datasets that involve different types of knowledge unlearning, such as factual knowledge, stylistic patterns, or specific behaviors. This would help to demonstrate the generalizability of the proposed method across diverse unlearning tasks.
3. The paper could explore the impact of different hyperparameters, such as the interpolation parameter λBST and the top-k parameter k, on the performance of BS-T and BS-S across various datasets and models. A more detailed analysis of the sensitivity of the method to these hyperparameters is needed, including a discussion of how these parameters should be tuned for different unlearning tasks. The paper should also investigate the interaction between these hyperparameters and their impact on the trade-off between forgetting and retention.
4. The paper could provide more insights into the practical implications of the proposed method, such as its applicability to real-world unlearning tasks and its robustness to adversarial attacks. The paper should discuss the potential challenges of deploying the proposed method in real-world scenarios, such as the need for efficient data sampling and the potential for unintended consequences of unlearning.

### Suggestions

To address the computational overhead concerns, the authors should provide a detailed analysis of the time and space complexity of both BS-T and BS-S. This analysis should include a breakdown of the computational cost associated with each step of the algorithm, such as the sampling process, the calculation of token-level and sequence-level probabilities, and the actual unlearning updates. Furthermore, the authors should explore techniques to reduce the computational cost of BS-S, such as using more efficient sampling methods or approximating the sequence-level probabilities. The paper should also discuss the scalability of the proposed method when dealing with large-scale unlearning tasks, including the memory requirements and the potential for parallelization. It would be beneficial to include a comparison of the computational cost of the proposed method with existing unlearning techniques, highlighting the trade-offs between performance and computational efficiency.

To strengthen the empirical validation, the authors should include experiments on a broader range of datasets and unlearning scenarios. This should include datasets that involve different types of knowledge unlearning, such as factual knowledge, stylistic patterns, or specific behaviors. For example, the authors could consider datasets that require unlearning of specific factual information, such as dates or names, or datasets that require unlearning of stylistic patterns, such as writing style or tone. This would help to demonstrate the generalizability of the proposed method across diverse unlearning tasks. Additionally, the authors should explore the performance of the proposed method under different unlearning scenarios, such as unlearning a small amount of data versus unlearning a large amount of data, or unlearning data that is highly correlated versus unlearning data that is less correlated. This would provide a more comprehensive understanding of the strengths and limitations of the proposed method.

Finally, the authors should provide a more detailed analysis of the impact of different hyperparameters on the performance of BS-T and BS-S. This analysis should include a discussion of how these parameters should be tuned for different unlearning tasks, as well as a discussion of the interaction between these hyperparameters and their impact on the trade-off between forgetting and retention. The authors should also explore the sensitivity of the method to these hyperparameters, including a discussion of how the performance of the method changes when these parameters are varied. Furthermore, the authors should provide practical guidelines for selecting appropriate values for these hyperparameters, based on the characteristics of the unlearning task and the available computational resources. The paper should also investigate the robustness of the proposed method to adversarial attacks, and discuss the potential challenges of deploying the proposed method in real-world scenarios.

### Questions

1. Could the authors provide a more detailed analysis of the computational overhead introduced by the BS framework, particularly BS-S, and discuss its scalability for large-scale unlearning tasks?
2. How do the interpolation parameter λBST and the top-k parameter k affect the performance of BS-T and BS-S across different datasets and models? Could the authors provide guidelines for selecting appropriate values for these hyperparameters?
3. How does the proposed BS framework perform on other commonly used unlearning benchmarks, such as the MUSE dataset (-News and -Books splits)? Are there any specific challenges or advantages when applying BS to these datasets?
4. Could the authors elaborate on the practical implications of the BS framework, such as its applicability to real-world unlearning tasks and its robustness to adversarial attacks?

### Rating

6

### Confidence

3

**********