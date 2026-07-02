### Summary

This paper introduces MermaidFlow, a framework for agentic workflow generation that leverages evolutionary programming and Mermaid, a structured graph language, to ensure safety and correctness in agentic workflows. Unlike existing methods that rely on brittle, low-level representations, MermaidFlow separates symbolic planning from execution, enabling robust, human-readable, and verifiable workflows. The framework’s evolutionary approach, with domain-aware operators like crossover and mutation, efficiently explores a high-quality workflow space, achieving superior performance on benchmarks without modifying task settings. MermaidFlow demonstrates a scalable, modular foundation for interpretable and adaptable agentic systems, advancing workflow optimization through a statically verifiable, declarative graph representation.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper is well-written and easy to follow.
2. The proposed MermaidFlow is interesting and novel. It is the first agentic workflow framework to guarantee static graph-level correctness across the entire generation process.
3. The authors provide comprehensive experiments to demonstrate the effectiveness of MermaidFlow.

### Weaknesses

#### Some Related Works


#### comment

1. The authors should provide more details on the implementation of MermaidFlow, including the specific evolutionary programming techniques used and how the Mermaid graph language is integrated into the workflow generation process. The description of the evolutionary operators (crossover, mutation, etc.) lacks sufficient detail to understand their precise implementation and impact on the search space. For example, how are nodes selected for crossover or mutation, and what are the constraints on these operations to ensure the validity of the resulting workflows? 
2. The authors should provide more details on the baselines, such as how they are implemented and how they compare to MermaidFlow in terms of performance and other metrics. It is unclear how the baselines are adapted to the specific problem settings and how their performance is evaluated. A more detailed comparison, including specific implementation choices and hyperparameter settings, would be beneficial. For instance, what specific algorithms or techniques are used in the baselines, and how do they differ in their approach to workflow generation?
3. The authors should provide more details on the evaluation metrics used in the experiments, such as how they are calculated and what they measure. The paper lacks a clear definition of the evaluation metrics and how they relate to the goals of the proposed framework. For example, how is the 'correctness' of a workflow defined and measured, and what are the limitations of the chosen metrics?

### Suggestions

To address the lack of implementation details, the authors should include a detailed description of the evolutionary programming techniques used in MermaidFlow. This should include a precise definition of the crossover, mutation, and other operators, along with examples of how they are applied to the Mermaid graph representations. The explanation should clarify how these operators are designed to maintain the validity of the workflows and how they explore the search space effectively. For instance, the authors could describe the specific algorithms used for selecting nodes for crossover or mutation and the constraints imposed to ensure that the resulting workflows remain semantically correct. Furthermore, the authors should provide a pseudocode or a more formal description of the evolutionary process to enhance clarity and reproducibility. This would allow other researchers to understand the inner workings of MermaidFlow and potentially build upon it.

To improve the comparison with baselines, the authors should provide a detailed explanation of how each baseline is implemented and adapted to the specific problem settings. This should include a description of the algorithms or techniques used in each baseline, as well as the specific hyperparameter settings and implementation choices. The authors should also discuss the differences in the approach to workflow generation between MermaidFlow and the baselines, highlighting the advantages and disadvantages of each method. For example, if a baseline uses a random search strategy, the authors should explain how this differs from the evolutionary approach used in MermaidFlow and how this difference impacts the performance and efficiency of the search process. A table summarizing the key differences between MermaidFlow and the baselines would be beneficial for the reader.

Finally, the authors should provide a clear and detailed definition of the evaluation metrics used in the experiments. This should include a description of how each metric is calculated and what it measures in the context of agentic workflow generation. For example, if the 'correctness' of a workflow is measured by its ability to produce the correct output, the authors should explain how this is determined and what are the limitations of this metric. The authors should also discuss the trade-offs between different metrics and how they relate to the goals of the proposed framework. For instance, if a metric measures the efficiency of a workflow, the authors should explain how this is calculated and how it relates to the overall performance of the system. A more detailed discussion of the evaluation metrics would enhance the credibility and interpretability of the experimental results.

### Questions

Please refer to the Weaknesses.

### Rating

6

### Confidence

4

**********