### Summary

This paper proposes a novel method for learning the parameters of a discrete Partially Observable Markov Decision Process (POMDP) from action-observation sequences. The authors extend spectral methods, typically used for learning Predictive State Representations (PSRs), to estimate transition and observation matrices up to a similarity transform. This approach allows for learning in POMDPs without assuming full state observability or full-rank transition matrices for all actions. The method leverages tensor decomposition to recover the unknown basis, enabling the estimation of explicit transition and observation likelihoods. The authors demonstrate the effectiveness of their approach through experiments on several POMDP domains, showing that it can learn accurate models and achieve comparable performance to PSRs when used with standard sampling-based POMDP solvers.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper presents a novel approach to learning POMDPs by combining spectral methods with tensor decomposition. This combination allows for learning in a broader class of POMDPs compared to existing tensor methods, which often rely on restrictive assumptions.

2. The authors provide a rigorous theoretical analysis of their method, including a theorem that characterizes the conditions under which the similarity transform can be recovered. This theoretical foundation strengthens the credibility of their approach.

3. The experimental results demonstrate the effectiveness of the proposed method in learning accurate POMDP models. The method achieves comparable performance to PSRs in terms of planning accuracy, while also providing explicit transition and observation likelihoods, which are valuable for downstream tasks.

### Weaknesses

#### Some Related Works


#### comment

1. The paper lacks a detailed discussion of the computational complexity of the proposed method. While the authors mention that their approach is efficient, they do not provide a formal analysis of its time and space complexity. This makes it difficult to assess the scalability of the method for larger POMDPs. Specifically, the paper should analyze the complexity of the tensor decomposition step, which is likely to be a bottleneck, and how it scales with the number of states, actions, and observations. Furthermore, the paper should discuss the memory requirements for storing the intermediate matrices and tensors, which can become significant for large problems.

2. The paper does not thoroughly explore the limitations of the proposed method. While the authors mention that their approach can handle POMDPs without full state observability, they do not discuss the types of POMDPs where their method might fail or perform poorly. For example, it is unclear how the method would perform in scenarios with highly stochastic transitions or when the observation space is very large and sparse. A more detailed analysis of the method's robustness to noise and its sensitivity to the choice of hyperparameters would be beneficial.

3. The experimental evaluation could be more comprehensive. While the authors compare their method to PSRs and EM, they do not compare it to other state-of-the-art POMDP learning algorithms. A more thorough comparison with a wider range of methods would provide a better understanding of the strengths and weaknesses of the proposed approach. For example, the paper should compare against methods that explicitly handle partial observability, such as those based on belief space planning or recurrent neural networks. Additionally, the paper should include experiments on more challenging POMDP domains with larger state and action spaces to better assess the scalability of the method.

### Suggestions

To address the lack of computational complexity analysis, the authors should provide a detailed breakdown of the time and space complexity of each step in their algorithm, including the tensor decomposition. This analysis should consider the dimensions of the input data (number of states, actions, and observations) and the rank of the tensors involved. The authors should also discuss the practical implications of these complexities, such as the expected runtime and memory usage for different problem sizes. Furthermore, it would be beneficial to include a discussion of potential optimizations that could be used to improve the scalability of the method, such as using sparse tensor representations or parallelizing the tensor decomposition step. This analysis should be supported by empirical results on a range of problem sizes to demonstrate the practical scalability of the method.

To better explore the limitations of the proposed method, the authors should conduct experiments on a wider range of POMDP domains, including those with highly stochastic transitions, large and sparse observation spaces, and varying levels of noise. The authors should also analyze the sensitivity of the method to the choice of hyperparameters, such as the rank of the tensor decomposition and the number of samples used for estimation. This analysis should include a discussion of how these hyperparameters affect the accuracy and robustness of the learned models. Furthermore, the authors should investigate the conditions under which the method might fail to converge or learn accurate models, and provide guidance on how to mitigate these issues. This could involve exploring alternative initialization strategies or incorporating regularization techniques.

To improve the experimental evaluation, the authors should compare their method to a wider range of state-of-the-art POMDP learning algorithms, including those that explicitly handle partial observability. This comparison should include both model-based and model-free methods, and should evaluate the performance of each method in terms of both model accuracy and planning performance. The authors should also include experiments on more challenging POMDP domains with larger state and action spaces to better assess the scalability of the method. Furthermore, the authors should provide a detailed analysis of the strengths and weaknesses of their method compared to the other methods, and discuss the specific scenarios where their method is expected to perform well or poorly. This would provide a more comprehensive understanding of the proposed approach and its potential applications.

### Questions

1. Could you provide a more detailed analysis of the computational complexity of your method? Specifically, how does the runtime and memory usage scale with the number of states, actions, and observations in the POMDP?

2. What are the limitations of your method? Are there specific types of POMDPs where your approach might fail or perform poorly? How sensitive is your method to the choice of hyperparameters?

3. Have you compared your method to other state-of-the-art POMDP learning algorithms? If so, how does your method perform in comparison? If not, what are the reasons for not including such comparisons?

### Rating

6

### Confidence

3

**********