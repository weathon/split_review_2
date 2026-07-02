### Summary

The paper introduces a novel framework called Planner-Composer-Evaluator (PCE) that aims to improve the performance of embodied agents in multi-agent, partially observable, and decentralized environments. The key idea is to convert the fragmented assumptions latent in LLM reasoning traces into a structured decision tree, which allows for more efficient action selection under uncertainty. The framework is evaluated on two challenging multi-agent benchmarks and demonstrates consistent outperformance over communication-centric baselines in terms of success rate and task efficiency, while maintaining comparable token usage. Ablation studies and a user study further validate the effectiveness of the proposed approach.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper presents a novel approach to handling uncertainty in multi-agent embodied agent tasks by leveraging the latent assumptions in LLM reasoning traces. This is a creative combination of existing ideas (LLM reasoning, decision trees) that results in a new and effective method.
2. The empirical evaluation is thorough and well-designed. The experiments on two multi-agent benchmarks (C-WAH and TDW-MAT) with three different LLM backbones provide strong evidence for the effectiveness of the proposed framework. The ablation studies and user study further strengthen the claims made in the paper.
3. The paper is generally well-written and easy to follow. The figures and tables are clear and informative, and the technical details are presented in a clear and concise manner.

### Weaknesses

#### Some Related Works


#### comment

1. The paper lacks a detailed analysis of the failure cases of the proposed framework. It would be beneficial to understand the limitations of the approach and the scenarios where it might not perform well. Specifically, the paper does not explore the types of errors made by the Planner, Composer, or Evaluator modules, nor does it analyze how these errors propagate through the system. A more granular analysis of failure modes, such as incorrect assumption generation, flawed decision tree construction, or inaccurate evaluation of action sequences, would be valuable.
2. The paper does not provide a thorough comparison with other uncertainty-aware planning methods that do not rely on LLMs. This makes it difficult to assess the relative advantages and disadvantages of the proposed approach compared to existing techniques. For instance, methods based on probabilistic planning or belief space search could offer alternative approaches to handling uncertainty, and a comparison with these methods would help to contextualize the performance of PCE.
3. The paper does not discuss the potential for bias in the LLM reasoning traces and how this might affect the performance of the framework. Since LLMs are known to exhibit biases, it is important to consider how these biases might influence the generated assumptions and the resulting decision tree. The paper should explore whether certain types of assumptions are favored over others, and how this might lead to suboptimal planning outcomes.

### Suggestions

To address the lack of failure case analysis, the authors should include a detailed breakdown of the types of errors made by each module of the PCE framework. This should include specific examples of scenarios where the Planner generates incorrect assumptions, where the Composer builds a flawed decision tree, and where the Evaluator makes inaccurate assessments. For example, the authors could analyze cases where the Planner fails to identify a critical uncertainty, leading to a suboptimal path in the decision tree. They could also examine instances where the Composer creates a decision tree that is too complex or too simplistic, resulting in inefficient action selection. Furthermore, the authors should investigate how errors in one module propagate to other modules, and how this affects the overall performance of the system. This analysis should be supported by quantitative data, such as the frequency of different error types, and should provide insights into the limitations of the proposed approach.

To provide a more comprehensive comparison with existing methods, the authors should include a detailed analysis of uncertainty-aware planning techniques that do not rely on LLMs. This should include methods based on probabilistic planning, such as Partially Observable Markov Decision Processes (POMDPs), or belief space search algorithms. The comparison should focus on the strengths and weaknesses of each approach, highlighting the advantages of PCE in terms of its ability to leverage LLM reasoning, while also acknowledging the limitations of LLM-based methods. The authors should also discuss the computational complexity of each method, and how this affects its scalability. This comparison should be supported by experimental results, where possible, and should provide a clear understanding of the relative performance of PCE compared to existing techniques.

To address the potential for bias in LLM reasoning, the authors should conduct a thorough analysis of the generated assumptions and their impact on the decision tree. This should include an investigation of whether certain types of assumptions are favored over others, and how this might lead to suboptimal planning outcomes. The authors should also explore techniques for mitigating bias, such as using diverse training data or incorporating fairness constraints into the LLM prompting strategy. Furthermore, the authors should discuss the ethical implications of using LLMs in embodied agents, and how these implications might affect the deployment of the proposed framework. This analysis should be supported by quantitative data, such as the frequency of different types of assumptions, and should provide insights into the potential for bias in the system.

### Questions

1. How does the performance of the PCE framework scale with the number of agents and the complexity of the environment? Are there any limitations in terms of the size or complexity of the tasks that can be handled by the proposed approach?
2. How sensitive is the performance of the PCE framework to the choice of hyperparameters, such as the depth of the decision tree or the parameters used in the Evaluator? Are there any guidelines for selecting appropriate hyperparameter values for different tasks or environments?
3. Can the proposed framework be extended to handle more complex forms of uncertainty, such as uncertainty about the goals or intentions of other agents? How would this affect the design of the Planner, Composer, and Evaluator modules?

### Rating

6

### Confidence

3

**********