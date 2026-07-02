### Summary

The paper proposes a novel method for evaluating unsupervised anonymous record linkage without requiring labeled training data. The authors derive observable lower bounds on both precision and relative recall by exploiting a common structural constraint that limits how many positive outcomes a single individual can have. The method is applied to detect loan applicants who submit multiple applications in the Home Mortgage Disclosure Act (HMDA) data.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper proposes a novel method for evaluating unsupervised anonymous record linkage without requiring labeled training data.
2. The authors derive observable lower bounds on both precision and relative recall, which enables principled tuning and comparison of label-generating models without labeled training data.
3. The method is applied to detect loan applicants who submit multiple applications in the Home Mortgage Disclosure Act (HMDA) data, and achieves good results.

### Weaknesses

#### Some Related Works


#### comment

1. The method relies on a structural constraint that limits how many positive outcomes a single individual can have. This constraint may not hold in all datasets, which limits the generalizability of the method.
2. The method is based on clustering, which can be computationally expensive for large datasets. The authors should provide more details on the computational complexity of their method and how it scales with the size of the dataset.
3. The paper does not provide a comprehensive comparison with existing methods for unsupervised record linkage. It would be helpful to compare the proposed method with other state-of-the-art methods on benchmark datasets to better understand its strengths and weaknesses.

### Suggestions

The authors should more thoroughly investigate the limitations imposed by the structural constraint that underpins their method. While the paper acknowledges that this constraint may not always hold, it would be beneficial to explore specific scenarios where the method would fail or produce unreliable results. For instance, if the dataset contains individuals with multiple legitimate outcomes, the method might incorrectly flag these as anomalies. A more detailed discussion of these edge cases, perhaps with illustrative examples, would help clarify the scope and applicability of the proposed method. Furthermore, the authors should consider how the method could be adapted or modified to handle such cases, or at least provide guidance on when the method should not be used.

Regarding the computational complexity, the authors should provide a more detailed analysis of the time and space requirements of their clustering algorithm. While they mention that the algorithm has a worst-case time complexity of O(N log N), it would be helpful to understand how this complexity translates to real-world performance on large datasets. Specifically, the authors should provide empirical results on the runtime of their method on datasets of varying sizes, and discuss any optimizations that can be used to improve performance. Additionally, the authors should discuss the memory requirements of their method, and how this might limit the size of datasets that can be processed. It would also be useful to compare the computational cost of their method with other clustering algorithms, such as k-means or DBSCAN, to provide a better understanding of its efficiency.

Finally, the authors should provide a more comprehensive comparison with existing methods for unsupervised record linkage. While the paper mentions that there are no existing methods that can be directly compared with their approach, it would still be beneficial to compare their method with other techniques that are used for similar tasks, such as anomaly detection or record linkage. For example, the authors could compare their method with probabilistic record linkage techniques, or with clustering algorithms that are commonly used for anomaly detection. This would help to better understand the strengths and weaknesses of their method, and to identify areas where it could be improved. The authors should also consider using benchmark datasets that are commonly used for evaluating record linkage and anomaly detection methods, to provide a more objective comparison.

### Questions

1. How does the method perform when the structural constraint does not hold?
2. What is the computational complexity of the method, and how does it scale with the size of the dataset?
3. How does the method compare with existing methods for unsupervised record linkage?

### Rating

6

### Confidence

3

**********