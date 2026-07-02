### Summary

The paper investigates the internal representations of DINOv2, a vision transformer model, using sparse autoencoders. The authors propose the Linear Representation Hypothesis (LRH), which suggests that models contain many more features than neurons, arranged as sparse, quasi-orthogonal directions. They operationalize this hypothesis using stable sparse autoencoders (SAEs) and extract a dictionary of 32,000 concepts from DINOv2. The study analyzes how different downstream tasks (classification, segmentation, depth estimation) recruit these concepts, revealing task-specific specialization. They also examine the geometry and statistics of the learned concepts, finding patterns that challenge a purely sparse-coding view. Finally, the authors propose the Minkowski Representation Hypothesis (MRH), which suggests that tokens are formed by combining convex mixtures of archetypal landmarks, and discuss its implications for interpretability and model steering.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

- The paper presents a novel approach to understanding the internal representations of vision transformers by extracting and analyzing a large concept dictionary using sparse autoencoders.
- The study provides a comprehensive analysis of how different downstream tasks recruit the learned concepts, revealing functional specialization and task-aligned anisotropy.
- The authors propose the Minkowski Representation Hypothesis (MRH) as an alternative to the Linear Representation Hypothesis (LRH), offering a new perspective on the geometry of representations in vision transformers.
- The paper includes extensive visualizations and analyses, providing a detailed exploration of the learned concepts and their properties.

### Weaknesses

#### Some Related Works


#### comment

 - The paper relies heavily on the assumption that the Linear Representation Hypothesis (LRH) is a valid starting point for studying DINOv2 representations. However, the paper does not provide sufficient evidence or justification for this assumption, and it is possible that DINOv2 representations do not satisfy the LRH at all, or only in a limited sense.
- The paper proposes the Minkowski Representation Hypothesis (MRH) as an alternative to the LRH, but the MRH is not well-defined or well-supported by the evidence. The paper does not provide a clear mathematical definition of the MRH, or a way to test it empirically. The paper also does not explain how the MRH relates to the LRH, or why it is a better fit for DINOv2 representations.

### Suggestions

To strengthen the paper, the authors should provide more rigorous justification for the Linear Representation Hypothesis (LRH). This could involve comparing the performance of the sparse autoencoder under the linear assumption with its performance under alternative, non-linear assumptions. For example, the authors could explore using a kernel-based method or a neural network with non-linear activation functions to learn the dictionary of concepts and compare the reconstruction error. If the linear assumption is indeed superior, this would provide stronger evidence for the LRH. Furthermore, the authors should explore the limitations of the LRH and discuss the potential for non-linear relationships in the model's representations. This would provide a more nuanced understanding of the model's internal workings and address the concern that the linear assumption might be too restrictive.

To address the issues with the Minkowski Representation Hypothesis (MRH), the authors should provide a formal mathematical definition of the hypothesis, including a clear definition of the 'Minkowski sum' in the context of token embeddings. They should also provide a concrete method for testing the MRH empirically. For example, they could propose a way to measure the degree to which the token embeddings can be represented as Minkowski sums of convex polytopes. This could involve developing a metric that quantifies the distance between the observed token embeddings and the embeddings predicted by the MRH. Furthermore, the authors should clearly explain how the MRH relates to the LRH and why it is a better fit for DINOv2 representations. This could involve showing that the MRH can explain some of the observed phenomena that the LRH cannot, or that the MRH is more consistent with the known properties of the DINOv2 model.

Finally, the authors should provide more detailed explanations of the experimental results, especially those related to the MRH. For example, they should explain how the visualizations and examples in the paper support the MRH. They should also discuss the limitations of their experiments and suggest future directions for research. This would make the paper more accessible and convincing to the readers. The paper would also benefit from a more thorough discussion of the implications of the MRH for the field of explainable AI. For example, the authors could discuss how the MRH could be used to develop new methods for interpreting and manipulating the representations of vision foundation models.

### Questions

- How do you define and measure the concept importance for different downstream tasks? What are the advantages and disadvantages of your method compared to other possible methods?
- How do you choose the number of concepts (32,000) for your dictionary? How does this number affect the quality and interpretability of the learned representations?
- How do you visualize and interpret the high-dimensional concept vectors? What are the limitations and biases of your visualization methods?

### Rating

6

### Confidence

2

**********