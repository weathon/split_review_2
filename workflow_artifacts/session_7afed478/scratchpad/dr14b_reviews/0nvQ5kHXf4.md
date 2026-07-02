### Summary

This paper introduces a method called Weight-Activation Subspace Iteration (WASI) to reduce memory usage and computational cost in transformer models. WASI leverages the idea that a model’s essential information lies in a fixed subspace, allowing for efficient training and inference. The method is particularly useful for on-device learning, addressing concerns about energy consumption and data privacy. The authors demonstrate that WASI achieves comparable accuracy to traditional training while significantly reducing memory and computational costs. The method is tested on various models, including ViT, SwinT, and TinyLlama, showing promising results in resource-constrained environments.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper is well-organized, with clear explanations of the motivation, methodology, and experimental results. The figures and tables are informative and support the claims made in the text.
2. The authors provide a thorough analysis of the method's performance, including comparisons with existing techniques and detailed evaluations of memory and computational efficiency.
3. The proposed method has practical implications for deploying transformer models on edge devices, which is a growing area of interest in the field of AI.

### Weaknesses

#### Some Related Works


#### comment

1. The paper could benefit from a more detailed discussion of the limitations of the proposed method, particularly in scenarios where the assumption of a stable subspace may not hold. Specifically, the paper does not address how the method would perform if the optimal subspace shifts significantly during training or if the data distribution changes, which could lead to a degradation in performance. A more rigorous analysis of the sensitivity of the method to these factors is needed.
2. The experiments are primarily focused on image classification tasks. It would be valuable to see how the method performs on other types of data and tasks, such as natural language processing or time-series analysis, to demonstrate its generalizability. The current evaluation does not explore the method's performance on tasks with different input modalities or sequence lengths, which could reveal potential limitations or areas for improvement.
3. The paper does not provide a detailed analysis of the computational overhead introduced by the WASI method itself. While the method aims to reduce computational costs, the overhead of the subspace iteration process should be quantified and compared to the savings achieved. This analysis should include the time and memory costs associated with the subspace identification and update steps, particularly in the context of on-device learning where resources are constrained.

### Suggestions

To address the limitations regarding the stability of the subspace, the authors should include experiments that explicitly test the method's robustness to shifts in the optimal subspace. This could involve introducing controlled perturbations to the data distribution or the model parameters during training and observing how the method adapts. For example, the authors could simulate a scenario where the model is initially trained on one dataset and then fine-tuned on a different, but related, dataset. This would help to understand how well the method can maintain performance when the underlying data distribution changes. Furthermore, the authors should provide a theoretical analysis of the conditions under which the subspace is expected to remain stable and discuss the potential impact of deviations from these conditions. This would provide a more complete understanding of the method's applicability and limitations.

To broaden the scope of the evaluation, the authors should include experiments on a wider range of tasks and data types. Specifically, they should evaluate the method on natural language processing tasks, such as text classification or machine translation, and on time-series analysis tasks, such as anomaly detection or forecasting. This would demonstrate the method's generalizability and identify any task-specific challenges. For NLP tasks, the authors should consider using different sequence lengths and vocabulary sizes to assess the method's scalability. For time-series analysis, the authors should explore different types of time-series data, such as stationary and non-stationary data, to understand the method's performance under various conditions. These additional experiments would provide a more comprehensive evaluation of the method's capabilities.

Finally, the authors should provide a detailed analysis of the computational overhead introduced by the WASI method. This analysis should include a breakdown of the time and memory costs associated with each step of the subspace iteration process, such as the SVD computation and the weight update. The authors should compare these costs to the savings achieved in terms of reduced memory usage and computational cost. This analysis should be performed for different model sizes and hardware configurations to understand how the overhead scales with the problem size. Furthermore, the authors should discuss the potential for optimizing the subspace iteration process to reduce its overhead. This would provide a more complete picture of the method's practical implications and help to identify areas for further improvement.

### Questions

1. How does the method perform when the assumption of a stable subspace does not hold? Are there any mechanisms in place to adapt to changes in the subspace during training?
2. Can the method be extended to other types of neural network architectures beyond transformers? If so, what modifications would be necessary?
3. What are the potential implications of the method for real-world applications, particularly in scenarios where energy consumption and data privacy are critical concerns?

### Rating

6

### Confidence

3

**********