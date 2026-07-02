### Summary

This paper proposes a novel method called Steady Thought (ST) to mitigate the under-thinking phenomenon in Large Language Models (LLMs). The authors introduce a three-stage framework consisting of thought segmentation, thought completion, and fine-grained preference optimization. The experiments conducted on multiple models and datasets demonstrate the effectiveness of the proposed method in reducing output length while improving accuracy.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper addresses an important issue in LLMs, the under-thinking phenomenon, which can lead to inefficient and low-quality reasoning.
2. The proposed method is novel and well-motivated. The three-stage framework provides a comprehensive approach to mitigate under-thinking.
3. The experiments are thorough and demonstrate the effectiveness of the proposed method across multiple models and datasets.

### Weaknesses

#### Some Related Works


#### comment

1. The paper could benefit from a more detailed discussion of the limitations of the proposed method and potential directions for future research.
2. The authors could provide more insights into the practical implications of their findings and how they can be applied in real-world scenarios.

### Suggestions

The paper would be strengthened by a more thorough discussion of the limitations of the proposed Steady Thought (ST) method. Specifically, the authors should explore scenarios where the method might fail or underperform. For example, how does the method handle complex reasoning tasks that require multiple steps or involve nuanced logical deductions? Are there specific types of problems where the segmentation or completion stages might introduce errors or biases? A detailed analysis of these failure cases would provide a more complete understanding of the method's capabilities and limitations. Furthermore, the authors should discuss the computational overhead of the ST framework, particularly the fine-grained preference optimization stage. How does the training time and resource consumption compare to existing methods? Addressing these practical concerns would make the paper more impactful and useful for researchers and practitioners.

To enhance the practical relevance of the work, the authors should delve deeper into the real-world implications of mitigating under-thinking in LLMs. While the paper demonstrates improvements in accuracy and output length, it would be beneficial to explore how these improvements translate to practical applications. For instance, how would the ST method perform in tasks such as complex question answering, code generation, or scientific discovery? Providing concrete examples of how the method can be applied in these domains would make the paper more compelling. The authors should also discuss the potential challenges in deploying the ST method in real-world scenarios, such as the need for large-scale training data or the sensitivity to hyperparameter tuning. A more detailed discussion of these practical considerations would make the paper more valuable to the broader community.

Finally, the authors should consider exploring potential avenues for future research. For example, could the ST framework be extended to other types of reasoning tasks or combined with other techniques to further improve performance? Are there alternative approaches to thought segmentation or completion that could be explored? A discussion of these future directions would not only highlight the potential of the proposed method but also stimulate further research in this area. The authors could also investigate the interpretability of the learned preferences in the fine-grained preference optimization stage. Understanding why the model prefers certain thoughts over others could provide valuable insights into the reasoning process and lead to further improvements in the method.

### Questions

1. How does the proposed method perform on other types of reasoning tasks, such as commonsense reasoning or logical reasoning?
2. Can the authors provide more insights into the computational overhead of the proposed method compared to existing approaches?

### Rating

6

### Confidence

3

**********