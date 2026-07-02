### Summary

This paper proposes a new optimization method called ANO, which decouples the direction and magnitude of updates to improve robustness in noisy and non-stationary optimization landscapes. The authors provide a theoretical analysis of ANO's convergence properties and demonstrate its effectiveness through experiments in reinforcement learning, NLP, and computer vision tasks. The results show that ANO outperforms existing optimizers in noisy and non-stationary environments while remaining competitive on low-noise tasks.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper is well-written and easy to follow, with clear explanations of the proposed method and its theoretical underpinnings.
2. The authors provide a comprehensive theoretical analysis of ANO's convergence properties, which strengthens the credibility of their approach.
3. The experiments are well-designed and cover a range of tasks, demonstrating the effectiveness of ANO in different domains.

### Weaknesses

#### Some Related Works


#### comment

1. The paper could benefit from a more detailed discussion of the limitations of ANO and potential areas for future research.
2. While the authors provide a theoretical analysis of ANO, it would be helpful to see more empirical comparisons with other state-of-the-art optimizers, especially in terms of computational efficiency and memory usage.

### Suggestions

The paper would be significantly strengthened by a more thorough discussion of the limitations of the proposed ANO optimizer. While the authors touch upon the idea of decoupling direction and magnitude, they should delve deeper into scenarios where this decoupling might be detrimental. For instance, in highly non-convex landscapes with sharp minima, the magnitude information, even if noisy, could be crucial for escaping poor local optima. A more detailed analysis of how ANO behaves in such scenarios, perhaps with specific examples or visualizations, would be beneficial. Furthermore, the authors should explore the sensitivity of ANO to its hyperparameters, particularly the decoupling parameter, and provide guidelines for tuning these parameters in different contexts. This would make the method more practical and accessible to a wider audience. The discussion should also include potential failure modes of ANO, such as when the noise is not random but structured, which could lead to biased updates and poor convergence.

To further enhance the empirical evaluation, the authors should include a more comprehensive comparison with other state-of-the-art optimizers, focusing not only on performance but also on computational efficiency and memory usage. While the paper mentions that ANO has the same memory cost as Adam, a more detailed analysis of the computational overhead would be valuable. For example, the authors could compare the number of floating-point operations per update step for ANO and other optimizers. Additionally, it would be beneficial to evaluate ANO on a wider range of tasks, including those with different levels of noise and non-stationarity. This would provide a more complete picture of the strengths and weaknesses of ANO. The authors should also consider comparing ANO with adaptive learning rate methods that also incorporate some form of noise handling, to better understand the specific advantages of the proposed decoupling approach.

Finally, the authors should consider providing more insights into the practical implications of their theoretical findings. While the convergence analysis is a valuable contribution, it would be helpful to connect these theoretical results to the observed empirical behavior. For example, the authors could discuss how the convergence rate of ANO relates to the choice of hyperparameters and the characteristics of the optimization landscape. This would provide a more intuitive understanding of the method and its limitations. Furthermore, the authors should explore the potential for extending ANO to other optimization settings, such as distributed training or federated learning, where noise and non-stationarity can be particularly challenging. This would broaden the impact of their work and open up new avenues for future research.

### Questions

1. How does the performance of ANO compare to other optimizers in terms of computational efficiency and memory usage?
2. Are there any specific scenarios where ANO might not perform as well as other optimizers, and if so, what are the potential reasons for this?

### Rating

6

### Confidence

3

**********