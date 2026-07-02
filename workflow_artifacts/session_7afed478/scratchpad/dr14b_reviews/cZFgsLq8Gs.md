### Summary

This paper presents DeepScientist, an LLM-based multi-agent system for automated scientific discovery. The system is designed to autonomously conduct scientific research and generate novel findings that surpass human performance. The key contributions include:

1. Formalizing scientific discovery as a goal-oriented Bayesian Optimization problem, where the objective is to maximize the value of a research program while balancing exploration and exploitation.
2. Developing a three-stage iterative workflow (Strategize & Hypothesize, Implement & Verify, Analyze & Report) that mimics the human research process, supported by a persistent Findings Memory that accumulates both successful and failed experiments.
3. Implementing a scalable architecture with specialized agents for different tasks (e.g., coding, planning, reasoning) and a shared knowledge base (Findings Memory) that enables efficient information sharing and learning.
4. Conducting large-scale experiments on three frontier AI research tasks (Agent Failure Attribution, LLM Inference Acceleration, AI Text Detection) and demonstrating that DeepScientist can surpass human SOTA methods by autonomously redesigning core methodologies.
5. Providing the first large-scale empirical evidence that an AI system can continuously advance scientific frontiers on complex AI tasks, rivaling human researchers under comparable compute budgets.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. Novel formalization of scientific discovery as a Bayesian Optimization problem with a goal-oriented approach, addressing the limitations of existing AI Scientist systems.
2. Innovative three-stage iterative workflow that mimics the human research process, enabling long-horizon, goal-directed scientific discovery.
3. Comprehensive system architecture with specialized agents, a persistent Findings Memory, and a robust implementation that supports large-scale experimentation.
4. Significant empirical results on three frontier AI tasks, demonstrating the system's ability to surpass human SOTA methods and achieve meaningful scientific progress.
5. Thorough ablation studies and analysis of the iterative exploration trajectory, providing valuable insights into the system's behavior and the scientific discovery process.

### Weaknesses

#### Some Related Works


#### comment

1. The paper does not provide a detailed analysis of the computational resources required by DeepScientist compared to human research efforts. While the authors mention that their compute budget is comparable to a "medium-sized lab," a more quantitative comparison would be beneficial. Specifically, the paper lacks a clear breakdown of the GPU hours, memory usage, and other computational resources consumed by DeepScientist, making it difficult to assess the practical feasibility of the approach. A comparison with the typical computational resources used in human-led research for similar tasks would provide a better understanding of the system's efficiency.
2. The reliance on LLMs for core logic raises concerns about the potential for hallucinations and the need for human oversight. Although the authors mention that three human experts supervised the process to verify outputs and filter out hallucinations, the paper does not provide a detailed analysis of the types of errors encountered or the frequency of human intervention. The paper should include a more thorough discussion of the limitations of the LLMs and the specific mechanisms used to mitigate these issues.
3. The paper acknowledges that the success rate of LLM-generated ideas is low, with approximately 60% of failed trials due to implementation errors. This highlights a potential bottleneck in the system's efficiency. The paper should provide a more detailed analysis of the types of implementation errors that occur and discuss potential strategies for improving the reliability of LLM-generated code. Additionally, the paper should discuss the trade-offs between exploration and exploitation in the context of code generation and how these trade-offs impact the overall efficiency of the system.

### Suggestions

To address the lack of detailed computational resource analysis, the authors should provide a comprehensive breakdown of the resources consumed by DeepScientist, including GPU hours, memory usage, and other relevant metrics. This should be compared to the typical computational resources used in human-led research for similar tasks. For example, if DeepScientist uses 1000 GPU hours to achieve a certain result, the paper should compare this to the equivalent cost in terms of researcher time and computational resources for a human team to achieve a similar outcome. This comparison should be made for each of the three tasks evaluated in the paper. Furthermore, the authors should discuss the scalability of their approach in terms of computational resources. This would provide a better understanding of the practical feasibility of the approach and its potential for real-world applications.

To mitigate the concerns about LLM hallucinations and the need for human oversight, the authors should provide a more detailed analysis of the types of errors encountered during the experiments. This analysis should include specific examples of LLM-generated ideas that were incorrect or led to implementation errors. The paper should also discuss the specific mechanisms used to filter out these errors and the frequency of human intervention. For example, the authors could provide a taxonomy of the errors and discuss how the system is designed to avoid each type of error. Additionally, the authors should explore alternative methods for reducing the reliance on human oversight, such as incorporating more robust verification mechanisms or using formal methods to verify the correctness of LLM-generated code. This would improve the reliability and autonomy of the system.

To improve the efficiency of the system, the authors should provide a more detailed analysis of the types of implementation errors that occur and discuss potential strategies for improving the reliability of LLM-generated code. This analysis should include specific examples of common implementation errors and discuss how these errors can be avoided. For example, the authors could analyze the types of coding errors that are most frequent and discuss how the system can be improved to generate more robust code. Additionally, the authors should discuss the trade-offs between exploration and exploitation in the context of code generation and how these trade-offs impact the overall efficiency of the system. The paper should also explore methods for improving the search efficiency, such as using more informed search strategies or incorporating prior knowledge into the search process. This would reduce the computational cost of the approach and make it more practical for real-world applications.

### Questions

1. Could the authors provide a more detailed comparison of the computational resources required by DeepScientist versus human research efforts for the same tasks? This would help in understanding the practical trade-offs of the approach.
2. What specific mechanisms are in place to minimize the potential for LLM hallucinations, and how effective were these mechanisms in the experiments? A more detailed analysis of the types of errors encountered and the frequency of human intervention would be valuable.
3. How does the system handle the low success rate of LLM-generated ideas in terms of computational efficiency, and what strategies are being considered to improve this? A discussion of the trade-offs between exploration and exploitation in the context of code generation would be beneficial.

### Rating

6

### Confidence

3

**********