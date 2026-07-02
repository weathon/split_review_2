### Summary

This paper explores the potential of generative models for general-purpose perceptual organization, specifically for category-agnostic instance segmentation. The authors fine-tune Stable Diffusion and Masked Autoencoder (MAE) models using a category-agnostic instance coloring loss on a limited dataset of indoor furnishings and cars. Surprisingly, the resulting models demonstrate strong zero-shot generalization capabilities, accurately segmenting object types and styles unseen during fine-tuning. The models even approach or surpass the performance of the heavily supervised SAM model in certain cases, particularly when segmenting fine structures and ambiguous boundaries. This suggests that generative models may learn inherent grouping mechanisms that transfer across categories and domains, even without internet-scale pretraining.

### Soundness

2

### Presentation

3

### Contribution

3

### Strengths

- The approach of repurposing generative models for instance segmentation is innovative and distinct from previous works that primarily use generative models for image synthesis or discriminatively pretrain on large datasets for perception tasks.
- The proposed method demonstrates impressive zero-shot generalization capabilities, effectively segmenting object types and styles not present in the fine-tuning data, which suggests an inherent grouping mechanism learned by generative models.
- The findings could have significant implications for developing more generalizable vision systems, potentially benefiting applications in robotics, medical imaging, and autonomous systems.

### Weaknesses

#### Some Related Works


#### comment

 - While the paper demonstrates promising results, further validation on more diverse and challenging datasets could strengthen the claims about the model's generalization capabilities.
- The performance on small objects is a limitation, which the authors attribute to pre-training biases. Exploring strategies to mitigate this issue could improve the model's robustness.
- The paper could benefit from a more in-depth discussion of the theoretical underpinnings of why generative models exhibit these generalization properties. Additionally, providing more detailed comparisons with a broader range of state-of-the-art methods would help contextualize the contributions more effectively.

### Suggestions

The paper's exploration of generative models for instance segmentation is compelling, but its evaluation could be significantly strengthened by incorporating more diverse and challenging datasets. While the current results demonstrate promising zero-shot generalization, the reliance on a limited set of evaluation scenarios raises concerns about the robustness of the findings. Specifically, the authors should consider including datasets that feature a wider range of object sizes, complex occlusions, and more varied environmental conditions. For instance, datasets with small, cluttered objects or images with significant motion blur could provide a more rigorous test of the model's capabilities. Furthermore, it would be beneficial to evaluate the model's performance on datasets with different types of visual artifacts or noise, which are common in real-world applications. This would help to better understand the limitations of the approach and identify areas for future improvement. The inclusion of such datasets would provide a more comprehensive assessment of the model's generalization capabilities and enhance the paper's overall impact.

Addressing the performance limitations on small objects is crucial for improving the practical applicability of the proposed method. The authors attribute this issue to pre-training biases, but a more detailed investigation into the underlying causes is warranted. For example, it would be valuable to analyze the feature representations learned by the generative models at different scales to understand why small objects are not being effectively captured. This analysis could involve visualizing the feature maps or examining the activation patterns of different network layers. Furthermore, the authors should explore specific strategies to mitigate this issue, such as incorporating multi-scale training techniques or using data augmentation methods that specifically target small objects. Another approach could involve modifying the model architecture to include specialized layers or modules that are better suited for capturing fine-grained details. By focusing on these specific areas, the authors can significantly improve the model's robustness and overall performance.

Finally, a more in-depth discussion of the theoretical underpinnings of the observed generalization properties is needed to fully appreciate the significance of the findings. While the paper suggests that generative models learn inherent grouping mechanisms, a more detailed explanation of how these mechanisms arise during the pre-training process is necessary. For instance, the authors could explore the relationship between the generative model's objective function and the emergence of these grouping capabilities. Additionally, it would be beneficial to compare the learned representations with those of other models, such as discriminatively trained models, to highlight the unique properties of generative models. This could involve analyzing the feature spaces of different models or examining their responses to various types of visual stimuli. Furthermore, a more comprehensive comparison with a broader range of state-of-the-art methods, including those that leverage different approaches to instance segmentation, would help to better contextualize the contributions of this work. This would provide a more complete understanding of the strengths and limitations of the proposed method and its position within the broader field of computer vision.

### Questions

1. Could the authors elaborate on why generative models, specifically Stable Diffusion and MAE, exhibit strong zero-shot generalization for instance segmentation? What inherent properties of these models contribute to this capability?
2. How does the proposed method compare with other recent approaches to instance segmentation in terms of performance, computational efficiency, and generalization capabilities?
3. What are the potential real-world applications of this approach, and what challenges need to be addressed before it can be widely deployed?
4. How does the choice of fine-tuning data (indoor furnishings and cars) influence the model's generalization capabilities? Would fine-tuning on a different or more diverse dataset lead to different results?
5. The paper mentions that the models perform particularly well on fine structures and ambiguous boundaries. Could the authors provide more insight into why this is the case and how the generative prior contributes to this performance?

### Rating

6

### Confidence

3

**********