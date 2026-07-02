### Summary

This paper explores the advantages of structure-preserving machine learning models for dynamical systems, arguing that these models require smaller sizes and less data to achieve robust generalization compared to structure-naive approaches. The authors present two case studies: a dissipative heat transfer system and a conservative Fermi-Pasta-Ulam-Tsingou (FPUT) system. They demonstrate that by incorporating geometric and physical priors, such as symmetric positive definite constraints for dissipative systems and symplectic structures for conservative systems, structure-aware models can better capture the underlying dynamics, leading to improved performance and stability.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper is well-organized and clearly written, making it easy to follow the authors' arguments and methodology.
2. The use of Riemannian optimization for dissipative systems and symplectic Hamiltonian neural networks for conservative systems is innovative and well-justified.
3. The paper provides a thorough comparison between structure-preserving and structure-naive models, demonstrating the advantages of the former in terms of generalization and stability.

### Weaknesses

#### Some Related Works


#### comment

1. The paper could benefit from a more detailed discussion of the limitations of the proposed methods, particularly in terms of scalability to high-dimensional systems and sensitivity to hyperparameter choices. Specifically, the paper lacks a discussion on how the computational cost of Riemannian optimization scales with the dimensionality of the system, and how the choice of the Riemannian metric affects the convergence and stability of the optimization process. Furthermore, the sensitivity of the symplectic Hamiltonian neural network to the choice of symplectic integrator and network architecture is not explored in sufficient detail.
2. While the case studies are well-chosen, the paper could be strengthened by including a wider range of examples, particularly from different engineering domains, to demonstrate the general applicability of the proposed approach. The current examples are limited to heat transfer and a specific type of conservative system. It would be beneficial to see examples from fluid dynamics, structural mechanics, or other areas where dynamical systems play a crucial role, to better assess the versatility of the proposed methods.
3. The paper could provide more details on the practical implementation of the proposed methods, including specific choices of optimization algorithms, hyperparameters, and evaluation metrics. For example, the paper does not specify the exact form of the loss function used for training the Riemannian optimization, nor does it detail the specific symplectic integrator used in the symplectic Hamiltonian neural network. This lack of detail makes it difficult to reproduce the results and assess the robustness of the proposed methods.

### Suggestions

To address the limitations regarding scalability, the authors should include a more detailed analysis of the computational complexity of their proposed methods, particularly the Riemannian optimization. This should include a discussion of how the computational cost scales with the dimensionality of the system and the number of parameters in the model. Furthermore, the authors should investigate the sensitivity of the Riemannian optimization to the choice of the Riemannian metric and provide guidelines for selecting appropriate metrics for different types of dissipative systems. For the symplectic Hamiltonian neural network, a more thorough analysis of the sensitivity to different symplectic integrators and network architectures is needed. This could involve comparing the performance of different integrators and architectures on a range of conservative systems, and providing recommendations for selecting the most appropriate options. The authors should also consider including a discussion of the limitations of the proposed methods in terms of their ability to handle non-smooth or discontinuous dynamics, which are common in many real-world systems.

To broaden the applicability of the proposed methods, the authors should include additional case studies from different engineering domains. For example, they could consider applying their methods to problems in fluid dynamics, such as the simulation of turbulent flows, or to problems in structural mechanics, such as the analysis of vibrations in complex structures. These additional examples would help to demonstrate the versatility of the proposed methods and their potential for solving a wider range of real-world problems. Furthermore, the authors should consider including a discussion of the challenges involved in applying their methods to systems with high levels of uncertainty or noise, and provide guidance on how to address these challenges. This could involve exploring the use of robust optimization techniques or incorporating uncertainty quantification methods into their framework.

Finally, to improve the reproducibility of the results, the authors should provide more detailed information on the practical implementation of their methods. This should include a specification of the exact form of the loss function used for training the Riemannian optimization, the specific symplectic integrator used in the symplectic Hamiltonian neural network, and the choice of hyperparameters. The authors should also provide a detailed description of the evaluation metrics used to assess the performance of their models, and explain why these metrics were chosen. Furthermore, the authors should consider making their code publicly available, which would greatly facilitate the reproducibility of their results and allow other researchers to build upon their work.

### Questions

1. How do the proposed methods scale to high-dimensional systems, and what are the computational trade-offs involved?
2. Can the authors provide more insights into the sensitivity of their methods to hyperparameter choices and the selection of inductive biases?
3. Are there any plans to extend the proposed framework to handle more complex or non-smooth dynamical systems?

### Rating

6

### Confidence

3

**********