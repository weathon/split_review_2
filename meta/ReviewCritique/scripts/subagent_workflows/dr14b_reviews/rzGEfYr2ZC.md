### Summary

This paper introduces SparseFW, a novel method for pruning large language models (LLMs) that leverages the Frank-Wolfe (FW) algorithm. Unlike traditional greedy pruning approaches, SparseFW employs a convex relaxation of the combinatorial constraints and solves the resulting problem using the FW algorithm. This approach allows for more effective pruning by accounting for weight interactions, leading to significant improvements in performance over existing methods like Wanda and RIA. SparseFW demonstrates consistent gains in perplexity and zero-shot accuracy across various GPT architectures, including Qwen 2.5, LLaMA 3, Yi 1.5, and Gemma 2. The method is memory-efficient, scalable, and adaptable to both unstructured and semi-structured sparsity patterns.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. **Theoretical Justification**: The paper provides strong theoretical guarantees for the proposed method, connecting the relaxed solution to an approximate solution of the original combinatorial problem.
2. **Empirical Performance**: SparseFW outperforms state-of-the-art methods in terms of perplexity and zero-shot accuracy, demonstrating its effectiveness in reducing pruning error.
3. **Memory Efficiency**: The method is designed to be memory-efficient, making it suitable for large-scale models.
4. **Scalability**: SparseFW scales well to large models and can handle both unstructured and semi-structured sparsity patterns.
5. **Novelty**: The use of the Frank-Wolfe algorithm for LLM pruning is a novel contribution, offering a new perspective on the problem.

### Weaknesses

#### Some Related Works


#### comment

1. **Greedy Heuristics**: The paper mentions that greedy heuristics ignore weight interactions, but it does not provide a detailed comparison of how SparseFW's performance changes when weight interactions are explicitly considered. It would be beneficial to see a quantitative analysis of the impact of these interactions on the final pruning performance. For example, the authors could analyze the correlation between the importance scores of weights and their neighbors, and how this correlation is captured by SparseFW but missed by greedy methods.
2. **Warm-Start Requirement**: The method requires a warm-start mask, which is obtained from existing methods like Wanda. The performance of SparseFW seems to depend on the quality of this warm-start mask. A more detailed analysis of the sensitivity of SparseFW to the warm-start mask would be beneficial. Specifically, it would be useful to see how the performance varies with different warm-start masks, and whether there are specific characteristics of the warm-start mask that are crucial for achieving good performance. The authors should also explore the possibility of using a suboptimal warm-start mask and how it affects the convergence of the Frank-Wolfe algorithm.
3. **Computational Cost**: While the paper claims that SparseFW is memory-efficient, it does not provide a detailed comparison of the computational cost with existing methods. A more thorough analysis of the time complexity and practical runtime would be helpful. This should include a breakdown of the time spent on each step of the algorithm, such as the gradient computation, the Frank-Wolfe update, and the thresholding operation. It would also be useful to compare the wall-clock time of SparseFW with other methods on the same hardware.
4. **Ablation Studies**: The paper lacks detailed ablation studies on the impact of different parameters, such as the number of iterations and the sparsity level. Such studies would provide more insights into the behavior of the method. For example, the authors could analyze how the performance changes with different numbers of Frank-Wolfe iterations, and how the optimal number of iterations varies with the sparsity level. It would also be useful to see how the performance varies with different sparsity patterns, such as unstructured and semi-structured sparsity.

### Suggestions

The paper introduces a novel approach to LLM pruning using the Frank-Wolfe algorithm, which is a promising direction. However, several aspects of the method could be further investigated to strengthen the paper. First, a more detailed analysis of the impact of weight interactions is needed. While the paper argues that greedy methods ignore these interactions, it would be beneficial to quantify this effect. For example, the authors could compute the correlation between the importance scores of weights and their neighboring weights, and show how SparseFW captures this correlation better than greedy methods. This could be done by visualizing the importance scores and their spatial distribution, and by computing metrics such as the average correlation between the importance scores of connected neurons. Furthermore, the authors could explore the impact of different types of weight interactions, such as those within the same layer or across different layers.

Second, the dependence on the warm-start mask needs to be addressed more thoroughly. The paper mentions that the method requires a warm-start mask from existing methods like Wanda, but it does not analyze the sensitivity of SparseFW to the quality of this mask. It would be useful to see how the performance varies with different warm-start masks, and whether there are specific characteristics of the warm-start mask that are crucial for achieving good performance. For example, the authors could experiment with warm-start masks obtained from different pruning methods, or with warm-start masks that have different sparsity levels. They could also explore the possibility of using a suboptimal warm-start mask and how it affects the convergence of the Frank-Wolfe algorithm. This analysis would help to understand the robustness of the method and its practical applicability.

Finally, a more detailed analysis of the computational cost of SparseFW is needed. While the paper claims that the method is memory-efficient, it does not provide a detailed comparison of the computational cost with existing methods. A more thorough analysis of the time complexity and practical runtime would be helpful. This should include a breakdown of the time spent on each step of the algorithm, such as the gradient computation, the Frank-Wolfe update, and the thresholding operation. It would also be useful to compare the wall-clock time of SparseFW with other methods on the same hardware. Furthermore, the authors should provide more ablation studies on the impact of different parameters, such as the number of iterations and the sparsity level. This would provide more insights into the behavior of the method and help to optimize its performance.

### Questions

1. **Warm-Start Sensitivity**: How sensitive is the performance of SparseFW to the quality of the warm-start mask? Are there specific characteristics of the warm-start mask that are crucial for achieving good performance?
2. **Computational Overhead**: What is the computational overhead of SparseFW compared to other methods? How does the runtime scale with the size of the model and the sparsity level?
3. **Ablation Studies**: Can you provide more detailed ablation studies on the impact of different parameters, such as the number of iterations and the sparsity level? How do these parameters affect the performance of SparseFW?
4. **Theoretical Guarantees**: Can you provide more details on the theoretical guarantees of the method? How do these guarantees translate to practical performance improvements?
5. **Generalization to Other Architectures**: How well does SparseFW generalize to other types of architectures, such as convolutional neural networks or recurrent neural networks?

### Rating

6

### Confidence

3

**********