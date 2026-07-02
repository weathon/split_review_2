### Summary

The paper proposes a new diffusion-based approach to solve general integer linear programming (ILP) problems, including both binary and non-binary cases. The authors introduce three one-step diffusion-based solvers, CMILP, SCMILP, and MFILP, which are inspired by consistency, shortcut, and meanflow training techniques, respectively. They also propose an iterative integer projection (IIP) layer to handle non-binary integer problems without requiring costly problem transformations. Additionally, an objective-guided sampling method with momentum is introduced to improve the sampling process. The experimental results demonstrate that the proposed approach outperforms existing learning-based methods on both binary and non-binary instances and shows strong scalability compared to traditional solvers.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a novel approach to solving general ILP problems using one-step diffusion-based solvers, which is a departure from previous two-stage methods.
2. The proposed Iterative Integer Projection (IIP) layer effectively handles non-binary integer problems without requiring costly problem transformations, which is a significant improvement over existing methods.
3. The objective-guided sampling method with momentum improves the sampling process and leads to better solution quality.
4. The experimental results demonstrate the superiority of the proposed methods over existing learning-based methods and show strong scalability compared to traditional solvers.

### Weaknesses

#### Some Related Works


#### comment

1. The paper does not provide a detailed analysis of the computational complexity of the proposed methods, which is important for understanding their scalability and practicality. Specifically, the analysis should consider the dependence of the runtime on the number of variables, constraints, and the dimensionality of the diffusion space. A breakdown of the time spent on different components of the algorithm, such as the forward pass, backward pass, and sampling, would be beneficial.
2. The paper lacks a thorough discussion of the limitations of the proposed methods, such as their performance on large-scale problems or their sensitivity to hyperparameter settings. For instance, it is unclear how the performance degrades as the number of variables and constraints increases significantly. Also, the paper does not explore the impact of different choices for the diffusion model architecture, the number of diffusion steps, or the learning rate on the final solution quality.
3. The paper does not provide a detailed explanation of the training process, including the specific hardware used, the optimization algorithm, and the loss function. This information is crucial for reproducibility and for understanding the computational resources required to train the proposed models. Details on the batch size, learning rate schedule, and regularization techniques should be included.

### Suggestions

The paper would benefit from a more in-depth analysis of the computational complexity of the proposed diffusion-based solvers. This analysis should go beyond simply reporting the runtime and should include a theoretical analysis of the time complexity with respect to the problem size (number of variables and constraints) and the dimensionality of the diffusion space. Furthermore, an empirical analysis should be provided, showing how the runtime scales with these parameters. This could involve experiments on problems of varying sizes, and the results should be presented in a way that clearly shows the relationship between problem size and runtime. A breakdown of the time spent on different parts of the algorithm, such as the forward pass, backward pass, and sampling, would also be valuable for identifying potential bottlenecks and areas for optimization. This detailed analysis would help readers understand the practical limitations of the proposed methods and their suitability for different problem sizes.

To address the lack of discussion on the limitations, the paper should include a more thorough exploration of the performance of the proposed methods on large-scale problems. This could involve experiments on benchmark datasets with a significantly larger number of variables and constraints. The paper should also investigate the sensitivity of the proposed methods to different hyperparameter settings. This could involve a systematic exploration of the impact of different choices for the diffusion model architecture, the number of diffusion steps, the learning rate, and other relevant hyperparameters. The results of these experiments should be presented in a way that clearly shows how the performance of the proposed methods varies with different hyperparameter settings. This would help readers understand the robustness of the proposed methods and how to tune them for different problem instances. Additionally, the paper should discuss the potential limitations of the proposed methods, such as their inability to guarantee optimality or their potential to get stuck in local optima.

Finally, the paper should provide a detailed explanation of the training process, including the specific hardware used, the optimization algorithm, and the loss function. This should include details on the batch size, learning rate schedule, and any regularization techniques used. The authors should also discuss any challenges encountered during training, such as convergence issues or instability. This information is crucial for reproducibility and for understanding the computational resources required to train the proposed models. By providing these details, the authors would make it easier for other researchers to replicate their results and build upon their work. Furthermore, this would allow readers to better understand the practical aspects of implementing the proposed methods and their potential limitations.

### Questions

Please refer to the weakness part.

### Rating

6

### Confidence

3

**********