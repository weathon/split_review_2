### Summary

This paper proposes a method for fitting stochastic processes to data in the one-trajectory-at-a-time setting. The idea is to learn a map that pushes i.i.d. noise forward into a trajectory of interest. The proposed map is learned by minimizing a loss on a set of observed trajectories. Once the map is trained, it can be used to generate many examples that are consistent with the observed data. The authors propose a specific model architecture based on deconvolution, and demonstrate its effectiveness on several synthetic and real-world problems.

### Soundness

2

### Presentation

3

### Contribution

2

### Strengths

The problem studied in the paper is quite interesting and well-motivated. There are many settings where one wants to learn a stochastic process from a single trajectory, and being able to do so effectively would be valuable. The presentation is generally quite clear. The authors provide just enough mathematical detail to be informative while still being accessible to most readers. The experimental results are drawn from a diverse set of applications, which helps to demonstrate that the proposed method is broadly applicable.

### Weaknesses

#### Some Related Works

[1] Sequential Neural Processes
[2] Autoregressive Conditional Neural Processes
[3] Practical Equivariances via Relational Conditional Neural Processes
[4] Identifying Latent Stochastic Differential Equations with Neural Controlled Differential Equations
[5] Likelihood-Free Inference of Stochastic Differential Equations with Conditional Normalizing Flows
[6] Scalable Inference of Stochastic Differential Equations with Flows

#### comment

The main weakness of this paper is the lack of strong evidence that the proposed method works well. The experimental results are quite mixed, and in several cases, the proposed method is outperformed by the baselines both in terms of predictive accuracy and uncertainty quantification. For example, in Table 1, WGP and MARKOV have lower MSE on average than DBPT, and in Table 2, CNP outperforms DBPT on CIFAR. The authors do a good job of explaining *why* the results look like they do, but the onus is on them to show that their method is an improvement over existing techniques. The results in this paper do not seem to do that.

There are also a number of important baselines that are missing. The authors should compare to sequential neural processes [1], autoregressive conditional neural processes [2], and relational conditional neural processes [3], which are all adaptations of conditional neural processes that have been shown to perform well in the one-trajectory setting. The authors also should compare to methods that learn stochastic differential equations from data, such as [4, 5, 6].

The authors should also clarify how their method works when the number of observations is small. If the number of observations is small, then there is not much information to constrain the behavior of the process in unobserved regions. It looks like this might be a problem for the deconvolution architecture that is proposed in the paper, since deconvolution is an ill-posed problem in general. The authors should provide a theoretical analysis of the conditions under which their method can succeed with limited data, and discuss how the choice of the base noise process affects the performance in low-data regimes.

### Suggestions

The paper would be significantly strengthened by a more thorough empirical evaluation. The current results are insufficient to demonstrate the superiority of the proposed method over existing techniques. Specifically, the authors should include comparisons to sequential neural processes, autoregressive conditional neural processes, and relational conditional neural processes, which are all relevant baselines for the one-trajectory setting. These methods, being adaptations of conditional neural processes, have shown strong performance in similar scenarios and should be included for a fair comparison. Furthermore, methods that learn stochastic differential equations from data, such as those based on neural SDEs or other likelihood-free inference techniques, should also be included as baselines. These methods represent a different approach to modeling stochastic processes and could provide valuable insights into the strengths and weaknesses of the proposed method. The authors should also provide a more detailed analysis of the performance of their method across different sample sizes, and discuss the limitations of their approach when the number of observations is very small.

To address the concerns about the deconvolution architecture, the authors should provide a more detailed explanation of how they regularize the deconvolution process, and how this regularization affects the stability and performance of the method. They should also discuss the limitations of their approach when the number of observations is very small, and how the choice of the base noise process affects the performance in low-data regimes. A theoretical analysis of the conditions under which their method can succeed with limited data would also be beneficial. It would be helpful to see experiments that systematically vary the number of observations and analyze the resulting performance. The authors should also clarify how their method handles irregularly sampled data, and how it can be extended to handle such data. This is particularly important for real-world applications where data is often not uniformly sampled.

Finally, the authors should provide a more detailed explanation of how their method can be used for forecasting and extrapolation. While the paper mentions that the method can be used for these tasks, it does not provide sufficient details on how this is done in practice. For example, how does the method handle the generation of future trajectories beyond the observed time range? How does the method ensure that the generated trajectories are consistent with the observed data? The authors should also discuss the limitations of their approach for long-term forecasting and extrapolation, and how these limitations can be addressed. Including examples of forecasting and extrapolation in the experimental results would also be beneficial.

### Questions

1. In Section 2.3.2, it is stated that the loss is a function of $\theta$ and not a random variable of $Z$, since the expectation over $Z$ is approximated using Monte Carlo. However, at test time, the loss will be a random variable, since it will depend on the particular draw of $Z$. How do you make predictions with a random loss?

2. The architecture that is proposed in the paper relies on deconvolution, which is an ill-posed problem in general. How do you make this well-posed? Do you use any kind of regularization? Is this done automatically by the architecture that is proposed in the paper?

3. How does your method work if the observations are irregularly sampled?

4. How does your method work for forecasting / extrapolation? Can you include some examples of this in the experimental results?

### Rating

3

### Confidence

4

**********