### Summary

This paper introduces CANON, a novel reinforcement learning framework for enhancing the reasoning capabilities of large language models (LLMs) by leveraging human priors on training metrics without assuming their directional impact on performance. CANON regroups sampled responses based on metric values and computes inter-group and intra-group advantages to identify beneficial behaviors. The authors demonstrate CANON's effectiveness across various LLMs and reasoning tasks, showing improvements in performance and efficiency compared to existing methods.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a novel method, CANON, which addresses the limitations of existing RLVR approaches by avoiding handcrafted priors and adaptively amplifying metric changes.
2. The authors provide a thorough theoretical analysis of CANON, including proofs of its properties and relationships to existing methods like DR.GRPO.
3. The experimental evaluation is comprehensive, covering multiple LLMs, reasoning tasks, and metrics. The results demonstrate CANON's effectiveness in improving both performance and efficiency.

### Weaknesses

#### Some Related Works


#### comment

1. The paper could benefit from more detailed ablation studies to isolate the contributions of different components of CANON (e.g., inter-group vs. intra-group advantage). Specifically, it is unclear how the performance varies when only inter-group or intra-group advantages are used, and how the weighting between these two components affects the final results. A more granular analysis of the impact of each component would strengthen the claims about the method's effectiveness.
2. The computational overhead of CANON compared to simpler methods is not thoroughly discussed. While the paper mentions that CANON involves regrouping and advantage calculations, it lacks a detailed analysis of the computational cost associated with these operations. A comparison of training time and resource requirements with baseline methods would be valuable for assessing CANON's practicality in real-world applications. This should include not just the overall training time, but also the time spent on the specific CANON-related computations.
3. The paper primarily focuses on math and logic reasoning tasks. Evaluating CANON on a broader range of reasoning tasks (e.g., commonsense reasoning, natural language inference) would provide a more comprehensive assessment of its generalizability. The current evaluation does not fully demonstrate the method's applicability to diverse reasoning scenarios, and it is unclear whether the observed improvements are specific to the chosen tasks or indicative of a more general capability.

### Suggestions

To address the lack of detailed ablation studies, the authors should conduct experiments that isolate the effects of inter-group and intra-group advantages. This could involve training models using only inter-group advantage, only intra-group advantage, and varying the weighting between the two. The results should be presented with clear visualizations, such as line plots showing performance across different weighting ratios. Furthermore, the analysis should include a discussion of the optimal weighting strategies for different tasks and models, providing insights into how to best utilize CANON in various scenarios. This would provide a more nuanced understanding of the method's inner workings and allow for more informed application.

To better assess the computational overhead, the authors should provide a detailed breakdown of the time spent on different parts of the CANON training process, including the regrouping of responses, advantage calculations, and policy updates. This analysis should be compared to the time spent on these operations in baseline methods like DR.GRPO. The comparison should include not only the total training time but also the time spent on the specific CANON-related computations. This would allow for a more precise understanding of the computational cost of CANON and its practical implications. Additionally, the authors should discuss the scalability of CANON with respect to the number of samples and the size of the model, providing insights into its applicability to larger-scale problems.

To demonstrate the generalizability of CANON, the authors should evaluate its performance on a wider range of reasoning tasks, including commonsense reasoning and natural language inference. This would involve selecting appropriate benchmarks for these tasks and adapting the CANON method to the specific requirements of each benchmark. The results should be compared to existing methods for these tasks, providing a more comprehensive assessment of CANON's capabilities. Furthermore, the authors should analyze the performance of CANON across different tasks and identify any task-specific adaptations that may be necessary. This would provide a more complete picture of CANON's strengths and limitations and its potential for broader application.

### Questions

1. How does CANON perform on tasks with less clear correctness criteria (e.g., commonsense reasoning, natural language inference)?
2. What are the computational costs of CANON compared to simpler methods like DR.GRPO?
3. How sensitive is CANON to the choice of metrics and scheduling strategies?

### Rating

6

### Confidence

3

**********