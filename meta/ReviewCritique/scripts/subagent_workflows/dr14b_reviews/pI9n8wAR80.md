### Summary

This paper proposes Co-Calibrated Logit Adjustment (CoLA), a framework designed to address the challenges of long-tailed semi-supervised learning (LTSSL). The primary focus is on improving pseudo-label quality by refining the Logit Adjustment (LA) strategy commonly used in LTSSL. The authors identify two main limitations in traditional LA methods: over-suppression of head classes due to redundant samples and a fixed overall adjustment strength that fails to adapt to varying data distributions. To overcome these issues, CoLA introduces two key innovations: (1) De-Duplicated Distribution Estimation (DDDE), which reduces over-suppression by accounting for sample redundancy when estimating class distributions, and (2) Logit Meta-Calibration (LMC), a meta-learning approach that dynamically adjusts the overall LA strength based on a proxy validation set. Through theoretical analysis and extensive experiments on multiple benchmark datasets, the authors demonstrate that CoLA achieves state-of-the-art performance in LTSSL tasks.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. Originality: The paper presents a novel approach to addressing the limitations of traditional Logit Adjustment (LA) methods in long-tailed semi-supervised learning (LTSSL). The introduction of De-Duplicated Distribution Estimation (DDDE) and Logit Meta-Calibration (LMC) represents a creative combination of ideas from distribution estimation and meta-learning. The concept of using effective rank to account for sample redundancy in distribution estimation is particularly innovative.
2. Quality: The theoretical analysis provides solid foundations for the proposed method, including generalization bounds and convexity analysis. The experimental evaluation is thorough, covering multiple benchmark datasets and various distribution scenarios. The ablation studies effectively demonstrate the contributions of individual components.
3. Clarity: The paper is well-written and organized, with clear explanations of the motivation, methodology, and experimental results. Figures and tables are used effectively to illustrate key concepts and findings.
4. Significance: The proposed CoLA framework addresses a fundamental challenge in LTSSL, namely the production of high-quality pseudo-labels. By improving the quality of pseudo-labels, CoLA contributes to reducing confirmation bias and enhancing model performance on tail classes. The demonstrated state-of-the-art performance across multiple benchmarks highlights the practical significance of the proposed method.

### Weaknesses

#### Some Related Works


#### comment

1. Limited Exploration of Alternative Distribution Estimation Techniques: While DDDE shows promise, the paper could benefit from exploring and comparing other advanced distribution estimation techniques. Specifically, the paper lacks a discussion on how DDDE compares to methods that explicitly model the covariance structure of the feature space, which could potentially capture more nuanced relationships between samples. Furthermore, investigating the sensitivity of DDDE to different choices of effective rank metrics would provide valuable insights into its robustness and generalizability. The current implementation uses a specific effective rank calculation, but the justification for this choice over alternatives, such as the nuclear norm or other Schatten-p norms, is not thoroughly explored.

2. Scalability Concerns: The meta-learning component (LMC) involves constructing a proxy validation set and optimizing the overall adjustment strength, which might introduce scalability challenges for very large datasets. The paper does not provide a detailed analysis of the computational complexity of the meta-learning process, particularly concerning the number of iterations required for convergence and the memory footprint of the proxy validation set. This lack of analysis makes it difficult to assess the practical applicability of the method to large-scale problems.

3. Limited Analysis of Hyperparameter Sensitivity: Although the paper presents extensive experimental results, there is limited analysis of the sensitivity of CoLA to hyperparameters such as the warm-up period for $\tau$ and the threshold $\rho$. A more systematic study of how these parameters affect performance across different datasets and imbalance ratios would strengthen the robustness claims. For example, the paper does not explore how the optimal warm-up period changes with varying levels of class imbalance or how the choice of $\rho$ interacts with the effectiveness of the DDDE component.

4. Lack of Comparison with Non-LA Methods: While the paper demonstrates CoLA's superiority over other LA-based methods, a more direct comparison with non-LA LTSSL approaches would provide a broader perspective on its effectiveness. The paper should include comparisons with methods that address long-tailed learning through techniques such as re-sampling, re-weighting, or data augmentation, to better contextualize the performance gains achieved by CoLA.

### Suggestions

To address the limitations in exploring alternative distribution estimation techniques, the authors should consider incorporating methods that explicitly model the covariance structure of the feature space. For instance, techniques based on Gaussian mixture models or other probabilistic models could be used to estimate class distributions, potentially capturing more intricate relationships between samples. Comparing the performance of DDDE with these methods would provide a more comprehensive understanding of its strengths and weaknesses. Additionally, the authors should investigate the sensitivity of DDDE to different choices of effective rank metrics. Instead of relying on a single effective rank calculation, the paper could explore alternatives such as the nuclear norm or other Schatten-p norms, and analyze how these choices impact the performance of the proposed method. This analysis should include a discussion of the theoretical implications of each choice and provide empirical evidence to support the selection of the specific effective rank metric used in the paper. Such an investigation would enhance the robustness and generalizability of the DDDE component.

Regarding the scalability concerns, the authors should provide a detailed analysis of the computational complexity of the meta-learning process. This analysis should include a breakdown of the time and memory requirements for each step of the LMC procedure, particularly concerning the construction of the proxy validation set and the optimization of the overall adjustment strength. The paper should also discuss strategies for mitigating the computational burden of the meta-learning process, such as using mini-batch optimization or approximate gradient calculations. Furthermore, the authors should investigate the convergence behavior of the meta-learning algorithm, including the number of iterations required for convergence and the sensitivity of the results to different initialization strategies. Providing empirical evidence of the scalability of the method on larger datasets would also be beneficial. This would help to clarify the practical applicability of the method to real-world problems.

Finally, to address the limited analysis of hyperparameter sensitivity, the authors should conduct a more systematic study of how the hyperparameters, such as the warm-up period for $\tau$ and the threshold $\rho$, affect performance across different datasets and imbalance ratios. This study should include a range of values for each hyperparameter and analyze the resulting performance variations. The paper should also explore how the optimal values of these hyperparameters change with varying levels of class imbalance and how the choice of $\rho$ interacts with the effectiveness of the DDDE component. Furthermore, the authors should include a more direct comparison with non-LA LTSSL approaches, such as re-sampling, re-weighting, or data augmentation techniques. This would provide a broader perspective on the effectiveness of CoLA and help to contextualize its performance gains. The paper should also discuss the limitations of the proposed method and suggest potential avenues for future research.

### Questions

1. Can you provide more details on the computational complexity of the meta-learning procedure? Specifically, how does the time and memory requirement scale with the size of the proxy validation set and the overall dataset?
2. Have you considered alternative approaches for dynamically adjusting the overall LA strength besides meta-learning? How do they compare in terms of performance and computational cost?
3. How sensitive is the performance of CoLA to the choice of effective rank metric used in DDDE? Did you experiment with other metrics, and if so, what were the results?
4. Can you elaborate on the criteria used for selecting the warm-up period for $\tau$? How does the performance vary with different warm-up periods, especially on datasets with varying degrees of class imbalance?
5. How does CoLA perform when the class distribution of the unlabeled data significantly deviates from the estimated distribution used in DDDE? Are there any strategies to mitigate potential performance degradation in such scenarios?

### Rating

6

### Confidence

3

**********