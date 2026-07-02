### Summary

This paper studies change point localization and inference in dynamic multilayer random dot product graphs (D-MRDPGs), where at each time point, a multilayer network is observed with shared node latent positions and time-varying, layer-specific connectivity patterns. A novel two-stage algorithm is proposed that combines seeded binary segmentation with low-rank tensor estimation, and its consistency in estimating both the number and locations of change points is established. The limiting distributions of the refined estimators are derived, and a fully data-driven procedure for constructing confidence intervals is developed. Extensive numerical experiments demonstrate the superior performance and practical utility of the proposed methods compared to existing alternatives.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper proposes a novel two-stage algorithm for offline change point detection in dynamic multilayer networks, combining seeded binary segmentation with refined CUSUM statistics and low-rank tensor estimation for change point localization and inference. 
2. The paper provides theoretical guarantees for the proposed method, including consistency in estimating the number and locations of change points, and derives the limit distributions of the refined estimators under both vanishing and non-vanishing jump regimes.
3. The paper develops a fully data-driven procedure for constructing confidence intervals, which is a novel contribution in the context of dynamic network data.
4. The paper includes extensive numerical experiments to demonstrate the superior performance and practical utility of the proposed methods compared to existing alternatives.

### Weaknesses

#### Some Related Works


#### comment

1. The paper assumes temporal independence among the four sequences in Algorithm 1 for theoretical convenience. While the authors mention that the same two split tensor sequences are used in practice, the theoretical analysis relies on the assumption of mutual independence, which may not hold in real-world applications. This discrepancy between the theoretical assumptions and the practical implementation raises concerns about the robustness of the theoretical guarantees in real-world scenarios. Specifically, the analysis does not account for potential dependencies that could arise from using the same data for both stages, which could lead to an underestimation of the variance of the estimators and overly optimistic theoretical bounds.
2. The paper focuses on the offline setting, where all the data are observed before the analysis. The extension to the online setting, where data arrive sequentially, is not addressed in detail. The current method requires access to the entire time series to perform the seeded binary segmentation and low-rank tensor estimation, which limits its applicability in real-time change point detection scenarios. The paper does not discuss the computational challenges of adapting the proposed method to an online setting, such as the need for efficient updates to the low-rank tensor estimates as new data arrives.
3. The paper assumes that the minimal spacing between successive change points scales with the time horizon, effectively bounding the number of changes. This assumption may not hold in all real-world applications, particularly in systems with frequent changes. The assumption that the minimal spacing between change points is proportional to the time horizon is a strong constraint that limits the applicability of the method to scenarios with relatively infrequent changes. This assumption may not be realistic in many real-world systems where changes can occur at arbitrary intervals, potentially leading to a significant underestimation of the number of change points and inaccurate localization.

### Suggestions

The paper would benefit from a more thorough discussion of the limitations imposed by the temporal independence assumption. While the authors acknowledge that the same data is used in practice, the theoretical analysis should be extended to account for the dependencies that arise from this. One approach could be to analyze the impact of using the same data on the variance of the estimators and provide bounds that are valid under weaker dependence assumptions. Furthermore, the authors should consider exploring alternative methods for estimating the covariance structure that do not rely on the assumption of independence. This could involve using techniques from time series analysis or robust statistics to handle potential dependencies in the data. A more detailed analysis of the sensitivity of the results to violations of the independence assumption would also be beneficial.

To enhance the practical applicability of the proposed method, the authors should investigate the feasibility of extending it to an online setting. This would require developing efficient algorithms for updating the low-rank tensor estimates as new data arrives, potentially using techniques from online optimization or streaming algorithms. The paper should also discuss the computational challenges associated with online change point detection, such as the need for efficient data structures and algorithms to handle large-scale network data. Furthermore, the authors should consider exploring adaptive methods for selecting the parameters of the algorithm in an online setting, such as the window size for the CUSUM statistics and the rank of the tensor estimates. A detailed analysis of the computational complexity of the online algorithm and its performance in real-time change point detection scenarios would be valuable.

Finally, the paper should address the limitations imposed by the assumption on the minimal spacing between change points. The authors should explore alternative methods for handling scenarios with frequent changes, such as using adaptive segmentation techniques or non-parametric methods for change point detection. The paper should also discuss the impact of violating this assumption on the performance of the proposed method, including the potential for underestimating the number of change points and inaccurate localization. A more detailed analysis of the robustness of the method to violations of this assumption would be beneficial, along with a discussion of potential strategies for mitigating the impact of frequent changes on the performance of the algorithm.

### Questions

1. How does the proposed method perform when the minimal spacing between change points is much smaller than the time horizon?
2. Can the proposed method be extended to handle temporal dependence in the data?
3. What are the computational bottlenecks of the proposed method, and how can they be addressed in practice?

### Rating

6

### Confidence

3

**********