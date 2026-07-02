### Summary

This paper proposes a new method for Unified Speech Recognition (USR) called USR 2.0, which aims to improve the efficiency and robustness of pseudo-labeling in speech recognition tasks. The key innovation is the introduction of CTC-driven teacher forcing, which uses CTC pseudo-labels to guide the generation of attention-based pseudo-labels in a single forward pass, avoiding the computational bottleneck of autoregressive decoding. Additionally, mixed sampling is proposed to mitigate the exposure bias introduced by CTC-driven teacher forcing. The method is evaluated on multiple benchmarks, including LRS3, LRS2, and WildVSR, and demonstrates significant improvements in robustness to out-of-distribution data and reduced training time compared to the original USR.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a novel approach to pseudo-labeling in USR by leveraging CTC-driven teacher forcing, which significantly reduces the computational cost associated with autoregressive decoding.
2. The method demonstrates strong empirical results, achieving state-of-the-art performance on multiple benchmarks, including LRS3, LRS2, and WildVSR.
3. The paper provides a thorough analysis of the robustness of USR 2.0 to out-of-distribution data, including noisy audio and long utterances, which are critical for real-world applications.

### Weaknesses

#### Some Related Works


#### comment

1. The paper could benefit from a more detailed discussion of the limitations of CTC-driven teacher forcing, particularly in scenarios where the CTC pseudo-labels are not reliable. The reliance on CTC pseudo-labels introduces a potential vulnerability; if the CTC model struggles with certain acoustic conditions or speaker variations, the subsequent attention-based pseudo-labels will likely inherit these errors, leading to compounding issues during training. This is especially concerning in low-resource settings or when dealing with highly diverse datasets where CTC performance might be suboptimal.
2. While the paper demonstrates strong empirical results, it would be valuable to include more ablation studies to understand the contribution of each component of USR 2.0. For example, the impact of mixed sampling and the specific weighting of CTC and attention losses could be further explored. It is unclear how sensitive the model is to the mixing ratio between CTC and attention-based pseudo-labels, and a more systematic exploration of this parameter would be beneficial. Additionally, the paper lacks a detailed analysis of the individual contributions of the CTC and attention branches to the final performance.
3. The paper could provide more details on the computational resources required for training USR 2.0, especially given the claim of reduced training time. While the paper mentions reduced training time, it does not provide specific details on the hardware used, the memory footprint of the model, or the training time per epoch. This information is crucial for assessing the practical applicability of the method, especially for researchers with limited computational resources.

### Suggestions

To address the limitations of CTC-driven teacher forcing, the authors should explore techniques to mitigate the impact of noisy CTC pseudo-labels. One approach could be to incorporate a confidence measure for the CTC predictions, using only high-confidence pseudo-labels for training the attention-based model. Another strategy could involve using a more robust CTC model, perhaps pre-trained on a larger and more diverse dataset, to generate the initial pseudo-labels. Furthermore, the authors could investigate methods for error correction in the CTC pseudo-labels, such as using a language model to refine the generated sequences. These techniques could help to reduce the propagation of errors from the CTC branch to the attention branch, leading to more stable and reliable training.

To better understand the contribution of each component of USR 2.0, the authors should conduct a more comprehensive ablation study. This should include varying the mixing ratio between CTC and attention-based pseudo-labels and analyzing the impact on both in-distribution and out-of-distribution performance. Additionally, the authors should investigate the effect of different weighting schemes for the CTC and attention losses. It would also be beneficial to analyze the performance of the model when trained solely on CTC pseudo-labels or solely on attention pseudo-labels, to understand the individual contributions of each branch. This analysis should be performed across different datasets and acoustic conditions to provide a more complete picture of the model's behavior. Furthermore, the authors should explore the impact of different sampling strategies during training, such as curriculum learning, to see if it can further improve the model's robustness.

Finally, the authors should provide more detailed information on the computational resources required for training USR 2.0. This should include the specific hardware used (e.g., GPU model, number of GPUs), the memory footprint of the model, and the training time per epoch. It would also be helpful to provide a breakdown of the computational cost of different components of the training process, such as the CTC and attention branches. This information would allow other researchers to better assess the practical applicability of the method and to reproduce the results more easily. Additionally, the authors could explore techniques for optimizing the training process, such as mixed-precision training or model parallelism, to further reduce the computational cost.

### Questions

1. How does the performance of USR 2.0 vary with different levels of noise in the training data? Are there specific types of noise that are more challenging for the model to handle?
2. Can the authors provide more details on the computational resources required for training USR 2.0, especially in comparison to the original USR? This would help to better understand the practical benefits of the proposed method.
3. How does the choice of the teacher model affect the performance of USR 2.0? Are there specific architectures or training strategies that are more effective for generating high-quality pseudo-labels?

### Rating

6

### Confidence

3

**********