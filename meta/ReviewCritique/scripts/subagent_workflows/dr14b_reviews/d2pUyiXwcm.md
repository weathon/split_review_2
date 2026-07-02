### Summary

The paper introduces SCaSML, a novel framework for improving the accuracy of pre-trained PDE solvers at inference time. SCaSML leverages a defect correction method to derive a new PDE, termed the Structural-preserving Law of Defect, which describes the error of a given surrogate model. This defect PDE retains the structure of the original problem, allowing it to be solved efficiently with traditional stochastic simulators, resulting in a targeted correction to the initial machine-learned solution. The framework is shown to reduce the error of surrogate models on challenging PDEs up to 160 dimensions, demonstrating its potential to enhance the trustworthiness of AI for scientific discovery.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

The paper presents a novel approach to improving the accuracy of pre-trained PDE solvers at inference time, which is a significant contribution to the field of Scientific Machine Learning. The idea of using a defect correction method to derive a new PDE that describes the error of a surrogate model is innovative and has the potential to be widely applicable. The paper is well-written and clearly explains the methodology and the theoretical underpinnings of the approach. The experimental results are compelling, demonstrating that SCaSML can significantly reduce the error of surrogate models on challenging PDEs. The authors also provide a thorough comparison with existing methods, highlighting the advantages of their approach.

### Weaknesses

#### Some Related Works


#### comment

The paper could benefit from a more detailed discussion of the computational cost associated with the SCaSML framework. While the authors mention that the method is efficient, a quantitative analysis of the computational overhead compared to traditional methods and pure machine learning approaches would be valuable. Specifically, the paper lacks a detailed breakdown of the time spent in each stage of the SCaSML framework, such as the surrogate model training, the defect correction PDE solution, and the stochastic simulation. This makes it difficult to assess the practical scalability of the method, especially for very high-dimensional problems. Furthermore, the paper does not discuss the memory requirements of the proposed method, which is a critical factor when dealing with high-dimensional PDEs.

The authors primarily focus on semi-linear parabolic PDEs. While this is a significant class of PDEs, it would be helpful to discuss the potential applicability and limitations of SCaSML for other types of PDEs, such as elliptic or hyperbolic equations. The paper should elaborate on the specific challenges that might arise when extending the method to these different types of PDEs, such as the need for different numerical solvers or the potential for instability. A more detailed discussion of the assumptions required for the defect correction method to be effective would also be beneficial.

### Suggestions

To address the lack of detailed computational cost analysis, the authors should include a comprehensive breakdown of the time complexity for each stage of the SCaSML framework. This should include the time spent on surrogate model training, defect correction PDE solution, and stochastic simulation. The analysis should also consider the scaling of computational cost with respect to the dimensionality of the problem and the desired accuracy. Furthermore, the authors should provide a comparison of the computational cost of SCaSML with traditional numerical methods and pure machine learning approaches, highlighting the trade-offs between accuracy and computational efficiency. This analysis should be supported by empirical results, showing the runtime of each stage for different problem sizes and complexities. The memory footprint of the method should also be discussed, especially in the context of high-dimensional problems, and potential strategies for reducing memory usage should be explored.

To broaden the scope of the paper, the authors should include a more detailed discussion of the applicability of SCaSML to other types of PDEs, such as elliptic and hyperbolic equations. This discussion should include the specific challenges that might arise when extending the method to these different types of PDEs, such as the need for different numerical solvers or the potential for instability. For example, the authors could discuss how the defect correction method would need to be modified for elliptic PDEs, which do not have a time-dependent component. Similarly, the authors could discuss the challenges of applying SCaSML to hyperbolic PDEs, which can exhibit shock waves and other discontinuities. A more detailed discussion of the assumptions required for the defect correction method to be effective would also be beneficial, including the regularity of the solution and the stability of the numerical solvers used.

Finally, the authors should provide more specific guidance on how to choose the hyperparameters of the SCaSML framework, such as the number of levels in the Multilevel Picard (MLP) iteration and the number of Monte Carlo samples at each level. The paper should discuss the trade-offs between accuracy and computational cost associated with these hyperparameters, and provide practical recommendations for selecting appropriate values. This discussion should be supported by empirical results, showing the impact of different hyperparameter choices on the accuracy and runtime of the method. The authors should also discuss the robustness of the method to different hyperparameter choices, and provide guidance on how to tune these parameters for different types of PDEs and problem complexities.

### Questions

1. How does the computational cost of SCaSML compare to traditional numerical methods and pure machine learning approaches, especially in high-dimensional settings?

2. Can the SCaSML framework be extended to other types of PDEs, such as elliptic or hyperbolic equations? What are the potential challenges and limitations in such extensions?

3. The paper mentions the use of Multilevel Picard (MLP) methods for simulating the Structural-preserving Law of Defect. Can you provide more details on the choice of MLP parameters and their impact on the accuracy and computational efficiency of SCaSML?

### Rating

6

### Confidence

3

**********