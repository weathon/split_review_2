### Summary

This paper studies the complexity of finding an $\epsilon$-stationary point for stochastic bilevel optimization when the upper-level problem is nonconvex and the lower-level problem is strongly convex. Recent work proposed the first-order method, F^2SA, achieving the $\tilde{\mathcal{O}}(\epsilon^{-6})$ upper complexity bound for first-order smooth problems. This is slower than the optimal $\Omega(\epsilon^{-4})$ complexity lower bound in its single-level counterpart. In this work, the authors show that faster rates are achievable for higher-order smooth problems. They first reformulate F^2SA as approximating the hyper-gradient with a forward difference. Based on this observation, they propose a class of methods F^2SA-p that uses p-th order finite difference for hyper-gradient approximation and improves the upper bound to $\tilde{\mathcal{O}}(p\epsilon^{-4-2/p})$ for p-th order smooth problems. Finally, they demonstrate that the $\Omega(\epsilon^{-4})$ lower bound also holds for stochastic bilevel problems when the high-order smoothness holds for the lower-level variable, indicating that the upper bound of F^2SA-p is nearly optimal in the region $p = \Omega(\log \epsilon^{-1} / \log \log \epsilon^{-1})$.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper is well-written and easy to follow.
2. The proposed method is novel and interesting. The authors use higher-order finite difference methods to approximate the hyper-gradient, which is a significant improvement over existing first-order methods. The theoretical analysis is rigorous and provides insights into the convergence properties of the proposed method.
3. The authors provide a detailed comparison of their method with existing approaches, highlighting the advantages and limitations of their work.

### Weaknesses

#### Some Related Works


#### comment

1. The paper's main contribution is theoretical, and it lacks experimental results to validate the practical performance of the proposed F^2SA-p methods. The absence of empirical validation makes it difficult to assess the real-world applicability of the proposed algorithms. Specifically, it is unclear how the theoretical improvements in convergence rates translate to practical performance gains, and whether the methods are robust to issues such as noisy gradients or hyperparameter sensitivity.
2. The improvement in complexity bounds is significant mainly for highly-smooth problems where $p = \Omega(\log \epsilon^{-1} / \log \log \epsilon^{-1})$. For small $p$, there remains a gap between the upper and lower complexity bounds, particularly when $p=1$. The paper does not fully address the practical implications of this gap, nor does it provide a clear explanation of why the proposed method does not achieve the optimal rate in the $p=1$ case, which is a common scenario in many applications. The analysis for odd values of $p$ is also not as tight as it could be, leaving open the question of whether the bounds can be further improved.
3. While the paper provides a lower bound, it does not fully close the gap in complexity between the upper and lower bounds, especially for the case of $p = 1$. The paper acknowledges the gap for $p=1$, but it does not provide a detailed discussion of the potential reasons for this gap or suggest specific directions for future research to address this issue. This leaves the reader with an incomplete picture of the theoretical landscape and the limitations of the proposed method.

### Suggestions

The paper's primary weakness lies in its lack of empirical validation. While the theoretical contributions are significant, the absence of experimental results makes it difficult to assess the practical relevance of the proposed F^2SA-p methods. To address this, the authors should conduct experiments on benchmark bilevel optimization problems, comparing the performance of F^2SA-p with existing methods, such as F^2SA and other Hessian-vector product based approaches. These experiments should evaluate the convergence speed, sensitivity to hyperparameters, and robustness to noisy gradients. Furthermore, the experiments should explore the performance of the method for different values of $p$, including the case $p=1$, to validate the theoretical claims and provide insights into the practical trade-offs between higher-order methods and first-order methods. The experimental section should also include a discussion of the computational cost associated with higher-order finite difference approximations, which is crucial for practical applications.

Another area that requires further attention is the gap between upper and lower complexity bounds, especially for small values of $p$. The paper should provide a more detailed analysis of the reasons for this gap, particularly in the $p=1$ case. This analysis should include a discussion of the limitations of the current analysis techniques and potential avenues for improvement. For instance, the authors could explore alternative analysis strategies, such as those used in recent works on stochastic optimization, to see if they can derive tighter bounds. The paper should also discuss the implications of this gap for practical applications, and whether the proposed method is competitive with existing methods in the $p=1$ case. Furthermore, the authors should investigate the possibility of extending their method to achieve optimal rates for $p=1$ in stochastic settings, which would be a significant contribution.

Finally, the paper should provide a more detailed discussion of the limitations of the proposed method and potential directions for future research. This discussion should include a more in-depth analysis of the assumptions made in the paper, and how these assumptions might affect the practical performance of the method. The authors should also discuss the potential for extending their method to other classes of bilevel optimization problems, such as those with non-strongly convex lower-level problems. Furthermore, the paper should explore the possibility of combining the proposed method with variance reduction techniques or momentum methods to further improve its performance. This would provide a more complete picture of the theoretical landscape and the potential for future research in this area.

### Questions

1. Can the authors provide more details on the practical implementation of the proposed F^2SA-p methods? Specifically, how do the authors choose the order $p$ of the finite difference approximation in practice? Are there any guidelines or heuristics for selecting $p$ based on the problem characteristics?
2. The paper focuses on the nonconvex-strongly-convex setting. Can the authors discuss the potential challenges and limitations of extending their method to other settings, such as nonconvex-nonconvex bilevel optimization problems?
3. The paper mentions that the proposed method is near-optimal when $p = \Omega(\log \epsilon^{-1} / \log \log \epsilon^{-1})$. Can the authors provide more insights into the practical implications of this result? How does this compare to the performance of existing methods in practice?

### Rating

6

### Confidence

3

**********