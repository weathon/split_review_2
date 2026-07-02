### Summary

This paper presents a systematic study on scaling RL training for LLMs, which is becoming increasingly important as RL training compute grows. The authors define a framework for analyzing and predicting RL scaling behavior, and propose a best-practice recipe called SCALERL that combines several existing techniques to achieve better performance and efficiency. The paper provides valuable insights into the scaling properties of different RL methods and design choices, and demonstrates the effectiveness of SCALERL on a large-scale experiment.

### Soundness

4

### Presentation

4

### Contribution

3

### Strengths

- The paper addresses an important and timely problem of scaling RL training for LLMs, which has significant implications for the development of more capable and reliable language models.
- The paper presents a comprehensive and rigorous empirical study, involving over 400,000 GPU-hours of experimentation, that systematically investigates the scaling behavior of different RL methods and design choices.
- The paper proposes a novel framework for analyzing and predicting RL scaling behavior, based on sigmoidal compute-performance curves, that can help researchers and practitioners evaluate the scalability of new RL algorithms without incurring the full compute cost.
- The paper introduces a best-practice recipe called SCALERL that combines several existing techniques to achieve better performance and efficiency than existing methods, and demonstrates its effectiveness on a large-scale experiment with 100,000 GPU-hours of training.
- The paper is well-written and organized, with clear explanations of the methodology, results, and implications. The figures and tables are informative and easy to understand.

### Weaknesses

#### Some Related Works


#### comment

 - The paper focuses primarily on mathematical reasoning tasks, which may limit the generalizability of the findings to other domains or tasks. It would be beneficial to see how the proposed framework and SCALERL recipe perform on a wider range of tasks, such as natural language understanding, generation, or dialogue. The current evaluation does not provide sufficient evidence to claim broad applicability.
- The paper does not provide a detailed analysis of the computational cost and resource requirements of different RL methods and design choices. While the authors mention the total GPU hours, a breakdown of the cost per task, or a comparison of the resource utilization of different methods, would be valuable for practitioners. This lack of detailed cost analysis makes it difficult to assess the practical feasibility of the proposed approach.
- The paper could benefit from a more thorough discussion of the limitations of the proposed framework and potential areas for future research. For example, how does the framework handle different model architectures or training objectives? What are the potential challenges in applying the framework to more complex or dynamic environments? Addressing these questions would provide a more complete picture of the scope and limitations of the work.

### Suggestions

The paper would be significantly strengthened by expanding the evaluation to include a more diverse set of tasks beyond mathematical reasoning. Specifically, the authors should consider evaluating the performance of SCALERL on tasks that involve natural language understanding, such as question answering or text summarization, as well as tasks that require more complex reasoning, such as planning or code generation. This would provide a more comprehensive assessment of the generalizability of the proposed framework and recipe. Furthermore, it would be beneficial to analyze the performance of SCALERL on tasks with varying levels of difficulty to understand its limitations and potential areas for improvement. Such an analysis would also help to identify the types of tasks where SCALERL is most effective and where it may struggle.

In addition to expanding the task evaluation, the paper should include a more detailed analysis of the computational cost and resource requirements of different RL methods and design choices. This analysis should include a breakdown of the cost per task, as well as a comparison of the resource utilization of different methods. For example, the authors could provide a table that shows the GPU hours, memory usage, and training time for each method on each task. This would allow practitioners to better assess the practical feasibility of the proposed approach and make informed decisions about which method to use for their specific needs. Furthermore, the authors should discuss the trade-offs between performance and computational cost, and provide guidance on how to choose the most appropriate method for a given budget.

Finally, the paper should include a more thorough discussion of the limitations of the proposed framework and potential areas for future research. This discussion should address questions such as how the framework handles different model architectures or training objectives, and what are the potential challenges in applying the framework to more complex or dynamic environments. The authors should also discuss the potential impact of different hyperparameters on the performance of the framework and provide guidance on how to tune these parameters for different tasks. Furthermore, the authors should explore the potential for extending the framework to other types of reinforcement learning algorithms, such as those based on transformers or graph neural networks. Addressing these questions would provide a more complete picture of the scope and limitations of the work and help to guide future research in this area.

### Questions

- How does the proposed framework handle different model architectures or training objectives? Are there any specific assumptions or limitations that need to be considered?
- What are the potential challenges in applying the framework to more complex or dynamic environments? How can these challenges be addressed?
- How sensitive is the framework to the choice of hyperparameters, such as the learning rate or the batch size? How can these hyperparameters be tuned for different tasks or models?

### Rating

8

### Confidence

4

**********