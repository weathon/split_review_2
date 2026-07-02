### Summary

This paper proposes a method called SwiReasoning, which dynamically switches between explicit and latent reasoning modes to improve reasoning accuracy and token efficiency. The authors evaluate SwiReasoning on various benchmarks, including mathematical, STEM, coding, and general reasoning tasks. The results show that SwiReasoning outperforms baselines in terms of both accuracy and efficiency. The authors also provide insights into the benefits of combining explicit and latent reasoning modes and the importance of balancing exploration and exploitation in reasoning processes.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The idea of dynamically switching between explicit and latent reasoning modes is novel and interesting. The proposed method, SwiReasoning, improves the accuracy and token efficiency of reasoning language models.
2. The paper is well-written and easy to follow. The authors provide clear explanations of the proposed method and the experimental results.
3. The authors evaluate SwiReasoning on a wide range of benchmarks, including mathematical, STEM, coding, and general reasoning tasks. The results show that SwiReasoning consistently outperforms baselines in terms of both accuracy and efficiency.

### Weaknesses

#### Some Related Works


#### comment

1. The authors only evaluate SwiReasoning on Qwen models. It is unclear how well SwiReasoning would perform on other model architectures and scales. Specifically, the interaction between the proposed switching mechanism and different attention mechanisms or layer normalization strategies across various architectures remains unexplored. This limits the generalizability of the findings.
2. The authors do not provide a detailed analysis of the computational overhead of SwiReasoning. It is important to understand the trade-offs between performance gains and computational costs, especially when deploying SwiReasoning on resource-constrained devices. The paper lacks a breakdown of the additional computational costs associated with the switching mechanism, such as the entropy calculation and the mode transition logic, which could be significant depending on the implementation.

### Suggestions

To strengthen the paper, the authors should evaluate SwiReasoning on a more diverse set of model architectures, including models with different attention mechanisms (e.g., sparse attention, linear attention) and layer normalization techniques. This would provide a more comprehensive understanding of the method's robustness and generalizability. For example, experiments could be conducted on models like the Llama family, which employs a different attention mechanism than the Qwen models, or on models with different layer normalization strategies. Furthermore, it would be beneficial to analyze the performance of SwiReasoning across various model scales within the same architecture to understand how the method scales with model size. This would involve testing on models with different numbers of parameters, which could reveal potential limitations or bottlenecks of the proposed approach.

In addition to architectural diversity, a detailed analysis of the computational overhead is crucial. The authors should provide a breakdown of the computational costs associated with each component of SwiReasoning, including the entropy calculation, the mode transition logic, and any additional operations required for switching between explicit and latent reasoning modes. This analysis should include both time and memory costs, and should be compared to the computational costs of the baseline methods. It would also be beneficial to analyze the computational overhead as a function of the input sequence length and the number of reasoning steps, as this could reveal potential scalability issues. The authors should also consider the impact of these overheads on different hardware platforms, such as GPUs and CPUs, to provide a more complete picture of the method's practical applicability.

Finally, the authors should investigate the sensitivity of SwiReasoning to its hyperparameters, such as the switch count control threshold and the entropy trend window size. A thorough sensitivity analysis would help to understand how these parameters affect the performance of the method and how to tune them for different tasks and datasets. This analysis should include a systematic exploration of the parameter space, and should provide clear guidelines for selecting appropriate parameter values. The authors could also consider using adaptive parameter tuning techniques to automatically adjust the hyperparameters based on the characteristics of the input data or the specific task at hand. This would make the method more robust and easier to use in practice.

### Questions

1. How does SwiReasoning perform on other model architectures and scales?
2. What is the computational overhead of SwiReasoning, and how does it compare to the computational overhead of baselines?
3. How sensitive is SwiReasoning to hyperparameters, such as the switch count control threshold and the entropy trend window size?

### Rating

6

### Confidence

3

**********