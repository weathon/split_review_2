### Summary

This paper introduces Automatic Complementary Separation Pruning (ACSP), a novel pruning method that combines structured and activation-based pruning to accelerate inference time in convolutional neural networks. ACSP constructs a graph space to evaluate the separation capabilities of each component across all class pairs, using clustering techniques to ensure diverse and complementary capabilities. The method automatically determines the pruning volume, reducing redundancy while maintaining high performance. ACSP significantly reduces FLOPs and inference time with minimal accuracy loss, validated across multiple architectures and datasets.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. ACSP introduces a novel approach by combining structured and activation-based pruning, which is a significant advancement over traditional methods that often rely on manual tuning.
2. The paper provides a thorough evaluation of ACSP across various architectures (VGG, ResNet, DenseNet, MobileNet) and datasets (CIFAR-10/100, ImageNet), demonstrating consistent performance improvements.
3. The method's ability to automatically determine the pruning volume is a practical advantage, reducing the need for manual intervention and making it more scalable for real-world applications.

### Weaknesses

#### Some Related Works


#### comment

1. The paper lacks a detailed comparison with state-of-the-art pruning methods, particularly those that also focus on automated pruning. For instance, methods like CAP and CAPNet, which utilize class-activation mapping for pruning, should be included in the comparison to provide a more comprehensive evaluation of ACSP's performance. The absence of these comparisons makes it difficult to ascertain the true novelty and effectiveness of the proposed method relative to existing automated pruning techniques.
2. The evaluation is limited to image classification tasks. The paper should include experiments on other tasks, such as object detection and segmentation, to demonstrate the generalizability of ACSP. The current evaluation does not provide sufficient evidence that the method can be effectively applied to different types of tasks with varying network architectures and data characteristics.
3. The paper does not provide a detailed analysis of the computational cost of the proposed method. It is important to understand the overhead introduced by the pruning process itself, especially when compared to other pruning techniques. The lack of this analysis makes it difficult to assess the practical applicability of ACSP in resource-constrained environments.
4. The paper lacks a discussion on the limitations of the proposed method. For example, how does the method perform on very large models or datasets? Are there specific types of network architectures where ACSP is less effective? A thorough discussion of these limitations would provide a more balanced view of the method's capabilities and applicability.

### Suggestions

To strengthen the paper, the authors should include a more comprehensive comparison with state-of-the-art automated pruning methods. Specifically, methods like CAP and CAPNet, which leverage class-activation mapping, should be included in the experimental evaluation. This would provide a clearer understanding of how ACSP performs relative to other automated pruning techniques and highlight its unique advantages. The comparison should not only focus on accuracy but also on other metrics such as the number of parameters, FLOPs, and inference time. Furthermore, the authors should provide a detailed analysis of the computational cost associated with the ACSP method. This analysis should include the time taken for graph construction, clustering, and pruning, and compare it with the computational cost of other pruning methods. This would help in understanding the practical applicability of ACSP, especially in resource-constrained environments. The authors should also investigate the sensitivity of ACSP to different hyperparameters and provide guidelines for selecting appropriate values. This would make the method more user-friendly and easier to apply in practice.

In addition to expanding the comparison with other pruning methods, the authors should also broaden the scope of their experimental evaluation. The current evaluation is limited to image classification tasks, which does not provide sufficient evidence of the method's generalizability. The authors should include experiments on other tasks, such as object detection and segmentation, to demonstrate the effectiveness of ACSP in different scenarios. These experiments should be conducted on a variety of datasets and network architectures to provide a more comprehensive evaluation of the method's performance. Furthermore, the authors should provide a more detailed analysis of the impact of pruning on the network's feature representations. This analysis should include visualizations of the feature maps before and after pruning to understand how the method affects the network's ability to extract meaningful features. This would provide a deeper understanding of the method's inner workings and help in identifying potential areas for improvement.

Finally, the authors should include a thorough discussion of the limitations of the proposed method. This discussion should address questions such as how the method performs on very large models or datasets, and whether there are specific types of network architectures where ACSP is less effective. The authors should also discuss the potential impact of the pruning process on the network's robustness to adversarial attacks and other types of perturbations. This would provide a more balanced view of the method's capabilities and applicability and help in identifying potential areas for future research. The authors should also consider providing an ablation study to understand the contribution of each component of the ACSP method. This would help in identifying the most important aspects of the method and guide future research in this area.

### Questions

1. How does ACSP compare to other state-of-the-art pruning methods in terms of accuracy and computational efficiency?
2. Can the authors provide more insights into the selection of hyperparameters for ACSP, and how sensitive is the method to these parameters?
3. What are the potential limitations of ACSP when applied to very large models or datasets?
4. How does the pruning process affect the network's robustness to adversarial attacks or other types of perturbations?

### Rating

6

### Confidence

3

**********