### Summary

The paper studies the unlearning problem in continual learning. The authors analyze the excess risk under continual learning and the unlearning loss to jointly determine the final post-unlearning excess risk. The authors propose two unlearning algorithms, one is gradient-based and the other is hessian-based, and provide theoretical guarantees for them. The authors also conduct experiments on MNIST to validate their theoretical findings.

### Soundness

3

### Presentation

3

### Contribution

2

### Strengths

1. The paper is the first to study the unlearning problem in continual learning, and provides the first theoretical analysis for this problem.
2. The paper provides rigorous theoretical guarantees for the proposed algorithms, and the analysis seems to be sound.
3. The paper is well-written and easy to follow.

### Weaknesses

#### Some Related Works


#### comment

1. The paper only considers the unlearning of an entire task, which is not practical in real-world scenarios. In many cases, we may only need to unlearn a small portion of the data, such as a few data points or a subset of the data within a task. The proposed algorithms do not address this scenario, which limits their applicability.
2. The paper only provides theoretical analysis for the proposed algorithms, without any empirical evaluation. While the theoretical analysis is rigorous, it is important to validate the performance of the algorithms in practice. The lack of empirical evaluation makes it difficult to assess the practical significance of the proposed algorithms.
3. The paper only considers the $\ell_2$-regularized continual learning algorithm, which is not representative of all continual learning algorithms. There are many other continual learning algorithms, such as those based on gradient episodic memory or learning without forgetting, and it is unclear whether the proposed algorithms can be applied to these algorithms. The paper should discuss the limitations of the proposed algorithms and their applicability to other continual learning algorithms.
4. The paper does not provide any discussion on the limitations of the proposed algorithms. For example, the paper does not discuss the computational cost of the proposed algorithms, or their sensitivity to the choice of hyperparameters. A discussion of the limitations of the proposed algorithms would help the reader to better understand their strengths and weaknesses.

### Suggestions

The paper makes a valuable contribution by introducing the unlearning problem in continual learning and providing theoretical analysis. However, the practical applicability of the proposed algorithms is limited by their focus on unlearning entire tasks. To enhance the practical relevance, future work should explore methods for unlearning subsets of data within a task. This could involve adapting the proposed gradient and Hessian-based approaches to selectively remove the influence of specific data points or subsets. For example, one could investigate techniques similar to influence functions to identify and remove the impact of specific data points on the model parameters. This would require a more fine-grained control over the unlearning process, potentially involving modifications to the update rules or the use of masking techniques. Furthermore, the theoretical analysis should be extended to cover these more granular unlearning scenarios, providing guarantees on the performance of the unlearned model when only a portion of the data is removed. This would significantly broaden the applicability of the proposed framework.

To address the lack of empirical validation, the authors should conduct experiments on benchmark datasets commonly used in continual learning research. These experiments should compare the performance of the proposed unlearning algorithms with existing continual learning methods, both with and without unlearning. The experiments should also evaluate the impact of different unlearning requests on the performance of the model, including scenarios where unlearning requests arrive in different orders or at different times. This would provide a more comprehensive understanding of the practical behavior of the proposed algorithms and their sensitivity to various factors. Furthermore, the experiments should explore the computational cost of the proposed algorithms, particularly the Hessian-based approach, and investigate potential optimizations to reduce the computational overhead. This would help to assess the scalability of the proposed algorithms and their suitability for real-world applications. The experiments should also include a sensitivity analysis of the hyperparameters, such as the regularization parameter, to understand their impact on the performance of the unlearning algorithms.

Finally, the paper should provide a more detailed discussion of the limitations of the proposed algorithms and their applicability to other continual learning algorithms. The authors should explore the challenges of applying the proposed algorithms to other continual learning methods, such as those based on gradient episodic memory or learning without forgetting. This discussion should include a theoretical analysis of the conditions under which the proposed algorithms can be applied to these other methods, and the potential modifications that may be required. The authors should also discuss the limitations of the theoretical analysis, such as the assumptions made about the loss function and the data distribution. This would provide a more complete picture of the strengths and weaknesses of the proposed framework and guide future research in this area. Furthermore, the paper should discuss the potential for extending the proposed framework to other related problems, such as federated learning or distributed learning, where unlearning is also an important consideration.

### Questions

1. Can the proposed algorithms be extended to other continual learning algorithms, such as gradient episodic memory or learning without forgetting?
2. How does the order of unlearning requests affect the performance of the proposed algorithms? Is there an optimal order for unlearning requests?
3. What is the computational cost of the proposed algorithms, especially the hessian-based algorithm? Are there any potential optimizations to reduce the computational cost?

### Rating

5

### Confidence

3

**********