### Summary

This paper presents a framework for constructing universally expressive equivariant machine learning architectures that process tensor data while respecting specific symmetries. The authors focus on equivariance with respect to the orthogonal group O(d), the indefinite orthogonal group O(s, k-s), and the symplectic group Sp(d). These symmetry groups are relevant in various scientific domains, including physics, materials science, and time series analysis.

The core contribution is a theoretical framework for building machine learning models that map tensors to tensors while preserving the underlying symmetries. The authors provide explicit parameterizations for polynomial and analytic functions that are equivariant with respect to the aforementioned groups. This framework generalizes prior work on equivariant models and leverages tensor invariant theory to create models suitable for machine learning applications.

The authors demonstrate their framework on three distinct problems:

Materials science: Learning the relationship between stress and strain tensors in materials.
Time series analysis: Representing time series data using path signatures and estimating them from sampled points.
Sparse vector estimation: Recovering a sparse vector from a random orthonormal basis.

The experimental results show that the proposed equivariant models outperform non-equivariant baselines and prior static methods in these applications. The authors highlight the practical benefits of incorporating symmetry constraints into machine learning models, leading to improved learning performance and generalization.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

Originality:
The paper introduces a novel framework for constructing equivariant machine learning models that process tensor data while respecting specific symmetries. The authors generalize prior work on equivariant models and leverage tensor invariant theory to create models suitable for machine learning applications. This approach is original in its explicit parameterization of equivariant functions using tensor invariants, providing a new perspective on building symmetry-preserving models.

Quality:
The paper is technically sound and well-supported by theoretical results. The authors provide rigorous proofs for their main theorems and corollaries, establishing a solid foundation for their framework. The experimental results are comprehensive and demonstrate the effectiveness of the proposed models across three diverse applications. The authors compare their models against relevant baselines and show consistent improvements, indicating the quality of their approach.

Clarity:
The paper is generally well-written and organized. The authors provide clear definitions and explanations of key concepts, making the paper accessible to readers with a background in machine learning and physics. The use of examples and illustrations helps to clarify the theoretical results and their practical implications.

Significance:
The paper addresses an important problem in machine learning: how to incorporate symmetry constraints into models that process tensor data. The proposed framework has the potential to impact various scientific domains where tensor data and symmetries are prevalent, such as physics, materials science, and time series analysis. The experimental results demonstrate the practical benefits of the framework, showing improved learning performance and generalization compared to non-equivariant models.

### Weaknesses

#### Some Related Works


#### comment

1. Limited Comparison with Existing Equivariant Models:
The paper primarily compares the proposed models against non-equivariant baselines. While the authors acknowledge related work on equivariant models, they do not provide a direct comparison with these methods in the experimental section. This makes it difficult to assess the relative strengths and weaknesses of the proposed framework compared to existing equivariant approaches. For instance, the paper could benefit from a comparison with methods that also leverage tensor representations and symmetry, such as those based on group convolutions or other tensor-based equivariant networks. A more thorough comparison would help to contextualize the contribution of this work within the broader landscape of equivariant machine learning.

2. Computational Complexity and Scalability:
The paper acknowledges that directly evaluating the equivariant functions defined in Corollary 1 can be computationally expensive, especially for high-order tensors. However, the authors do not provide a detailed analysis of the computational complexity of their framework or discuss potential strategies for mitigating this issue. The paper would benefit from a more rigorous analysis of the computational cost associated with the proposed parameterization, particularly in terms of the number of parameters and the time required for forward and backward passes. Furthermore, the authors should discuss the practical limitations of their approach when dealing with very large tensors or high-order polynomial approximations. It is unclear how the proposed method scales with increasing tensor order or dimensionality, and this needs to be addressed with concrete examples and analysis.

3. Generalization to Other Symmetry Groups:
While the paper focuses on the orthogonal, indefinite orthogonal, and symplectic groups, it does not discuss the potential for generalizing the framework to other symmetry groups relevant in different scientific domains. The paper could be strengthened by exploring the challenges and possibilities of extending the framework to other Lie groups or discrete symmetry groups. For example, it would be valuable to discuss whether the proposed approach can be adapted to handle symmetries such as permutations or other non-continuous transformations. A discussion of the limitations of the current framework and potential avenues for future research in this direction would be beneficial.

4. Practical Implementation Details:
The paper provides a high-level overview of the framework but lacks detailed implementation guidelines for practitioners. While the authors mention that the coefficients in Corollary 1 can be learned using MLPs, they do not provide specific details on how to implement this in practice. The paper would benefit from a more detailed discussion of the practical aspects of implementing the framework, including specific choices of neural network architectures for the coefficients, optimization strategies, and hyperparameter tuning. Concrete examples of how to implement the proposed method in popular deep learning frameworks would also be valuable for practitioners.

### Suggestions

To address the limited comparison with existing equivariant models, the authors should include a more comprehensive experimental evaluation that directly compares their approach with other state-of-the-art equivariant methods. This should include methods that also leverage tensor representations and symmetry, such as those based on group convolutions or other tensor-based equivariant networks. The comparison should not only focus on performance metrics but also on computational efficiency and scalability. For example, the authors could compare their method with a tensor field network or other similar architectures on a benchmark dataset. This would provide a more complete picture of the strengths and weaknesses of the proposed framework and help to contextualize its contribution within the broader landscape of equivariant machine learning. Furthermore, the authors should provide a more detailed analysis of the computational complexity of their framework, including the number of parameters and the time required for forward and backward passes. This analysis should consider the impact of tensor order and dimensionality on the computational cost. The authors should also discuss potential strategies for mitigating the computational burden, such as using low-degree polynomials or other approximation techniques. A practical demonstration of these strategies would be beneficial.

To improve the practical implementation details, the authors should provide more specific guidelines on how to implement their framework in popular deep learning frameworks. This should include detailed examples of how to construct the equivariant layers using the proposed parameterization, as well as specific choices of neural network architectures for the coefficients in Corollary 1. The authors should also discuss optimization strategies and hyperparameter tuning, providing practical advice for practitioners who want to use their framework. For example, the authors could provide a code snippet demonstrating how to implement a simple equivariant layer using PyTorch or TensorFlow. This would make the framework more accessible to a wider audience and facilitate its adoption in practical applications. Furthermore, the authors should discuss the limitations of their approach and potential avenues for future research, including the generalization to other symmetry groups. This should include a discussion of the challenges involved in extending the framework to other Lie groups or discrete symmetry groups, as well as potential solutions. For example, the authors could discuss the possibility of using different parameterizations for different symmetry groups or developing new techniques for handling non-continuous transformations. This would help to broaden the impact of their work and inspire future research in this area.

Finally, the authors should provide a more detailed discussion of the practical implications of their work, including the potential benefits and limitations of using equivariant models in different scientific domains. This should include a discussion of the types of problems where their framework is most likely to be effective, as well as the challenges involved in applying it to real-world datasets. For example, the authors could discuss the potential applications of their framework in areas such as materials science, physics, and time series analysis, providing concrete examples of how their method could be used to solve practical problems. This would help to demonstrate the relevance of their work and inspire further research in this area.

### Questions

1. Comparison with Existing Equivariant Models:
Could you provide a more detailed comparison of your framework with existing equivariant models, particularly those that also leverage tensor representations and symmetry? How does your approach differ in terms of computational efficiency, expressiveness, and ease of implementation?

2. Computational Complexity and Scalability:
What is the computational complexity of your framework, and how does it scale with the order and dimensionality of the tensors? Have you explored any strategies for mitigating the computational burden, such as using low-degree polynomials or other approximation techniques? How do these strategies affect the accuracy of the model?

3. Generalization to Other Symmetry Groups:
What are the main challenges in generalizing your framework to other symmetry groups, such as other Lie groups or discrete symmetry groups? Are there any specific symmetry groups that you believe would be particularly challenging or interesting to consider?

4. Practical Implementation Details:
Could you provide more detailed implementation guidelines for practitioners who want to use your framework? What are the key considerations when choosing the neural network architectures for the coefficients in Corollary 1? How sensitive is the performance of your framework to the choice of hyperparameters?

### Rating

6

### Confidence

3

**********