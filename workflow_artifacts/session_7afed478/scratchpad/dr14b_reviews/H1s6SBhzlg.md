### Summary

This paper studies the problem of aggregating answers from multiple LLMs, which is a fundamental challenge in multi-agent LLM reasoning. The authors propose two new aggregation algorithms, Optimal Weight (OW) and Inverse Surprising Popularity (ISP), that leverage both first-order and second-order information to improve upon majority voting. They provide theoretical analysis and empirical validation of their methods on synthetic datasets, popular LLM fine-tuning benchmarks, and a real-world healthcare setting.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper addresses a fundamental challenge in multi-agent LLM reasoning, which is the aggregation of answers from multiple LLMs. The proposed methods, OW and ISP, are novel and theoretically grounded, offering a significant improvement over the widely used majority voting approach.

2. The authors provide a rigorous theoretical analysis of their methods, demonstrating their optimality and advantages over existing approaches. They also conduct extensive empirical validation on both synthetic and real-world datasets, showing that their methods consistently outperform majority voting.

3. The paper is well-written and easy to follow, with clear explanations of the algorithms and their theoretical underpinnings. The authors also provide detailed experimental results and analysis, making it easy to understand the performance of their methods.

### Weaknesses

#### Some Related Works


#### comment

1. The paper assumes that the outputs of all LLM agents are not affected by the ordering of the options. However, this assumption may not hold in practice, especially for smaller LLMs. The authors should discuss the potential impact of option ordering on the performance of their methods and consider extending their algorithms to handle this issue.

2. The paper does not provide a detailed analysis of the computational cost of the proposed methods. While the authors mention that the cost of generating outputs from LLMs is negligible, the estimation of second-order information and the optimization process for OW-L may still be computationally expensive, especially for large-scale applications.

### Suggestions

The paper should address the potential impact of option ordering on the performance of the proposed aggregation methods. Specifically, the authors should investigate how the permutation of answer choices affects the accuracy of OW and ISP, especially for smaller LLMs that might be more susceptible to positional biases. This could involve conducting experiments where the order of options is systematically varied and the resulting changes in aggregation accuracy are measured. Furthermore, the authors should explore methods to mitigate the impact of option ordering, such as using techniques like positional encoding or data augmentation to make the models more robust to permutations. The paper should also discuss the limitations of the current approach and suggest directions for future research that could address this issue more effectively.

To address the computational concerns, the paper should provide a detailed analysis of the time and space complexity of the proposed methods. This analysis should include a breakdown of the computational cost for each step, such as the empirical estimation of conditional probabilities, the optimization procedure for OW-L, and the aggregation process itself. The authors should also discuss the practical implications of these costs, such as the memory requirements and the scalability of the proposed methods to a large number of LLMs or answer options. Furthermore, the paper should explore potential optimizations to reduce the computational overhead, such as using more efficient optimization algorithms or parallelizing the computation. This would make the proposed methods more practical for large-scale applications and increase their overall impact.

### Questions

1. How does the performance of OW and ISP change when the number of answer options increases? Are there any practical limitations to the number of options that can be handled effectively?

2. What are the computational costs of the proposed methods, especially for large-scale applications with many LLMs and answer options? Are there any potential optimizations to reduce the computational overhead?

### Rating

6

### Confidence

3

**********