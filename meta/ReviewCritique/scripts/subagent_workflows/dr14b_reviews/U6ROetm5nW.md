### Summary

This paper studies the kernel density estimation (KDE) problem, where given a dataset of $n$ points in Euclidean space and a kernel $K(p, q)$, the goal is to prepare a low-space data structure that can quickly output a $1 \pm \epsilon$ approximation to $\mu = (\sum_{p \in \mathcal{P}} K(p, q))/n$ for a query $q$. Recent advances have used LSH and ANN techniques to achieve sublinear query time in $1/\mu$ and linear space in $1/\mu$. This paper improves the query time to $O(1/\mu^{0.05})$ at the cost of higher space complexity $O(1/\mu^{4.15})$. More generally, the paper presents the first known query time vs. space tradeoffs for KDE, where for any $\delta \geq 0$, a data structure with space $O(1/\mu^{1+\delta})$ can achieve query time $O(1/\mu^{\xi(\delta)})$, with $\xi(\delta)$ being a non-increasing function of $\delta$. Notably, for the linear space regime ($\delta = 0$), the paper obtains a query time of $O(1/\mu^{0.1865})$, improving upon previous bounds and nearly matching the bound of Charikar et al. (2020) with a simpler analysis.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper presents a novel approach to KDE by leveraging asymmetric LSH constructions, which allows for a tradeoff between query time and space complexity. This is a significant advancement in the field, as it provides more flexibility in designing KDE data structures based on available resources.

2. The paper achieves a notable improvement in query time for the linear space regime, reaching $O(1/\mu^{0.1865})$, which is better than the previous non-adaptive bound of $O(1/\mu^{0.25})$ from Charikar et al. (2020). This improvement, combined with a simpler analysis, makes the result both theoretically and practically valuable.

### Weaknesses

#### Some Related Works


#### comment

1. The paper's focus on the Gaussian kernel limits its applicability. While the Gaussian kernel is widely used, the analysis and results might not directly extend to other common kernels, such as the Laplace kernel. The paper should discuss the potential challenges and modifications required to adapt the proposed techniques to other kernels. Specifically, the analysis relies on specific properties of the Gaussian kernel, such as its smoothness and rapid decay, which may not hold for other kernels. For instance, the Laplace kernel, while also a radial basis function, has a slower decay rate, which could significantly impact the performance of the proposed data structure and require different LSH families or analysis techniques. The paper should at least discuss the theoretical hurdles in extending their approach.

2. The paper lacks empirical evaluation of the proposed data structure. While the theoretical improvements are significant, it is crucial to demonstrate the practical performance of the data structure on real-world datasets. The paper should include experiments comparing the query time and space usage of the proposed data structure with existing methods, especially in the linear space regime. This would help validate the theoretical claims and assess the practical benefits of the proposed approach. The experiments should also explore the impact of different parameter settings on the performance of the data structure.

3. The paper does not provide a detailed comparison with existing KDE data structures, particularly those that achieve different tradeoffs between query time and space. A more comprehensive comparison would help readers understand the advantages and limitations of the proposed approach in the context of existing work. The comparison should not only focus on the asymptotic bounds but also discuss the practical implications of these bounds, such as the constant factors involved and the dependence on the dimensionality of the data. A table summarizing the performance of different methods would be beneficial.

### Suggestions

The paper should include a more thorough discussion on the limitations of the proposed approach, particularly regarding its applicability to kernels other than the Gaussian kernel. The authors should explore the theoretical challenges in adapting their techniques to other kernels, such as the Laplace kernel, and discuss potential modifications to their analysis. This discussion should include an analysis of how the different properties of these kernels, such as their decay rates and smoothness, would affect the performance of the proposed data structure. Furthermore, the authors should consider providing some preliminary results or simulations to demonstrate the feasibility of their approach for other kernels, even if a full theoretical analysis is not yet available. This would significantly strengthen the paper's contribution and broaden its impact.

To address the lack of empirical evaluation, the authors should conduct experiments on real-world datasets to validate the practical performance of their proposed data structure. These experiments should compare the query time and space usage of the proposed data structure with existing methods, especially in the linear space regime. The experiments should also explore the impact of different parameter settings on the performance of the data structure. It would be beneficial to include a variety of datasets with different characteristics, such as varying dimensionality and data distributions, to assess the robustness of the proposed approach. The experimental results should be presented clearly, with appropriate statistical analysis, to provide a comprehensive evaluation of the proposed data structure.

Finally, the paper should include a more detailed comparison with existing KDE data structures, particularly those that achieve different tradeoffs between query time and space. This comparison should not only focus on the asymptotic bounds but also discuss the practical implications of these bounds, such as the constant factors involved and the dependence on the dimensionality of the data. A table summarizing the performance of different methods, including their query time, space complexity, and any other relevant parameters, would be beneficial. This would help readers understand the advantages and limitations of the proposed approach in the context of existing work and provide a clearer picture of the state-of-the-art in KDE data structures.

### Questions

1. Can the proposed techniques be extended to other kernels, such as the Laplace kernel? If so, what modifications would be required?

2. How does the proposed data structure perform in practice compared to existing methods, especially in the linear space regime? Are there any specific scenarios where the proposed approach offers a significant advantage?

### Rating

6

### Confidence

3

**********