### Summary

This paper proposes an extension of RoPE, RoPE++, that re-incorporates the discarded imaginary component of the complex-valued dot product. The authors demonstrate that the imaginary component contains valuable phase information that is crucial for modeling long-context dependencies. RoPE++ leverages the full complex-valued representation to create a dual-component attention score, enhancing the modeling of long-context dependencies. The paper provides theoretical and empirical evidence to support the effectiveness of RoPE++. Evaluations on a suite of long-context language modeling benchmarks show that RoPE++ consistently improves performance over the standard RoPE, with the benefits becoming more significant as context length increases.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper identifies a previously overlooked limitation in standard RoPE and proposes a novel solution by re-incorporating the imaginary component of the complex-valued dot product. This approach is well-motivated and theoretically grounded.
2. The introduction of RoPE++<sub>EH</sub> and RoPE++<sub>EC</sub> provides flexibility in balancing performance and efficiency, making the method applicable in various scenarios.
3. The paper includes a comprehensive suite of experiments on both short- and long-context benchmarks, demonstrating the effectiveness of RoPE++ across different model sizes and tasks. The results show consistent improvements over standard RoPE, particularly in long-context scenarios.
4. The analysis of attention patterns provides valuable insights into how the imaginary component contributes to capturing long-range dependencies, supporting the theoretical claims with empirical evidence.

### Weaknesses

#### Some Related Works


#### comment

1. The paper lacks a detailed analysis of the computational overhead introduced by RoPE++. While the authors mention efficiency gains in terms of memory, a thorough breakdown of the computational cost, including FLOPs and latency, would be valuable. The analysis should include a comparison of the computational cost of RoPE++ with standard RoPE, not just in terms of overall training time, but also in terms of the cost of the attention mechanism itself. This should include a breakdown of the operations involved in both the real and imaginary components of the attention calculation, and how these contribute to the overall computational cost.
2. The paper could benefit from a more in-depth discussion of the limitations of RoPE++. For instance, are there specific types of long-context tasks where RoPE++ might not offer significant improvements? The paper should explore scenarios where the benefits of RoPE++ are marginal or non-existent, and discuss the potential reasons for this. This could include tasks with specific types of dependencies or data distributions where the imaginary component does not provide additional useful information.
3. The paper primarily focuses on the imaginary component's role in long-context modeling. However, a more detailed exploration of how the real and imaginary components interact and complement each other would be beneficial. The paper should provide a more granular analysis of the attention patterns, showing how the real and imaginary components attend to different parts of the input sequence, and how this contributes to the overall performance. This could include visualizations of attention weights for both components, and a discussion of how these patterns change with different input sequences and tasks.

### Suggestions

To address the lack of detailed computational analysis, the authors should include a breakdown of the FLOPs and latency introduced by RoPE++. This should involve a comparison of the computational cost of the attention mechanism in RoPE++ versus standard RoPE, detailing the operations involved in both the real and imaginary components. Specifically, the analysis should quantify the additional multiplications and additions required for the imaginary component, and how these scale with sequence length and model size. Furthermore, the authors should provide a more detailed analysis of the memory access patterns, as this can be a significant factor in overall computational cost. This analysis should be presented in a way that allows for a clear comparison of the computational efficiency of RoPE++ with standard RoPE, and should include both training and inference scenarios.

To further explore the limitations of RoPE++, the authors should conduct experiments on a wider range of long-context tasks, including those where RoPE++ might not offer significant improvements. This should include tasks with different types of dependencies and data distributions, to identify scenarios where the imaginary component does not provide additional useful information. The authors should also analyze the performance of RoPE++ on tasks with varying context lengths, to determine if there is a point where the benefits of the imaginary component diminish. This analysis should include a discussion of the potential reasons for the observed performance, such as the nature of the dependencies in the task, or the limitations of the model architecture. This would provide a more complete understanding of the applicability of RoPE++ and its limitations.

To enhance the understanding of the interaction between the real and imaginary components, the authors should provide a more granular analysis of the attention patterns. This should include visualizations of the attention weights for both components, showing how they attend to different parts of the input sequence. The authors should also analyze how these patterns change with different input sequences and tasks, and how this contributes to the overall performance. This analysis should also include a discussion of the semantic differences between the real and imaginary components, and how these differences contribute to the model's ability to capture long-range dependencies. This could involve analyzing the types of relationships that each component attends to, and how these relationships contribute to the overall performance.

### Questions

1. How does the performance of RoPE++ scale with even larger model sizes (e.g., billions of parameters)? Are there any architectural modifications needed to maintain the benefits of RoPE++ at such scales?
2. The paper mentions that the imaginary component helps capture long-range dependencies. Could the authors provide more insights into the specific types of dependencies that the imaginary component is better at capturing compared to the real component?
3. How sensitive is RoPE++ to the choice of hyperparameters, such as the scaling factor for the imaginary component? Are there any guidelines for tuning these parameters for optimal performance?
4. The paper focuses on text-based long-context tasks. How does RoPE++ perform on other types of sequential data, such as code or multimodal data?

### Rating

6

### Confidence

3

**********