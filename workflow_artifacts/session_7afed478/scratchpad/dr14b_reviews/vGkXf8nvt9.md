### Summary

This paper explores the use of unlearning as a method to improve domain specialization in LLMs. The authors propose a two-stage protocol called Forget-to-Focus (F2F), which first performs targeted unlearning on a "forget" set and then fine-tunes the model on a domain-specific dataset. The paper presents empirical evidence that F2F consistently outperforms standard fine-tuning across various domains and model sizes. The authors also provide a theoretical analysis of the unlearning process and its impact on the model's internal representations.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a novel approach to domain specialization by using unlearning as a preparatory step before fine-tuning. This is a creative application of unlearning, which is typically used for privacy purposes.
2. The paper provides a rigorous theoretical analysis of the unlearning process, including convergence analysis and representational geometry analysis. This adds depth to the empirical findings and provides a better understanding of the underlying mechanisms.
3. The paper demonstrates that F2F improves model calibration on medical QA tasks, reducing overconfidence and mitigating reliability issues that persist under standard fine-tuning. This is an important finding, as it highlights the potential of unlearning to improve the reliability of LLMs in sensitive domains.

### Weaknesses

#### Some Related Works


#### comment

1. The paper does not provide a detailed analysis of the computational overhead introduced by the unlearning phase. This is a significant concern, as the unlearning process could be computationally expensive, especially for large models. The authors should provide a breakdown of the time and resources required for the unlearning step, including the number of gradient updates and the memory footprint, and compare it to the computational cost of standard fine-tuning. This analysis should also consider the impact of different unlearning methods (GA, GA+GD, GA+KL, NPO) on the overall computational cost.
2. The paper lacks a thorough investigation into the sensitivity of the F2F protocol to the choice of hyperparameters, such as the learning rate and the number of unlearning steps. The authors should conduct a sensitivity analysis to determine how these hyperparameters affect the performance of the F2F protocol. This analysis should include a range of hyperparameter values and should report the performance of the model across different domains. It is important to understand how robust the F2F protocol is to variations in these hyperparameters, as this will affect its practical applicability.
3. The paper does not explore the potential negative impacts of unlearning on the model's general capabilities beyond the target domain. While the paper focuses on domain specialization, it is important to understand whether the unlearning process degrades the model's performance on general tasks. The authors should evaluate the model's performance on a set of general benchmarks after applying the F2F protocol to assess the extent of any negative impact. This analysis should include tasks that are not related to the target domain to provide a comprehensive view of the model's overall capabilities.

### Suggestions

To address the lack of computational overhead analysis, the authors should provide a detailed breakdown of the time and resources required for the unlearning phase. This should include the number of gradient updates, the memory footprint, and the wall-clock time for each unlearning method (GA, GA+GD, GA+KL, NPO). The authors should also compare the computational cost of the unlearning phase to the cost of standard fine-tuning, providing a clear understanding of the trade-offs involved. Furthermore, the authors should investigate how the size of the 'forget' set impacts the computational cost and the final performance of the model. This analysis should be presented in a way that allows practitioners to make informed decisions about the practical applicability of the F2F protocol, considering their computational constraints.

To address the sensitivity of the F2F protocol to hyperparameters, the authors should conduct a systematic sensitivity analysis. This should involve varying the learning rate and the number of unlearning steps across a range of values and reporting the performance of the model on different domains. The authors should present the results in a way that clearly shows how the performance of the F2F protocol changes with different hyperparameter settings. This analysis should also include a discussion of the optimal hyperparameter values for each domain and model size, providing practical guidance for users of the F2F protocol. The authors should also investigate the interaction between different hyperparameters and their combined effect on the performance of the model. This analysis will help to understand the robustness of the F2F protocol and its sensitivity to variations in hyperparameter settings.

To address the potential negative impacts of unlearning on general capabilities, the authors should evaluate the model's performance on a set of general benchmarks after applying the F2F protocol. This should include tasks that are not related to the target domain, such as common sense reasoning, reading comprehension, and other general language understanding tasks. The authors should compare the performance of the F2F model to the performance of the base model and the standard fine-tuned model on these benchmarks. This analysis should provide a comprehensive view of the model's overall capabilities and the extent to which the unlearning process degrades its general performance. The authors should also investigate whether the degradation in general capabilities is correlated with the degree of specialization achieved in the target domain. This analysis will help to understand the trade-offs between domain specialization and general capabilities.

### Questions

1. How does the computational overhead of the unlearning phase compare to the benefits in terms of performance gains? Are there any optimizations that can be applied to reduce the computational cost of unlearning?
2. How sensitive is the F2F protocol to the choice of hyperparameters, such as the learning rate and the number of unlearning steps? Are there any guidelines for selecting optimal hyperparameters for different domains and model sizes?
3. What is the impact of unlearning on the model's general capabilities beyond the target domain? Does the unlearning process degrade the model's performance on general tasks, and if so, how can this be mitigated?

### Rating

6

### Confidence

3

**********