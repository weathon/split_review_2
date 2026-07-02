### Summary

The paper studies the trade-off between model accuracy and inference cost under a fixed training budget. It begins by demonstrating how architectural choices influence both inference throughput and model accuracy. Building on this, it extends Chinchilla scaling laws to incorporate architectural factors and proposes a two-step conditional framework for optimal architecture search: (i) train small models to fit the conditional scaling law (Eq. 3), and (ii) solve Eq. 4 for the predicted optimal architecture, followed by a local search over GQA to maximize inference efficiency. Using the fitted scaling laws and the framework, the paper trains models up to 3B parameters, achieving up to 42% higher inference throughput and 2.1% accuracy gains across nine downstream tasks.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper is well-written and easy to follow.
2. The paper conducts extensive experiments to demonstrate the trade-off between model accuracy and inference cost under a fixed training budget. The results show that the proposed conditional scaling law can effectively predict optimal architectural choices.
3. The paper proposes a two-step conditional framework for optimal architecture search, which is a novel approach to addressing the trade-off between model accuracy and inference cost.

### Weaknesses

#### Some Related Works


#### comment

1. The paper focuses on a fixed training budget, which may not be realistic in all scenarios. In practice, the training budget may vary depending on the specific application and available resources.
2. The paper only considers a limited set of architectural choices, such as hidden size and MLP-to-attention ratio. Other architectural choices, such as the number of layers and the type of attention mechanism, may also affect the trade-off between model accuracy and inference cost.
3. The paper does not provide a detailed analysis of the computational cost of the proposed architecture search framework. The computational cost of training multiple models to fit the conditional scaling law and the cost of solving Eq. 4 for the predicted optimal architecture should be considered.

### Suggestions

The paper's focus on a fixed training budget, while providing a controlled environment for analysis, limits its direct applicability to real-world scenarios where training budgets are often variable and constrained by available resources. Future work should explore how the proposed conditional scaling laws adapt to different training budgets, perhaps by introducing a parameter that explicitly models the relationship between training budget and optimal architecture. This could involve analyzing the sensitivity of the scaling laws to changes in the training budget and developing strategies for dynamically adjusting the architecture based on available resources. Furthermore, it would be beneficial to investigate the impact of different optimization techniques on the trade-off between model accuracy and inference cost, as these techniques can significantly affect the training process and the final model performance.

While the paper considers hidden size and MLP-to-attention ratio, it neglects other crucial architectural parameters that can significantly impact both model accuracy and inference efficiency. For instance, the number of layers, the type of attention mechanism (e.g., local vs. global), and the use of techniques like layer normalization or residual connections can all influence the model's performance and computational cost. Future research should explore a more comprehensive set of architectural choices and their interactions with the proposed scaling laws. This could involve conducting a more extensive hyperparameter search and analyzing the impact of different architectural configurations on the trade-off between accuracy and inference cost. Additionally, the paper should investigate the impact of different quantization techniques on the trade-off between model accuracy and inference cost, as these techniques can significantly reduce the computational cost of inference.

The paper lacks a detailed analysis of the computational cost associated with the proposed architecture search framework. Training multiple models to fit the conditional scaling law and solving Eq. 4 for the optimal architecture can be computationally expensive, especially for large models. Future work should provide a more thorough analysis of the computational cost of the search process, including the time and resources required for each step. This analysis should also consider the trade-off between the computational cost of the search process and the potential gains in model accuracy and inference efficiency. Furthermore, it would be beneficial to explore more efficient search algorithms that can reduce the computational cost of the architecture search process, such as Bayesian optimization or reinforcement learning.

### Questions

1. How does the proposed conditional scaling law generalize to different model architectures, such as encoder-decoder models or graph neural networks?
2. How does the proposed conditional scaling law adapt to different training budgets? Can it be used to guide the selection of optimal architectures under different training budgets?
3. How does the proposed conditional scaling law compare to other methods for optimizing model architectures, such as neural architecture search (NAS)?
4. How does the proposed conditional scaling law perform on different datasets and tasks? Can it be used to guide the selection of optimal architectures for specific applications?

### Rating

6

### Confidence

3

**********