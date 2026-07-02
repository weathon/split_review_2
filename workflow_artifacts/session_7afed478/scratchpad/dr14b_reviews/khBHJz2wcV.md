### Summary

The paper introduces a novel framework for fine-tuning flow-matching generative models to enforce physical constraints and solve inverse problems in scientific systems. The authors leverage the adjoint-matching framework to reformulate reward fine-tuning for flow-based generative models as a control problem, steering the base generative process towards high-reward samples via modifying the learned vector field. The method is evaluated on several PDE problems, demonstrating improved satisfaction of physical constraints and accurate recovery of latent coefficients. The authors also show the cross-domain utility of their approach by fine-tuning natural-image models.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper proposes a novel approach for fine-tuning flow-matching generative models to enforce physical constraints and solve inverse problems in scientific systems. The use of adjoint matching for fine-tuning is a technically sound approach, and the theoretical grounding provided through the stochastic optimal control formulation adds rigor to the proposed method.
2. The experimental results demonstrate the effectiveness of the proposed framework across various PDE problems, including Darcy flow, linear elasticity, Helmholtz, and Stokes flow. The ability to reduce residuals and jointly generate solution-parameter pairs is a valuable contribution.
3. The paper is well-written and clearly explains the proposed method and its evaluation. The authors provide a detailed description of the experimental setup and the results, making it easy for readers to understand the contributions of the paper.

### Weaknesses

#### Some Related Works


#### comment

1. The paper primarily focuses on demonstrating the effectiveness of the framework through empirical results. While the experiments cover several canonical PDE problems, a more rigorous theoretical analysis of the proposed method's convergence properties, stability, and error bounds would strengthen the contribution.
2. The comparison with baseline methods is somewhat limited. While PBFM is included, a more comprehensive comparison with other state-of-the-art physics-informed neural networks or methods for solving inverse problems would provide a clearer picture of the advantages and limitations of the proposed framework.
3. The computational cost of the fine-tuning procedure, especially the adjoint matching component, is not discussed in detail. Providing insights into the computational efficiency and scalability of the method would be valuable for practitioners.

### Suggestions

The paper would benefit from a more in-depth theoretical analysis of the proposed method. While the empirical results are promising, a rigorous investigation into the convergence properties of the fine-tuning process is needed. Specifically, it would be valuable to explore how the choice of the reward function and the adjoint matching procedure affect the convergence rate and the stability of the fine-tuned model. Analyzing the error bounds of the approximated solutions and the impact of the noise schedule on the final results would also strengthen the theoretical foundation of the work. Furthermore, a discussion on the sensitivity of the method to the choice of hyperparameters, such as the regularization strength and the parameters of the noise schedule, would be beneficial. This analysis should include a discussion of how these parameters affect the trade-off between the accuracy of the solution and the preservation of the base model's distribution.

To provide a more comprehensive evaluation of the proposed framework, the authors should include a more extensive comparison with other state-of-the-art methods for solving inverse problems and enforcing physical constraints. While the comparison with PBFM is a good starting point, it would be beneficial to compare the proposed method with other physics-informed neural networks (PINNs) and methods that leverage adjoint equations for constraint enforcement. This comparison should include a discussion of the advantages and limitations of each method, as well as a quantitative analysis of their performance on the same set of benchmark problems. Furthermore, the authors should consider comparing their method with other techniques for solving inverse problems, such as those based on optimization or Bayesian inference. This would provide a more complete picture of the strengths and weaknesses of the proposed approach.

Finally, the paper should include a more detailed discussion of the computational cost and scalability of the proposed method. The authors should provide a breakdown of the computational resources required for each step of the fine-tuning process, including the pre-training phase, the adjoint matching phase, and the sampling phase. This analysis should include a discussion of the memory requirements and the time complexity of each step. Furthermore, the authors should discuss the scalability of the method to larger and more complex problems, as well as the potential for parallelization and optimization of the computational pipeline. This discussion should also include an analysis of the trade-off between the computational cost and the accuracy of the results, as well as guidelines for selecting the appropriate hyperparameters to achieve a desired balance between these two factors.

### Questions

1. How does the choice of the reward function affect the performance of the fine-tuning process? Are there specific types of reward functions that are more suitable for certain types of PDE problems?
2. Can the authors provide more details on the computational cost of the fine-tuning procedure? How does it scale with the complexity of the PDE and the size of the training data?
3. How sensitive is the method to the choice of hyperparameters, such as the regularization strength and the parameters of the noise schedule? Are there any guidelines for selecting these hyperparameters in practice?

### Rating

6

### Confidence

3

**********