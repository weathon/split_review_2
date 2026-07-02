### Summary

This paper introduces a novel mapping-based compression framework for CLIP models, aiming to address the limitations of existing select-based weight inheritance methods. The proposed CLIP-Map framework utilizes learnable matrices to map and combine pretrained weights, preserving more information from the original model. To mitigate optimization challenges, the authors propose Diagonal Inheritance Initialization, which reduces distribution shifting and enables efficient mapping learning. Experimental results demonstrate that CLIP-Map outperforms select-based frameworks across various compression ratios, especially under high compression settings.

### Soundness

2

### Presentation

2

### Contribution

2

### Strengths

1. The proposed CLIP-Map framework introduces a novel mapping-based compression approach, differing from traditional select-based pruning methods. This approach leverages learnable matrices to map and combine pretrained weights, aiming to preserve more information from the original model. The use of Kronecker Factorization for efficient parameter mapping is also a notable technical innovation.

2. The paper provides extensive experimental results across various compression ratios and benchmarks, demonstrating the effectiveness of CLIP-Map. The performance gains, especially under high compression settings, highlight the framework's ability to maintain model performance while significantly reducing model size.

3. The introduction of Diagonal Inheritance Initialization addresses the optimization challenges associated with learnable mapping, contributing to the stability and efficiency of the training process. This initialization strategy, combined with knowledge distillation, facilitates effective knowledge transfer from the teacher model to the compressed student model.

### Weaknesses

#### Some Related Works


#### comment

1. The paper could benefit from a more detailed comparison with existing methods, particularly in terms of computational efficiency and memory usage during the training process. While the authors mention reduced training overhead, a quantitative comparison with other compression techniques would strengthen the claims. Specifically, the paper lacks a detailed breakdown of the computational cost associated with the proposed mapping-based compression, such as the number of floating-point operations (FLOPs) and the memory footprint of the learnable matrices. A comparison with other pruning and quantization methods, including a discussion of their respective training costs, would be beneficial.

2. The discussion on the limitations of the proposed method is relatively brief. Expanding on scenarios where CLIP-Map might underperform or face challenges would provide a more balanced view. For instance, the paper does not explore the sensitivity of the method to different initialization strategies or the impact of extreme compression ratios on the quality of the learned mappings. A more thorough analysis of these aspects would be valuable.

3. The paper could provide more insights into the choice of hyperparameters for the mapping matrices and their impact on the final model performance. A sensitivity analysis or guidelines for hyperparameter selection would be helpful for practitioners. The paper lacks a discussion on how the size and structure of the learnable matrices affect the compression performance and the trade-off between model size and accuracy. A more detailed analysis of the impact of these hyperparameters would be beneficial.

### Suggestions

To enhance the paper, the authors should include a detailed analysis of the computational cost associated with their proposed CLIP-Map framework. This should include a breakdown of the FLOPs required for training the mapping matrices and the memory footprint of these matrices. A comparison with other compression techniques, such as pruning and quantization, should be provided, including a discussion of their respective training costs. This would allow readers to better understand the trade-offs between different compression methods and the advantages of the proposed approach. Furthermore, the authors should investigate the sensitivity of their method to different initialization strategies. This could involve experimenting with different initialization schemes for the mapping matrices and analyzing their impact on the final model performance. A discussion of the limitations of the method, such as the impact of extreme compression ratios on the quality of the learned mappings, should also be included. This would provide a more balanced view of the proposed approach and its potential drawbacks.

Additionally, the authors should provide a more detailed analysis of the hyperparameters associated with the mapping matrices. This should include a discussion of how the size and structure of these matrices affect the compression performance and the trade-off between model size and accuracy. A sensitivity analysis of these hyperparameters would be beneficial, allowing practitioners to better understand how to tune the method for their specific needs. The authors could also provide guidelines for hyperparameter selection, based on their experimental results. This would make the method more accessible and easier to use for other researchers. For example, the authors could explore the impact of different matrix sizes on the final model performance and provide recommendations on how to choose the optimal size for a given compression ratio.

Finally, the authors should consider including a more detailed analysis of the knowledge distillation process. This could involve investigating the impact of different distillation strategies on the final model performance. For example, the authors could explore the use of different loss functions or different teacher models. A more detailed analysis of the knowledge distillation process would provide a better understanding of how the proposed method works and how it can be further improved. This would also allow readers to better understand the role of knowledge distillation in the overall performance of the method and how it contributes to the preservation of model performance under high compression settings.

### Questions

1. How does the computational cost of the proposed CLIP-Map framework compare to traditional pruning and quantization methods during the training phase? Are there specific scenarios where CLIP-Map might be more computationally intensive?

2. What are the limitations of the Diagonal Inheritance Initialization in terms of optimization stability and convergence speed? Are there scenarios where this initialization might not be as effective?

3. How does the performance of CLIP-Map vary with different compression ratios, especially beyond the tested ranges? Are there any observed limitations or performance degradation at extremely high compression ratios?

### Rating

5

### Confidence

3

**********