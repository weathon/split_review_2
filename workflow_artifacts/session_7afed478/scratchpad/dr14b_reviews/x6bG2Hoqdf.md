### Summary

The paper introduces CALM, a framework that combines verbal and numerical guidance to fine-tune large language models (LLMs) for automatic heuristic design. CALM leverages reinforcement learning (RL) to adapt the LLM based on the quality of generated heuristics, enabling the model to co-evolve with the search process. The framework employs evolutionary operators and a memory-efficient RL algorithm to optimize heuristic generation. Experimental results demonstrate that CALM outperforms state-of-the-art baselines across various optimization tasks, including Online Bin Packing, Traveling Salesman Problem, Capacitated Vehicle Routing Problem, and Orienteering Problem. The authors highlight the effectiveness of their approach in discovering high-performing heuristics while running entirely on a local computer with a single 24GB GPU.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a novel approach to automatic heuristic design by combining verbal and numerical guidance, which allows the LLM to co-evolve with the search process.
2. The framework employs a suite of evolutionary operators and a memory-efficient RL algorithm (GRPO) to fine-tune the LLM, enhancing the efficiency of the heuristic generation process.
3. The paper provides a comprehensive evaluation of the framework on several optimization tasks, demonstrating its effectiveness compared to state-of-the-art baselines.
4. The authors provide an analysis of the impact of different components of the framework, such as the reward function and the collapse mechanism, which offers insights into the design choices and their effects on performance.

### Weaknesses

#### Some Related Works


#### comment

1. The paper does not provide a detailed analysis of the computational cost of the proposed method compared to existing approaches. It is unclear how the fine-tuning of the LLM impacts the overall time and resources required, especially when compared to methods that do not involve fine-tuning. A more thorough comparison, including wall-clock time and GPU usage, would be beneficial.
2. The paper does not discuss the limitations of the proposed method in detail. For example, how does the method perform on problems with different characteristics (e.g., different size, different domain)? It is unclear how the method would scale to much larger problem instances or how it would perform on problems with different structural properties than those tested. A discussion of the method's sensitivity to problem characteristics is needed.
3. The paper does not provide a detailed analysis of the discovered heuristics. It would be interesting to see if the discovered heuristics are interpretable and if they provide any insights into the problems being solved. The paper lacks a qualitative analysis of the generated heuristics, making it difficult to understand the underlying strategies learned by the LLM. A deeper dive into the nature of the discovered heuristics is needed.

### Suggestions

The paper would benefit from a more detailed analysis of the computational cost of the proposed method. Specifically, the authors should provide a breakdown of the time spent on different stages of the algorithm, such as prompt evolution, LLM fine-tuning, and heuristic evaluation. This should include a comparison of the wall-clock time and GPU usage of CALM with existing methods, such as EvoTune, under similar experimental conditions. Furthermore, the authors should investigate the scalability of their method with respect to the size of the LLM and the complexity of the optimization problems. This could involve experiments with different LLM sizes and problem instances of varying scales. It would also be beneficial to analyze the convergence behavior of the method, showing how the performance of the discovered heuristics improves over time and how the computational cost varies with the number of iterations. This analysis should also consider the impact of the collapse mechanism on the overall computational cost and performance.

To address the limitations of the method, the authors should conduct a more comprehensive evaluation on a wider range of optimization problems with diverse characteristics. This should include problems with different sizes, domains, and structural properties. For example, the authors could test their method on problems with different constraint types, objective functions, and solution spaces. This would help to identify the strengths and weaknesses of the method and to determine the types of problems for which it is most suitable. The authors should also analyze the sensitivity of the method to different hyperparameters and provide guidelines for selecting appropriate values for different problems. This analysis should include a discussion of the method's robustness and its ability to generalize to unseen problem instances. Furthermore, the authors should investigate the impact of the initial seed heuristics on the performance of the method and explore strategies for generating effective initial heuristics.

Finally, the paper should include a more detailed analysis of the discovered heuristics. This should involve a qualitative analysis of the generated heuristics, focusing on their interpretability and the underlying strategies they employ. The authors should provide examples of the discovered heuristics and discuss their strengths and weaknesses. This analysis should also explore the diversity of the discovered heuristics and their ability to generalize to different problem instances. The authors could also investigate the relationship between the structure of the heuristics and their performance. This analysis should also consider the impact of the LLM fine-tuning on the nature of the discovered heuristics. A deeper understanding of the discovered heuristics would provide valuable insights into the problem-solving strategies learned by the LLM and would help to improve the method's effectiveness.

### Questions

1. How does the computational cost of CALM compare to existing methods, such as EvoTune? Could you provide a detailed comparison of the time and resources required for each method?
2. How does the method perform on problems with different characteristics (e.g., different size, different domain)? Could you provide more details on the limitations of your method and the types of problems for which it is most suitable?
3. Could you provide a detailed analysis of the discovered heuristics? Are they interpretable, and do they provide any insights into the problems being solved?

### Rating

8

### Confidence

3

**********