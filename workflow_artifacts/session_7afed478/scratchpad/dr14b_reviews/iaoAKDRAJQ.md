### Summary

This paper studies the convergence of adaptive optimizers in the non-convex setting. The authors extend the notion of adaptive smoothness to the non-convex setting and show that it precisely characterizes the convergence of adaptive optimizers. They also establish that adaptive smoothness enables acceleration of adaptive optimizers with Nesterov momentum in the convex setting, a guarantee unattainable under standard smoothness for certain non-Euclidean geometry.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

The paper is well-written and easy to follow. The results are novel and significantly improve previous bounds for a wide range of adaptive optimizers. The theoretical analysis is rigorous and well-supported by empirical evidence.

### Weaknesses

#### Some Related Works


#### comment

The paper's focus is primarily on theoretical analysis, and it lacks experiments to validate the theoretical findings. While the convergence analysis is comprehensive, it would be beneficial to see some empirical results that demonstrate the practical implications of the theoretical findings. 

The paper does not discuss the limitations of the proposed analysis and potential directions for future research. Adding a section that addresses these aspects would enhance the paper's completeness and provide valuable insights for the readers.

### Suggestions

The paper would significantly benefit from the inclusion of empirical experiments to validate the theoretical results. Specifically, the authors should demonstrate the performance of adaptive optimizers on non-convex functions, comparing their convergence rates with and without Nesterov momentum. These experiments should be conducted on a variety of datasets and model architectures to show the robustness of the theoretical findings. Furthermore, it would be valuable to visualize the convergence behavior of the optimizers, showing how the adaptive smoothness impacts the optimization process. For example, plotting the objective function value against the number of iterations for different optimizers and settings would provide a clear visual representation of the theoretical results. The experiments should also explore the impact of different hyperparameter settings on the convergence rates, providing practical guidance for users of these optimizers. This would help bridge the gap between theory and practice, making the paper more impactful.

In addition to empirical validation, the paper should include a more detailed discussion of the limitations of the proposed analysis. For instance, the analysis assumes a specific form of adaptive smoothness, and it would be beneficial to discuss how the results might change under different smoothness conditions. The authors should also address the computational cost of the proposed optimizers, especially when compared to simpler methods. Furthermore, the paper should discuss the potential challenges in applying these optimizers to very high-dimensional problems, where the computation of the adaptive smoothness might become prohibitive. It would also be valuable to explore the sensitivity of the results to the choice of hyperparameters, and provide guidelines for selecting appropriate values. This discussion should also include potential directions for future research, such as extending the analysis to other types of adaptive optimizers or exploring the application of these optimizers to different domains.

Finally, the paper should provide more concrete examples of non-convex functions where the proposed analysis is particularly relevant. While the paper provides a theoretical framework, it would be helpful to illustrate how this framework applies to specific practical problems. For example, the authors could discuss the application of their results to training deep neural networks or other machine learning models with non-convex loss functions. This would help readers understand the practical implications of the theoretical findings and motivate further research in this area. The paper should also discuss the potential limitations of the analysis in the context of these specific examples, providing a more nuanced understanding of the applicability of the results.

### Questions

Could you provide some experiments to validate your theoretical findings?

Could you discuss the limitations of your analysis and potential directions for future research?

### Rating

6

### Confidence

4

**********