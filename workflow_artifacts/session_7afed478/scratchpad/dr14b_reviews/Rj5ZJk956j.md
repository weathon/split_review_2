### Summary

This paper introduces a novel method for analyzing gated neurons in large language models (LLMs) by examining the cosine similarities between their weight vectors. The authors identify a class of neurons called "weakening neurons" that, despite their scarcity, have a substantial impact on model behavior. They observe that these neurons are prevalent in later layers of LLMs and significantly influence model output, even when gate values are negative. The study provides insights into the inner workings of transformers and highlights the importance of negative gate values in model functionality.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a novel method for analyzing gated neurons in LLMs, focusing on the cosine similarities between weight vectors to understand their read-write (RW) functionality.

2. The discovery of "weakening neurons" and their impact on model behavior is a significant contribution to the field of mechanistic interpretability.

3. The study provides insights into the inner workings of transformers, particularly the role of negative gate values in model functionality.

4. The authors conduct extensive experiments across multiple models, providing a comprehensive analysis of neuron behavior.

### Weaknesses

#### Some Related Works


#### comment

1. The paper's reliance on cosine similarity as the primary metric for analyzing neuron behavior may not capture the full complexity of neuron interactions. The authors could consider additional metrics or methods to provide a more comprehensive understanding of neuron functionality. For instance, while cosine similarity measures the alignment of weight vectors, it does not directly quantify the magnitude of the weight vectors or the impact of different input activations on the neuron's output. A neuron with a large weight vector might have a significant impact on the model's behavior even if its cosine similarity is not exceptionally high. Furthermore, the analysis does not consider the dynamic nature of neuron activations during inference, which could be influenced by the specific input sequence and the model's internal state. 

2. The paper could benefit from a more detailed discussion of the limitations of the proposed method and potential directions for future research. For example, the authors could discuss how the method might be extended to analyze other types of neurons or models, or how it could be used to improve model interpretability or performance. The current discussion lacks a critical evaluation of the method's sensitivity to hyperparameter choices, such as the threshold for defining weakening neurons, and how these choices might affect the results. Additionally, the paper does not explore the potential for adversarial attacks that could exploit the identified weakening neurons to manipulate model behavior.

### Suggestions

To enhance the analysis, the authors should consider incorporating additional metrics beyond cosine similarity to capture the full complexity of neuron interactions. For example, they could analyze the magnitude of the weight vectors associated with each neuron, as well as the distribution of input activations that lead to significant neuron outputs. This could involve examining the variance and skewness of the input activations, as well as the correlation between different input features. Furthermore, the authors could explore the use of techniques such as activation patching or ablation studies to directly assess the impact of individual neurons on model behavior. This would provide a more direct measure of a neuron's influence, rather than relying solely on the indirect measure of cosine similarity. The authors should also consider analyzing the temporal dynamics of neuron activations during inference, as this could reveal important patterns that are not captured by static weight vector analysis. This could involve tracking the activation patterns of neurons across different layers and time steps, and identifying any recurrent or sequential patterns that might be indicative of specific functional roles.

In addition to expanding the analysis, the authors should provide a more detailed discussion of the limitations of their method and potential directions for future research. This should include a critical evaluation of the method's sensitivity to hyperparameter choices, such as the threshold for defining weakening neurons, and how these choices might affect the results. The authors should also discuss the potential for adversarial attacks that could exploit the identified weakening neurons to manipulate model behavior. Furthermore, they should explore how the method might be extended to analyze other types of neurons or models, or how it could be used to improve model interpretability or performance. For example, the authors could investigate whether the identified weakening neurons are specific to certain types of tasks or datasets, or whether they are a general feature of large language models. They could also explore whether the weakening neurons play a role in specific model behaviors, such as hallucination or bias. Finally, the authors should consider how their method could be used to develop more robust and reliable models, by identifying and mitigating the impact of potentially problematic neurons.

Finally, the authors should consider the implications of their findings for model training and optimization. For example, they could investigate whether the identified weakening neurons are a result of specific training procedures or hyperparameter settings, and whether they can be mitigated through changes to the training process. This could involve exploring different optimization algorithms, regularization techniques, or data augmentation strategies. The authors should also consider whether the weakening neurons are a necessary component of model functionality, or whether they are an artifact of the training process that could be eliminated without affecting model performance. This could involve comparing the performance of models with and without the weakening neurons, and analyzing the impact of these neurons on specific model behaviors. By addressing these questions, the authors could provide valuable insights into the inner workings of large language models and contribute to the development of more robust and reliable models.

### Questions

1. Could the authors elaborate on how the cosine similarity metric was chosen and whether other metrics were considered? How might different metrics affect the analysis of neuron RW functionality?

2. How sensitive are the findings to the choice of models used in the study? Would the results generalize to other types of models or architectures?

3. The paper mentions that weakening neurons can have a significant impact on model behavior even with negative gate values. Could the authors provide more context on why this is surprising or counterintuitive?

### Rating

6

### Confidence

3

**********