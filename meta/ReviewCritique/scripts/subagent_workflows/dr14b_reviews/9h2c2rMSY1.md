### Summary

This paper proposes a weighted conformal prediction method for uncertainty quantification of time-dependent PDEs. The paper shows the limitations of naive conformal prediction methods in this setting, and shows that the proposed method can address these limitations.

### Soundness

3

### Presentation

3

### Contribution

2

### Strengths

The paper is well-written and easy to follow. The proposed method is sound and addresses an important problem.

### Weaknesses

#### Some Related Works


#### comment

1. The proposed method is limited to linear PDEs. Extending it to non-linear PDEs seems challenging.
2. The experiments are limited to a synthetic dataset. More real-world applications should be considered to demonstrate the practical applicability of the method.
3. The experiments only consider a specific type of PDEs, and with a specific surrogate model. More types of PDEs and surrogate models should be considered to demonstrate the broad applicability of the proposed method.  
4. The proposed method requires the calculation of the mean and covariance matrix of the Gaussian distribution at each time $t$. This can be computationally expensive, especially for high-dimensional problems.

### Suggestions

The paper's primary limitation lies in its focus on linear PDEs, which significantly restricts its applicability to real-world scenarios where non-linear PDEs are the norm. While the authors propose a weighted conformal prediction method, the core theoretical results rely on the linearity of the PDE, specifically the ability to express the solution as a linear transformation of the initial conditions. This approach does not readily extend to non-linear PDEs, where such a linear relationship does not exist. The authors should acknowledge this limitation more explicitly and discuss the challenges of extending their method to non-linear cases. For example, they could explore the use of linearization techniques, such as Taylor series expansions, or consider alternative approaches, such as kernel methods, which can handle non-linearities. Furthermore, the paper should include a discussion on the limitations of the Gaussian assumption, and how this might affect the performance of the method in practice.

Another significant weakness is the limited experimental validation. The experiments are conducted solely on synthetic datasets, which do not fully capture the complexities of real-world problems. The authors should include more real-world applications to demonstrate the practical applicability of their method. For example, they could consider problems from fluid dynamics, heat transfer, or other areas where PDEs are commonly used. Additionally, the experiments should explore a wider range of PDEs and surrogate models. The current experiments only consider a specific type of PDE with a specific surrogate model, which does not provide sufficient evidence for the broad applicability of the proposed method. The authors should consider different types of PDEs, such as parabolic, hyperbolic, and elliptic equations, and different surrogate models, such as neural networks, Gaussian processes, and other machine learning models. This would provide a more comprehensive evaluation of the method's performance and robustness.

Finally, the computational cost of the proposed method is a concern, particularly the calculation of the mean and covariance matrix at each time step. While the authors mention that the covariance matrix can be computed using fast Fourier transforms, they do not provide a detailed analysis of the computational complexity of their method. The authors should provide a more thorough discussion of the computational cost and its scaling with the problem size. They should also explore potential ways to reduce the computational cost, such as using low-rank approximations of the covariance matrix or other techniques for reducing the computational burden. Furthermore, the authors should discuss the practical implications of the $\mathcal{O}(n_\infty > 0)$ complexity, and how this might limit the applicability of their method to large-scale problems. The authors should also consider the memory requirements of their method, particularly for high-dimensional problems.

### Questions

1. Can the proposed method be extended to non-linear PDEs? 
2. Can the authors provide more real-world applications?
3. Can the authors provide more types of PDEs and surrogate models in the experiments?
4. The proposed method requires the calculation of the mean and covariance matrix of the Gaussian distribution at each time $t$. This can be computationally expensive, especially for high-dimensional problems. Can the authors discuss the computational complexity of the proposed method and potential ways to reduce it?

### Rating

6

### Confidence

4

**********