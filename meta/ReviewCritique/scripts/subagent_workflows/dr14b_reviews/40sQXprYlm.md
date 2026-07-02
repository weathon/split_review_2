### Summary

The authors propose a new architecture that they call a distributed neural network. In this architecture, each token is routed via its own path through the network. The authors show that these networks can be trained and can achieve performance competitive with dense networks. They also show that the paths that tokens take through the network are often interpretable.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

The authors propose a new architecture that they call a distributed neural network. In this architecture, each token is routed via its own path through the network. The authors show that these networks can be trained and can achieve performance competitive with dense networks. They also show that the paths that tokens take through the network are often interpretable.

### Weaknesses

#### Some Related Works


#### comment

The authors propose a new architecture that they call a distributed neural network. In this architecture, each token is routed via its own path through the network. The authors show that these networks can be trained and can achieve performance competitive with dense networks. They also show that the paths that tokens take through the network are often interpretable.

### Suggestions

The paper introduces an interesting concept of distributed neural networks, but the experimental validation could be significantly strengthened. While the authors demonstrate that their proposed architecture achieves competitive performance, the scale of the experiments is a major concern. The models used appear to be quite small by current standards, and it's unclear whether the observed behavior would scale to larger, more practical models. For instance, the number of parameters and the depth of the networks should be increased to match those of state-of-the-art models in both vision and language tasks. This would provide more convincing evidence that the proposed routing mechanism is not just an artifact of small model sizes. Furthermore, the authors should explore the computational cost of their approach, as the dynamic routing of tokens might introduce overhead that could limit its practical applicability. A detailed analysis of the training time and inference time compared to dense networks would be valuable.

Additionally, the paper lacks a thorough exploration of the design space for these distributed neural networks. The authors should investigate the impact of different routing strategies, such as varying the number of routers, the connectivity patterns between modules, and the criteria used for routing tokens. For example, they could explore whether a fixed routing strategy or a dynamic one based on token features is more effective. The choice of activation functions and normalization layers within the modules could also be varied to see how these choices affect performance and interpretability. A more systematic exploration of these design choices would provide a deeper understanding of the strengths and limitations of the proposed architecture. It would also help to identify the optimal configurations for different tasks and datasets. The current work only scratches the surface of what is possible with distributed neural networks.

Finally, the interpretability analysis, while intriguing, could be more rigorous. The authors mention that the paths taken by tokens are often interpretable, but they do not provide a clear methodology for quantifying or validating these interpretations. It would be beneficial to develop metrics that measure the interpretability of the learned paths and to compare these metrics across different models and datasets. For example, one could analyze the correlation between the learned paths and known semantic structures in the data. Furthermore, the authors should investigate whether the interpretability of the paths is consistent across different inputs or whether it varies significantly. A more detailed and quantitative analysis of interpretability would make this aspect of the paper more convincing and impactful.

### Questions

The authors propose a new architecture that they call a distributed neural network. In this architecture, each token is routed via its own path through the network. The authors show that these networks can be trained and can achieve performance competitive with dense networks. They also show that the paths that tokens take through the network are often interpretable.

### Rating

6

### Confidence

3

**********