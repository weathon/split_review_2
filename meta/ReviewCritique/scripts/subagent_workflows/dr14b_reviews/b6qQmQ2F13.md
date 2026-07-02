### Summary

This paper studies the memory optimization strategies for LLM reasoning models. The paper aims to address the memory usage challenges posed by the KV cache in reasoning models, which can dominate GPU memory usage during long generations. The authors conduct systematic experiments to explore the trade-offs between model size, weight precision, token budget, parallel scaling, and KV cache compression. The findings suggest that there is no one-size-fits-all strategy for memory optimization in reasoning models, and the optimal approach depends on the model's effective size and the nature of the task.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

- The paper provides a systematic study on the memory-accuracy trade-offs for reasoning models, which is a practical problem in deploying such models.
- The findings of the paper are well-supported by empirical evidence. The authors conduct extensive experiments across different model sizes, weight precisions, token budgets, and KV cache compression strategies.
- The paper is well-written and easy to follow. The authors clearly explain the experimental setup and results.

### Weaknesses

#### Some Related Works


#### comment

 - The paper focuses on a specific set of reasoning tasks and models. It is not clear how the findings generalize to other types of reasoning tasks or models.
- The paper does not provide concrete guidelines or recommendations for practitioners on how to choose the optimal memory optimization strategy for their specific use case. While the findings suggest that the optimal approach depends on the model's effective size and the nature of the task, the paper does not provide a clear framework for making these decisions.

### Suggestions

The paper would benefit from a more thorough investigation into the generalizability of its findings. While the authors explore a range of reasoning tasks, it is crucial to examine how the observed memory-accuracy trade-offs behave across a broader spectrum of model architectures and reasoning paradigms. For instance, the study could include models with different attention mechanisms or those trained with varied pre-training objectives. Furthermore, the tasks could be expanded to include more complex reasoning scenarios, such as those involving multi-hop reasoning or commonsense reasoning. This would provide a more robust understanding of the factors influencing the optimal memory optimization strategy and enhance the practical applicability of the research. It would also be beneficial to explore the impact of different hardware platforms on the observed trade-offs, as memory bandwidth and latency can significantly affect the performance of various optimization techniques. 

To address the lack of concrete guidelines, the paper should aim to provide a more prescriptive framework for practitioners. This could involve developing a decision tree or a set of rules of thumb that guide users in selecting the most appropriate memory optimization strategy based on their specific model size, task characteristics, and available resources. For example, the authors could provide recommendations on how to balance the trade-offs between weight quantization, KV cache compression, and parallel scaling based on the model's effective size and the nature of the reasoning task. This framework should also consider the practical constraints of real-world deployments, such as the limitations of specific hardware platforms and the need for real-time inference. The inclusion of such a framework would significantly enhance the practical value of the paper and make it more accessible to a wider audience.

Finally, the paper could benefit from a more in-depth analysis of the interaction between different memory optimization techniques. For example, how does the effectiveness of KV cache compression change when combined with different levels of weight quantization? Exploring these interactions could reveal synergistic effects and lead to more effective memory optimization strategies. Furthermore, the paper should investigate the impact of these optimization techniques on the stability and robustness of the model's reasoning capabilities. It is important to ensure that memory optimization does not come at the cost of reduced model reliability or increased susceptibility to adversarial attacks. A more comprehensive analysis of these aspects would provide a more complete picture of the trade-offs involved in memory optimization for reasoning models.

### Questions

- How do the findings generalize to other types of reasoning tasks or models?
- What are the implications of these findings for the future development of reasoning models?

### Rating

6

### Confidence

3

**********