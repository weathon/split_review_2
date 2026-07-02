### Summary

This paper proposes a novel method called Prompt-Invariant CCA Certificates (PI-CCA) for continual learning in vision-language models (VLMs) without replaying past data. The key idea is to preserve the cross-modal alignment geometry by summarizing it in a compact "CCA certificate" that captures the top-k canonical correlations and subspaces. This certificate is used to constrain alignment during training on new tasks, ensuring that the model retains its zero-shot capabilities and prompt robustness. The method also incorporates prompt invariance by averaging over prompt perturbations. The authors demonstrate the effectiveness of PI-CCA across several benchmarks, achieving state-of-the-art results among replay-free methods.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper presents a novel perspective on continual learning in VLMs by focusing on preserving the geometry of cross-modal alignment, which is a unique approach compared to existing methods that rely on proxy signals.
2. The introduction of the CCA certificate is a creative way to summarize and maintain the essential alignment information without storing past data, addressing memory constraints in continual learning.
3. The method is evaluated across multiple benchmarks and shows superior performance compared to other replay-free methods, demonstrating its effectiveness in preserving zero-shot capabilities and resilience to prompt variations.

### Weaknesses

#### Some Related Works


#### comment

1. The paper could benefit from a more thorough comparison with existing methods that also aim to preserve cross-modal alignment, to better highlight the unique advantages of PI-CCA.
2. While the method is shown to be effective across several benchmarks, it would be helpful to see an analysis of its performance on a wider range of tasks and datasets to assess its generalizability.
3. The reliance on canonical correlations and subspaces might be a limitation in scenarios where the underlying data structure is not well-represented by these measures.
4. The method introduces several hyperparameters (e.g., k, h, λ1, λ2, λ3, α, β, η, M), which might require careful tuning for different tasks and datasets, potentially limiting its ease of use.
5. The paper does not provide a detailed analysis of the computational complexity of PI-CCA, especially concerning the SVD and sketching operations, which could be a concern for large-scale applications.

### Suggestions

The paper would be strengthened by a more detailed comparison to existing methods that also aim to preserve cross-modal alignment. While the authors mention related work, a more in-depth analysis of how PI-CCA differs in its approach and performance would be beneficial. Specifically, the paper should include a discussion of the trade-offs between PI-CCA and methods that use replay buffers or knowledge distillation, highlighting the advantages and disadvantages of each approach in terms of memory usage, computational cost, and performance. A more thorough comparison would help to better position PI-CCA within the existing literature and clarify its unique contributions.

Furthermore, the paper should include a more comprehensive analysis of the method's performance across a wider range of tasks and datasets. While the current evaluation demonstrates the effectiveness of PI-CCA on several benchmarks, it would be helpful to see how the method performs on more diverse and challenging datasets. This would help to assess the generalizability of the approach and identify potential limitations. For example, it would be useful to evaluate the method on datasets with different types of image and text modalities, as well as datasets with varying levels of noise and complexity. Additionally, the paper should include an analysis of the method's performance on tasks that require more complex reasoning and understanding of the relationships between modalities.

Finally, the paper should provide a more detailed analysis of the computational complexity of PI-CCA, especially concerning the SVD and sketching operations. The current analysis is insufficient to fully understand the computational cost of the method, particularly for large-scale applications. The paper should include a breakdown of the time and memory requirements for each step of the algorithm, as well as a comparison to other methods. This analysis should also consider the impact of different hyperparameter settings on the computational cost. Furthermore, the paper should discuss potential strategies for optimizing the implementation of PI-CCA to reduce its computational overhead.

### Questions

1. How does the performance of PI-CCA compare to methods that use replay or synthetic data generation for continual learning in VLMs?
2. Can the authors provide more insights into the choice of hyperparameters for PI-CCA, and how sensitive the performance is to these settings?
3. How does the prompt invariance mechanism in PI-CCA compare to other methods for improving prompt robustness in VLMs?
4. What are the computational requirements of PI-CCA, especially concerning the SVD and sketching operations, and how does it scale with the size of the dataset and model?
5. Are there any scenarios or types of tasks where PI-CCA might not be the most suitable approach for continual learning in VLMs?

### Rating

6

### Confidence

3

**********