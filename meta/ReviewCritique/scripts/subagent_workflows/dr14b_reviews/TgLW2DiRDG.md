### Summary

This paper studies the geometry of the polyhedral complex formed by ReLU neural networks. The authors provide theoretical results on the connectivity graph of this complex, showing that the average degree is upper bounded by $2d$ and the diameter is upper bounded by $(m+1)^\ell$, where $d$ is the input dimension, $m$ is the maximum layer width, and $\ell$ is the number of hidden layers. They also present an algorithm for calculating the boundaries of these polyhedra and conduct experiments to validate their theoretical findings.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper presents novel theoretical results on the connectivity graph of the polyhedral complex formed by ReLU networks, specifically on the average degree and diameter. These results are significant for understanding the geometric structure of ReLU networks.

2. The authors provide a clear and rigorous mathematical framework for their analysis, with detailed proofs and well-defined concepts.

### Weaknesses

#### Some Related Works


#### comment

1. The paper focuses exclusively on fully-connected ReLU networks, and the results may not generalize to other types of neural networks, such as convolutional or residual networks. The analysis relies heavily on the specific structure of fully-connected layers and the way ReLU activations create polyhedral regions in the input space. It is unclear how the connectivity graph would be defined or analyzed for networks with shared weights or skip connections, which are common in modern architectures.

2. The algorithm for calculating polyhedron boundaries has exponential time complexity, making it impractical for large-scale neural networks. The authors do not provide a detailed analysis of the algorithm's runtime with respect to the input dimension, number of neurons, or depth of the network. This lack of analysis makes it difficult to assess the practical applicability of the proposed algorithm, especially for networks with moderate to high dimensionality.

3. The significance of the theoretical results is not entirely clear. It is not clear why understanding the connectivity graph is important for understanding the behavior of neural networks. The paper does not provide concrete examples or applications where the derived bounds on the average degree and diameter of the connectivity graph would be directly useful. The connection between these graph properties and the learning capabilities or generalization performance of the network remains unclear.

### Suggestions

The paper would benefit from a more thorough discussion of the limitations of the proposed approach, particularly regarding the types of neural networks it can be applied to. While the analysis of fully-connected ReLU networks is a valuable starting point, the authors should acknowledge the significant differences in the activation patterns and decision boundaries of other architectures, such as convolutional or residual networks. A discussion of how the concepts of polyhedral complexes and connectivity graphs could be adapted or extended to these architectures would be beneficial. For example, the authors could explore whether the notion of a 'polyhedral complex' can be generalized to the feature maps of convolutional layers, and how the connectivity between these regions would be defined. This would help to clarify the scope and limitations of the current work and suggest potential directions for future research.

To address the practical limitations of the proposed algorithm, the authors should provide a more detailed analysis of its computational complexity. This analysis should include a breakdown of the runtime with respect to the input dimension, number of neurons, and depth of the network. Furthermore, the authors should explore alternative algorithms or approximation techniques that could be used to compute the polyhedron boundaries more efficiently. For example, they could investigate whether sampling-based methods or optimization techniques could be used to approximate the boundaries without requiring an exhaustive search. This would make the results more accessible and applicable to a wider range of neural network architectures and datasets. The authors should also consider providing empirical results on the runtime of the algorithm for different network sizes and input dimensions, to better illustrate its practical limitations.

Finally, the paper needs to provide a more compelling argument for the significance of the theoretical results. The authors should provide concrete examples or applications where the derived bounds on the average degree and diameter of the connectivity graph would be directly useful. For instance, they could explore whether these bounds can be used to predict the generalization performance of the network, or to guide the design of more efficient training algorithms. The authors could also investigate whether the connectivity graph properties are related to the robustness of the network to adversarial attacks or to the interpretability of its decision-making process. This would help to establish a clear connection between the theoretical results and the practical behavior of neural networks, and would make the paper more impactful.

### Questions

1. How do the results extend to other types of neural networks, such as convolutional or residual networks?

2. Can the authors provide more insights into the practical implications of their theoretical results? How can the bounds on the average degree and diameter of the connectivity graph be used to understand or improve neural networks?

### Rating

6

### Confidence

3

**********