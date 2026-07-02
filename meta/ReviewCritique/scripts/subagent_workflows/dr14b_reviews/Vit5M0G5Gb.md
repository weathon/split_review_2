### Summary

This work studies the simplicity bias of neural networks, which refers to the tendency of networks to learn solutions of increasing complexity over time. The authors propose a theoretical framework based on saddle-to-saddle dynamics to explain this phenomenon across various architectures, including fully-connected, convolutional, and attention-based networks. They analyze fixed points and invariant manifolds of gradient descent dynamics, showing how networks transition between different complexity levels. The paper also explores how data distribution and weight initialization influence the learning process.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper provides a unified theoretical framework based on saddle-to-saddle dynamics that applies to diverse neural network architectures.
2. The theoretical analysis is rigorous and well-supported by empirical evidence.
3. The paper offers insights into how data distribution and initialization affect learning dynamics.

### Weaknesses

#### Some Related Works


#### comment

1. The analysis is limited to two-layer networks in many of its technical sections, which may restrict the applicability of the findings to deeper architectures. While the authors propose a conjecture for deep networks, it remains unproven and lacks experimental validation. The theoretical framework, while elegant, needs further development to explicitly address the complexities introduced by skip connections, batch normalization, and other common components of deep networks. The current analysis does not fully capture the inter-layer dynamics and potential emergent behaviors in deeper architectures.

2. Some experimental details are not fully described, which could affect reproducibility. For instance, the specific optimization algorithms, learning rate schedules, and hyperparameter tuning processes are not clearly outlined. The lack of detail regarding the data preprocessing steps and the specific architectures used in the experiments makes it difficult to replicate the results and verify the claims.

3. The discussion of the implications for understanding inductive biases in neural networks could be more detailed. The paper identifies the simplicity bias but does not fully explore how this bias interacts with the specific inductive biases of different architectures. A more thorough analysis of how the saddle-to-saddle dynamics relate to the generalization performance and the learning of specific features would be beneficial. The connection between the theoretical framework and the practical implications for model design and training is not fully elaborated.

### Suggestions

To strengthen the paper, the authors should extend their theoretical analysis to encompass deeper networks, explicitly addressing the impact of common architectural components such as skip connections and batch normalization. This could involve developing new mathematical tools or adapting the existing framework to account for the increased complexity of inter-layer interactions. For example, the authors could investigate how the invariant manifolds and fixed points of the gradient descent dynamics are affected by the presence of these components. Furthermore, the authors should provide a more detailed analysis of the conditions under which the saddle-to-saddle dynamics emerge in deep networks, and how these conditions relate to the architecture and the data distribution. This would involve a more rigorous treatment of the inter-layer dynamics and potential emergent behaviors in deeper architectures, possibly through the use of techniques from dynamical systems theory.

In addition, the authors should provide a more comprehensive description of the experimental setup, including specific details about the optimization algorithms, learning rate schedules, hyperparameter tuning processes, data preprocessing steps, and the exact architectures used in the experiments. This would significantly improve the reproducibility of the results and allow other researchers to verify the claims made in the paper. For example, the authors could include a table summarizing the hyperparameters used in each experiment, along with a detailed description of the data preprocessing steps. Furthermore, the authors should consider releasing their code and data to further enhance the reproducibility of their work. This would allow the community to build upon their findings and explore the implications of their theoretical framework in more detail.

Finally, the authors should delve deeper into the implications of their findings for understanding inductive biases in neural networks. This could involve exploring how the saddle-to-saddle dynamics interact with the specific inductive biases of different architectures and how this interaction affects the generalization performance of the models. For example, the authors could investigate how the simplicity bias influences the learning of specific features and how this relates to the architecture's ability to generalize to unseen data. A more thorough analysis of the connection between the theoretical framework and the practical implications for model design and training would significantly enhance the impact of the paper. This could also involve exploring the relationship between the identified simplicity bias and other known biases in neural networks, such as the bias towards low-frequency functions.

### Questions

1. How would the proposed framework extend to architectures with skip connections or residual connections?
2. Could the authors provide more detailed experimental settings to facilitate reproducibility?

### Rating

6

### Confidence

3

**********