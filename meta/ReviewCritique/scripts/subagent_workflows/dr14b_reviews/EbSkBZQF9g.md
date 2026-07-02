### Summary

This paper investigates the ability of a single-layer transformer to solve the 0-1 knapsack problem, an NP-complete problem. The authors use visualizations and interpretability techniques to analyze the model's internal behavior and conclude that the transformer struggles to generalize on NP-complete problems due to the combinatorial explosion in considerations involved. They also hypothesize that transformer-based models with k layers will only be able to generalize to tasks which can be solved using O(n^k) time complexity algorithms.

### Soundness

2

### Presentation

2

### Contribution

2

### Strengths

1. The paper addresses an important question about the ability of transformer-based models to solve complex problems, and uses a combination of visualisations and interpretability techniques to provide insights into the model's behaviour.
2. The paper is well-structured and easy to follow, with clear explanations of the methods and results.

### Weaknesses

#### Some Related Works


#### comment

1. The paper lacks a clear definition of the 0-1 knapsack problem and its significance in the context of the study. It is important to explain the problem and its relevance to the research question.
2. The paper does not provide sufficient details about the experimental setup, including the size of the dataset, the training procedure, and the evaluation metrics used. This makes it difficult to reproduce the results and assess the validity of the findings.
3. The paper's conclusion that transformer-based models struggle to generalize on NP-complete problems is not well-supported by the evidence presented. The authors should provide more rigorous analysis and empirical evidence to support their claims.
4. The hypothesis that transformer-based models with k layers will only be able to generalize to tasks which can be solved using O(n^k) time complexity algorithms is not well-justified and requires further investigation.

### Suggestions

The paper needs to provide a more thorough explanation of the 0-1 knapsack problem, including its mathematical formulation and its significance as a benchmark for computational complexity. The authors should clearly articulate why this specific problem is chosen and how it relates to the broader question of transformer model limitations. For example, they could discuss the known algorithms for solving the knapsack problem, such as dynamic programming, and explain why a transformer-based approach might be expected to struggle. Furthermore, the paper should include a discussion of the problem's NP-completeness and how this property makes it challenging for machine learning models. This would provide a stronger foundation for the subsequent analysis and conclusions.

To improve the reproducibility and validity of the findings, the authors must provide a detailed description of the experimental setup. This should include the exact size of the dataset used for training and testing, the specific architecture of the single-layer transformer, the training procedure (including the optimizer, learning rate, batch size, and number of epochs), and the evaluation metrics used to assess the model's performance. The authors should also specify how the input data is encoded and fed into the transformer model. Furthermore, it would be beneficial to include a discussion of the hyperparameter tuning process and the sensitivity of the results to different hyperparameter settings. Without these details, it is difficult to assess the robustness of the findings and to compare them with other studies.

The paper's conclusion that transformer-based models struggle to generalize on NP-complete problems needs more rigorous support. The authors should provide a more in-depth analysis of the model's internal behavior, beyond simple visualizations. For example, they could investigate the attention patterns of the transformer to understand which parts of the input sequence are being attended to and how this relates to the problem's structure. They could also analyze the learned representations of the input data to see if the model is capturing meaningful features. Furthermore, the authors should consider comparing the performance of the transformer model with other machine learning models, such as recurrent neural networks or graph neural networks, to see if the observed limitations are specific to transformers or are a more general issue. Finally, the hypothesis about the relationship between the number of layers and the time complexity of solvable tasks needs more justification and should be framed as a conjecture rather than a conclusion.

### Questions

1. Can you provide a more detailed explanation of the 0-1 knapsack problem and its significance in the context of this study?
2. Can you provide more details about the experimental setup, including the size of the dataset, the training procedure, and the evaluation metrics used?
3. Can you provide more evidence to support your conclusion that transformer-based models struggle to generalize on NP-complete problems?
4. Can you provide more justification for your hypothesis that transformer-based models with k layers will only be able to generalize to tasks which can be solved using O(n^k) time complexity algorithms?

### Rating

3

### Confidence

3

**********