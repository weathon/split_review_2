### Summary

This paper proposes a new framework, Contrastive-Online-Meta (COM), for dynamic adaptation of instruction-tuned CodeLLMs. COM addresses the issues of catastrophic forgetting and noisy feedback during deployment by combining contrastive pre-training and online meta-learning. The framework separates task-invariant representation learning from fast adaptation, preserving core programming knowledge while enabling real-time adjustments. Experiments show that COM outperforms static and incremental tuning baselines in adaptation efficiency and task generalization, providing a scalable solution for real-world code generation systems requiring continuous learning.

### Soundness

2

### Presentation

2

### Contribution

2

### Strengths

1. The paper is well-organized and easy to follow.
2. The proposed method is technically sound and achieves improvements over baselines.

### Weaknesses

#### Some Related Works


#### comment

1. The novelty of this paper is limited, as it simply combines contrastive learning and meta-learning.
2. The experimental results are not sufficiently convincing due to the limited scale of the experiments and the lack of ablation studies.
3. The paper lacks a thorough analysis of the computational complexity and scalability of the proposed framework, which is crucial for practical applications.

### Suggestions

The paper's primary weakness lies in its limited novelty. While combining contrastive learning and meta-learning is not inherently flawed, the paper does not adequately justify why this specific combination is particularly well-suited for instruction-tuned CodeLLMs, beyond a general statement about their synergistic potential. The authors should provide a more detailed explanation of how contrastive learning's ability to create distinct representations for similar instructions directly addresses the challenges of catastrophic forgetting in meta-learning, specifically within the context of code generation. For instance, they could elaborate on how the contrastive loss function is tailored to the specific characteristics of programming language instructions and how this differs from standard contrastive learning applications. Furthermore, a more rigorous theoretical analysis of the interaction between the contrastive and meta-learning components would strengthen the paper's contribution. This could involve analyzing the convergence properties of the combined framework or providing theoretical guarantees on its ability to mitigate catastrophic forgetting. Without this deeper analysis, the proposed method appears to be an incremental combination of existing techniques rather than a novel approach.

To address the concerns regarding the experimental results, the authors should conduct more comprehensive experiments with a larger scale and include detailed ablation studies. The current experiments, while demonstrating some improvements, do not provide sufficient evidence to support the claims of superior adaptation efficiency and task generalization. Specifically, the authors should explore the impact of various hyperparameters, such as the learning rate, batch size, and the number of negative samples used in contrastive learning, on the performance of the proposed framework. Furthermore, it is crucial to investigate the sensitivity of the method to different task distributions and the number of tasks. The ablation studies should systematically evaluate the contribution of each component of the framework, including the contrastive pre-training, the meta-learning algorithm, and the dynamic memory buffer. This would help to identify the key factors that contribute to the performance gains and provide a more nuanced understanding of the framework's behavior. The authors should also consider comparing their method with more recent and relevant baselines in the field of continual learning for code generation.

Finally, the paper needs a thorough analysis of the computational complexity and scalability of the proposed framework. The authors should provide a detailed breakdown of the computational cost associated with each component of the framework, including the contrastive pre-training, the meta-learning updates, and the dynamic memory buffer operations. This analysis should consider both the time and memory requirements of the framework and should be compared to the computational cost of the baselines. Furthermore, the authors should discuss the scalability of the framework to larger models and datasets. This could involve analyzing the impact of the number of parameters on the computational cost and exploring techniques for optimizing the framework for resource-constrained environments. Without a clear understanding of the computational overhead, it is difficult to assess the practical applicability of the proposed framework, especially for real-world code generation systems that often require efficient and scalable solutions.

### Questions

Please refer to the weaknesses.

### Rating

5

### Confidence

3

**********