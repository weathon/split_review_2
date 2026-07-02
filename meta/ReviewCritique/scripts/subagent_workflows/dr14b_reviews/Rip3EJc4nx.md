### Summary

This paper proposes a novel structured pruning approach for large language models (LLMs), aiming to reduce their substantial computational and memory demands. Traditional pruning methods often rely on one-hot cross-entropy loss to assess neuron importance, which limits the evaluation to the probability of a single predicted token, neglecting other potential predictions. While self-distillation can be used to address this, it introduces significant computational overhead. To overcome these limitations, the authors introduce a pruning criterion based on the information entropy of the model’s output distribution. This label-free approach allows for a more comprehensive evaluation of neuron importance, minimizing the impact on the model’s global prediction distribution. Experimental results demonstrate that this method outperforms existing pruning techniques on LLaMA and Qwen series models, offering better performance and efficiency.

### Soundness

2

### Presentation

3

### Contribution

2

### Strengths

1. The paper is well-organized and clearly presented. The figures and algorithms are helpful and easy-to-understand. This paper first introduces the motivation of the method with Figure 1, which makes readers understand the method more easily.

2. The authors provide detailed experiments and analyses, validating the effectiveness of the proposed method. The paper also addresses potential issues by comparing the proposed method with other criteria.

### Weaknesses

#### Some Related Works

[1] Entropy-based pruning for self-supervised contrastive learning.
[2] Entropy and the performance of neural network models.

#### comment

1. The novelty of this paper is limited. As shown in Table 2, the proposed method achieves limited improvements over existing baselines. Given the recent surge in LLM pruning methods, the contributions of this paper are not sufficiently compelling.

2. The authors should include a more comprehensive review of existing entropy-based pruning methods, such as [1, 2], in the Related Work section.

3. The paper lacks a comparison of memory usage. A reduction in parameters does not necessarily translate to reduced memory consumption during inference. For a fair comparison, latency and memory usage should be evaluated using the same framework, such as Huggingface and FP16.

4. The paper lacks a comparison of different pruning ratios. As shown in Table 1, the performance of the proposed method is lower than that of LoRAPrune at the 30% pruning ratio. The authors should provide results for finer-grained pruning ratios, such as 25% and 35%, to better understand the trends in performance.

### Suggestions

The paper's primary weakness lies in its limited novelty and marginal performance gains compared to existing methods. While the use of information entropy as a pruning criterion is interesting, the overall approach is not significantly different from other structured pruning techniques. The authors should more clearly articulate the unique aspects of their method and provide a more thorough analysis of its advantages over existing approaches. Specifically, the paper should delve deeper into the theoretical underpinnings of why entropy-based pruning is superior to other criteria, such as magnitude-based or gradient-based methods, in the context of large language models. Furthermore, the experimental results should demonstrate more substantial improvements across a wider range of pruning ratios and model architectures to establish the robustness and generalizability of the proposed method. The current results, particularly the performance drop at higher pruning ratios, raise concerns about the method's practical applicability.

To address the lack of comprehensive memory usage analysis, the authors should provide a detailed breakdown of memory consumption during inference for both the original and pruned models. This analysis should include not only the memory required for model parameters but also the memory used for intermediate activations and other overheads. The comparison should be conducted using a consistent framework, such as Huggingface, and a standard precision format, such as FP16, to ensure a fair evaluation. Furthermore, the authors should investigate the impact of different pruning ratios on memory usage and identify the optimal trade-off between model size, performance, and memory consumption. This analysis should also consider the potential for memory savings through techniques such as quantization and knowledge distillation, which could be combined with the proposed pruning method to further improve efficiency.

Finally, the paper should include a more detailed analysis of the impact of different pruning ratios on model performance. The current results show that the proposed method performs worse than LoRAPrune at a 30% pruning ratio, which suggests that the method may not be optimal at higher sparsity levels. The authors should conduct a more fine-grained analysis of performance across a wider range of pruning ratios, such as 25% and 35%, to better understand the trends in performance and identify the optimal pruning ratio for the proposed method. This analysis should also include a discussion of the potential reasons for the performance drop at higher pruning ratios and suggest strategies for mitigating this issue. Additionally, the authors should explore the possibility of using adaptive pruning techniques that can dynamically adjust the pruning ratio based on the specific task or input data.

### Questions

Please refer to the weakness.

### Rating

3

### Confidence

4

**********