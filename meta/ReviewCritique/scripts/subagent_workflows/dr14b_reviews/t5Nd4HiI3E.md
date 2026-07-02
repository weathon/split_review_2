### Summary

This paper proposes a novel method called Bias-Variance Optimized Preference Optimization (BVPO) for aligning Large Reasoning Models (LRMs) with human preferences. The key idea is to combine two gradient estimators: a high-variance trace-based estimator and a low-variance empty-trace estimator. The authors provide theoretical analysis showing that BVPO reduces trace-induced variance and derive a closed-form choice of the mixing weight that minimizes mean-squared error. Empirical results demonstrate that BVPO improves alignment performance on AlpacaEval 2 and Arena-Hard, and also boosts reasoning performance on math reasoning benchmarks.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a novel approach to preference optimization by explicitly addressing the bias-variance trade-off, which is a significant contribution to the field of aligning Large Reasoning Models (LRMs).
2. The theoretical analysis is thorough and well-supported, providing a strong foundation for the proposed method. The proofs for variance reduction, MSE optimality, and convergence guarantees are rigorous and add credibility to the approach.
3. The empirical results are compelling, showing consistent improvements over baselines across multiple benchmarks and model sizes. The gains in both alignment and reasoning performance highlight the practical effectiveness of BVPO.

### Weaknesses

#### Some Related Works


#### comment

1. The paper lacks a detailed discussion on the computational overhead introduced by BVPO compared to standard DPO. While the authors mention that the additional computation is minimal, a more thorough analysis of the time and memory costs would be beneficial. Specifically, the paper should quantify the increase in forward and backward passes required by BVPO, and how this scales with model size and sequence length. Furthermore, the memory footprint of storing and processing both the trace-based and empty-trace gradients should be analyzed, especially for large models.
2. The choice of the mixing coefficient α is crucial for the performance of BVPO, but the paper does not provide sufficient guidance on how to select this parameter in practice. While the authors derive a closed-form solution for the optimal α, it would be helpful to discuss the sensitivity of the method to deviations from this optimal value. Additionally, the paper should explore adaptive strategies for α, such as annealing or learning the coefficient during training, and provide empirical evidence of their effectiveness. The current discussion lacks practical guidance on how to implement and tune this parameter in real-world scenarios.
3. The paper primarily focuses on math reasoning tasks, but it would be valuable to see how BVPO performs on other types of reasoning tasks or in different domains. The current evaluation is limited to a specific type of reasoning, and it is unclear whether the benefits of BVPO would generalize to other tasks such as commonsense reasoning, code generation, or question answering. A more comprehensive evaluation across diverse tasks would strengthen the paper's claims about the general applicability of the method.

### Suggestions

To address the lack of detailed computational analysis, the authors should include a comprehensive breakdown of the time and memory costs associated with BVPO. This should include a comparison of the number of forward and backward passes required by BVPO versus standard DPO, as well as an analysis of the memory footprint for storing and processing the gradients. The analysis should consider how these costs scale with model size, sequence length, and batch size. Furthermore, the authors should provide empirical measurements of the training time and memory usage for both BVPO and DPO on different hardware configurations. This would provide a more concrete understanding of the practical overhead introduced by BVPO and help practitioners make informed decisions about its applicability. For example, providing a table that shows the training time per epoch for both methods across different model sizes and batch sizes would be very useful.

Regarding the mixing coefficient α, the authors should provide more practical guidance on its selection and tuning. While the closed-form solution for the optimal α is a valuable theoretical contribution, the paper should discuss the sensitivity of the method to deviations from this optimal value. The authors should conduct experiments to evaluate the performance of BVPO with different values of α and provide a sensitivity analysis. Additionally, the paper should explore adaptive strategies for α, such as annealing or learning the coefficient during training, and provide empirical evidence of their effectiveness. The authors should also discuss the potential trade-offs between the variance reduction achieved by BVPO and the potential bias introduced by the empty-trace gradient, and how the choice of α affects this trade-off. This would provide a more practical and robust approach to using BVPO in real-world scenarios. For instance, a plot showing the performance of BVPO with different values of α, along with a discussion of the optimal range, would be beneficial.

To broaden the evaluation of BVPO, the authors should include experiments on a wider range of reasoning tasks and domains. This should include tasks such as commonsense reasoning, code generation, and question answering, in addition to math reasoning. The authors should also consider evaluating BVPO on tasks that require different types of reasoning, such as inductive, deductive, and abductive reasoning. This would provide a more comprehensive understanding of the generalizability of BVPO and its effectiveness across different tasks. Furthermore, the authors should analyze the performance of BVPO on tasks with varying levels of complexity and data availability, to understand its limitations and potential areas for improvement. This would strengthen the paper's claims about the broad applicability of BVPO and its potential impact on the field. For example, including results on a benchmark like BigBench, which covers a diverse set of reasoning tasks, would be a valuable addition.

### Questions

1. Could you provide more details on the computational overhead of BVPO compared to standard DPO? How does the additional computation of the empty-trace gradient affect the overall training time?
2. How does the choice of the mixing coefficient α affect the performance of BVPO in practice? Is there a principled way to choose this coefficient, or does it require extensive tuning?
3. How does BVPO perform on other types of reasoning tasks or in different domains? Is the improvement in alignment and reasoning ability consistent across different tasks?

### Rating

6

### Confidence

3

**********