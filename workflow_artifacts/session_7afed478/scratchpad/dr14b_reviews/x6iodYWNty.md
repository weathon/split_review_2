### Summary

This paper presents Neural Predictor-Corrector (NPC), a reinforcement learning-based framework that unifies diverse problems, including robust optimization, global optimization, polynomial system root-finding, and sampling, under the homotopy paradigm. NPC replaces hand-crafted heuristics with learned policies, achieving superior efficiency and stability across tasks. Extensive experiments demonstrate NPC's effectiveness, outperforming existing approaches in computational efficiency while maintaining high accuracy.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper is well-organized, with clear explanations of the homotopy paradigm, predictor-corrector algorithms, and the proposed Neural Predictor-Corrector (NPC) framework. The use of figures and tables effectively illustrates key concepts and experimental results.

2. The paper provides a comprehensive review of related works, highlighting the gaps that motivate the proposed research. The authors also discuss the limitations of their approach in Appendix D, demonstrating a thorough understanding of the problem domain.

3. The Neural Predictor-Corrector (NPC) framework is a novel contribution that addresses the limitations of traditional homotopy solvers. By unifying diverse problems under a single framework and employing reinforcement learning, the authors present a general, learning-based solver that can be applied across different tasks.

4. The experimental results are extensive and demonstrate the effectiveness of the proposed method. The authors evaluate NPC on four representative homotopy problems, showing that it generalizes well to unseen instances and consistently outperforms existing approaches in terms of computational efficiency and numerical stability.

### Weaknesses

#### Some Related Works


#### comment

1. The paper does not provide a detailed analysis of the computational complexity of the proposed method. While the experimental results demonstrate efficiency gains, a theoretical analysis of the computational cost would be valuable. Specifically, the paper lacks a discussion on how the number of parameters in the neural network scales with the dimensionality of the problem, and how this impacts the overall runtime. Furthermore, the paper does not analyze the computational cost of the reinforcement learning training process itself, which is a significant factor in the overall efficiency of the method.

2. The paper could benefit from a more detailed discussion of the limitations of the proposed method. While Appendix D briefly mentions some limitations, a more in-depth analysis of potential failure cases and scenarios where the method might not perform well would be valuable. For example, the paper does not discuss the sensitivity of the method to the choice of hyperparameters, or how the performance might degrade when applied to problems with highly non-convex landscapes or discontinuous solution spaces. A more thorough analysis of these aspects would provide a more complete picture of the method's applicability.

### Suggestions

To address the lack of computational complexity analysis, the authors should include a detailed discussion on how the number of parameters in the neural network scales with the input dimensionality. This should include a breakdown of the number of parameters in each layer and how these numbers change as the problem size increases. Furthermore, the authors should analyze the computational cost of the reinforcement learning training process, including the time required for each training iteration and the total training time. This analysis should also consider the impact of different hyperparameter settings on the training time. It would be beneficial to provide a theoretical analysis of the computational complexity of the predictor and corrector steps, and how these complexities are affected by the use of neural networks. This analysis should also consider the impact of the number of iterations required for convergence on the overall computational cost.

To improve the discussion of limitations, the authors should provide a more detailed analysis of the method's sensitivity to hyperparameter choices. This should include a discussion of how different learning rates, batch sizes, and network architectures affect the performance of the method. The authors should also investigate the method's performance on problems with highly non-convex landscapes or discontinuous solution spaces. This could involve testing the method on a wider range of benchmark problems and analyzing the results to identify potential failure cases. Furthermore, the authors should discuss the limitations of the method in terms of its ability to generalize to unseen problem instances. This should include an analysis of how the performance of the method degrades as the problem instances become more dissimilar to the training data. The authors should also discuss the potential for the method to be applied to problems with different types of homotopy paths, and how the choice of homotopy path affects the performance of the method.

Finally, the authors should consider including a more detailed analysis of the method's performance in terms of both accuracy and computational efficiency. This should include a comparison of the method's performance with existing approaches in terms of both the number of iterations required for convergence and the overall runtime. The authors should also analyze the trade-off between accuracy and computational efficiency, and discuss how the method can be tuned to achieve the desired balance between these two factors. This analysis should also consider the impact of different problem characteristics on the performance of the method, and how the method can be adapted to handle different types of problems.

### Questions

See weaknesses

### Rating

6

### Confidence

3

**********