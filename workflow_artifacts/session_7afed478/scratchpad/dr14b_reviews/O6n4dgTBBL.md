### Summary

This paper studies the stability of gradient descent from a control-theoretic perspective. The authors formulate gradient descent as a second-order dynamical system and introduce a controller that guarantees local asymptotic stability by regulating the system’s eigen-structure. The proposed controller is shown to be effective in improving the stability and convergence of gradient descent in numerical experiments.

### Soundness

2

### Presentation

3

### Contribution

2

### Strengths

1. The paper is well-written and easy to follow.
2. The connection between the stability of gradient descent and the curvature of the loss landscape is interesting.
3. The proposed controller is shown to be effective in improving the stability and convergence of gradient descent in numerical experiments.

### Weaknesses

#### Some Related Works


#### comment

1. The proposed controller requires knowledge of the Hessian matrix, which may be difficult to compute or approximate in practice, especially for high-dimensional problems. The paper does not provide a clear strategy for approximating the Hessian in high-dimensional settings, which significantly limits the practical applicability of the proposed method. The computational cost of calculating or approximating the Hessian, and its inverse, is a major concern that needs to be addressed more thoroughly.
2. The paper focuses on the continuous-time formulation of GD, and it is not clear how the results translate to the discrete-time setting. The stability analysis relies on the assumption that the learning rate is sufficiently small, but the paper does not provide a precise characterization of the range of learning rates for which the continuous-time approximation is valid. Furthermore, the paper does not discuss how the discretization process affects the stability properties of the system, and whether the proposed controller remains effective in the discrete-time setting. The lack of analysis in the discrete-time setting is a significant limitation.
3. The experimental results are limited to synthetic loss functions and do not demonstrate the effectiveness of the controller on real-world problems or large-scale datasets. The paper lacks experiments on more complex, non-convex loss landscapes that are typical of real-world machine learning problems. The authors should provide empirical evidence that their method can improve the stability and convergence of GD in more realistic settings.

### Suggestions

The paper introduces an interesting control-theoretic perspective on gradient descent, but there are several areas where the analysis and presentation could be improved. First, the paper should provide a more detailed discussion of the computational cost associated with the proposed controller. Specifically, the authors should analyze the complexity of computing the Hessian and its inverse, and discuss potential strategies for approximating these quantities in high-dimensional settings. It would be beneficial to explore the use of techniques such as low-rank approximations or iterative methods to reduce the computational burden. Furthermore, the authors should provide a more rigorous justification for the use of the continuous-time approximation, including a precise characterization of the range of learning rates for which this approximation is valid. It would also be helpful to discuss the potential impact of discretization on the stability properties of the system, and whether the proposed controller remains effective in the discrete-time setting. The authors could consider providing a discrete-time analysis of the proposed controller, or at least discuss the challenges involved in such an analysis.

Second, the paper should include a more detailed discussion of the limitations of the proposed method. For example, the authors should discuss the potential challenges of applying the controller to non-convex loss landscapes, and whether the controller can guarantee convergence to a global minimum. It would also be helpful to discuss the sensitivity of the controller to the choice of design parameters, and whether there are any guidelines for selecting these parameters in practice. The authors should also address the potential for the controller to introduce new instabilities or oscillations in the system, and how these issues can be mitigated. A more thorough discussion of these limitations would help to provide a more balanced assessment of the proposed method.

Finally, the paper should include more extensive experimental results on a wider range of loss functions, including non-convex functions that are more representative of real-world machine learning problems. The authors should also consider evaluating the performance of the controller on large-scale datasets, and comparing its performance to other stabilization techniques. It would be beneficial to include experiments that explore the sensitivity of the controller to the choice of design parameters, and whether there are any guidelines for selecting these parameters in practice. The authors should also provide a more detailed analysis of the computational cost of the proposed method, and compare it to other optimization algorithms. These additional experiments would help to provide a more comprehensive evaluation of the proposed method and its potential for practical applications.

### Questions

1. Can the authors provide more details on the computational cost of the proposed controller, and discuss potential strategies for reducing the computational cost in high-dimensional settings?
2. How does the proposed controller compare to other stabilization techniques for GD, such as gradient clipping or weight decay?
3. Can the authors provide more insights into the choice of the design parameters $K_1$ and $K_2$? How sensitive is the performance of the controller to the choice of these parameters?

### Rating

5

### Confidence

3

**********