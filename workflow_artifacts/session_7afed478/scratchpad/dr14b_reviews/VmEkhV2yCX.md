### Summary

This paper investigates the impact of reasoning data introduced at different stages of training large language models (LLMs), specifically pretraining and supervised fine-tuning (SFT). The authors systematically vary the scale, diversity, and quality of reasoning data to determine its effect on LLM performance. Their findings reveal that front-loading reasoning data during pretraining establishes foundational capabilities that cannot be fully replicated by SFT alone, even with more data. They also find that pretraining benefits most from broad diversity in reasoning patterns, while SFT is more sensitive to data quality. The study challenges the conventional separation of language modeling and reasoning, providing a principled guide for strategically allocating data across the entire training pipeline to build more capable models.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper presents a novel and systematic investigation into the impact of reasoning data introduced at different stages of training, addressing a critical gap in the understanding of how to best leverage reasoning data for LLMs. The study's focus on the interplay between pretraining and SFT is particularly innovative, as it challenges the conventional separation of language modeling and reasoning.

2. The methodology is rigorous and well-designed. The authors carefully control for various factors, such as the scale, diversity, and quality of reasoning data, and conduct experiments across multiple stages of training (pretraining, SFT, and RL). The use of a hybrid transformer architecture with a mixture of Mamba 2, self-attention, and FFN layers adds to the robustness of the experimental setup. The paper also provides detailed descriptions of the datasets used, the training procedures, and the evaluation metrics, ensuring reproducibility.

3. The findings are significant and have practical implications for the development of LLMs. The discovery that front-loading reasoning data during pretraining is crucial for establishing foundational reasoning capabilities provides valuable insights for practitioners. The asymmetric principle for optimal data allocation—prioritizing diversity in pretraining and quality in SFT—offers a clear and actionable guide for data strategy. The demonstration that high-quality pretraining data can have latent effects, activated only after SFT, and that naively scaling SFT data can be detrimental, further enriches the understanding of the training process.

### Weaknesses

#### Some Related Works


#### comment

1. While the paper provides a comprehensive analysis of the impact of reasoning data, it could benefit from a more detailed discussion of the limitations of the study. For instance, the paper does not extensively explore the potential for overfitting when introducing reasoning data at different stages, especially in the pretraining phase. A more thorough investigation into how the model's generalization capabilities are affected by the timing and nature of reasoning data injection would strengthen the paper's conclusions. Specifically, the paper should investigate the impact of reasoning data on out-of-distribution generalization, and whether the observed gains are consistent across different reasoning tasks. It would be beneficial to see an analysis of the model's performance on tasks that require different types of reasoning, such as inductive, deductive, and abductive reasoning, to understand the scope of the findings.

2. The paper could also benefit from a more in-depth analysis of the computational costs associated with the proposed strategies. While the authors mention the computational feasibility of their experiments, a detailed breakdown of the resources required for each stage of training, especially when scaling up the model size or the amount of reasoning data, would be valuable for practitioners. This includes not only the training time and memory requirements, but also the inference costs associated with the different training strategies. A comparison of the computational costs of front-loading reasoning data versus introducing it later in the training process would be particularly useful.

### Suggestions

To address the limitations regarding overfitting and generalization, the authors should conduct a more rigorous analysis of the model's performance on out-of-distribution reasoning tasks. This could involve evaluating the model on datasets that are significantly different from the training data, both in terms of domain and the type of reasoning required. For example, if the training data primarily focuses on mathematical reasoning, the model should be evaluated on tasks that require common-sense reasoning, logical inference, or causal reasoning. Furthermore, the authors should investigate the impact of different regularization techniques, such as dropout or weight decay, on the model's generalization capabilities when reasoning data is introduced at different stages. This would help to determine whether the observed gains are robust or whether they are due to overfitting to the specific training data. It would also be beneficial to analyze the model's performance on a range of reasoning tasks with varying levels of complexity to understand the limitations of the proposed approach.

To provide a more comprehensive understanding of the computational costs, the authors should include a detailed analysis of the resources required for each stage of training. This should include not only the training time and memory requirements, but also the inference costs associated with the different training strategies. A comparison of the computational costs of front-loading reasoning data versus introducing it later in the training process would be particularly useful. This analysis should also consider the impact of different model sizes and the amount of reasoning data on the computational costs. For example, the authors could investigate how the training time and memory requirements scale with the number of parameters and the size of the reasoning dataset. This would provide valuable insights for practitioners who need to balance the performance gains with the available computational resources. Furthermore, the authors should explore the use of techniques such as model compression or knowledge distillation to reduce the computational costs of the proposed approach.

Finally, the authors should provide a more detailed analysis of the types of reasoning that are most effectively improved by front-loading reasoning data during pretraining. This could involve analyzing the model's performance on different reasoning tasks, such as mathematical reasoning, logical inference, and common-sense reasoning, to understand which types of reasoning are most sensitive to the timing of reasoning data injection. This analysis should also consider the impact of different types of reasoning data on the model's performance. For example, the authors could investigate whether the model benefits more from reasoning data that is explicitly labeled or from reasoning data that is implicitly present in the text. This would provide valuable insights for practitioners who need to select the most appropriate reasoning data for their specific application.

### Questions

1. How does the model's performance on reasoning tasks change when the reasoning data is introduced in a more gradual manner during pretraining, rather than all at once? Is there an optimal schedule for introducing reasoning data during pretraining?

2. The paper focuses on the impact of reasoning data on the model's performance on reasoning tasks. How does the introduction of reasoning data at different stages of training affect the model's performance on other types of tasks, such as natural language understanding, generation, and dialogue? Is there a trade-off between reasoning capabilities and other language abilities?

3. The study uses a specific hybrid transformer architecture with a mixture of Mamba 2, self-attention, and FFN layers. How do the findings generalize to other model architectures, such as those based solely on self-attention or other types of recurrent layers? Are there certain architectural features that make a model more or less receptive to front-loading reasoning data?

4. The paper mentions that naively scaling SFT data can be detrimental. What are the underlying reasons for this phenomenon? Is it due to the introduction of noisy or irrelevant data, or is there a more fundamental issue with the way the model learns from large amounts of SFT data?

### Rating

6

### Confidence

3

**********