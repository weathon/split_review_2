### Summary

This paper investigates the optimization dynamics of modern recurrent models, specifically State-Space Models (SSMs) like Mamba, in comparison to Transformers on associative recall and copying tasks. The authors find that SSMs exhibit critical optimization instabilities, with performance highly sensitive to learning rate selection, unlike Transformers which are more robust. They also observe contrasting scaling behaviors: SSMs benefit from increased width, while Transformers struggle in single-layer configurations. The study suggests that the performance gap between SSMs and Transformers may stem from optimization challenges rather than fundamental expressivity limitations.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper provides a comprehensive empirical comparison of SSMs and Transformers on associative recall and copying tasks, using over 3,000 runs and 20,000 GPU hours. The experiments are well-designed and the results are clearly presented.
2. The authors identify and analyze critical optimization instabilities in SSMs, demonstrating that their performance is highly sensitive to learning rate selection. They show that a sparse learning rate grid search can disproportionately impact training outcomes, potentially leading to misleading conclusions about model capabilities.
3. The paper makes important contributions to understanding the practical differences between SSMs and Transformers, highlighting the need for careful hyperparameter tuning and scaling strategies. The findings have implications for both theoretical analysis and practical applications of sequence models.

### Weaknesses

#### Some Related Works


#### comment

1. The paper focuses on synthetic benchmarks and does not validate the findings on real-world language modeling tasks. It is unclear whether the observed optimization dynamics and scaling behaviors would generalize to more complex, natural language data. The synthetic tasks, while useful for controlled experiments, may not capture the nuances of real-world data distributions, potentially limiting the practical relevance of the conclusions. Specifically, the associative recall and copying tasks may not fully reflect the complexities of long-range dependencies and semantic understanding required in natural language processing.
2. The paper primarily focuses on empirical comparisons and does not provide theoretical explanations for the observed optimization instabilities in SSMs. The lack of theoretical grounding makes it difficult to understand the underlying mechanisms causing the sensitivity to learning rates, and whether these instabilities are inherent to the SSM architecture or a result of specific implementation choices. A theoretical analysis could provide insights into how to mitigate these issues. For example, an analysis of the loss landscape or the gradient flow could be beneficial.
3. While the paper identifies the convolutional component as crucial for Mamba's expressivity, it does not fully explore the role of other architectural differences between SSMs and Transformers. The analysis could be expanded to include a more detailed investigation of the impact of gating mechanisms, normalization layers, and different types of recurrent connections on the observed optimization dynamics. This would provide a more complete picture of the factors contributing to the performance differences. For instance, the effect of different activation functions or the depth of the convolutional layers could be investigated.

### Suggestions

To strengthen the paper, the authors should consider expanding their analysis to include real-world language modeling tasks. This would involve evaluating the models on standard benchmarks such as the Penn Treebank or WikiText-103, which would provide a more robust assessment of the generalizability of their findings. Such experiments would help determine if the optimization instabilities observed in the synthetic tasks also manifest in more complex, natural language settings. Furthermore, it would be beneficial to explore the impact of different data preprocessing techniques and data augmentation strategies on the training dynamics of SSMs and Transformers. This would provide a more comprehensive understanding of how these models behave under different data conditions. Additionally, the authors could investigate the effect of different optimization algorithms beyond standard SGD or Adam, as these might interact differently with the architectures.

In addition to empirical analysis, the authors should attempt to provide a theoretical explanation for the observed optimization instabilities in SSMs. This could involve analyzing the loss landscape of these models and investigating the properties of the gradients during training. For example, examining the condition number of the Hessian matrix could provide insights into the curvature of the loss landscape and the sensitivity to learning rate changes. Furthermore, exploring the impact of different initialization schemes on the training dynamics could shed light on the origin of these instabilities. A theoretical analysis could also help identify potential regularization techniques that could mitigate these issues and improve the robustness of SSMs. This could involve techniques such as weight normalization or spectral normalization.

Finally, the authors should conduct a more detailed ablation study to investigate the impact of various architectural components on the performance and stability of SSMs. This could include varying the size and number of convolutional filters, exploring different gating mechanisms, and analyzing the effect of normalization layers. For example, comparing the performance of Mamba with and without layer normalization or with different types of recurrent connections could provide valuable insights into the role of these components. Furthermore, it would be beneficial to explore the impact of different activation functions on the training dynamics. Such a detailed analysis would help identify the key architectural factors contributing to the observed optimization instabilities and provide guidance for designing more robust and efficient SSMs.

### Questions

1. How do the optimization dynamics of SSMs and Transformers compare on real-world language modeling tasks? Do the same learning rate sensitivities and scaling behaviors observed in the synthetic tasks persist in more complex settings?
2. What theoretical explanations might account for the observed optimization instabilities in SSMs? Are there specific properties of their architecture or loss landscape that contribute to this sensitivity?
3. How do other architectural variants of SSMs, such as those with different gating mechanisms or convolutional structures, compare in terms of optimization stability and scaling behavior?

### Rating

6

### Confidence

3

**********