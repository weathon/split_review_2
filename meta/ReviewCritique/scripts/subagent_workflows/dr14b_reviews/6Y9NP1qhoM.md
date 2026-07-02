### Summary

This paper introduces a novel dataset and a training-free framework for mitigating the spread of misinformation in multi-agent LLM systems. The proposed dataset includes complex, realistic tasks designed to evaluate the robustness of MAS against misinformation threats. The authors also propose a two-stage defense framework, ARGUS, which leverages goal-aware reasoning to identify and rectify misinformation in information flows. Experimental results show that ARGUS significantly reduces misinformation toxicity and improves task success rates under various injection attacks.

### Soundness

2

### Presentation

2

### Contribution

2

### Strengths

1. The paper addresses a critical and underexplored area in multi-agent LLM systems, specifically the propagation of misinformation, which is distinct from and often more insidious than overtly malicious attacks.
2. The introduction of the MISINFOTASK dataset is a significant contribution, providing a benchmark for evaluating misinformation defenses in MAS.
3. The proposed ARGUS framework is innovative, combining adaptive localization of misinformation channels with goal-aware persuasive rectification.
4. The paper provides a thorough evaluation of ARGUS across different attack methods and LLM architectures, demonstrating its effectiveness and generalizability.

### Weaknesses

#### Some Related Works


#### comment

1. The paper could benefit from a more detailed discussion of the limitations of the proposed approach, particularly in terms of scalability to very large MAS and robustness against more sophisticated misinformation attacks.
2. The evaluation metrics, while generally well-defined, could be further refined to capture more nuanced aspects of misinformation impact, such as the long-term effects on agent behavior and system performance.
3. The writing is generally good, but some sections, particularly the technical details of the ARGUS framework, could be more clearly explained to enhance readability and understanding.

### Suggestions

The paper should delve deeper into the practical limitations of the ARGUS framework, especially concerning its scalability to large-scale multi-agent systems. While the current evaluation includes a 5x5 MAS, it is crucial to analyze how the computational overhead of the corrective agent scales with the number of agents and the complexity of the communication graph. Specifically, the paper should provide a detailed analysis of the time and space complexity of the edge betweenness centrality calculation, which is a key component of the adaptive localization mechanism. Furthermore, the authors should explore potential optimization strategies, such as approximation algorithms for betweenness centrality or distributed monitoring approaches, to mitigate the computational burden in large MAS. The paper should also consider the impact of network dynamics, such as changing communication patterns and agent failures, on the effectiveness of the proposed defense mechanism. A more thorough discussion of these practical challenges would significantly enhance the paper's contribution.

To address the limitations of the evaluation metrics, the authors should consider incorporating metrics that capture the long-term effects of misinformation on agent behavior and system performance. For example, the paper could explore the use of metrics that measure the persistence of misinformation-induced biases in agent beliefs, even after the corrective agent has intervened. This could involve analyzing the evolution of agent beliefs over time and assessing whether agents continue to exhibit skewed reasoning or decision-making patterns. Additionally, the paper should consider the impact of misinformation on the overall trust and cooperation within the multi-agent system. Metrics that quantify the level of trust between agents and the degree of cooperation in achieving common goals would provide a more comprehensive evaluation of the system's resilience to misinformation. The authors should also explore the potential for cascading effects, where misinformation propagates through the system and triggers a chain of negative consequences. A more nuanced evaluation framework would provide a more complete picture of the impact of misinformation on multi-agent systems.

The paper should also provide a more detailed explanation of the technical details of the ARGUS framework, particularly the adaptive localization and goal-aware persuasive rectification mechanisms. The current description of the adaptive localization mechanism lacks sufficient detail, making it difficult to understand how the corrective agent identifies and monitors critical misinformation propagation channels. The authors should provide a more precise definition of the edge betweenness centrality calculation and explain how it is used to determine the most influential communication channels. Similarly, the explanation of the goal-aware persuasive rectification mechanism is somewhat vague. The paper should provide more details on how the corrective agent identifies suspicious elements in messages, resonates with internal knowledge, and reconstructs persuasive corrective statements. A more detailed and step-by-step explanation of these mechanisms would significantly improve the readability and understanding of the paper.

### Questions

1. How does the performance of ARGUS scale with the size and complexity of the MAS? Are there any computational bottlenecks or limitations in deploying ARGUS in very large systems?
2. The paper focuses on a specific set of misinformation injection attacks. How robust is ARGUS against more sophisticated or adaptive attacks that might evolve in response to the defense mechanism?
3. The paper mentions that the corrective agent uses CoT prompting to guide its analysis and intervention. Can you provide more details on the specific CoT prompts used and how they were designed to effectively identify and rectify misinformation?
4. How does the choice of the three importance scores (topological importance, information relevance, and usage frequency) impact the performance of ARGUS? Is there a sensitivity analysis to determine the optimal weighting of these scores?
5. The paper discusses the adaptive re-localization of the corrective agent. How quickly can ARGUS adapt to changes in the misinformation strategy or the MAS topology?
6. Can you provide more details on the ablation study mentioned in the paper? It would be interesting to see how the removal of different components of ARGUS affects its overall performance.
7. The paper focuses on mitigating misinformation. How does ARGUS interact with other potential security threats in MAS, such as malicious agents or data breaches?
8. The paper mentions that the dataset includes tasks from various domains. Can you provide more details on the diversity of these tasks and how they were designed to reflect real-world challenges in MAS?
9. How does the performance of ARGUS vary across different LLM architectures? Are there any specific architectures where ARGUS performs particularly well or poorly?
10. The paper discusses the use of an LLM judge to evaluate the outputs. How reliable is this evaluation method, and are there any potential biases in the LLM's scoring?

### Rating

5

### Confidence

4

**********