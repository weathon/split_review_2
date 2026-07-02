### Summary

This paper studies the problem of minimizing a convex objective function. The authors propose an adaptive accelerated gradient method that can adapt its stepsize to the local curvature of the objective function. The proposed method achieves near-optimal iteration complexities for both $L$-smooth and $(L_0, L_1)$-smooth functions.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper proposes a new adaptive accelerated gradient method that can adapt its stepsize to the local curvature of the objective function. This is a significant improvement over existing methods that require prior knowledge of the smoothness parameters or extensive hyperparameter tuning.

2. The proposed method achieves near-optimal iteration complexities for both $L$-smooth and $(L_0, L_1)$-smooth functions. This demonstrates the theoretical robustness and practical effectiveness of the method.

3. The paper provides rigorous theoretical analysis, proving that the proposed method achieves near-optimal iteration complexities for both $L$-smooth and $(L_0, L_1)$-smooth functions.

### Weaknesses

#### Some Related Works


#### comment

1. The paper lacks experimental results to validate the performance of the proposed method. While the theoretical analysis is rigorous, it is important to demonstrate the practical effectiveness of the algorithm on real-world problems. The absence of empirical evidence makes it difficult to assess the method's performance in comparison to existing optimization algorithms, especially in scenarios where the theoretical assumptions might not perfectly hold.

2. The paper does not provide a detailed comparison of the proposed method with existing adaptive gradient methods. While the authors mention that their method achieves near-optimal iteration complexities, it is not clear how it compares to other methods in terms of practical performance, computational cost, and ease of implementation. A more thorough comparison with state-of-the-art adaptive methods, including a discussion of their respective strengths and weaknesses, would be beneficial.

### Suggestions

To strengthen the paper, the authors should include a comprehensive experimental evaluation of their proposed method. This evaluation should include a variety of test problems, both synthetic and real-world, to demonstrate the method's performance under different conditions. The experiments should compare the proposed method with existing state-of-the-art adaptive gradient methods, such as AdaGrad, RMSprop, and Adam, as well as non-adaptive methods like gradient descent and Nesterov's accelerated gradient descent. The comparison should focus on metrics such as convergence speed, solution quality, and sensitivity to hyperparameter settings. Furthermore, the authors should provide a detailed analysis of the computational cost of their method, including the time spent on gradient computations and other operations, and compare it with the computational cost of other methods. This would provide a more complete picture of the practical trade-offs associated with the proposed method.

In addition to the experimental evaluation, the authors should provide a more detailed comparison of their method with existing adaptive gradient methods. This comparison should not only focus on the theoretical iteration complexities but also on the practical performance, computational cost, and ease of implementation. For example, the authors could discuss the specific scenarios where their method is expected to outperform other methods and the scenarios where other methods might be more suitable. A table summarizing the key differences between the proposed method and existing methods, including their respective strengths and weaknesses, would be beneficial. This would help the reader to better understand the contribution of the proposed method and its potential impact on the field.

Finally, the authors should consider providing a more detailed discussion of the limitations of their method and potential directions for future research. For example, they could discuss the assumptions made in their theoretical analysis and how these assumptions might affect the practical performance of the method. They could also discuss the potential challenges in implementing their method in practice and how these challenges might be addressed. This would provide a more balanced and nuanced view of the proposed method and its potential for future development.

### Questions

1. Can you provide some experimental results to demonstrate the performance of the proposed method?

2. The paper can be improved by including a comparison of the computational time required by the proposed method and other methods.

### Rating

6

### Confidence

3

**********