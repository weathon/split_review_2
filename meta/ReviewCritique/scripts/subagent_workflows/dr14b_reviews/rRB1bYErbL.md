### Summary

This paper proposes R-HORIZON, a method to enhance long-horizon reasoning in large reasoning models (LRMs) through query composition. The authors introduce a benchmark for evaluating LRMs on complex multi-step reasoning tasks, revealing that even advanced models struggle with performance degradation over extended reasoning horizons. By using R-HORIZON to generate long-horizon reasoning data for reinforcement learning with verified rewards (RLVR), the study demonstrates improvements in both multi-horizon and standard reasoning tasks. The results suggest that R-HORIZON offers a scalable and effective approach for advancing the reasoning capabilities of LRMs.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The R-HORIZON method provides a scalable and efficient way to construct complex multi-horizon reasoning tasks from simpler questions. This approach allows for systematic evaluation and training of LRMs on tasks that more closely resemble real-world reasoning scenarios.

2. The paper presents a comprehensive evaluation of various LRMs, providing valuable insights into the limitations of current models in handling long-horizon reasoning tasks. The analysis highlights specific challenges, such as limited effective reasoning length and poor allocation of thinking budgets across multiple interdependent problems.

3. The use of R-HORIZON for RLVR shows promising improvements in model performance, not only on multi-horizon tasks but also on standard reasoning benchmarks. This suggests that training with R-HORIZON-generated data can enhance both depth and breadth of reasoning capabilities.

### Weaknesses

#### Some Related Works


#### comment

1. The construction method for R-HORIZON may be somewhat limited, as it primarily focuses on mathematical tasks. This could restrict the generalizability of the approach to a broader range of reasoning tasks, particularly those involving more complex or abstract dependencies. The current method relies on composing problems with numerical dependencies, which may not translate well to tasks requiring logical inference or common-sense reasoning.

2. The paper does not provide a detailed analysis of how R-HORIZON impacts the token allocation across different problems within a composed task. Understanding this allocation is crucial for optimizing model performance on multi-horizon reasoning tasks. Specifically, it is unclear whether the model allocates tokens proportionally to the difficulty of each sub-task, or if it exhibits a bias towards earlier or later steps in the reasoning chain. This lack of analysis makes it difficult to diagnose performance bottlenecks.

3. While the paper discusses the overthinking phenomenon, it does not thoroughly explore how different reward functions in RLVR might mitigate this issue in long-horizon tasks. A deeper investigation could provide insights into optimizing training for complex reasoning. For example, the paper does not analyze the impact of using a sparse reward function that only rewards the final correct answer, versus a dense reward function that provides feedback at each step. This is a critical aspect that needs further investigation.

4. The generalization of R-HORIZON to other types of reasoning tasks beyond math, code, and simple agentic tasks is not discussed in detail. It remains unclear how well the method would perform on tasks involving natural language understanding, commonsense reasoning, or complex planning scenarios. The paper should provide a more thorough discussion of the limitations and potential adaptations required for these more diverse tasks.

### Suggestions

The paper introduces an interesting approach to enhancing long-horizon reasoning, but several aspects could be improved to strengthen its impact. First, the construction method for R-HORIZON should be expanded beyond mathematical tasks. The current approach of composing problems with numerical dependencies is limiting. Future work should explore methods for composing tasks that involve logical inference, common-sense reasoning, or other forms of abstract reasoning. For example, the authors could investigate how to compose tasks that require understanding of temporal or causal relationships, or tasks that involve multiple agents with conflicting goals. This would significantly broaden the applicability of R-HORIZON and make it more relevant to real-world reasoning scenarios. The authors could also explore techniques for automatically generating diverse and challenging composed tasks, rather than relying on manually crafted examples. This would improve the scalability and efficiency of the approach.

Second, the paper needs to provide a more detailed analysis of token allocation across different problems within a composed task. The authors should investigate how the model allocates tokens to each sub-task and whether this allocation is optimal. This could involve analyzing the correlation between token allocation and the difficulty of each sub-task, as well as the impact of different token allocation strategies on overall performance. For example, the authors could experiment with different prompting strategies that explicitly instruct the model to allocate tokens based on the perceived difficulty of each sub-task. They could also explore techniques for dynamically adjusting token allocation during the reasoning process, based on the model's confidence in its intermediate answers. This analysis would provide valuable insights into the model's reasoning process and help identify areas for improvement. Furthermore, the authors should investigate the impact of different reward functions on mitigating the overthinking phenomenon. The paper should compare the performance of different reward functions, such as sparse rewards that only reward the final correct answer, and dense rewards that provide feedback at each step. This analysis should also consider the impact of different reward functions on the model's token allocation strategy. For example, a sparse reward function might encourage the model to allocate more tokens to the later steps of the reasoning process, while a dense reward function might encourage a more balanced allocation. This analysis would provide valuable insights into how to optimize training for complex reasoning tasks.

Finally, the paper should provide a more thorough discussion of the generalization of R-HORIZON to other types of reasoning tasks. The authors should discuss the limitations of the current approach and the potential adaptations required for tasks involving natural language understanding, commonsense reasoning, or complex planning scenarios. This discussion should include concrete examples of how R-HORIZON could be applied to these tasks, as well as the challenges that might arise. For example, the authors could discuss how to compose tasks that require understanding of nuanced language, or tasks that involve reasoning about physical environments. They could also explore techniques for automatically generating diverse and challenging composed tasks for these more complex domains. This would significantly broaden the impact of the paper and make it more relevant to a wider range of reasoning tasks.

### Questions

1. Could the authors elaborate on how the R-HORIZON construction method could be adapted for more diverse reasoning tasks beyond math, code, and simple agentic tasks? Are there specific limitations in the current composition methods that might hinder generalization to broader reasoning domains?

2. How does R-HORIZON influence the allocation of tokens across different problems within a composed task? Is there an observed pattern in how models distribute their "thinking budget" among multiple interdependent problems?

3. Could the authors provide more details on how different reward functions in RLVR might affect the overthinking phenomenon in long-horizon reasoning tasks? Has there been any exploration of alternative reward structures that could encourage more efficient reasoning?

4. The paper mentions that training with R-HORIZON data improves response length efficiency. Could the authors clarify how this efficiency is quantified and whether it consistently translates to better performance across different types of reasoning tasks?

### Rating

6

### Confidence

3

**********