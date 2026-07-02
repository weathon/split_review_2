### Summary

The paper proposes a method for learning rules in natural language for classification tasks using LLMs. The method is called RLIE and consists of four stages: rule generation, logistic regression, iterative refinement, and evaluation. The method is evaluated on six binary classification tasks from HypoBench and compared to a number of baselines. The main findings are that the method is competitive with the baselines and that the rules learned by the method are more compact and clearer than the rules learned by HypoGeniC.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

- The paper is well-written and easy to follow.
- The method is well-motivated and addresses an important problem in the field of natural language processing.
- The method is evaluated on a number of real-world datasets and compared to a number of baselines.
- The results show that the method is competitive with the baselines and that the rules learned by the method are more compact and clearer than the rules learned by HypoGeniC.

### Weaknesses

#### Some Related Works


#### comment

 - The paper does not provide a detailed analysis of the limitations of the method. For example, it would be interesting to see how the method performs on more complex classification tasks or on tasks with a larger number of classes.
- The paper does not provide a detailed analysis of the computational cost of the method. It would be interesting to see how the method scales with the size of the dataset and the number of rules.
- The paper does not provide a detailed analysis of the sensitivity of the method to the choice of hyperparameters. It would be interesting to see how the performance of the method varies with different choices of hyperparameters.

### Suggestions

The paper would benefit from a more thorough investigation into the limitations of the proposed RLIE method. While the current evaluation demonstrates its effectiveness on several binary classification tasks, it is crucial to understand its behavior on more complex scenarios. Specifically, the authors should explore the method's performance on multi-class classification problems, which often present unique challenges due to the increased number of decision boundaries and potential for class imbalance. Furthermore, it would be valuable to assess the method's robustness when dealing with datasets that have a higher degree of noise or ambiguity. This could involve introducing adversarial examples or using datasets with varying levels of label noise. Such an analysis would provide a more comprehensive understanding of the method's strengths and weaknesses, and help identify areas for future improvement. The authors should also consider evaluating the method on tasks with varying degrees of rule complexity, such as those requiring more intricate logical combinations or dependencies between features.

In addition to the limitations of the method, a more detailed analysis of its computational cost is needed. The paper should provide a breakdown of the time complexity of each stage of the RLIE method, including rule generation, logistic regression, iterative refinement, and evaluation. This analysis should consider the impact of various factors, such as the size of the dataset, the number of rules, and the complexity of the rules themselves. It would be beneficial to provide empirical results demonstrating how the runtime scales with these factors. For example, the authors could show how the runtime changes when the number of training examples is increased by an order of magnitude or when the number of rules is doubled. This analysis would help practitioners understand the practical limitations of the method and make informed decisions about its applicability to their specific problems. Furthermore, the authors should discuss the memory requirements of the method, particularly when dealing with large datasets or complex rule sets.

Finally, a more detailed analysis of the sensitivity of the method to the choice of hyperparameters is essential. The paper should provide a systematic study of how the performance of the method varies with different choices of hyperparameters, such as the learning rate, the regularization strength, and the number of iterations. This analysis should include both quantitative results and qualitative observations. For example, the authors could show how the performance of the method changes when the learning rate is increased or decreased by a certain factor. They could also discuss how the choice of regularization strength affects the sparsity of the learned rules and the overall performance of the method. This analysis would help practitioners understand the trade-offs involved in choosing different hyperparameter values and provide guidance on how to select the optimal values for their specific problems. The authors should also consider using techniques such as cross-validation to select the optimal hyperparameters.

### Questions

- How does the method perform on more complex classification tasks or on tasks with a larger number of classes?
- How does the method scale with the size of the dataset and the number of rules?
- How does the performance of the method vary with different choices of hyperparameters?

### Rating

6

### Confidence

3

**********