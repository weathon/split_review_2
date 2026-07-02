### Summary

The paper proposes a new calibration procedure for constructing a lower prediction bound (LPB) for survival time under different treatments in the presence of right-censored data. The key innovation is a reweighting scheme that transforms the problem into a weighted conformal inference problem, allowing for exact marginal coverage guarantees rather than the probably approximately correct (PAC) guarantees provided by previous methods. The procedure is doubly robust, meaning it remains valid if either the weight function or the counterfactual quantile regression model is correctly specified. Empirical evaluations on synthetic and real-world clinical data demonstrate the validity and informativeness of the constructed LPBs, showing that they are less conservative than existing methods while maintaining the desired coverage.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper provides a rigorous theoretical framework, including proofs of exact marginal coverage and the doubly robust property, which strengthens the validity of the proposed method.
2. The method is evaluated on both synthetic and real-world clinical data, demonstrating its practical applicability and effectiveness in a high-stakes domain.
3. The paper is well-organized and clearly written, making the technical details accessible to readers with a background in causal inference and survival analysis.

### Weaknesses

#### Some Related Works


#### comment

1. The paper assumes strong ignorability and overlap conditions, which may not always hold in practice. The authors could discuss the sensitivity of their method to violations of these assumptions. Specifically, the assumption of no unmeasured confounders is a strong one, and the paper should discuss how the presence of such confounders would affect the validity of the lower prediction bound (LPB). Furthermore, while the overlap assumption is mentioned, the paper does not discuss the practical implications of near-violations, where the probability of receiving a particular treatment is very low for some individuals, potentially leading to unstable estimates.
2. The computational complexity of the weighted conformal prediction procedure could be a limitation for large datasets. The paper could benefit from a more detailed analysis of the computational cost and potential strategies for improving efficiency. The current discussion lacks a precise characterization of how the runtime scales with the number of observations, the number of treatments, and the complexity of the underlying survival models. It would be beneficial to include a breakdown of the computational cost associated with each step of the algorithm, such as the estimation of the weight function and the counterfactual quantile regression model.
3. The paper could provide more details on the practical implementation of the method, such as how to choose the hyperparameter τ and how to handle multiple testing or model selection. The choice of τ is critical for the performance of the method, and the paper should provide more guidance on how to select this parameter in practice. Additionally, the paper should discuss how the method can be adapted to handle scenarios where multiple hypotheses are being tested or where model selection is involved, as these situations can introduce additional challenges for maintaining valid coverage.

### Suggestions

The paper should delve deeper into the practical implications of the strong ignorability assumption. While it is a common assumption in causal inference, it is crucial to acknowledge its limitations and discuss how violations might affect the results. For instance, the presence of unmeasured confounders could bias the estimated LPBs, and the paper should explore sensitivity analysis techniques to assess the robustness of the method to such violations. Furthermore, the paper should provide more guidance on how to assess the overlap assumption in practice, including the use of diagnostic plots or statistical tests to identify potential violations. It would also be beneficial to discuss strategies for mitigating the impact of near-violations, such as truncating the weights or using alternative estimation techniques that are more robust to small treatment probabilities. The authors could also consider including a simulation study that explicitly examines the performance of the method under different degrees of violation of the ignorability and overlap assumptions.

To address the computational concerns, the paper should provide a more detailed analysis of the time and space complexity of the proposed method. This analysis should include a breakdown of the computational cost associated with each step of the algorithm, such as the estimation of the weight function and the counterfactual quantile regression model. The authors should also discuss potential strategies for improving the efficiency of the method, such as using parallel computing or approximation techniques. It would be helpful to include a table or figure that shows how the runtime scales with the number of observations, the number of treatments, and the complexity of the underlying survival models. Furthermore, the paper should discuss the memory requirements of the method, particularly for large datasets, and provide guidance on how to manage memory usage effectively.

Regarding the practical implementation, the paper should provide more specific guidance on how to choose the hyperparameter τ. The authors should discuss the trade-offs between coverage and the informativeness of the LPB, and provide recommendations on how to select τ based on the specific application. It would be beneficial to include a sensitivity analysis that examines the impact of different values of τ on the performance of the method. Additionally, the paper should discuss how the method can be adapted to handle scenarios where multiple hypotheses are being tested or where model selection is involved. This could include the use of Bonferroni correction or other methods for controlling the family-wise error rate. The authors should also discuss the potential impact of model selection on the validity of the LPBs and provide guidance on how to select the best model while maintaining valid coverage.

### Questions

1. How sensitive is the method to violations of the strong ignorability and overlap assumptions?
2. What are the computational costs of the proposed method, and how does it scale with the size of the dataset?
3. How should the hyperparameter τ be chosen in practice, and how does it affect the performance of the method?

### Rating

6

### Confidence

3

**********