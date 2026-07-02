### Summary

This paper proposes a regression-based test-time adaptation (RTA) method to improve the performance of vision-language models (VLMs) on out-of-distribution (OOD) data. The key idea is to train a regression model that maps augmented views of an input image to their corresponding cross-entropy loss. During test time, the regression model is used to select the most confident views for ensemble prediction. The authors demonstrate the effectiveness of RTA on several single-label and multi-label image classification benchmarks, showing consistent improvements over existing entropy-based TTA methods.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

- The idea of using regression to predict cross-entropy loss for view selection is novel and interesting.
- The method is simple yet effective, requiring only a one-time training of the regression model on diverse unlabeled data.
- The paper provides thorough experimental evaluations on multiple benchmarks, demonstrating the robustness of RTA across different datasets and model architectures.
- The authors also analyze the impact of various factors such as the number of augmented views and the size of the regression mapping data, providing valuable insights into the method's behavior.

### Weaknesses

#### Some Related Works


#### comment

 - The method relies on having access to a diverse set of unlabeled data for training the regression model. This might be a limitation in practice, especially for domain-specific applications where such data is scarce.
- The paper does not provide a detailed analysis of the computational cost associated with training the regression model and performing test-time adaptation. This is important for assessing the practicality of the method.
- The paper does not explore the potential of combining RTA with other TTA methods, which could lead to further performance improvements.

### Suggestions

The paper introduces an interesting regression-based approach for test-time adaptation, but several aspects could be strengthened to enhance its practical applicability and theoretical grounding. Firstly, while the method demonstrates strong performance on the evaluated benchmarks, the reliance on a diverse, unlabeled dataset for training the regression model poses a practical challenge. The paper should explore the sensitivity of the method to the diversity and size of this training data. For instance, experiments could be conducted using datasets with varying degrees of semantic overlap with the target domain, or by systematically reducing the size of the training set. This would provide a clearer understanding of the method's robustness and limitations in real-world scenarios where such diverse data might not be readily available. Furthermore, the paper should investigate the impact of different sampling strategies for creating the diverse unlabeled dataset, as this could significantly affect the performance of the regression model.

Secondly, the paper lacks a detailed analysis of the computational overhead associated with the proposed method. While the authors mention that the regression model is trained only once, the computational cost of this initial training phase, as well as the cost of performing test-time adaptation, should be quantified and compared with existing TTA methods. This analysis should include the time and memory requirements for both training the regression model and performing the view selection during test time. It would be beneficial to provide a breakdown of the computational cost for each step of the pipeline, including the augmentation process, the forward pass through the vision-language model, and the regression model inference. This would allow readers to better assess the practical feasibility of the method, especially in resource-constrained environments. Additionally, the paper should explore potential optimizations to reduce the computational burden, such as using more efficient augmentation techniques or lighter regression models.

Finally, the paper should explore the potential of combining RTA with other test-time adaptation techniques. While the authors briefly touch upon this possibility, a more thorough investigation is warranted. For example, the paper could explore combining RTA with entropy minimization-based methods, or with techniques that explicitly address catastrophic forgetting. This could involve using RTA to select the most confident views and then applying another TTA method to refine the predictions. Such an approach could potentially lead to further performance improvements and provide a more robust solution for adapting vision-language models to out-of-distribution data. The paper should also discuss the challenges and opportunities associated with combining different TTA methods, and provide guidelines for selecting the most appropriate combination for a given task.

### Questions

- How does the performance of RTA vary with the diversity and size of the regression mapping data?
- What is the computational overhead of training the regression model and performing test-time adaptation?
- Can RTA be combined with other TTA methods to achieve further performance improvements?
- How does the performance of RTA compare to other methods that use auxiliary information or external data for TTA?

### Rating

6

### Confidence

4

**********