### Summary

This paper studies the effect of the sparsity hyperparameter $L_0$ on sparse autoencoders (SAEs) trained on large language model (LLM) activations. The authors demonstrate that when $L_0$ is too low, the SAE mixes correlated features to improve reconstruction, and when $L_0$ is too high, the SAE also mixes features. They propose a proxy metric based on decoder patterns to guide the selection of the correct $L_0$ for an SAE on a given training distribution. The authors validate their findings on toy models and real LLM SAEs, showing that their method finds the correct $L_0$ and coincides with peak sparse probing performance in LLM SAEs.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

- The paper is well-written and easy to follow.
- The authors provide a clear and detailed explanation of the toy model experiments, which helps to understand the effect of $L_0$ on SAEs.
- The authors validate their findings on real LLM SAEs, which demonstrates the practical significance of their work.
- The authors provide a proxy metric to guide the selection of the correct $L_0$ for an SAE on a given training distribution.

### Weaknesses

#### Some Related Works


#### comment

 - The authors only evaluate their method on one model (Gemma-2-2b) and one dataset (Pile). It would be helpful to see how the method performs on other models and datasets.
- The authors only evaluate their method on one layer of the model (layer 5). It would be helpful to see how the method performs on other layers of the model.
- The authors do not compare their method to other methods for selecting the correct $L_0$.

### Suggestions

The paper would benefit from a more thorough evaluation of the proposed method across a wider range of models and datasets. While the results on Gemma-2-2b and the Pile dataset are promising, it is crucial to assess the method's robustness and generalizability. Specifically, the authors should consider evaluating their approach on models with different architectures and sizes, such as Llama or other open-source models, and on datasets with varying characteristics, such as code or scientific text. This would provide a more comprehensive understanding of the method's strengths and limitations. Furthermore, it would be beneficial to explore the performance of the method on datasets that are significantly different from the training data to assess its ability to generalize to unseen data distributions. This would help to establish the practical applicability of the method in real-world scenarios.

In addition to expanding the evaluation to different models and datasets, the authors should also investigate the method's performance across different layers of the model. The current evaluation focuses solely on layer 5, which may not be representative of the entire model. It is important to analyze how the optimal $L_0$ value varies across different layers and whether the proposed metric can effectively capture these variations. For example, earlier layers might require different sparsity levels compared to later layers due to the different types of features they learn. By evaluating the method on multiple layers, the authors can gain a more complete understanding of its behavior and identify potential limitations. This analysis should include a comparison of the optimal $L_0$ values across layers and an investigation into the reasons behind these differences.

Finally, the authors should provide a more detailed comparison of their method to existing approaches for selecting the correct $L_0$. While the paper mentions that the sparsity-reconstruction tradeoff is not a good metric, it does not provide a comprehensive comparison to other methods. The authors should discuss the advantages and disadvantages of their approach compared to alternative techniques, such as those based on information theory or Bayesian methods. This comparison should include a discussion of the computational cost, accuracy, and robustness of each method. Furthermore, the authors should provide a theoretical justification for their proposed metric and explain why it is expected to perform well in practice. This would help to establish the novelty and significance of their contribution.

### Questions

- Have you evaluated your method on other models and datasets? If so, how does it perform?
- Have you evaluated your method on other layers of the model? If so, how does it perform?
- How does your method compare to other methods for selecting the correct $L_0$?

### Rating

6

### Confidence

3

**********