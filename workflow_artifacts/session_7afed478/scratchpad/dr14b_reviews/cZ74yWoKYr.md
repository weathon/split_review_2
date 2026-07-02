### Summary

This paper explores a novel approach to identifying critical KV cache entries in large language models (LLMs) by analyzing output perturbation. The authors argue that current cache eviction methods, which primarily rely on attention weights, are inadequate. They propose a perturbation-constrained selection algorithm that takes into account both attention weights and value states projected through parameter matrices. This approach aims to minimize the worst-case perturbation in attention output when replacing the full KV cache with a reduced version. The proposed algorithm is designed as a plug-and-play enhancement that can be integrated with existing state-of-the-art cache eviction methods. Through comprehensive evaluations on 29 datasets from the Ruler and LongBench benchmarks, the authors demonstrate that their algorithm significantly reduces compression loss by more than half on average across three distinct LLMs. Further analysis confirms the benefits of the perturbation-constrained selection algorithm at both the head and layer levels, highlighting its potential for optimizing critical cache selection from a theoretical perspective of output perturbation.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. Novel Perspective: The paper introduces a fresh perspective on cache eviction by framing the problem as minimizing output perturbation rather than solely relying on attention weights. This shift in focus provides a more comprehensive understanding of critical KV cache entries.

2. Theoretical Foundation: The authors provide a rigorous theoretical analysis of output perturbation, deriving an upper bound and formulating a perturbation-constrained selection algorithm. This theoretical grounding adds credibility to the proposed approach.

3. Plug-and-Play Enhancement: The proposed algorithm is designed as a universal, plug-and-play enhancement that can be seamlessly integrated with existing cache eviction methods without modifying their underlying mechanisms. This versatility makes it applicable to a wide range of scenarios.

4. Significant Performance Improvements: The experimental results demonstrate substantial reductions in compression loss when the proposed algorithm is integrated with state-of-the-art cache eviction methods. The consistent performance improvements across various settings underscore the robustness of the approach.

5. Comprehensive Evaluation: The paper presents a thorough evaluation across 29 datasets from the Ruler and LongBench benchmarks, involving three distinct LLMs. This extensive experimentation provides strong evidence for the generalizability of the proposed algorithm.

### Weaknesses

#### Some Related Works


#### comment

1. Limited Implementation Details: While the paper outlines the proposed algorithm, it lacks specific implementation details, such as the exact data structures used and the computational complexity analysis. Providing more information on the practical aspects of implementing the algorithm would enhance its reproducibility and usability.

2. Computational Overhead: Although the authors claim that the proposed algorithm incurs negligible computational overhead, a more detailed quantitative analysis comparing its computational cost to existing methods would be beneficial. Understanding the trade-offs between computational efficiency and compression performance is crucial for practical adoption.

3. Generalizability Across Different LLMs: The paper primarily evaluates the proposed algorithm on three specific LLMs. Expanding the evaluation to include a wider range of LLMs with different architectures and sizes would provide a more comprehensive assessment of the algorithm's generalizability.

### Suggestions

The paper would benefit from a more detailed exposition of the implementation specifics. For instance, elaborating on the data structures used to represent the KV cache and attention weights, along with their memory layouts, would be valuable. Furthermore, a discussion on the computational complexity of the proposed algorithm, including both theoretical bounds and empirical measurements, is needed. This should include a breakdown of the time spent on different stages of the algorithm, such as the perturbation calculation and the selection process. Providing pseudocode or a simplified code snippet illustrating the core logic would also significantly enhance the clarity and reproducibility of the work. This level of detail is crucial for other researchers to implement and build upon the proposed method effectively.

To strengthen the claims regarding computational overhead, a more rigorous analysis is required. This should involve a comparative study of the runtime performance of the proposed algorithm against existing cache eviction methods, across various hardware configurations and model sizes. The analysis should not only focus on the overall execution time but also break down the time spent on different operations, such as the computation of perturbation scores and the selection of critical KV entries. Additionally, it would be beneficial to analyze the memory footprint of the proposed algorithm, including the space required for storing intermediate results and data structures. This detailed analysis will allow practitioners to make informed decisions about the suitability of the proposed method for their specific use cases.

Finally, the generalizability of the proposed algorithm should be further investigated. While the current evaluation includes three different LLMs, expanding the scope to encompass a wider range of models with varying architectures, sizes, and training methodologies would provide a more robust assessment of the algorithm's performance. This could include models with different numbers of layers, attention heads, and embedding dimensions. Furthermore, it would be valuable to explore the sensitivity of the algorithm to different hyperparameter settings, such as the size of the critical KV cache entries. A systematic analysis of these factors would provide a clearer understanding of the algorithm's strengths and limitations, and help identify potential areas for improvement.

### Questions

1. Could you provide more details on the implementation of the perturbation-constrained selection algorithm? Specifically, what are the key steps involved in integrating the algorithm with existing cache eviction methods?

2. How does the computational cost of the proposed algorithm compare to existing methods? Are there any trade-offs between computational efficiency and compression performance?

3. Have you evaluated the proposed algorithm on other LLMs besides the three mentioned in the paper? If so, what were the results? If not, what are your expectations regarding the algorithm's performance on other models?

### Rating

8

### Confidence

3

**********