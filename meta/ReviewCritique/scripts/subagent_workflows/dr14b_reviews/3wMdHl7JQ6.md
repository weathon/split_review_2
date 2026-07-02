### Summary

This paper proposes a simplified method for the classic stochastic block model problem. The authors simplified the previous method by removing some correction steps, and used the properties of second eigenvalue to improve the error bounds of the algorithm.

### Soundness

2

### Presentation

2

### Contribution

2

### Strengths

The authors improved the error bounds of the algorithm by using the properties of the second eigenvalue.

### Weaknesses

#### Some Related Works


#### comment

1. The authors claimed that the simplified method achieved better performance than the previous one, but there is no experimental section in the paper to support this argument. Specifically, the paper lacks any empirical validation of the theoretical claims, making it difficult to assess the practical impact of the proposed simplification. The absence of numerical results comparing the proposed method with existing approaches leaves a significant gap in the evaluation.
2. The authors should include a complexity analysis to show how their method improves the computational efficiency. Without a detailed analysis of the time and space complexity, it is hard to quantify the practical benefits of the proposed simplification. A comparison of the computational cost of the proposed method with the original algorithm is necessary to justify the claim of improved efficiency.
3. The problem is well-studied and the authors should include more comparisons with the existing methods in the literature. The paper does not adequately position the proposed method within the broader context of existing literature on stochastic block models. A more thorough discussion of how this method compares to other state-of-the-art algorithms, including their strengths and weaknesses, is needed.

### Suggestions

To address the lack of experimental validation, the authors should include a comprehensive experimental section that demonstrates the performance of the proposed method on various datasets. This section should include a comparison with existing methods, using appropriate evaluation metrics. Specifically, the authors should generate synthetic graphs using the stochastic block model with varying parameters and compare the performance of their method against the original algorithm and other relevant methods. The results should be presented in clear and concise tables and figures, with appropriate statistical analysis to support the claims. Furthermore, the experimental setup should be described in detail, including the parameter settings and the hardware used, to ensure reproducibility.

To strengthen the claims of improved computational efficiency, the authors should provide a detailed complexity analysis of their method. This analysis should include both time and space complexity, and should be compared to the complexity of the original algorithm. The analysis should be rigorous and should clearly identify the factors that contribute to the improved efficiency. For example, the authors should analyze the number of operations required for each step of the algorithm and should provide a detailed breakdown of the computational cost. This analysis should be complemented with empirical measurements of the running time of the proposed method and the original algorithm on various datasets. The results should be presented in a table, showing the running time for different graph sizes and parameter settings.

Finally, the authors should provide a more comprehensive comparison with existing methods in the literature. This comparison should include a discussion of the strengths and weaknesses of each method, and should clearly position the proposed method within the broader context of existing literature. The authors should discuss the theoretical guarantees of each method, as well as their practical performance. This comparison should not be limited to the original algorithm, but should include other relevant methods that have been proposed in the literature. The authors should also discuss the limitations of their method and should identify potential directions for future research. This will help to provide a more complete and balanced view of the contribution of the paper.

### Questions

Please see above.

### Rating

3

### Confidence

4

**********