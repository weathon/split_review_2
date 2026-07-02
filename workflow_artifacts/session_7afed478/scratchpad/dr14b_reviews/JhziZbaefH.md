### Summary

This paper presents a model named OML, a brain-inspired neural network with a hierarchical and modular architecture designed for online multimodal learning (OML). The model adapts its structure and parameters dynamically to learn new multimodal concepts and associations without forgetting previously learned information. It features ascending, descending, and lateral pathways for multimodal interaction and conflict detection, and includes a reference extraction algorithm for identifying word references.

### Soundness

2

### Presentation

2

### Contribution

2

### Strengths

1. The paper presents a novel brain-inspired neural network architecture for online multimodal learning, which is an innovative approach in the field.
2. The model's ability to learn new concepts online without forgetting previous knowledge addresses a critical challenge in machine learning.
3. The inclusion of mechanisms for conflict detection and human interaction makes the model more adaptable and robust in real-world scenarios.

### Weaknesses

#### Some Related Works


#### comment

1. The experimental validation may not be comprehensive enough, lacking sufficient experiments and comparisons with other models. The paper does not explore the model's performance across a diverse set of multimodal tasks, limiting the assessment of its generalizability. Specifically, the experiments focus on a limited set of datasets and do not include comparisons with state-of-the-art models in multimodal learning, making it difficult to gauge the true effectiveness of the proposed approach.
2. The paper has limitations in explaining how the model handles scalability and complexity as the number of modalities and concepts increases. The description of the network's architecture and learning mechanisms lacks detail on how it would adapt to a significantly larger number of input modalities or more complex relationships between them. There is no discussion on the computational complexity of the model, which is crucial for understanding its practical applicability.
3. The model's reliance on human input for conflict resolution may not be feasible in all real-world applications. The paper does not explore alternative strategies for handling conflicts when human intervention is not available or practical, which limits the model's autonomy and usability in fully automated systems.

### Suggestions

To address the limitations in experimental validation, the authors should conduct a more comprehensive evaluation of the OML model across a wider range of multimodal datasets and tasks. This should include comparisons with state-of-the-art models in multimodal learning to provide a clearer understanding of the model's relative performance. Specifically, the evaluation should not only focus on accuracy but also on other relevant metrics such as learning speed, memory retention, and the model's ability to handle noisy or ambiguous inputs. Furthermore, the experimental setup should be described in more detail, including the specific hyperparameter settings and training procedures used, to ensure reproducibility and allow for a more thorough analysis of the results. The inclusion of ablation studies to assess the contribution of different components of the model would also be beneficial.

To improve the discussion of scalability and complexity, the authors should provide a more detailed analysis of the model's architecture and learning mechanisms, focusing on how they would adapt to a larger number of input modalities and more complex relationships between them. This should include a discussion of the computational complexity of the model, including the time and space requirements for training and inference. The authors should also explore strategies for optimizing the model's performance, such as techniques for reducing the dimensionality of the input data or using more efficient learning algorithms. Furthermore, the paper should include a theoretical analysis of the model's capacity and generalization ability, which would provide a more solid foundation for understanding its limitations and potential.

Finally, to address the reliance on human input for conflict resolution, the authors should explore alternative strategies for handling conflicts when human intervention is not available or practical. This could include the use of automated conflict resolution mechanisms, such as those based on confidence scores or prior knowledge. The paper should also discuss the trade-offs between human-in-the-loop and fully automated conflict resolution approaches, considering factors such as accuracy, efficiency, and robustness. The authors should also investigate how the model can learn from its mistakes and improve its conflict resolution capabilities over time, which would enhance its autonomy and adaptability.

### Questions

1. How does the OML model perform in terms of scalability and efficiency when dealing with a large number of modalities and complex associations?
2. Can the authors provide more empirical evidence or theoretical justification for the model's ability to prevent catastrophic forgetting in online learning scenarios?
3. How does the model handle ambiguous or noisy inputs, and what mechanisms are in place to ensure robustness in real-world environments?

### Rating

3

### Confidence

5

**********