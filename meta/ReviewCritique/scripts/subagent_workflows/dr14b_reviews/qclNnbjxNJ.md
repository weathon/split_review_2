### Summary

This paper introduces a novel causal formulation that explicitly models post-treatment selection and reveals how its differential reactions to interventions can distinguish causal relations from selection patterns, allowing us to go beyond traditional equivalence classes toward the underlying true causal structure. The authors then characterize its Markov properties and propose a Fine-grained I nterventiontal equivalence class, named FI -Markov equivalence, represented by a new graphical diagram, F -PAG. Finally, the authors develop a provably sound and complete algorithm, F -FCL, to identify causal relations, latent confounders, and post-treatment selection up toFI -Markov equivalence, using both observational and interventional data.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper is well-written and easy to follow.
2. The problem studied in this paper is interesting and important.
3. The proposed method is sound.

### Weaknesses

#### Some Related Works


#### comment

1. The authors should provide more details on the experiments, such as the number of runs and the variance of the results.
2. The authors should provide more details on the real-world application, such as the data description and the experimental results.
3. The authors should provide more details on the proposed algorithm, such as the time complexity and the space complexity.
4. The authors should provide more details on the proposed method, such as the assumptions and the limitations.
5. The authors should provide more details on the comparison with existing methods, such as the advantages and the disadvantages.

### Suggestions

The experimental section needs significant expansion to allow for a thorough evaluation of the proposed method. Specifically, the authors should include a detailed description of the data generation process for the synthetic experiments, including the specific parameters used to create the graphs, the number of samples generated for each experiment, and the variance of the results across multiple runs. It is crucial to report not only the average performance but also the standard deviation or confidence intervals to assess the robustness of the method. Furthermore, the authors should provide a more detailed explanation of the real-world dataset used, including its size, the nature of the variables, and any preprocessing steps applied. The experimental results should be presented in a clear and concise manner, with appropriate visualizations and statistical analysis to support the claims made in the paper. For example, the authors could include tables or graphs showing the performance of the proposed method compared to existing methods across different datasets and experimental settings. This would allow readers to better understand the strengths and weaknesses of the proposed approach.

Regarding the proposed algorithm, the authors should provide a more detailed analysis of its computational complexity, including both time and space complexity. This analysis should consider the worst-case scenario and should be supported by empirical evidence. The authors should also discuss the assumptions underlying the proposed method, such as the faithfulness assumption, and the limitations of the method, such as its sensitivity to noise or missing data. It is important to clearly state the conditions under which the method is expected to perform well and the conditions under which it may fail. Furthermore, the authors should provide a more detailed comparison with existing methods, highlighting the advantages and disadvantages of the proposed approach. This comparison should not only focus on the theoretical aspects but also on the practical performance of the methods. For example, the authors could compare the computational cost, the accuracy, and the robustness of the proposed method with existing methods on a range of datasets.

Finally, the authors should provide more details on the implementation of the proposed method, including the specific software or libraries used, the parameter settings, and the hardware used for the experiments. This would allow other researchers to reproduce the results and to build upon the proposed method. The authors should also discuss the potential impact of the proposed method on the field of causal inference and should identify potential directions for future research. This would help to contextualize the contribution of the paper and to highlight its significance. In addition, the authors should clarify the novelty of their approach compared to existing methods, especially in the context of interventional causal discovery. A more detailed discussion of the differences in assumptions, methodology, and performance would be beneficial.

### Questions

1. How does the proposed method compare to existing methods in terms of computational complexity and scalability?
2. How does the proposed method handle noisy or incomplete data?
3. How does the proposed method perform in the presence of unobserved confounders or selection variables?
4. How does the proposed method deal with the issue of identifiability in causal inference?
5. How does the proposed method address the problem of causal discovery in the presence of feedback loops or cyclic causal relationships?

### Rating

6

### Confidence

3

**********