### Summary

The paper proposes VISTA, a modular framework for causal structure learning that decomposes the problem into local subgraphs based on Markov Blankets and integrates them through weighted voting and acyclicity enforcement. While the idea of modular integration is not entirely new, VISTA's approach to using weighted voting with exponential decay and a Feedback Arc Set (FAS) algorithm for acyclicity is presented as a novel contribution. The authors claim that the framework is model-agnostic and imposes no assumptions on base learners, making it broadly applicable across different data settings. Theoretical guarantees on error bounds and asymptotic consistency are provided, along with empirical results showing improvements in accuracy and efficiency over several baselines.

### Soundness

2

### Presentation

3

### Contribution

2

### Strengths

1. VISTA's modular design allows for flexibility in choosing base learners, which can be advantageous in practice.
2. The paper provides theoretical analysis, including error bounds and consistency guarantees, which adds rigor to the proposed framework.
3. The experimental results demonstrate improvements in both accuracy and efficiency, particularly for large-scale datasets.

### Weaknesses

#### Some Related Works


#### comment

1. The core mechanism of weighted voting with exponential decay and thresholding for aggregating local causal structures is not sufficiently novel to warrant significant contribution. This approach is conceptually similar to existing methods that use weighted aggregation or consensus mechanisms for combining results from different sources or models. The paper does not adequately differentiate its approach from these existing techniques, nor does it provide a clear explanation of why this specific combination of exponential decay and thresholding is superior to other possible aggregation methods.
2. The theoretical analysis, while rigorous, relies on several assumptions that may not hold in practice, such as the reliability of base learners and the independence of subgraph samples. The paper does not provide a thorough discussion of the potential impact of these assumptions on the practical performance of VISTA. For example, the assumption of reliable base learners is particularly concerning, as it is not clear how to ensure this reliability in real-world scenarios where the true causal structure is unknown. Furthermore, the assumption of independent subgraph samples is questionable, as the subgraphs are derived from the same dataset and are likely to exhibit dependencies.
3. The paper does not adequately address the limitations of the Feedback Arc Set (FAS) algorithm in ensuring acyclicity, especially in cases where cycles are not dense. While the FAS algorithm is a known heuristic, its application in this context does not introduce any novel insights or solutions. The paper lacks a discussion of the potential drawbacks of using FAS, such as its computational complexity and its potential to introduce errors in the final causal structure.
4. The experimental section lacks a comprehensive comparison with state-of-the-art methods, particularly those that also employ modular or divide-and-conquer strategies for causal discovery. The paper does not provide a clear justification for the choice of baselines, and it is unclear whether the reported improvements are significant when compared to the most relevant existing methods.

### Suggestions

The paper should provide a more detailed explanation of the novelty of the proposed weighted voting mechanism. It should clearly articulate how the specific combination of exponential decay and thresholding differs from existing aggregation methods and why it is superior. A more thorough analysis of the sensitivity of the method to different parameter settings would also be beneficial. For example, the paper could explore how the choice of the decay parameter and the threshold affects the performance of VISTA on different types of datasets. Furthermore, the paper should include a discussion of the computational complexity of the weighted voting mechanism and how it scales with the size of the graph.

To address the concerns regarding the theoretical assumptions, the paper should include a more detailed discussion of the potential impact of these assumptions on the practical performance of VISTA. Specifically, the paper should explore how the performance of VISTA degrades when the base learners are not reliable or when the subgraph samples are not independent. The paper could also consider providing some empirical analysis to validate the theoretical assumptions and to demonstrate the robustness of VISTA to violations of these assumptions. For example, the paper could simulate scenarios where the base learners are known to be unreliable or where the subgraphs are highly correlated and analyze how VISTA performs in these scenarios. The paper should also discuss how to choose reliable base learners in practice.

The paper should also provide a more detailed analysis of the limitations of the FAS algorithm and explore alternative methods for ensuring acyclicity. The paper could consider comparing the performance of VISTA with other acyclicity enforcement methods and discussing the trade-offs between different approaches. Furthermore, the experimental section should be expanded to include a more comprehensive comparison with state-of-the-art methods, particularly those that also employ modular or divide-and-conquer strategies for causal discovery. The paper should provide a clear justification for the choice of baselines and should ensure that the reported improvements are significant when compared to the most relevant existing methods. The paper should also include a discussion of the computational cost of the proposed method and how it compares to other methods.

### Questions

1. How does the proposed weighted voting mechanism differ from existing methods that use weighted aggregation or consensus mechanisms for causal structure learning?
2. What are the specific advantages of using exponential decay and thresholding in the voting process compared to other possible aggregation methods?
3. How does the FAS algorithm ensure acyclicity in cases where cycles are not dense, and what are the limitations of this approach?
4. Can the theoretical guarantees be strengthened to relax the assumptions on the reliability of base learners and the independence of subgraph samples?
5. How does VISTA compare to state-of-the-art methods in terms of accuracy and efficiency, particularly for large-scale datasets?

### Rating

3

### Confidence

5

**********