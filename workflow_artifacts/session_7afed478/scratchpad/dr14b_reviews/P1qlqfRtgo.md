### Summary

This paper explores the impact of neural network architecture on modeling thermal explosions in hydrogen-oxygen-air mixtures. Using a dataset generated from a reduced kinetic mechanism with 11 reagents, the study compares three architectures: a standard multi-layer perceptron (MLP), a DeepONet-inspired model, and a U-Net-style residual network. The U-Net architecture demonstrated superior performance, achieving a mean squared error (MSE) of 0.0013, significantly outperforming the DeepONet-inspired model and MLP. This indicates that careful selection of network architecture is crucial for accurate, reliable predictive models in combustion and reactive-flow applications.

### Soundness

2

### Presentation

2

### Contribution

2

### Strengths

The paper provides a thorough comparison of neural network architectures for a specific application, offering insights into the strengths of U-Net for complex dynamic systems.

### Weaknesses

#### comment

1. While the paper effectively compares different architectures, it does not introduce a novel neural network structure or significantly advance the theoretical understanding of neural networks in this domain. The contribution is primarily empirical, which may limit its impact on the broader field of neural network research.
2. The study focuses on a specific problem (thermal explosion in hydrogen-oxygen-air mixtures) with a fixed dataset. This raises concerns about the generalizability of the findings to other types of combustion processes or different reactive systems. More diverse datasets or theoretical insights into why U-Net performs better could strengthen the conclusions.

### Questions

1. Could the authors provide more theoretical insights into why the U-Net architecture outperforms the others in this specific application? A deeper analysis could help generalize these findings to other domains.
2. How would the proposed models perform with different or more complex chemical mechanisms? Would the U-Net still outperform the others, or would the performance gap change?

### Rating

3

### Confidence

3

**********