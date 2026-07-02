### Summary

This paper presents a theoretical analysis of separable neural networks (SepNNs), a class of neural networks that factorize a multivariate function into a linear combination of univariate functions. The paper makes three main contributions:

1) It proves that SepNNs are universal approximators, meaning they can approximate any continuous multivariate function with arbitrary precision.

2) It derives the neural tangent kernel (NTK) regimes for SepNNs, showing that the NTK converges to a deterministic kernel under infinite width and infinite decomposition rank, and to a random kernel under infinite width and fixed decomposition rank.

3) It proposes a new optimization method called separable preconditioned gradient descent (SepPGD) that provably adjusts the eigenvalue distribution of the NTK matrix, alleviating the spectral bias of SepNNs and improving training efficiency.

The paper also includes experiments validating the efficiency of SepNNs and the effectiveness of SepPGD on various tasks such as kernel ridge regression, image and surface representation, and numerical PDE solving using PINNs.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1) The paper provides a comprehensive theoretical analysis of SepNNs, including approximation theory, NTK regimes, and optimization properties.

2) It introduces a new optimization method SepPGD that improves training efficiency and alleviates spectral bias.

3) The paper validates its theoretical results with extensive experiments on various tasks.

4) The work has potential applications in various domains such as computer vision, computational physics, and machine learning.

### Weaknesses

#### Some Related Works


#### comment

1) The paper is very technical and may be difficult for readers without a strong background in neural networks and optimization theory.

2) The experiments mainly focus on synthetic data and some basic applications; more real-world case studies could further demonstrate the practical impact of the work.

3) The proposed SepPGD method may have higher computational overhead than standard gradient descent, especially for large-scale problems.

### Suggestions

The paper would benefit from a more detailed discussion of the practical implications of the theoretical results, particularly regarding the convergence properties of SepPGD. While the authors establish that the NTK converges to a deterministic kernel under certain conditions, it would be valuable to explore how this translates to the optimization landscape and the practical convergence of the SepPGD algorithm. Specifically, a more in-depth analysis of the relationship between the eigenvalue distribution of the NTK and the convergence rate of SepPGD would be beneficial. This could involve examining how the preconditioning affects the condition number of the Hessian and how this impacts the optimization process. Furthermore, it would be useful to provide more concrete examples of how the theoretical results can guide the selection of hyperparameters for SepPGD, such as the learning rate and the frequency of preconditioner updates. A more detailed analysis of the computational cost of SepPGD, including a breakdown of the time spent on preconditioner computation and gradient updates, would also be valuable. This should include a comparison with standard gradient descent and other optimization methods, considering both the number of iterations and the time per iteration. 

To enhance the practical relevance of the work, the authors should consider including experiments on more complex, real-world datasets. While the current experiments on synthetic data and basic applications are useful for validating the theoretical results, they do not fully demonstrate the potential of SepNNs and SepPGD in real-world scenarios. For example, experiments on image classification or natural language processing tasks could provide a more compelling case for the practical impact of the proposed method. Furthermore, it would be beneficial to explore the performance of SepPGD on larger-scale problems, as the current experiments are limited in scale. This could involve using larger datasets or more complex network architectures. It would also be useful to investigate the robustness of SepPGD to different initialization strategies and hyperparameter settings. A sensitivity analysis of the key hyperparameters, such as the learning rate and the preconditioning frequency, would provide valuable insights into the practical applicability of the method. 

Finally, the paper could be improved by providing a more intuitive explanation of the connection between the NTK regime and the optimization behavior of SepNNs. While the authors derive the NTK regimes for SepNNs, it is not immediately clear how these results translate to the practical training dynamics. A more detailed discussion of how the NTK analysis can be used to understand the convergence properties of SepPGD would be beneficial. This could involve explaining how the eigenvalue distribution of the NTK affects the optimization landscape and how the preconditioning in SepPGD mitigates the spectral bias. Furthermore, it would be useful to provide a more detailed comparison of the proposed method with other optimization techniques, such as adaptive gradient methods, in the context of the NTK regime. This would help to clarify the advantages and disadvantages of SepPGD compared to existing approaches.

### Questions

1) How does the computational complexity of SepPGD compare to other preconditioning methods in practice, not just in theory?

2) What are the limitations of the proposed method? Are there any types of problems where SepPGD may not be effective?

3) How does the choice of the rank parameter R affect the performance of SepNNs in practice?

4) Can the theoretical results be extended to other types of neural networks or architectures?

5) How does the NTK regime of SepNNs relate to its optimization behavior and generalization properties?

### Rating

6

### Confidence

3

**********