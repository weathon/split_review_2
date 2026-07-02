### Summary

The paper introduces Agentic Reinforced Policy Optimization (ARPO), a novel reinforcement learning algorithm designed to enhance the performance of multi-turn, LLM-based agents. The authors identify that LLMs experience increased uncertainty, indicated by higher entropy, after utilizing tools in reasoning tasks. To address this, ARPO employs an entropy-based adaptive rollout mechanism, which encourages the model to explore alternative reasoning paths during high-entropy tool-use steps. This mechanism allows for more fine-grained, step-level exploration of tool-use behaviors. Additionally, ARPO incorporates advantage attribution estimation, enabling the model to better understand the effectiveness of different tool-use interactions. The authors conducted experiments across 13 challenging benchmarks, demonstrating that ARPO outperforms traditional trajectory-level RL algorithms, achieving better performance with only half the tool-use budget. The paper also provides theoretical justification for the ARPO algorithm, highlighting its adaptability in multi-turn training scenarios for LLM-based agents.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

The paper introduces a novel approach to reinforcement learning for LLM-based agents, specifically addressing the challenge of tool use in multi-turn reasoning tasks. The proposed Agentic Reinforced Policy Optimization (ARPO) algorithm is innovative in its use of an entropy-based adaptive rollout mechanism, which allows for more fine-grained exploration of tool-use behaviors at the step level. This is a significant departure from traditional trajectory-level RL methods, and the authors provide a clear motivation for this approach. The integration of advantage attribution estimation further enhances the algorithm's ability to learn effective tool-use strategies. The theoretical analysis provided in the paper strengthens the proposed approach, demonstrating its adaptability in multi-turn training scenarios. The empirical evaluation of ARPO is comprehensive, with experiments conducted across 13 challenging benchmarks. The results demonstrate that ARPO consistently outperforms existing methods, achieving better performance with only half the tool-use budget. This highlights the efficiency and effectiveness of the proposed algorithm. Overall, the paper makes a significant contribution to the field of reinforcement learning for LLM-based agents, offering a novel and effective approach to training multi-turn agents with tool use.

### Weaknesses

#### Some Related Works


#### comment

While the paper presents a novel and promising approach, there are several areas where further clarification and analysis could strengthen the work. The paper could benefit from a more detailed analysis of the computational complexity of the ARPO algorithm compared to existing methods. While the authors mention that ARPO achieves better performance with only half the tool-use budget, they do not provide a thorough analysis of the computational cost associated with the entropy-based adaptive rollout mechanism. Specifically, the paper lacks a detailed breakdown of the time complexity of calculating token-level entropy and how this scales with the number of tool-use steps and the size of the language model. A comparison of the computational cost of ARPO with other RL algorithms, such as REINFORCE++ and GRPO, in terms of FLOPS or wall-clock time, would be beneficial to understand the practical trade-offs of the proposed method. Furthermore, the paper does not discuss the memory requirements of ARPO, which could be a limiting factor for large-scale applications. A more detailed analysis of the memory footprint of the algorithm, particularly during the adaptive rollout phase, would be valuable. Additionally, providing insights into the sensitivity of the algorithm to hyperparameter settings, such as the entropy threshold for branching, would enhance the practical applicability of the method. The paper also lacks a discussion of the potential limitations of the entropy-based exploration strategy. For example, it is unclear how the algorithm would perform in scenarios where the entropy is not a reliable indicator of uncertainty or where the optimal policy requires exploring low-entropy actions. A more thorough analysis of these limitations would provide a more balanced view of the proposed method. Finally, while the paper demonstrates the effectiveness of ARPO across 13 benchmarks, a more detailed analysis of the performance differences across these benchmarks would be beneficial. Specifically, it would be useful to understand why ARPO performs better on some tasks than others and whether there are specific characteristics of the tasks that make them more or less suitable for the proposed method.

### Suggestions

To strengthen the paper, the authors should provide a more detailed analysis of the computational complexity of the ARPO algorithm. This should include a breakdown of the time complexity of each component of the algorithm, particularly the entropy calculation and the adaptive rollout mechanism. The analysis should consider how the computational cost scales with the number of tool-use steps, the size of the language model, and the number of samples used for training. A comparison of the computational cost of ARPO with other RL algorithms, such as REINFORCE++ and GRPO, in terms of FLOPS or wall-clock time, would be beneficial. Furthermore, the authors should discuss the memory requirements of ARPO, including the memory footprint during the adaptive rollout phase. This analysis should consider the memory needed to store the policy network, the value function, and the entropy estimates. It would also be helpful to provide an analysis of the sensitivity of the algorithm to hyperparameter settings, such as the entropy threshold for branching. This could be done by conducting experiments with different hyperparameter values and analyzing the impact on the performance of the algorithm. This analysis should also include a discussion of how these hyperparameters should be tuned for different tasks and datasets. 

Additionally, the authors should discuss the potential limitations of the entropy-based exploration strategy. This should include an analysis of scenarios where the entropy is not a reliable indicator of uncertainty or where the optimal policy requires exploring low-entropy actions. The authors could consider alternative exploration strategies, such as Thompson sampling or upper confidence bound (UCB), and discuss how these strategies could be integrated into the ARPO framework. It would also be beneficial to provide a more detailed analysis of the performance differences across the 13 benchmarks used in the experiments. This analysis should include a discussion of the characteristics of the tasks that make them more or less suitable for the proposed method. For example, the authors could analyze the complexity of the tool-use interactions required for each task and how this relates to the performance of ARPO. This analysis could also include a discussion of the types of errors that ARPO makes on different tasks and how these errors could be addressed in future work. 

Finally, the authors should consider providing more practical guidance on how to implement the ARPO algorithm. This could include a discussion of the software and hardware requirements for running the algorithm, as well as practical tips for debugging and optimizing the implementation. The authors could also consider releasing the source code for the algorithm, which would allow other researchers to reproduce their results and build upon their work. This would also facilitate a more thorough evaluation of the algorithm by the research community. By addressing these points, the authors can significantly enhance the practical applicability and impact of their work.

### Questions

1. Could the authors provide a more detailed analysis of the computational complexity of the ARPO algorithm compared to existing methods? Specifically, how does the entropy-based adaptive rollout mechanism impact the overall training time and resource requirements? 
3. How sensitive is the ARPO algorithm to the choice of hyperparameters, such as the entropy threshold for branching? Are there any guidelines or best practices for tuning these parameters in different scenarios? 
2. Can the authors discuss the potential limitations of the entropy-based exploration strategy? Are there scenarios where this approach might not be effective, and if so, how could these be addressed?

### Rating

6

### Confidence

3

**********