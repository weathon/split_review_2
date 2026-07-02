### Summary

This paper introduces a novel generative framework called CorreGen, which addresses the challenges of noisy correspondence in multi-view clustering. The authors identify two critical forms of noisy correspondence: category-level mismatch and sample-level mismatch. CorreGen formulates noisy correspondence learning as maximum likelihood estimation over underlying cross-view correspondences, solved via an Expectation-Maximization algorithm. The framework effectively uncovers latent correspondences and filters out noise, demonstrating significant improvements in clustering robustness on both synthetic and real-world noisy datasets.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper presents a novel generative framework, CorreGen, which shifts from the traditional discriminative contrastive objective to a generative one, offering a fresh perspective on handling noisy correspondence in multi-view clustering.
2. The authors provide a comprehensive analysis of the noisy correspondence problem, identifying and formalizing two critical types of noisy correspondence: category-level mismatch and sample-level mismatch.
3. The paper is well-structured and clearly written, making it easy to follow the proposed methodology and understand the experimental results.

### Weaknesses

#### Some Related Works


#### comment

1. The paper does not provide a thorough analysis of the computational complexity of the CorreGen framework. Specifically, the time and memory requirements for training and inference, especially with respect to the number of views, samples, and latent variables, are not discussed. This lack of analysis makes it difficult to assess the scalability of the proposed method for large-scale datasets. Furthermore, the paper does not provide any empirical results on the convergence speed of the EM algorithm, which is crucial for practical applications.
2. The paper does not include a detailed ablation study to evaluate the contribution of individual components of the CorreGen framework, such as the GMM-guided marginals in the E-step and the robust correspondence learning in the M-step. Without such an analysis, it is difficult to understand the importance of each component and whether the overall performance gain is due to a specific part of the framework or the synergistic effect of all components. For example, it is unclear how much performance is lost if the GMM marginals are replaced with simpler alternatives, or if the robust correspondence learning is not used.
3. The paper lacks a discussion of the sensitivity of the CorreGen framework to hyperparameter settings, such as the number of GMM components, the learning rate, and the regularization parameters. Without this analysis, it is difficult to determine the robustness of the method and provide guidance for practitioners on how to choose appropriate hyperparameter values for different datasets. The paper should also discuss the potential impact of these hyperparameters on the convergence and stability of the EM algorithm.

### Suggestions

The paper should include a detailed analysis of the computational complexity of the CorreGen framework. This analysis should consider the time and memory requirements for each step of the algorithm, including the E-step and the M-step, and how these requirements scale with the number of views, samples, and latent variables. The authors should also provide empirical results on the convergence speed of the EM algorithm, such as the number of iterations required to reach a certain level of performance or the change in log-likelihood over iterations. This analysis should be presented in a clear and concise manner, with appropriate tables and figures to support the claims. Furthermore, the authors should discuss the practical implications of their findings, such as the feasibility of using the method on large-scale datasets and the potential for optimization.

To better understand the contribution of individual components of the CorreGen framework, the authors should conduct a thorough ablation study. This study should systematically remove or replace each component of the framework and evaluate the impact on the overall performance. For example, the authors could compare the performance of the full CorreGen framework with a version that uses simpler alternatives to the GMM-guided marginals, or a version that does not use robust correspondence learning. The results of this ablation study should be presented in a clear and concise manner, with appropriate tables and figures to support the claims. This analysis will help to identify the most important components of the framework and provide insights into the underlying mechanisms of the method.

Finally, the paper should include a detailed analysis of the sensitivity of the CorreGen framework to hyperparameter settings. This analysis should systematically vary the values of key hyperparameters, such as the number of GMM components, the learning rate, and the regularization parameters, and evaluate the impact on the overall performance. The authors should also discuss the potential impact of these hyperparameters on the convergence and stability of the EM algorithm. The results of this analysis should be presented in a clear and concise manner, with appropriate tables and figures to support the claims. This analysis will help to determine the robustness of the method and provide guidance for practitioners on how to choose appropriate hyperparameter values for different datasets.

### Questions

1. How sensitive is the CorreGen framework to the choice of hyperparameters, such as the number of GMM components, the learning rate, and the regularization parameters? What are the best practices for selecting these hyperparameters for different datasets?
2. What is the computational complexity of the CorreGen framework, and how does it scale with the number of views, samples, and latent variables? What are the time and memory requirements for training and inference?
3. How does the convergence speed of the EM algorithm in CorreGen compare to other multi-view clustering methods? What are the practical implications of the convergence speed for large-scale datasets?
4. How does the performance of CorreGen vary with different levels of category-level and sample-level mismatch? What are the limitations of the method in handling extreme cases of mismatch?
5. Can the authors provide more insights into the choice of the GMM for marginal estimation in the E-step? How does the number of GMM components affect the performance, and what are the guidelines for selecting this parameter?

### Rating

6

### Confidence

3

**********