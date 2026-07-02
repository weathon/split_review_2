### Summary

This paper introduces EconAgentBench, a suite of benchmarks designed to evaluate the capabilities of LLM agents in economic decision-making tasks within unknown environments. The benchmarks focus on three core economic tasks: procurement, scheduling, and pricing. Each benchmark is designed to be scalable in difficulty, allowing for the assessment of LLM agents across a range of complexities. The paper evaluates the performance of various LLM agents, including state-of-the-art models like GPT-5 and Gemini 2.5 Pro, and provides insights into their abilities to learn and strategize in these economic settings.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. EconAgentBench provides a novel and relevant set of benchmarks for evaluating LLM agents in economic decision-making tasks, which is a growing area of interest.
2. The benchmarks are designed with scalable difficulty, which is crucial for testing the limits of current LLMs and for future-proofing the benchmarks against rapid advancements in LLM capabilities.
3. The paper includes evaluations of cutting-edge LLM agents, offering a snapshot of the current state of the art in this domain.
4. The authors provide economically meaningful insights derived from the benchmark results, which can inform the development of more capable LLM agents for economic applications.

### Weaknesses

#### Some Related Works


#### comment

1. The paper could benefit from a more detailed comparison with existing benchmarks, highlighting the unique contributions of EconAgentBench.
2. While the paper mentions the use of synthetic data, it could elaborate on the implications of this choice for the generalizability of the results to real-world economic scenarios.
3. The analysis of the LLM agents' behavior could be more in-depth, particularly regarding the strategies they employ and the reasons behind their successes and failures.

### Suggestions

The paper would be significantly strengthened by a more thorough comparison to existing benchmarks. While the authors mention that their work is concurrent with VendingBench, a deeper analysis is needed to clarify the specific advantages of EconAgentBench. For example, a detailed comparison of the task complexity, the types of economic reasoning required, and the evaluation metrics used in both benchmarks would be beneficial. This comparison should not only highlight the differences but also discuss the potential trade-offs. For instance, does the multi-turn nature of EconAgentBench introduce complexities that are not present in single-turn benchmarks, and how does this impact the evaluation of LLM agents? Furthermore, the authors should discuss how the choice of tasks (procurement, scheduling, and pricing) reflects the broader landscape of economic decision-making and whether these tasks are representative of real-world economic challenges. A more detailed discussion of the limitations of existing benchmarks and how EconAgentBench addresses these limitations would also be valuable.

Regarding the use of synthetic data, the paper should provide a more detailed analysis of the potential limitations and biases introduced by this approach. While synthetic data allows for controlled experiments and scalability, it is crucial to address the question of how well the results generalize to real-world economic scenarios. The authors should discuss the specific parameters used to generate the synthetic data and how these parameters might affect the behavior of LLM agents. For example, do the distributions of costs, budgets, and demands in the synthetic data reflect real-world distributions, and how might deviations from these distributions impact the performance of LLM agents? Furthermore, the authors should consider the potential for overfitting to the synthetic data and discuss strategies for mitigating this risk. This could include techniques such as data augmentation or the use of more diverse synthetic data sets. A discussion of the limitations of synthetic data and the potential for future work using real-world data would also be beneficial.

Finally, the analysis of LLM agent behavior needs to be more detailed and insightful. The paper should go beyond simply reporting performance metrics and delve into the specific strategies employed by the LLM agents. For example, in the procurement task, do the agents exhibit any specific patterns in their purchasing decisions, and how do these patterns relate to the underlying economic principles? In the scheduling task, do the agents use any specific algorithms or heuristics to find stable matchings, and how do these strategies compare to known algorithms? In the pricing task, do the agents adapt their pricing strategies over time, and how do these adaptations relate to the observed market dynamics? The authors should also discuss the reasons behind the successes and failures of the LLM agents, providing a more nuanced understanding of their capabilities and limitations. This could include an analysis of the agents' exploration strategies, their ability to learn from feedback, and their capacity for long-term planning. A more detailed analysis of the agents' behavior would provide valuable insights for the development of more capable LLM agents for economic applications.

### Questions

1. How do the authors ensure that the synthetic environments accurately reflect the complexities of real-world economic scenarios?
2. Can the authors provide more details on the computational resources required to run these benchmarks, especially at the highest difficulty levels?
3. How do the authors plan to update the benchmarks as LLM technology continues to advance?

### Rating

6

### Confidence

3

**********