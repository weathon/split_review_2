### Summary

This paper addresses the challenge of machine unlearning in scenarios where the class label and target concept do not coincide. The authors introduce three new unlearning tasks—target mismatch, model mismatch, and data mismatch—and propose a novel framework called TARF (TARGET-aware Forgetting) to tackle these challenges. TARF combines annealed gradient ascent on forgetting data with selected gradient descent on hard-to-affect remaining data, enabling selective forgetting while preserving model utility. The paper provides extensive empirical validation of TARF's effectiveness across various datasets and model architectures, demonstrating its superiority over existing methods in handling mismatched label domains.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a novel and practical perspective on machine unlearning by decoupling the class label and target concept, which is a significant departure from conventional approaches. This new framework addresses real-world complexities that were previously overlooked, making the work highly relevant and impactful.

2. The proposed TARF framework is technically robust, combining annealed gradient ascent and target-aware gradient descent in a novel way. The theoretical analysis, including the exploration of forgetting dynamics and representation gravity, provides a solid foundation for the method.

3. The empirical evaluation is comprehensive, covering a wide range of datasets and model architectures. The results clearly demonstrate the effectiveness of TARF in handling mismatched label domains, and the ablation studies provide valuable insights into the method's components.

### Weaknesses

#### Some Related Works


#### comment

1. While the paper provides a strong theoretical foundation for TARF, it could benefit from a more detailed discussion of the practical challenges and limitations of implementing the method in real-world scenarios. For instance, the sensitivity of the method to hyperparameter settings, such as the annealing schedule for gradient ascent and the criteria for selecting hard-to-affect remaining data, is not thoroughly explored. Furthermore, the computational cost associated with the iterative optimization process, especially when dealing with large-scale models and datasets, needs more detailed analysis. The paper should also address the potential for instability during the unlearning phase, particularly when the target concept is highly entangled with other concepts in the model's representation space.

2. The paper primarily focuses on image classification tasks. While the results are compelling, it would be beneficial to explore the applicability of TARF to other domains, such as natural language processing or time-series analysis. The current evaluation lacks a discussion of how the method's performance might vary across different data modalities and model architectures. For example, the effectiveness of gradient-based unlearning might be different in recurrent neural networks compared to convolutional neural networks, and the paper should address these potential differences. Additionally, the paper should discuss the challenges of applying TARF to tasks with more complex output spaces, such as sequence generation or multi-label classification.

### Suggestions

To enhance the practical applicability of TARF, the authors should conduct a more thorough investigation into the method's sensitivity to hyperparameter settings. Specifically, they should explore different annealing schedules for the gradient ascent phase and provide guidelines for selecting appropriate schedules based on the characteristics of the dataset and the target concept. Furthermore, the criteria for selecting hard-to-affect remaining data should be analyzed in detail, and the authors should investigate the impact of different selection strategies on the unlearning performance. For example, they could compare the performance of TARF when using data points with the highest loss values versus those with the smallest representation distances. The authors should also provide a detailed analysis of the computational cost associated with TARF, including the time and memory requirements for different datasets and model architectures. This analysis should include a comparison with other unlearning methods and provide insights into the scalability of TARF for large-scale applications. Finally, the authors should investigate the potential for instability during the unlearning phase and propose strategies for mitigating this issue, such as using adaptive learning rates or regularization techniques.

To broaden the scope of the paper, the authors should extend their evaluation to include other domains beyond image classification. For example, they could explore the applicability of TARF to natural language processing tasks, such as text classification or sentiment analysis, and time-series analysis tasks, such as anomaly detection or forecasting. This would involve adapting the method to handle different data modalities and model architectures. For instance, in NLP, the authors could investigate how TARF performs with transformer-based models, and in time-series analysis, they could explore its effectiveness with recurrent neural networks. The authors should also discuss the challenges of applying TARF to tasks with more complex output spaces, such as sequence generation or multi-label classification. This would involve analyzing how the method's performance might vary with different loss functions and output representations. The authors should also consider the potential for concept drift in these domains and discuss how TARF can be adapted to handle such scenarios.

In addition to the above, the authors should also consider the ethical implications of their work. While the paper focuses on the technical aspects of machine unlearning, it is important to acknowledge the potential for misuse of this technology. For example, TARF could be used to selectively remove information from a model, which could lead to biased or unfair outcomes. The authors should discuss these ethical considerations and propose guidelines for responsible use of their method. This could include developing methods for verifying the effectiveness of unlearning and ensuring that the model's performance is not compromised after the unlearning process. Furthermore, the authors should consider the potential for adversarial attacks on the unlearning process and propose defenses against such attacks.

### Questions

1. How does the choice of hyperparameters, such as the annealing schedule for gradient ascent and the criteria for selecting hard-to-affect remaining data, affect the performance of TARF in different scenarios? Could the authors provide more insights into the sensitivity of the method to these parameters?

2. The paper primarily focuses on image classification tasks. How well does TARF generalize to other domains, such as natural language processing or time-series analysis? Are there any specific challenges or adaptations required for these domains?

### Rating

6

### Confidence

3

**********