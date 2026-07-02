### Summary

The authors propose "Count Bridges," a stochastic bridge process on the integers for modeling RNA sequencing and other count-based data. This approach provides a framework for generative modeling and deconvolution of aggregated count data, with applications in deconvolving bulk RNA-seq data and spatial transcriptomic spots into single-cell count profiles. The authors demonstrate state-of-the-art performance on benchmarks and real-world applications, showing that Count Bridges can effectively model and deconvolve count data while preserving the ordinal structure of counts.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a novel framework for modeling count data using stochastic bridge processes, which is an interesting and original application of bridge models in the context of RNA sequencing and biological count data.
2. The authors provide rigorous mathematical formulation and theoretical analysis of the proposed method, including proofs of closed-form conditionals and discussion of the underlying birth-death dynamics.

### Weaknesses

#### Some Related Works


#### comment

1. The paper could benefit from more detailed explanation of the technical details and mathematical notation. Some sections, particularly the description of the bridge process and the deconvolution algorithm, are dense and may be difficult for readers not familiar with stochastic processes and bridge models. Specifically, the connection between the proposed Poisson birth-death process and the resulting bridge behavior is not intuitively clear. The paper would benefit from a more step-by-step explanation of how the birth-death dynamics translate into the conditional distributions required for a bridge process. Furthermore, the description of the deconvolution algorithm lacks a clear explanation of how the EM procedure is adapted to the count data setting, making it difficult to understand the practical implementation.
2. The authors could also provide more empirical evidence of the method's effectiveness, including comparisons to existing methods for modeling and deconvolving count data. While the paper presents some results, a more comprehensive evaluation is needed to fully assess the practical utility of the proposed approach. This should include a wider range of datasets, including those with varying levels of noise and complexity, and a more thorough comparison against state-of-the-art methods for count data modeling and deconvolution. The current evaluation lacks a clear demonstration of the method's robustness and limitations.

### Suggestions

To improve the clarity of the technical details, the authors should provide a more intuitive explanation of the connection between the Poisson birth-death process and the bridge behavior. This could involve a step-by-step derivation of the conditional distributions, starting from the basic properties of the Poisson process and demonstrating how these lead to the required bridge properties. For example, the authors could explicitly show how the birth and death rates influence the transition probabilities and how these probabilities satisfy the bridge conditions. Additionally, the description of the deconvolution algorithm should be expanded to include a more detailed explanation of the EM procedure. This should include a clear statement of the E-step and M-step, along with the specific equations used to update the model parameters. The authors should also discuss the convergence properties of the EM algorithm and provide guidelines for choosing the initial parameters.

To strengthen the empirical evaluation, the authors should include a more comprehensive set of experiments using a wider range of datasets. This should include datasets with varying levels of noise, complexity, and sample sizes. The authors should also compare their method against a broader range of state-of-the-art methods for count data modeling and deconvolution, including methods based on zero-inflated models and other generative approaches. The comparison should not only focus on overall performance metrics but also on the computational efficiency and scalability of the different methods. Furthermore, the authors should provide a more detailed analysis of the method's limitations, including scenarios where it may not perform well. This could involve exploring the sensitivity of the method to different parameter settings and identifying potential failure modes.

Finally, the authors should consider providing a more detailed discussion of the practical implications of their work. This could include a discussion of the potential applications of the method in different areas of biology and medicine, as well as the limitations of the method in real-world scenarios. The authors should also discuss the computational resources required to run their method and provide guidelines for choosing the appropriate parameters for different datasets. By addressing these points, the authors can make their work more accessible and useful to a wider audience.

### Questions

1. Could the authors provide more detailed explanation of the technical details and mathematical notation?
2. Could the authors provide more empirical evidence of the method's effectiveness, including comparisons to existing methods for modeling and deconvolving count data?

### Rating

6

### Confidence

2

**********