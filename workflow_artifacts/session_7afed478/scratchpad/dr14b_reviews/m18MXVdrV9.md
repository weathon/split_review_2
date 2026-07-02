### Summary

This paper introduces a novel approach, INFO-SEDD, for estimating information-theoretic measures, such as Mutual Information (MI), for high-dimensional discrete data. The method leverages Continuous Time Markov Chains (CTMCs) and score functions to compute Kullback-Leibler (KL) divergences, enabling the estimation of MI and entropy. The authors demonstrate the effectiveness of INFO-SEDD through experiments on synthetic data, text summarization, and genomics, showing that it outperforms existing methods in accuracy and robustness, especially in high-dimensional settings.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

* The paper presents a novel approach to information-theoretic estimation for discrete data using CTMCs, which is both theoretically sound and practically relevant.
* The method is shown to be robust and accurate across various high-dimensional datasets, outperforming existing methods.
* The paper is well-organized, with clear explanations of the methodology, theoretical background, and experimental results.

### Weaknesses

#### Some Related Works


#### comment

 * The method may require careful tuning of hyperparameters, such as the transition matrix and score function approximations, which could affect performance.
* The paper could benefit from a more detailed discussion of the computational complexity and scalability of INFO-SEDD, especially for very large datasets.
* While the paper compares INFO-SEDD to several existing methods, a more comprehensive comparison with a wider range of baselines could further strengthen the claims of superiority.

### Suggestions

The paper should delve deeper into the practical aspects of hyperparameter selection for INFO-SEDD. Specifically, the authors should provide more guidance on how to choose the transition matrix for the CTMC, as this choice can significantly impact the accuracy and stability of the MI estimates. A sensitivity analysis of the score function approximation, including the choice of neural network architecture and training parameters, would also be beneficial. For instance, the authors could explore the impact of different activation functions, network depths, and optimization algorithms on the final MI estimates. Furthermore, the paper should discuss the potential for using adaptive hyperparameter tuning methods to mitigate the need for manual tuning, which would make the method more accessible to practitioners.

To address the computational complexity concerns, the paper should include a more detailed analysis of the time and space complexity of the INFO-SEDD algorithm. This should include an analysis of the computational cost of each step, such as the score function estimation, the CTMC simulation, and the final MI calculation. The authors should also discuss the memory requirements of the method, particularly for large datasets. It would be helpful to see a comparison of the computational cost of INFO-SEDD with existing methods, including both theoretical analysis and empirical results. The authors should also explore potential optimizations to improve the scalability of the method, such as parallelization or approximation techniques. For example, they could investigate the use of sparse matrix representations for the transition matrix, or the use of stochastic gradient descent for the score function estimation. The paper should also include a discussion of the practical limitations of the method, such as the maximum dataset size that can be handled.

Finally, the paper should include a more comprehensive comparison with a wider range of baseline methods. While the paper compares INFO-SEDD to several existing methods, it would be beneficial to include comparisons with other state-of-the-art MI estimators, particularly those designed for high-dimensional discrete data. This could include methods based on variational inference, kernel density estimation, or other techniques. The authors should also consider including comparisons with methods that are specifically designed for the application domains considered in the paper, such as text summarization and genomics. This would provide a more complete picture of the strengths and weaknesses of INFO-SEDD compared to existing approaches. The comparison should not only focus on the final MI estimate but also on other metrics, such as the convergence speed, the robustness to noise, and the computational cost.

### Questions

* How does the choice of the transition matrix in the CTMC affect the performance of INFO-SEDD?
* Can the authors provide more details on the computational complexity and scalability of the method, especially for very large datasets?
* How does INFO-SEDD compare to other state-of-the-art MI estimators for high-dimensional discrete data?

### Rating

6

### Confidence

3

**********