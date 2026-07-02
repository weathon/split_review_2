### Summary

This paper presents a theoretical analysis of how semantic associations emerge in attention-based language models during training. The authors use a leading-term approximation of the gradients to derive closed-form expressions for the weights at early stages of training, revealing that these weights can be decomposed into three basis functions: bigram mapping, interchangeability mapping, and context mapping. The paper validates these theoretical findings through experiments on both toy and real-world language models, demonstrating that the learned weights closely match the theoretical predictions.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper provides a novel theoretical framework for understanding how semantic associations are learned in transformers, offering a fresh perspective on the training dynamics of these models.
2. The use of closed-form expressions for the weights at early stages of training is a significant technical innovation, allowing for a more tractable analysis of the model's behavior.
3. The empirical validation on both toy and real-world language models strengthens the credibility of the theoretical findings, showing that the results are not limited to simplified settings.

### Weaknesses

#### Some Related Works


#### comment

1. The analysis focuses primarily on the early stages of training. It's unclear how well the leading-term approximation holds for longer training periods or more complex tasks. The paper does not provide sufficient justification for why the early-stage analysis is sufficient to understand the full training dynamics, especially given that many interesting capabilities of transformers emerge later in training. The assumption that early learned structures persist without significant alteration may not hold, particularly as the model learns more complex relationships and abstract concepts.
2. The study is limited to attention-based transformers. It would be valuable to see if similar patterns emerge in other architectures or with different training regimes. The paper does not explore the extent to which the identified basis functions are specific to attention mechanisms or if they are a more general property of neural network learning. This limits the generalizability of the findings and leaves open the question of whether similar theoretical frameworks could be developed for other architectures.
3. While the theoretical framework is well-developed, the practical implications for improving model design or training efficiency are not fully explored. The paper does not provide concrete examples of how the identified basis functions could be used to guide the design of more efficient or effective models. The connection between the theoretical analysis and practical applications remains somewhat abstract, limiting the immediate impact of the work.

### Suggestions

To address the limitation of focusing primarily on early training stages, the authors should investigate the evolution of the identified basis functions over longer training periods. This could involve tracking the cosine similarity between the theoretical and learned weights at different stages of training, and analyzing how the relative importance of the bigram, interchangeability, and context mappings changes over time. Furthermore, the authors should explore whether the leading-term approximation remains accurate as training progresses, and if not, what additional factors need to be considered. This analysis should also include experiments on more complex tasks to determine if the early-stage dynamics are representative of the learning process in more challenging scenarios. Such an analysis would provide a more complete picture of the training dynamics and the role of the identified basis functions.

To broaden the scope of the study, the authors should consider extending their analysis to other neural network architectures, such as recurrent neural networks (RNNs) or convolutional neural networks (CNNs). This would help to determine whether the identified basis functions are specific to attention-based models or if they are a more general property of neural network learning. Additionally, the authors should investigate the impact of different training regimes, such as varying batch sizes, learning rates, or optimization algorithms, on the emergence of these basis functions. This would provide a more comprehensive understanding of the factors that influence the learning of semantic associations and the generalizability of the theoretical framework. Such an analysis would also help to identify the key architectural and training factors that contribute to the emergence of semantic associations.

Finally, to enhance the practical impact of the work, the authors should explore concrete applications of their theoretical findings. This could involve using the identified basis functions to initialize model weights in a way that accelerates training or improves generalization. For example, the authors could investigate whether initializing the attention weights with the theoretical predictions leads to faster convergence or better performance on downstream tasks. Additionally, the authors should explore whether manipulating the basis functions during training can lead to models that are more robust to adversarial examples or that exhibit better transfer learning capabilities. This would provide a more direct link between the theoretical analysis and practical applications, making the work more relevant to the broader machine learning community.

### Questions

1. How do the identified basis functions evolve over longer training periods? Are they still relevant after the model has converged?
2. Can the theoretical framework be extended to other neural network architectures or different training regimes?
3. Are there any practical applications of the findings that could be explored further, such as using the basis functions to improve model training or interpretability?

### Rating

6

### Confidence

3

**********