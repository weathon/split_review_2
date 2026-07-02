### Summary

This paper introduces HiSo, a Hessian-informed zeroth-order federated optimization method that accelerates convergence in federated learning (FL) while preserving dimension-free communication. The key innovation is leveraging global diagonal Hessian approximations to guide the search direction without increasing communication costs. The authors provide theoretical analysis showing that HiSo achieves an accelerated convergence rate independent of model dimension and Lipschitz constant under certain Hessian approximation assumptions. Empirical results across diverse LLM fine-tuning benchmarks demonstrate significant improvements over existing state-of-the-art ZO-FL baselines.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

- The paper is well-organized and easy to follow. 
- The theoretical analysis is rigorous, providing convergence guarantees for non-convex settings under standard assumptions. 
- The proposed method is well-motivated and practical, addressing a critical bottleneck in federated LLM fine-tuning.

### Weaknesses

#### Some Related Works


#### comment

 - The convergence analysis relies on strong assumptions about Hessian approximation quality that may not hold in practice. Specifically, the assumption that the diagonal Hessian approximation accurately captures the curvature of the loss landscape is questionable, especially in highly non-convex scenarios common in deep learning. This could lead to a significant discrepancy between the theoretical convergence rate and the actual performance.
- The method introduces additional complexity in terms of Hessian estimation and preconditioning, potentially increasing computational overhead per round. While communication costs are reduced, the computational burden on each client might become a bottleneck, especially with resource-constrained devices. The paper lacks a detailed analysis of the computational cost associated with Hessian estimation and preconditioning, making it difficult to assess the overall efficiency of the method.
- The experimental evaluation primarily focuses on LLM fine-tuning tasks. The generalization ability of HiSo to other types of models and optimization problems needs further investigation. It is unclear whether the observed performance gains would translate to other tasks, such as training from scratch or fine-tuning smaller models with different architectures.

### Suggestions

The paper should provide a more thorough analysis of the Hessian approximation quality and its impact on convergence. Specifically, it would be beneficial to include experiments that evaluate the correlation between the quality of the diagonal Hessian approximation and the observed convergence rate. This could involve comparing the performance of HiSo with different levels of Hessian approximation accuracy, perhaps by varying the frequency of Hessian updates or using different approximation techniques. Furthermore, the theoretical analysis should be extended to consider scenarios where the Hessian approximation is not perfect, possibly by introducing a bound on the approximation error and analyzing its effect on the convergence rate. This would provide a more realistic assessment of the method's performance in practical settings.

To address the concern about computational overhead, the authors should include a detailed breakdown of the computational cost associated with each step of the HiSo algorithm, including Hessian estimation, preconditioning, and the zeroth-order gradient update. This analysis should compare the computational cost of HiSo with that of existing zeroth-order federated learning methods, such as DeComFL. It would also be helpful to investigate techniques for reducing the computational cost of Hessian estimation, such as using sparse approximations or low-rank methods. Additionally, the paper should discuss the trade-off between communication efficiency and computational overhead, providing guidance on when HiSo is most appropriate.

Finally, the experimental evaluation should be expanded to include a wider range of models and optimization problems. This could involve evaluating HiSo on tasks such as training from scratch, fine-tuning smaller models with different architectures, and optimizing non-convex functions with different characteristics. This would provide a more comprehensive assessment of the method's generalization ability and its applicability to different scenarios. It would also be beneficial to compare the performance of HiSo with other federated learning methods that are not based on zeroth-order optimization, to better understand the trade-offs between different approaches.

### Questions

1. How sensitive is HiSo's performance to the quality of the diagonal Hessian approximation in practice? 
2. What is the computational overhead per round compared to existing ZO-FL methods? 
3. How does HiSo perform when applied to other types of models and optimization problems beyond LLM fine-tuning?

### Rating

6

### Confidence

3

**********