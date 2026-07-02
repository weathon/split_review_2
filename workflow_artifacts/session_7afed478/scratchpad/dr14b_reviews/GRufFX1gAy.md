### Summary

The paper introduces InnoGym, a benchmark and framework designed to evaluate the innovation potential of AI agents. It addresses the limitations of existing benchmarks that primarily focus on correctness by introducing two metrics: performance gain and novelty. The benchmark includes 18 tasks from real-world engineering and scientific domains, and a unified execution environment, iGym, is provided for reproducible evaluations. Experiments reveal that while some agents produce novel approaches, their lack of robustness limits performance gains, highlighting a gap between creativity and effectiveness.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a novel benchmark and framework (InnoGym) for evaluating the innovation potential of AI agents, addressing a gap in existing benchmarks that primarily focus on correctness.
2. The authors provide a well-defined task framework and clear metrics for assessing innovation, contributing valuable insights into the creative and performance capabilities of AI agents.
3. The paper is well-structured and clearly written, making it accessible to a broad audience.

### Weaknesses

#### Some Related Works


#### comment

1. The paper's main weakness lies in its reliance on the GPT-5 model for evaluating novelty, which raises concerns about the objectivity and accuracy of the novelty scores. Additionally, the complexity of the InnoGym framework and the limited analysis of its computational requirements may hinder its practical implementation and scalability.

2. The entire evaluation of N depends on GPT-5, which is very strange to me. The authors should at least include multiple LLMs to provide an inter-quartile range for the N score.

3. The paper does not discuss the computational resources required for implementing InnoGym, which could be a barrier for some researchers.

4. The paper does not address how the framework can be scaled to accommodate more complex tasks or a larger number of agents.

5. The paper does not discuss the potential biases that may be present in the training data of the LLMs used for novelty evaluation, which could affect the fairness of the N score.

6. The paper does not provide a detailed analysis of the cases where agents achieved high novelty but low performance gain, which could provide valuable insights into the limitations of current AI agents.

### Suggestions

The reliance on a single LLM, specifically GPT-5, for evaluating novelty is a significant concern that needs to be addressed. The authors should explore using an ensemble of LLMs, potentially including models with different architectures and training data, to generate novelty scores. This would not only provide a more robust measure of novelty but also allow for the calculation of inter-quantile ranges, giving a better sense of the uncertainty in the novelty assessment. Furthermore, the prompts used to elicit novelty judgments from these models should be carefully analyzed and validated to ensure they are not introducing biases or artifacts. It would be beneficial to include a sensitivity analysis of how different prompts affect the resulting novelty scores. The authors should also consider incorporating human evaluation as a benchmark for the LLM-based novelty scores, at least on a subset of the data, to establish the validity of the approach.

To improve the practicality and accessibility of the InnoGym framework, the authors should provide a detailed analysis of the computational resources required for its implementation. This should include not only the hardware requirements (e.g., GPU memory, CPU cores) but also the time complexity of the different components of the framework. The authors should also explore strategies for optimizing the computational efficiency of InnoGym, such as parallelization or distributed computing. Furthermore, the paper should discuss the limitations of the framework in terms of scalability and provide recommendations for how to adapt it to more complex tasks or a larger number of agents. This could involve exploring techniques for hierarchical task decomposition or using more efficient search algorithms. The authors should also consider providing a cloud-based implementation of InnoGym to make it more accessible to researchers with limited computational resources.

Finally, the paper should include a more in-depth analysis of the cases where agents achieve high novelty but low performance gain. This analysis should focus on understanding the reasons behind these results, such as whether the novel solutions are simply incorrect or if they represent valid but suboptimal approaches. The authors should also investigate whether there are specific types of tasks or agent architectures that are more prone to generating novel but low-performing solutions. This analysis could provide valuable insights into the limitations of current AI agents and guide the development of more innovative and effective AI systems. Additionally, the authors should explore methods for encouraging agents to generate solutions that are both novel and high-performing, such as using reward shaping or curriculum learning techniques.

### Questions

1. How do the authors plan to address the potential biases in the novelty evaluation process, especially given the reliance on a single LLM (GPT-5)?
2. Can the authors provide more details on the computational resources required for implementing InnoGym, and how they plan to make it more accessible to researchers with limited resources?
3. What are the authors' plans for scaling the InnoGym framework to accommodate more complex tasks or a larger number of agents?
4. Can the authors provide a more detailed analysis of the cases where agents achieved high novelty but low performance gain, and what insights can be drawn from these cases?

### Rating

6

### Confidence

4

**********