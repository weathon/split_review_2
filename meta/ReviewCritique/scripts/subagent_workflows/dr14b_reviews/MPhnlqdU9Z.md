### Summary

The paper introduces the concept of monitorability, which is the intrinsic ability of a model to highlight potential inference errors through internal activations. The paper proposes the Monitorability via Input peRturbAtion (MIRA) Score, a practical measure that quantifies this property without requiring external OoD data. The method accounts for the behavior of the model near the decision boundary by applying norm-bounded input perturbations, and evaluates how distinguishable the resulting internal representations are by using Mahalanobis distance. The paper validates MIRA by comparing it against the best achievable OoD detection performance across three representative methods. Through experiments across multiple architectures and domain applications, the paper shows that the MIRA Score correlates with the strongest actual detection performance, providing a reliable tool for evaluating and comparing monitorability across different models.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

- The paper introduces a novel concept of monitorability, which is the intrinsic ability of a model to highlight potential inference errors through internal activations. This is an important and timely problem, as it addresses the need for reliable and trustworthy AI systems.
- The paper provides a formal definition of monitorability and proposes the Monitorability via Input peRturbAtion (MIRA) Score, a practical measure that quantifies this property without requiring external OoD data. This is a significant contribution, as it provides a way to evaluate and compare the monitorability of different models.
- The paper validates MIRA by comparing it against the best achievable OoD detection performance across three representative methods. This provides empirical evidence for the effectiveness of MIRA as a measure of monitorability.
- The paper shows that the MIRA Score correlates with the strongest actual detection performance, providing a reliable tool for evaluating and comparing monitorability across different models. This is a valuable result, as it suggests that MIRA can be used to identify models that are more likely to detect potential inference errors.

### Weaknesses

#### Some Related Works


#### comment

 - The paper does not provide a clear explanation of how the MIRA Score is computed. It would be helpful to provide a step-by-step explanation of the algorithm, including the inputs, outputs, and intermediate steps. Specifically, the paper lacks details on how the Mahalanobis distance is calculated for the internal representations, and how the perturbations are applied to the input data. The description of the perturbation process is vague, and it is unclear how the magnitude of the perturbation is determined and whether it is adaptive to the input data or fixed.
- The paper does not provide a clear explanation of how the MIRA Score is related to the concept of monitorability. It would be helpful to provide a more detailed explanation of the theoretical underpinnings of the MIRA Score and how it captures the intrinsic ability of a model to highlight potential inference errors through internal activations. The connection between the Mahalanobis distance and the ability to detect inference errors is not clearly established. It is unclear why a larger Mahalanobis distance would necessarily indicate a higher likelihood of detecting inference errors. The paper needs to provide a more rigorous justification for this connection.
- The paper does not provide a clear explanation of how the MIRA Score can be used to improve the performance of existing OoD detection methods. It would be helpful to provide a more detailed explanation of how the MIRA Score can be used to identify models that are more likely to detect potential inference errors, and how this information can be used to improve the performance of existing OoD detection methods. The paper should provide concrete examples of how the MIRA score can be used to select models or guide the development of new OoD detection techniques. It is not clear how the MIRA score can be integrated into existing OoD detection pipelines.

### Suggestions

The paper should provide a more detailed explanation of the MIRA score computation, including a step-by-step breakdown of the algorithm. Specifically, the authors should clarify how the Mahalanobis distance is calculated for the internal representations. This should include a description of the mean and covariance matrix used in the calculation, and how these are derived from the training data. The paper should also provide a detailed explanation of the perturbation process, including how the magnitude of the perturbation is determined, and whether it is adaptive to the input data or fixed. It would be beneficial to include a pseudocode representation of the algorithm to enhance clarity. Furthermore, the authors should provide a more detailed explanation of the theoretical underpinnings of the MIRA score and how it captures the intrinsic ability of a model to highlight potential inference errors through internal activations. The connection between the Mahalanobis distance and the ability to detect inference errors needs to be rigorously justified. The authors should explain why a larger Mahalanobis distance would necessarily indicate a higher likelihood of detecting inference errors. This explanation should include a discussion of the assumptions made about the distribution of internal representations and how these assumptions relate to the detection of inference errors. The paper should also discuss the limitations of the MIRA score and under what conditions it might not be a reliable measure of monitorability.

To enhance the practical utility of the MIRA score, the paper should provide concrete examples of how it can be used to improve the performance of existing OoD detection methods. The authors should explain how the MIRA score can be used to identify models that are more likely to detect potential inference errors, and how this information can be used to improve the performance of existing OoD detection methods. For example, the paper could explore how the MIRA score can be used to select models for a specific task, or how it can be used to guide the development of new OoD detection techniques. The authors should also discuss how the MIRA score can be integrated into existing OoD detection pipelines. This could include a discussion of the computational cost of computing the MIRA score, and how this cost can be minimized. The paper should also provide a more detailed analysis of the experimental results, including a discussion of the limitations of the evaluation methods used. The authors should discuss the potential biases in the evaluation methods, and how these biases might affect the conclusions drawn from the results. The paper should also provide a more detailed analysis of the relationship between the MIRA score and the performance of different OoD detection methods, including a discussion of the factors that might influence this relationship.

Finally, the paper should provide a more detailed discussion of the limitations of the MIRA score and under what conditions it might not be a reliable measure of monitorability. The authors should discuss the potential biases in the evaluation methods, and how these biases might affect the conclusions drawn from the results. The paper should also provide a more detailed analysis of the relationship between the MIRA score and the performance of different OoD detection methods, including a discussion of the factors that might influence this relationship. The authors should also discuss the potential for future work in this area, including the development of new methods for measuring monitorability and improving the performance of OoD detection methods. The paper should also discuss the potential for using the MIRA score to identify models that are vulnerable to adversarial attacks, and how this information can be used to improve the robustness of AI systems.

### Questions

- Can you provide a more detailed explanation of how the MIRA Score is computed, including a step-by-step breakdown of the algorithm?
- Can you provide a more detailed explanation of how the MIRA Score is related to the concept of monitorability, and how it captures the intrinsic ability of a model to highlight potential inference errors through internal activations?
- Can you provide a more detailed explanation of how the MIRA Score can be used to improve the performance of existing OoD detection methods, and how this information can be used to identify models that are more likely to detect potential inference errors?

### Rating

6

### Confidence

3

**********