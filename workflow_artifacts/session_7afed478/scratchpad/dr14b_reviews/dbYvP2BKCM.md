### Summary

This paper proposes a novel method for learning representations of instrumental variables using a neural network framework. The proposed method, ZNet, aims to address the challenge of unobserved confounding in causal inference by decomposing observed variables into representations that satisfy the instrumental variable assumptions of relevance, exclusion restriction, and unconfoundedness. The paper demonstrates that ZNet can recover known instruments and construct proxy latent instruments in various settings, offering a potential solution for causal effect estimation in observational studies.

### Soundness

2

### Presentation

2

### Contribution

2

### Strengths

- The paper addresses the challenging problem of learning representations of instrumental variables, which is important for causal inference in the presence of unobserved confounders.
- The proposed ZNet method is designed to satisfy the key instrumental variable assumptions, and the paper provides theoretical justifications for the method's ability to recover ground-truth instruments and construct proxy latent instruments.

### Weaknesses

#### Some Related Works


#### comment

 - The paper's introduction of ZNet and its underlying principles could benefit from clearer explanations. Providing additional details on the network architecture, training process, and the connection between the proposed loss function and the instrumental variable assumptions would enhance the reader's understanding. For instance, the specific layers used in the neural network, the activation functions, and the optimization algorithm are not clearly defined. A more detailed explanation of how the network is structured to enforce the exclusion restriction would be beneficial. The paper should also elaborate on how the different components of the loss function contribute to the identification of valid instruments.
- The experimental evaluation primarily focuses on comparisons with other IV methods, but it could be strengthened by including comparisons with non-IV methods as baselines. This would provide a broader context for assessing the performance of ZNet and its advantages over existing causal inference techniques. Specifically, comparisons with methods that explicitly model confounders or use adversarial techniques to mitigate confounding bias would be valuable. This would help to clarify the specific scenarios where ZNet is most effective compared to other approaches.
- The paper could benefit from a more thorough discussion of the limitations of ZNet and potential areas for future research. For example, the sensitivity of the method to hyperparameter choices, the computational cost for large datasets, and the potential for extending the framework to handle time-varying treatments or more complex causal structures are not adequately addressed. A discussion of the assumptions under which the method is guaranteed to recover valid instruments would also be beneficial.
- The paper's writing quality could be improved in several areas. For instance, the introduction of technical terms and concepts could be more accessible to a broader audience, and the explanations of the experimental results could be more detailed and insightful. The paper would benefit from a more rigorous definition of the problem being addressed, including a clear statement of the assumptions being made. Additionally, the paper could use more visual aids, such as diagrams of the network architecture and causal graphs, to improve clarity.

### Suggestions

To improve the clarity of the ZNet architecture and training process, the authors should provide a detailed description of the neural network's structure, including the specific types of layers used (e.g., fully connected, convolutional, recurrent), the activation functions (e.g., ReLU, sigmoid, tanh), and the optimization algorithm (e.g., Adam, SGD). The paper should also include a diagram of the network architecture to aid visualization. Furthermore, a more detailed explanation of how the network is trained, including the batch size, learning rate, and number of epochs, would be beneficial. The authors should also elaborate on how the proposed loss function is connected to the instrumental variable assumptions. For example, they could explain how each term in the loss function contributes to the relevance, exclusion restriction, and unconfoundedness assumptions. This could be done by providing a theoretical analysis of the loss function and its relationship to the instrumental variable conditions. Finally, the paper should include a discussion of the identifiability of the learned representations, including the conditions under which the method is guaranteed to recover valid instruments.

To strengthen the experimental evaluation, the authors should include comparisons with non-IV methods that are commonly used in causal inference. This could include methods that explicitly model confounders, such as propensity score matching or inverse probability weighting, as well as methods that use adversarial techniques to mitigate confounding bias. The paper should also include a discussion of the performance of ZNet in different settings, such as when the instruments are weak or invalid. The authors should also provide a more detailed analysis of the experimental results, including a discussion of the statistical significance of the findings. This could include confidence intervals or p-values for the estimated treatment effects. Furthermore, the paper should include a discussion of the limitations of the experimental evaluation, including the specific datasets used and the potential for bias in the results. The authors should also consider including a sensitivity analysis to assess the robustness of the results to different choices of hyperparameters.

To address the limitations of ZNet, the authors should include a discussion of the sensitivity of the method to hyperparameter choices, such as the learning rate, batch size, and the number of hidden layers. The paper should also include a discussion of the computational cost of the method, including the time and memory requirements for training the neural network. The authors should also discuss the potential for extending the framework to handle more complex scenarios, such as time-varying treatments or non-linear causal relationships. This could include a discussion of the challenges involved in extending the method to these settings and potential solutions. Finally, the paper should include a discussion of the assumptions under which the method is guaranteed to recover valid instruments, including a discussion of the limitations of these assumptions. This could include a discussion of the potential for bias in the estimated treatment effects when the assumptions are violated.

### Questions

- Could the authors provide more details on the ZNet architecture and training process? For example, how is the network structured to enforce the exclusion restriction, and what are the key hyperparameters that influence the performance of the method?
- How does ZNet perform in comparison to non-IV methods for causal effect estimation? Are there specific scenarios where ZNet is expected to outperform these methods, and can the authors provide empirical evidence to support these claims?
- What are the limitations of ZNet in terms of scalability and computational cost? How does the method perform on large-scale datasets, and are there any potential bottlenecks in the training process?
- Can the authors discuss the potential for extending the ZNet framework to handle more complex scenarios, such as time-varying treatments or non-linear causal relationships? What are the main challenges involved in these extensions, and how might they be addressed?

### Rating

3

### Confidence

3

**********