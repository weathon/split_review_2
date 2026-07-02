### Summary

This paper introduces LoRA-Mixer, a novel framework that integrates Low-Rank Adaptation (LoRA) with a mixture-of-experts (MoE) architecture for efficient multi-task adaptation of Large Language Models (LLMs). Unlike traditional approaches that replace entire attention or FFN layers with switch experts, LoRA-Mixer routes task-specific LoRA experts into the core projection matrices of the attention module (input/output linear layers). This design enables fine-grained token-level specialization by leveraging the attention mechanism, while maintaining compatibility with both Transformers and state-space models (SSMs). To train robust routers from limited data, LoRA-Mixer employs an adaptive Routing Specialization Loss (RSL) that enforces global load balance and input-aware specialization through an entropy-shaping objective. The framework supports two regimes: joint optimization of adapters and router, and plug-and-play routing over frozen, pre-trained LoRA modules. Experiments across 15 benchmarks demonstrate that RSL-optimized LoRA-Mixer outperforms state-of-the-art routing and LoRA-MoE baselines with significantly fewer trainable parameters. Cross-model transfer and adapter reuse experiments further highlight the approach's versatility and data efficiency.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper is well-written and easy to follow.
2. The idea of integrating LoRA with MoE is novel.
3. The experiments are comprehensive and convincing.

### Weaknesses

#### Some Related Works


#### comment

1. The proposed method is only evaluated on small LLMs. It would be better to evaluate the proposed method on larger LLMs (e.g., 70B).
2. The proposed method is only evaluated on English tasks. It would be better to evaluate the proposed method on more languages.

### Suggestions

The paper presents a novel approach to integrating LoRA with MoE, which is a promising direction for efficient adaptation of LLMs. However, the evaluation is limited to relatively small models and English-only tasks. To strengthen the paper, it is crucial to demonstrate the scalability of the proposed method to larger models, such as those with 70B parameters or more. This is important because the behavior of MoE architectures can change significantly as the model size increases, and it is not clear if the observed performance gains would hold for larger models. Furthermore, the routing mechanism might require adjustments to handle the increased complexity of larger models. Therefore, future work should include experiments on larger models to validate the robustness and scalability of the proposed approach. This would involve not only training the model but also analyzing the routing behavior and the impact of the routing loss on the overall performance.

In addition to scaling the model size, it is also important to evaluate the proposed method on a more diverse set of languages. The current evaluation is limited to English tasks, which might not be representative of the performance of the method in other languages. Different languages have different linguistic structures and characteristics, which can affect the performance of the model. Therefore, it is important to evaluate the method on a variety of languages to ensure that it is not biased towards English. This would involve training and evaluating the model on datasets in different languages, and analyzing the performance differences across languages. This would provide a more comprehensive understanding of the strengths and limitations of the proposed method.

Finally, while the paper introduces a novel routing loss, it would be beneficial to provide more insights into the behavior of this loss. Specifically, it would be helpful to analyze how the routing loss affects the distribution of tokens across different experts, and how this distribution changes during training. This analysis could provide a better understanding of the inner workings of the proposed method and help to identify potential areas for improvement. Furthermore, it would be useful to compare the proposed routing loss with other routing losses used in MoE architectures, and to analyze the advantages and disadvantages of each approach. This would provide a more comprehensive understanding of the proposed method and its relationship to existing approaches.

### Questions

1. What is the difference between the proposed routing loss and the auxiliary loss in Eq. (3)?

### Rating

6

### Confidence

4

**********