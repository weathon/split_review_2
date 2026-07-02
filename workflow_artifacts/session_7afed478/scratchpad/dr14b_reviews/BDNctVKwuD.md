### Summary

This paper introduces ContrastiveCAMs and Core-Focused Cross-Entropy to improve the interpretability of convolutional neural networks. The authors first identify a limitation in HiResCAM, where explanations are not unique due to a spurious shift matrix. To address this, they propose ContrastiveCAMs, which provide more consistent and class-specific explanations. Additionally, Core-Focused Cross-Entropy is introduced to encourage models to focus on core image regions, enhancing feature alignment and reducing reliance on spurious features. Experiments on Hard-ImageNet and Oxford-IIIT Pets demonstrate the effectiveness of the proposed methods in improving both interpretability and model robustness.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper provides a thorough theoretical analysis of HiResCAM's limitations and proposes a well-motivated solution with ContrastiveCAMs.
2. The introduction of Core-Focused Cross-Entropy is a novel approach to improving model robustness by focusing on core image regions.
3. The experiments are comprehensive, with results on multiple datasets demonstrating the effectiveness of the proposed methods.

### Weaknesses

#### Some Related Works


#### comment

1. The paper primarily focuses on convolutional neural networks (CNNs) and does not explore the applicability of ContrastiveCAMs and Core-Focused Cross-Entropy to other architectures, such as transformers. This could limit the generalizability of the proposed methods.
2. The paper assumes the availability of core region masks, which may not always be available in real-world applications. The reliance on these masks, especially when they are manually annotated, introduces a practical limitation. The paper does not fully explore the sensitivity of the method to inaccuracies or noise in these masks, which could significantly impact the method's robustness in real-world scenarios.
3. The paper does not provide a detailed analysis of the computational overhead introduced by ContrastiveCAMs and Core-Focused Cross-Entropy. This is a critical aspect for practical applications, especially when considering the additional steps involved in generating contrastive explanations and the modified loss function. A thorough analysis of the computational cost, including memory usage and training time, is needed to assess the feasibility of the proposed methods.

### Suggestions

The authors should investigate the performance of ContrastiveCAMs and Core-Focused Cross-Entropy on non-CNN architectures, such as Vision Transformers. This would involve adapting the methods to handle the different feature extraction mechanisms of these architectures. For instance, the concept of 'core regions' might need to be redefined for transformer-based models, which do not rely on convolutional filters. Furthermore, the authors should explore how the contrastive loss function can be adapted to the attention mechanisms used in transformers. This would provide a more comprehensive understanding of the method's generalizability and applicability to a wider range of models. The experiments should include a comparison of performance and interpretability metrics across different architectures to validate the effectiveness of the proposed methods in diverse settings.

To address the limitation of requiring core region masks, the authors should explore methods for automatically generating these masks. This could involve using weakly supervised segmentation techniques or leveraging pre-trained models to identify salient regions in the images. The paper should also include a detailed analysis of the sensitivity of the method to the quality of these masks. This could be done by introducing controlled noise or inaccuracies in the masks and evaluating the impact on the model's performance and interpretability. The authors should also consider exploring alternative loss functions that do not rely on explicit core region masks, which would make the method more practical for real-world applications where such masks are not readily available. This would significantly enhance the practical applicability of the proposed method.

The authors should provide a detailed analysis of the computational overhead introduced by ContrastiveCAMs and Core-Focused Cross-Entropy. This analysis should include a breakdown of the time and memory costs associated with each step of the proposed methods, including the generation of contrastive explanations and the modified loss function. The authors should compare the computational cost of their method with that of standard training procedures and other interpretability techniques. This analysis should also consider the scalability of the method to larger datasets and more complex models. Furthermore, the authors should explore potential optimizations to reduce the computational overhead of their method, such as using more efficient algorithms or hardware acceleration. This would make the proposed methods more feasible for practical applications.

### Questions

1. How sensitive is the performance of Core-Focused Cross-Entropy to the quality of the core region masks? Have you tested the method with automatically generated or noisy masks?
2. Can ContrastiveCAMs be adapted for use with other model architectures, such as transformers or recurrent neural networks?
3. How does the computational overhead of ContrastiveCAMs and Core-Focused Cross-Entropy compare to standard training procedures?

### Rating

6

### Confidence

3

**********