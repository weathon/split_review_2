### Summary

The paper introduces the problem of *reliability scoring* for datasets collected from potentially strategic sources. The true data are unobserved, but we see outcomes of an unknown statistical experiment that depends on them. To benchmark reliability, the authors define ground-truth-based orderings that capture how much reported data deviate from the truth. They then propose the *Gram determinant score*, which measures the volume spanned by vectors describing the empirical distribution of the observed data and experiment outcomes. They show that this score preserves several ground-truth-based reliability orderings and, uniquely up to scaling, yields the same reliability ranking of datasets regardless of the experiment – a property they term *experiment agnosticism*. Experiments on synthetic noise models, CIFAR-10 embeddings, and real employment data demonstrate that the Gram determinant score effectively captures data quality across diverse observation processes.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper is well-written and easy to follow.
2. The problem of reliability scoring is interesting and important.
3. The proposed Gram determinant score is novel and has strong theoretical guarantees.

### Weaknesses

#### Some Related Works


#### comment

1. The paper does not provide a clear comparison of the proposed Gram determinant score with existing methods for reliability scoring. It would be helpful to discuss the advantages and disadvantages of the proposed method compared to other approaches and to provide empirical results comparing the performance of the proposed method with existing methods on benchmark datasets.
2. The paper does not discuss the computational complexity of the proposed method. It would be helpful to analyze the time and space requirements of the method and to discuss its scalability for large datasets.
3. The paper does not provide a clear discussion of the limitations of the proposed method. It would be helpful to discuss the potential challenges and limitations of the method and to suggest directions for future research.

### Suggestions

The paper would benefit from a more thorough discussion of how the proposed Gram determinant score compares to existing reliability scoring methods. While the authors introduce a novel approach, they do not adequately position it within the broader landscape of data reliability assessment. Specifically, the paper should include a detailed comparison with methods that also aim to quantify data quality without direct access to ground truth. This comparison should not only highlight the theoretical differences but also discuss the practical implications of these differences. For example, how does the Gram determinant score handle noisy data compared to methods that rely on statistical assumptions about the noise? Furthermore, the authors should provide empirical results that directly compare the performance of their method with existing approaches on benchmark datasets. This would allow readers to better understand the strengths and weaknesses of the proposed method in practical scenarios. Without such a comparison, it is difficult to assess the true contribution of the proposed method.

In addition to a comparative analysis, the paper needs a more detailed discussion of the computational aspects of the proposed method. The authors should provide a precise analysis of the time and space complexity of computing the Gram determinant score. This analysis should consider the impact of the size of the dataset and the dimensionality of the data on the computational cost. Furthermore, the authors should discuss the scalability of their method for large datasets. Are there any approximations or optimizations that can be used to reduce the computational cost? For example, could random sampling or low-rank approximations be used to speed up the computation of the Gram matrix? Without a clear understanding of the computational complexity, it is difficult to assess the practicality of the proposed method for real-world applications. The authors should also discuss the memory requirements of their method, especially when dealing with large datasets.

Finally, the paper should include a more comprehensive discussion of the limitations of the proposed method. The authors should discuss the potential challenges and limitations of their approach. For example, how does the method perform when the data is highly correlated or when the underlying distribution is non-Gaussian? What are the assumptions underlying the method, and how do these assumptions affect its performance? The authors should also discuss the sensitivity of the method to the choice of the experiment. How does the reliability score change when the experiment is modified? Furthermore, the authors should suggest directions for future research that could address the limitations of the proposed method. This discussion should not only highlight the current limitations but also provide a roadmap for future work in this area.

### Questions

1. How does the proposed Gram determinant score compare to existing methods for reliability scoring in terms of performance and computational complexity?
2. What are the potential challenges and limitations of the proposed method?
3. How can the proposed method be extended to handle more complex data structures, such as time series or images?

### Rating

6

### Confidence

3

**********