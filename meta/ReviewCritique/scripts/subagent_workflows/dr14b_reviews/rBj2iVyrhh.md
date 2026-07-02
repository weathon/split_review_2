### Summary

This paper proposes a classifier-constrained alternating training method to address the issue of modality imbalance. The authors first pre-train a shared classifier using bidirectional cross-attention and a regularization term to constrain the differences in modality contributions. This pre-trained classifier is then frozen and serves as a stable decision anchor during subsequent training, preventing bias towards any particular modality. To preserve modality-specific features while leveraging this anchor, the authors integrate modality-specific Low-Rank Adaptation (LoRA) modules into the classifier. During alternating training, only the encoder of the active modality and its corresponding LoRA parameters are updated. Additionally, a sample-level imbalance detection mechanism is introduced to quantify contribution disparities, enabling targeted optimization of severely imbalanced samples to further support weaker modalities.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper is well-written and easy to follow.
2. The motivation is clear and the proposed method is reasonable.
3. The experimental results are sufficient and promising.

### Weaknesses

#### Some Related Works


#### comment

1. In the experimental section, the authors only use ResNet18 as the encoders for all modalities. It would be beneficial to explore the impact of using different encoders for different modalities, as this could potentially lead to improved performance.
2. The proposed method requires a classifier pre-training stage, which adds complexity to the overall training process. It would be helpful to discuss the computational overhead associated with this additional stage and whether it significantly increases the training time or resource requirements.

### Suggestions

The paper would benefit from a more thorough investigation into the impact of encoder architecture on the performance of the proposed method. While ResNet18 is a common choice, it is not necessarily optimal for all modalities. For instance, convolutional neural networks with larger receptive fields or transformers might be more suitable for capturing the complex spatial or temporal dependencies in certain modalities. The authors should consider experimenting with a range of encoder architectures, such as ResNet50, EfficientNet, or even transformer-based encoders, and analyze how these choices affect the overall performance and the degree of modality imbalance. Furthermore, it would be valuable to explore whether modality-specific encoders, tailored to the characteristics of each modality, could further enhance the results. This could involve using different architectures or pre-training strategies for each modality before integrating them into the proposed framework. Such an analysis would provide a more comprehensive understanding of the method's robustness and generalizability.

Regarding the computational overhead, a more detailed analysis of the pre-training stage is needed. The authors should provide a breakdown of the time and resources required for each step of the pre-training process, including the time for training the classifier, the number of parameters involved, and the memory requirements. It would also be helpful to compare the computational cost of the proposed method with other existing approaches for addressing modality imbalance. This comparison should consider not only the training time but also the inference time, as the use of LoRA modules might introduce additional computational overhead during inference. A clear understanding of the computational trade-offs is crucial for assessing the practical applicability of the proposed method. Furthermore, the authors should discuss potential strategies for reducing the computational burden, such as using more efficient pre-training techniques or optimizing the implementation of the LoRA modules.

Finally, while the paper introduces a sample-level imbalance detection mechanism, it would be beneficial to provide more details on how this mechanism is implemented and how it affects the training process. Specifically, the authors should discuss the criteria used to identify severely imbalanced samples and how these samples are targeted for optimization. It would also be valuable to analyze the sensitivity of the method to the choice of the imbalance threshold and to explore different strategies for handling imbalanced samples. For example, the authors could investigate the use of re-weighting techniques or data augmentation methods to further mitigate the impact of modality imbalance. A more detailed analysis of the sample-level imbalance detection mechanism would provide a deeper understanding of its effectiveness and limitations.

### Questions

Please refer to the weaknesses.

### Rating

6

### Confidence

3

**********