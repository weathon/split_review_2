### Summary

This paper investigates the effects of compression techniques on Large Reasoning Models (LRMs), focusing on quantization, distillation, and pruning. The authors benchmark compressed DeepSeek-R1 models on four reasoning datasets and use mechanistic interpretability to identify which weights are crucial for reasoning. Key findings include that weight count impacts knowledge retention more than reasoning, specific components in the final layer are vital for distilled models, and protecting certain weights in quantized models can significantly improve accuracy.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper is well-organized and easy to follow, with clear explanations of the methodology and findings.
2. The study benchmarks multiple compression techniques (quantization, distillation, and pruning) on various reasoning datasets, providing a comprehensive view of their effects on model performance.
3. The authors use mechanistic interpretability techniques to identify the importance of different weight matrices, offering insights into which components are crucial for reasoning.

### Weaknesses

#### Some Related Works


#### comment

1. The study focuses on a specific model family (DeepSeek-R1) and its distilled variants, which may limit the generalizability of the findings to other LRMs. The lack of experiments on other model architectures, such as those with different attention mechanisms or pre-training objectives, makes it difficult to ascertain whether the observed trends are specific to the DeepSeek-R1 family or more broadly applicable to LRMs in general. For example, models like LLaMA or Qwen, which have different architectural designs and training procedures, could exhibit different sensitivity to compression techniques.
2. The mechanistic interpretability analysis relies on specific techniques (difference of means and attribution patching) that may not capture the full complexity of reasoning processes in LRMs. These methods, while useful, primarily focus on the contribution of individual weights or small groups of weights, potentially overlooking more complex interactions and dependencies within the network. For instance, reasoning might rely on specific patterns of activation across multiple layers, which these techniques might not fully capture. Furthermore, the choice of baseline for attribution patching can significantly influence the results, and the paper does not fully explore the sensitivity of the findings to different baselines.

### Suggestions

To strengthen the generalizability of the findings, the authors should expand their experiments to include a more diverse set of LRM architectures. This could involve testing models with different attention mechanisms (e.g., sparse attention), varying numbers of layers, or different pre-training datasets. Specifically, including models like LLaMA or Qwen, which have different architectural designs and training procedures, would provide a more robust assessment of the impact of compression techniques on reasoning capabilities. Furthermore, the authors should consider exploring models with different pre-training objectives, as this could influence the sensitivity of the model to compression. Such an analysis would help determine whether the observed trends are specific to the DeepSeek-R1 family or more broadly applicable to LRMs in general. This would also help to identify any architectural biases that might influence the effectiveness of different compression techniques.

To address the limitations of the mechanistic interpretability analysis, the authors should consider incorporating additional techniques that can capture more complex interactions within the network. For example, methods like Integrated Gradients or SHAP values could provide a more comprehensive view of the importance of different weights and their interactions. Furthermore, the authors should explore the sensitivity of their findings to different baselines used in attribution patching. This could involve testing different baseline inputs or using a distribution of baselines to assess the robustness of the results. Additionally, the authors could investigate the impact of compression on the activation patterns of different layers, which might provide insights into how compression affects the flow of information within the network. This could involve visualizing the activation patterns or using techniques like representational similarity analysis to compare the activations of compressed and uncompressed models.

Finally, the authors should provide a more detailed analysis of the specific reasoning tasks used in their experiments. It would be beneficial to categorize these tasks based on their complexity and the type of reasoning they require (e.g., logical reasoning, mathematical reasoning, common-sense reasoning). This would allow for a more nuanced understanding of how compression affects different types of reasoning. For example, it is possible that compression has a greater impact on tasks that require multi-step reasoning or those that rely on specific types of knowledge. By analyzing the performance of compressed models on different categories of reasoning tasks, the authors could provide more targeted insights into the strengths and weaknesses of different compression techniques.

### Questions

1. How do the findings generalize to other LLMs that are not part of the R1 family?
2. Could the authors provide more details on the specific reasoning tasks used in the benchmarking? How do they ensure that these tasks comprehensively cover the range of reasoning capabilities expected of LRMs?

### Rating

6

### Confidence

3

**********