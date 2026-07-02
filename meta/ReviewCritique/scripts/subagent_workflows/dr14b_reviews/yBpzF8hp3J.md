### Summary

The paper studies differentially private domain discovery, where each user holds a subset of items from a shared but unknown domain, and the goal is to output an informative subset of items. For set union, the paper shows that the simple baseline Weighted Gaussian Mechanism (WGM) has a near-optimal $\ell_1$ missing mass guarantee on Zipfian data as well as a distribution-free $\ell_\infty$ missing mass guarantee. The paper then applies the WGM as a domain-discovery precursor for existing known-domain algorithms for private top-$k$ and $k$-hitting set and obtains new utility guarantees for their unknown domain variants. Finally, experiments demonstrate that all of the WGM-based methods are competitive with or outperform existing baselines for all three problems.

### Soundness

3

### Presentation

3

### Contribution

2

### Strengths

1. The paper is well-written and easy to follow.
2. The studied problem is interesting and important.
3. The paper provides solid theoretical analysis and empirical evaluation.

### Weaknesses

#### Some Related Works


#### comment

1. The paper seems to be incremental. The paper mainly studies the Weighted Gaussian Mechanism (WGM) which is proposed in [1]. The paper proves that the WGM has near-optimal $\ell_1$ missing mass guarantee on Zipfian data as well as a distribution-free $\ell_\infty$ missing mass guarantee. Then, the paper applies the WGM as a domain-discovery precursor for existing known-domain algorithms for private top-$k$ and $k$-hitting set and obtains new utility guarantees for their unknown domain variants. Although the paper proves some new theoretical results, the techniques seem to be standard and the results are not very surprising.

2. The paper does not compare with the recent work [2] which also studies the problem of differentially private domain discovery and improves the WGM.

### Suggestions

The paper's primary weakness lies in its incremental nature, particularly concerning the analysis of the Weighted Gaussian Mechanism (WGM). While the paper does provide new theoretical results, the core mechanism is not novel, and the analysis techniques employed appear to be standard. To strengthen the contribution, the authors could explore more novel algorithmic approaches or provide a more in-depth analysis that reveals previously unknown properties of the WGM in the context of domain discovery. For example, instead of focusing solely on the $\ell_1$ and $\ell_\infty$ missing mass guarantees, the authors could investigate tighter bounds under specific data distributions or explore the trade-offs between privacy and utility in a more nuanced manner. Furthermore, the paper could benefit from a more detailed discussion of the limitations of the WGM and how these limitations might impact the performance of the proposed algorithms in practice.

Another significant weakness is the lack of comparison with the recent work [2], which also addresses the problem of differentially private domain discovery and proposes improvements to the WGM. The absence of this comparison makes it difficult to assess the relative performance of the proposed methods. To address this, the authors should include a comprehensive experimental comparison with the methods proposed in [2]. This comparison should not only focus on the empirical performance but also on the theoretical guarantees and computational complexity. Furthermore, the authors should discuss the specific scenarios where their proposed methods outperform or underperform the methods in [2], providing a clear understanding of the strengths and weaknesses of each approach. This would allow the reader to better understand the practical implications of the proposed methods and their applicability in different settings.

Finally, the paper could benefit from a more thorough exploration of the practical implications of the proposed methods. While the theoretical analysis is important, it is equally important to understand how these methods perform in real-world scenarios. The authors could consider conducting experiments on real-world datasets to validate their theoretical findings and to demonstrate the practical utility of their proposed algorithms. This would involve not only comparing the performance of the proposed methods with existing baselines but also analyzing the sensitivity of the methods to different parameters and data characteristics. Furthermore, the authors could provide guidelines for selecting the appropriate parameters for their algorithms based on the specific characteristics of the data and the desired level of privacy.

### Questions

Please see the weaknesses.

### Rating

5

### Confidence

3

**********