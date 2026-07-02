### Summary

The paper proposes a test-time training framework for supervised causal learning (SCL), addressing the limitations of traditional SCL methods, which struggle with out-of-distribution data and compositional generalization. The authors introduce a method called Test-time Aligned Causal Training with Informed Construction (TACTIC), which dynamically generates training data tailored to each test instance. TACTIC uses an Alignment of Distribution (AD) metric to ensure similarity between training and test data and incorporates sparsity constraints to enforce causal minimality. Experiments on synthetic, pseudo-real, and real-world datasets demonstrate that TACTIC outperforms existing SCL and traditional causal discovery methods, showing improved robustness and generalization.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper is well-organized and easy to follow. The authors effectively present the problem, their proposed solution, and experimental results.
2. The authors identify and address significant limitations of static supervised causal learning (SCL) pre-training, specifically fragility to distribution shifts, failure in compositional generalization, and a performance gap between synthetic benchmarks and real-world data.
3. The introduction of the Alignment of Distribution (AD) metric and the sparsity constraint is well-motivated and theoretically sound.
4. The experimental results are comprehensive, covering synthetic, pseudo-real, and real-world datasets, and they demonstrate the effectiveness of TACTIC compared to existing methods.

### Weaknesses

#### Some Related Works


#### comment

1. The paper does not provide a detailed analysis of the computational complexity of TACTIC, especially concerning the stochastic graph refinement process. Specifically, the paper lacks a discussion on how the number of variables and the size of the training dataset impact the runtime of the algorithm. This is crucial for understanding the scalability of the method.
2. The choice of the hyperparameter $\lambda$ in the joint optimization score is not thoroughly discussed. The paper does not provide a clear rationale for the specific value of $\lambda=0.05$ used in the experiments, nor does it explore the sensitivity of the method to different values of this hyperparameter. This makes it difficult to assess the robustness of the method.
3. The paper could benefit from a more detailed comparison with other test-time adaptation methods, especially those that are not specific to causal learning. This would help contextualize the novelty and effectiveness of TACTIC within the broader landscape of test-time adaptation techniques. The current comparison is limited, and a more thorough analysis is needed to understand the relative strengths and weaknesses of TACTIC.

### Suggestions

The paper should include a more detailed analysis of the computational complexity of the TACTIC algorithm, particularly focusing on the stochastic graph refinement process. This analysis should include a discussion of how the number of variables ($d$) and the size of the training dataset ($n$) affect the runtime. For instance, the paper could analyze the time complexity of each step in the algorithm, such as the graph generation, data sampling, and model training, and express it in terms of $d$ and $n$. Furthermore, empirical results on the runtime of TACTIC for different values of $d$ and $n$ should be provided to validate the theoretical analysis. This would allow readers to better understand the practical limitations of the method and its applicability to large-scale problems. The analysis should also consider the impact of the number of generated graphs ($K$) on the runtime, as this is a crucial parameter that affects both performance and computational cost.

Regarding the hyperparameter $\lambda$, the paper should provide a more thorough discussion on its selection and impact on the performance of TACTIC. The authors should explore the sensitivity of the method to different values of $\lambda$ through a sensitivity analysis. This analysis should include experiments with a range of $\lambda$ values, and the results should be presented in a way that clearly shows how the performance of TACTIC changes with different values. The paper should also provide a rationale for the specific value of $\lambda=0.05$ used in the experiments, explaining why this value was chosen and how it relates to the trade-off between the Alignment of Distribution (AD) metric and the sparsity constraint. This would help readers understand the robustness of the method and how to choose appropriate values of $\lambda$ for different datasets. The authors could also consider using a cross-validation approach to select the optimal value of $\lambda$.

Finally, the paper should include a more comprehensive comparison with other test-time adaptation methods, especially those that are not specific to causal learning. This comparison should include a discussion of the similarities and differences between TACTIC and other methods, as well as a comparison of their performance on the same datasets. The paper should also discuss the advantages and disadvantages of TACTIC compared to these other methods, and explain why TACTIC is a better choice for the specific problem of causal discovery. This would help contextualize the novelty and effectiveness of TACTIC within the broader landscape of test-time adaptation techniques. The comparison should also include a discussion of the computational cost of TACTIC compared to other methods, as this is an important factor to consider when choosing a method for practical applications.

### Questions

1. How does the choice of the initial seed graph affect the performance of TACTIC? Are there any strategies for selecting a good initial seed?
2. Can the authors provide more details on the computational complexity of TACTIC, especially for large-scale datasets?
3. How sensitive is TACTIC to the choice of hyperparameters, particularly $\lambda$ in the joint optimization score?
4. The paper mentions that optimizing AD alone can lead to degenerate dense solutions. Can the authors provide more theoretical analysis or empirical evidence to support this claim?
5. How does TACTIC perform when the test data is highly noisy or contains outliers? Are there any robustness measures that can be incorporated into the framework?

### Rating

6

### Confidence

3

**********