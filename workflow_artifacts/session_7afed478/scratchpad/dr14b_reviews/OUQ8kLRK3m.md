### Summary

This paper introduces a new benchmark for evaluating the fluid intelligence of large language models (LLMs). The benchmark is based on a hierarchical cognitive framework and consists of 36 abstract reasoning tasks organized across four cognitive levels. The authors evaluate several state-of-the-art LLMs on this benchmark and find that most LLMs struggle with high-level cognition and exhibit limited generalization as task complexity grows.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

- The paper proposes a new benchmark for evaluating the fluid intelligence of LLMs, which is a novel and important contribution to the field.
- The benchmark is based on a hierarchical cognitive framework, which provides a more structured and comprehensive system for analyzing the reasoning abilities of LLMs.
- The paper develops a verifiable and scalable data engine to dynamically generate abstract reasoning data with various complexities, which is a significant technical innovation.
- The paper performs comprehensive evaluations on a variety of popular LLMs, providing valuable insights into the current capabilities of LLMs in abstract reasoning.

### Weaknesses

#### Some Related Works


#### comment

 - The paper does not provide a detailed analysis of the limitations of the proposed benchmark. It would be beneficial to discuss potential biases or limitations in the benchmark design that could affect the evaluation results.
- The paper could benefit from a more thorough comparison with existing benchmarks for evaluating LLMs' reasoning capabilities. This would help to contextualize the contributions of DRE-Bench and highlight its unique advantages and disadvantages.
- The paper does not discuss the potential for using DRE-Bench to guide the development of more intelligent LLMs. It would be valuable to explore how the benchmark could be used to identify areas where LLMs need improvement and to track progress in reasoning capabilities over time.

### Suggestions

The authors should provide a more detailed analysis of potential biases within DRE-Bench. For example, the benchmark might inadvertently favor models that are better at specific types of visual reasoning or those that have been pre-trained on datasets with similar structures. A thorough investigation into how different model architectures and pre-training strategies might interact with the benchmark is needed. This could involve analyzing the performance of various models across different task categories within DRE-Bench to identify any systematic biases. Furthermore, the authors should consider the impact of prompt engineering on the results. It is possible that certain prompts might elicit better performance from specific models, which could skew the overall evaluation. A systematic study of prompt sensitivity would be beneficial to ensure the robustness of the benchmark.

To better contextualize DRE-Bench, the authors should provide a more detailed comparison with existing benchmarks. This comparison should go beyond simply listing the differences in task types and should delve into the underlying assumptions and evaluation methodologies of each benchmark. For example, how does DRE-Bench compare to benchmarks that focus on symbolic reasoning or those that evaluate common-sense reasoning? A detailed analysis of the strengths and weaknesses of each benchmark would help to clarify the unique contributions of DRE-Bench. This comparison should also include a discussion of the types of reasoning skills that are not covered by DRE-Bench, which would help to identify areas for future research and development.

Finally, the authors should explore how DRE-Bench can be used to guide the development of more intelligent LLMs. This could involve using the benchmark to identify specific areas where models struggle and then developing targeted training strategies to address these weaknesses. For example, if models consistently perform poorly on tasks that require multi-step reasoning, then the benchmark could be used to develop new training data or architectures that specifically address this issue. The authors should also consider how DRE-Bench can be used to track progress in reasoning capabilities over time. This could involve periodically re-evaluating models on the benchmark as they are updated and then analyzing the changes in performance. This would provide a valuable way to measure the progress of the field and to identify areas where further research is needed.

### Questions

Please see the weaknesses.

### Rating

6

### Confidence

4

**********