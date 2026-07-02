### Summary

This paper introduces a multi-grade deep learning (MGDL) framework, which incrementally builds neural networks by training shallow networks on the residuals of previous grades. The authors provide theoretical analysis showing that MGDL reduces to a sequence of convex optimization subproblems when using ReLU activations, enhancing stability and convergence. Empirical results on image regression, denoising, deblurring, and CIFAR-10/100 classification demonstrate that MGDL outperforms standard single-grade deep learning (SGDL) in terms of robustness to learning rates and overall performance.

### Soundness

2

### Presentation

2

### Contribution

2

### Strengths

1. The paper provides a rigorous theoretical foundation for MGDL, including convergence guarantees and spectral analysis of the Jacobian matrices.
2. The authors demonstrate the effectiveness of MGDL across a range of tasks and architectures, including fully connected networks, CNNs, and transformers.
3. The paper includes a detailed analysis of the impact of learning rate, showing that MGDL is more robust than SGDL.

### Weaknesses

#### Some Related Works


#### comment

1. The theoretical analysis relies on several assumptions, such as the convexity of the compact set $\mathcal{W}$ and the boundedness of the Hessian of the loss function. The practical implications of these assumptions are not fully explored. For instance, the assumption of a bounded Hessian might not hold in highly non-convex loss landscapes typical of deep learning, potentially limiting the applicability of the convergence guarantees. Furthermore, the paper does not discuss how the size and shape of the convex set $\mathcal{W}$ might affect the convergence rate or the final solution quality.
2. The experiments are primarily conducted on relatively small datasets and networks. The CIFAR-10 and CIFAR-100 datasets, while standard benchmarks, are limited in size and complexity compared to modern large-scale datasets. This raises concerns about the scalability of MGDL to more complex and realistic scenarios. The paper lacks experiments on larger datasets such as ImageNet or with deeper network architectures, which are necessary to fully validate the practical applicability of MGDL.
3. The paper does not provide a detailed analysis of the computational overhead of MGDL compared to SGDL. While the authors mention that MGDL involves training multiple shallow networks, they do not quantify the additional computational cost in terms of training time or memory requirements. A detailed comparison of the number of parameters, floating-point operations (FLOPs), and GPU memory usage would be necessary to assess the practical efficiency of MGDL, especially when considering the potential need for training multiple grades.

### Suggestions

To strengthen the theoretical analysis, the authors should investigate the sensitivity of their convergence guarantees to violations of the assumptions, particularly the boundedness of the Hessian and the convexity of the set $\mathcal{W}$. It would be beneficial to explore how the convergence behavior changes when these assumptions are relaxed or violated, perhaps through numerical experiments or by considering alternative theoretical frameworks. For example, the authors could analyze the impact of different Hessian norms or explore non-convex optimization techniques to provide a more robust theoretical foundation. Furthermore, a discussion on how to choose the set $\mathcal{W}$ in practice, and how its properties affect the convergence, would be valuable. This could involve providing guidelines or heuristics for selecting appropriate bounds or constraints for the parameter space.

To address the limitations of the experimental evaluation, the authors should conduct experiments on larger and more complex datasets, such as ImageNet, and with deeper network architectures. This would provide a more comprehensive assessment of the scalability and practical applicability of MGDL. It would also be beneficial to compare the performance of MGDL with state-of-the-art optimization algorithms, such as Adam or its variants, to demonstrate its competitiveness in real-world scenarios. The experiments should also include a detailed analysis of the training dynamics, such as the convergence rate and the stability of the training process, to provide a deeper understanding of the behavior of MGDL. Additionally, the authors should explore the impact of different hyperparameter settings on the performance of MGDL, such as the number of grades and the learning rate schedule, to provide practical guidance for users.

Finally, the authors should provide a detailed analysis of the computational overhead of MGDL compared to SGDL. This should include a comparison of the number of parameters, floating-point operations (FLOPs), and GPU memory usage. The authors should also discuss the trade-offs between the computational cost and the performance gains of MGDL. For example, they could investigate whether the performance gains of MGDL justify the additional computational cost, or whether there are ways to reduce the computational overhead of MGDL. This analysis should also consider the potential for parallelizing the training of different grades to reduce the overall training time. A clear understanding of the computational cost of MGDL is essential for assessing its practical applicability and for making informed decisions about when to use it.

### Questions

1. How does the choice of the convex set $\mathcal{W}$ affect the convergence guarantees? Are there any guidelines for selecting $\mathcal{W}$ in practice?
2. Can the authors provide more insights into the eigenvalue analysis? How do the eigenvalues of the Jacobian matrices relate to the performance of MGDL?
3. How does MGDL perform on more complex datasets and architectures, such as ImageNet or ResNet? Are there any limitations to the scalability of MGDL?
4. What is the computational overhead of MGDL compared to SGDL? Is MGDL computationally efficient for large-scale applications?

### Rating

5

### Confidence

3

**********