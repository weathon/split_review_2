### Summary

The paper introduces "Marginal Flow," a novel and efficient framework for density estimation that addresses several limitations of current models, including high computational costs, mode collapse, and restrictive architectures. Unlike traditional methods, Marginal Flow leverages a marginalization technique that samples latent parameters from a learnable distribution, enabling fast and exact density evaluations. This approach allows for flexibility in neural network design, efficient handling of multi-modal distributions, and adaptation to lower-dimensional manifolds. Extensive experiments demonstrate that Marginal Flow outperforms competing models in speed and accuracy across various tasks, including synthetic data generation, simulation-based inference, and complex data structures like positive definite matrices and image latents.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

- Novelty: The paper presents a unique approach to density estimation by leveraging marginalization, overcoming limitations of existing models.
- Efficiency: Marginal Flow offers significant improvements in computational efficiency, achieving faster sampling and density evaluation compared to competing methods.
- Versatility: The framework handles multimodal distributions effectively, supports manifold learning, and adapts well to diverse data types.
- Empirical Validation: Comprehensive experiments validate the theoretical claims, demonstrating superior performance on multiple benchmarks.
- Practical Impact: The proposed method has potential applications in various domains requiring efficient and accurate density estimation.

### Weaknesses

#### Some Related Works


#### comment

 - Limited discussion of potential limitations or failure modes of the proposed method
- Theoretical analysis could be expanded to provide deeper insights into the properties and guarantees of Marginal Flow

### Suggestions

The paper would benefit from a more thorough exploration of the limitations and potential failure modes of the Marginal Flow framework. While the empirical results are promising, it is crucial to understand the scenarios where the method might struggle. For instance, it would be valuable to investigate the sensitivity of the method to the choice of the base distribution for the latent parameters. Does the performance degrade significantly with poorly chosen base distributions? Furthermore, the paper should discuss the computational cost associated with increasing the number of latent parameters, $N_c$. While the authors claim efficiency, a detailed analysis of how the runtime scales with $N_c$ is necessary to fully assess the practical applicability of the method, especially in high-dimensional settings. It would also be beneficial to explore the impact of the neural network architecture used to model the learnable distribution. Are there specific architectures that are more suitable for this framework, and what are the trade-offs involved in choosing different architectures? Providing a more nuanced discussion of these aspects would strengthen the paper's contribution and provide valuable guidance for practitioners.

To enhance the theoretical foundation of the paper, a more rigorous analysis of the properties of Marginal Flow is needed. Specifically, the paper should delve deeper into the convergence properties of the proposed iterative algorithm. What are the conditions under which the algorithm is guaranteed to converge to a stable solution? Moreover, it would be beneficial to investigate the relationship between the learned distribution of latent parameters and the target distribution. Can we establish any theoretical bounds on the approximation error? Furthermore, the paper should explore the implications of using a Monte Carlo estimate for the density evaluation. While the authors mention that the variance decreases as $1/N_c$, a more detailed analysis of the bias and variance trade-offs would be valuable. This could involve exploring alternative estimation techniques or providing guidelines for choosing an appropriate value of $N_c$ to balance accuracy and computational cost. A more robust theoretical analysis would significantly increase the credibility and impact of the proposed method.

Finally, the paper should provide more clarity on the practical aspects of implementing Marginal Flow. For example, the authors should elaborate on the specific optimization techniques used to train the neural network and the hyperparameter tuning process. What are the best practices for initializing the network weights and selecting the learning rate? Furthermore, the paper should discuss the memory requirements of the method, especially when dealing with large values of $N_c$. How does the memory footprint scale with the number of latent parameters and the dimensionality of the data? Addressing these practical considerations would make the paper more accessible and useful to a wider audience. Including a more detailed discussion of these implementation details would greatly improve the paper's overall quality and impact.

### Questions

1. What are the main limitations or failure modes of Marginal Flow?
2. Is there a theoretical guarantee for the convergence of the iterative algorithm presented in Eq. (12)?
3. How sensitive is the performance of Marginal Flow to the choice of hyperparameters, such as the number of latent parameters, $N_c$, and the architecture of the neural network?

### Rating

6

### Confidence

3

**********