### Summary

The authors study the behavior of the neural tangent kernel (NTK) as the depth of the underlying neural network increases. More precisely, they focus on fully-connected networks with ReLU activations and infinite width, and show that the NTK converges to the matrix of ones as depth goes to infinity. They also show that the corresponding closed-form solution approaches a fixed limit on the sphere. The authors provide empirical evaluations to estimate the depth scale needed to observe this convergence.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

The paper is well-written and easy to read. The topic is interesting and the results are novel to my knowledge. The authors provide a good overview of the related literature and clearly explain the motivation behind their work. The theoretical results are presented in a clear and concise manner, and the empirical evaluations are well-designed and informative.

### Weaknesses

#### Some Related Works


#### comment

My main concern is the practical implication of this paper. First, the analysis is conducted in an idealized regime where the width grows much faster than the depth, which may not accurately represent real-world neural networks. Second, the convergence of the limiting kernel to the matrix of ones suggests that the kernel loses its discriminative power, making it impossible to effectively learn and classify data. Third, the empirical evaluations, while useful, do not fully bridge the gap between the theoretical analysis and practical applications.

### Suggestions

The authors should investigate the practical implications of their theoretical findings by conducting experiments on more realistic network architectures. Specifically, they could explore the behavior of the NTK in networks where the width and depth are comparable, as this is more representative of modern deep learning models. It would be beneficial to examine how the convergence of the NTK to the matrix of ones is affected by varying the width-to-depth ratio, and to determine if there are any practical thresholds where the kernel retains sufficient discriminative power. Furthermore, the authors should consider incorporating techniques such as batch normalization or residual connections, which are commonly used in practice and may influence the behavior of the NTK. These experiments would provide a more comprehensive understanding of the practical relevance of the theoretical results.

To address the concern that the limiting kernel converges to the matrix of ones, the authors should provide a more detailed analysis of the closed-form solution they mention. Specifically, they should investigate how this closed-form solution behaves on different data distributions and how it relates to the generalization performance of the network. It would be helpful to visualize the closed-form solution for simple datasets and to compare it with the predictions of the limiting kernel. Furthermore, the authors should explore whether the closed-form solution can be used to develop new training algorithms or regularization techniques that can improve the performance of deep neural networks. This would help to bridge the gap between the theoretical analysis and practical applications.

Finally, the authors should expand their empirical evaluations to include a wider range of datasets and tasks. While the current evaluations are useful for verifying the theoretical results, they do not fully demonstrate the practical implications of the findings. It would be beneficial to evaluate the performance of networks with varying depths on benchmark datasets such as CIFAR-10 or ImageNet, and to compare the results with those obtained using shallower networks. This would provide a more comprehensive assessment of the practical relevance of the theoretical results and help to identify potential areas for future research. Additionally, the authors could explore the impact of different activation functions and initialization schemes on the convergence of the NTK and the performance of the network.

### Questions

1. What is the significance of the limiting kernel converging to the matrix of ones? Does this imply that the kernel becomes useless for learning and classifying data?
2. How do the theoretical results connect to practical neural networks with comparable width and depth?

### Rating

6

### Confidence

3

**********