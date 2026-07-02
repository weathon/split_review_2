### Summary

This paper proposes a novel approach for generating high-quality remote sensing images from object layouts, addressing limitations in existing methods. The proposed method, called Object Fidelity Diffusion (OF-Diff), leverages object layouts to extract structural shape priors and employs an online distillation strategy to integrate complex image features. This allows for highly controllable and high-fidelity image generation without relying on real-image references. Additionally, the method uses DDPO to fine-tune the diffusion process, enhancing the diversity and semantic consistency of the generated images. The paper demonstrates that OF-Diff outperforms state-of-the-art methods in remote sensing image generation across various quality metrics, particularly improving performance for challenging object classes such as airplanes, ships, and vehicles.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a novel approach, Object Fidelity Diffusion (OF-Diff), which combines object layout extraction, online distillation, and DDPO fine-tuning to achieve high-fidelity and controllable remote sensing image generation. This approach is innovative and addresses the limitations of existing methods that rely on additional textual guidance or real-image references.

2. The paper provides a comprehensive evaluation of the proposed method across multiple datasets (DIOR, DOTA, HRSC2016) and various quality metrics (FID, KID, CMMD, CAS, YOLOScore, mAP). The results demonstrate that OF-Diff outperforms state-of-the-art methods in terms of generation fidelity, layout consistency, and shape fidelity. The improvements are particularly significant for challenging object classes.

3. The paper is well-structured and clearly explains the proposed method, including the Enhanced Shape Generation Module (ESGM), online distillation, and DDPO fine-tuning. The authors provide detailed descriptions of the experimental setup, implementation details, and ablation studies, which enhance the reproducibility and understanding of the work.

### Weaknesses

#### Some Related Works


#### comment

1. The paper lacks a detailed discussion on the computational complexity and efficiency of the proposed method. While the method achieves high-fidelity and controllable image generation, it is unclear how the computational cost compares to existing methods. This is particularly important for practical applications where computational resources may be limited. The paper should include a more thorough analysis of the number of parameters, FLOPs, and memory requirements, especially in comparison to other layout-to-image generation models. Furthermore, the inference time should be analyzed, considering the impact of the online distillation and DDPO fine-tuning steps.

2. The paper does not provide a comprehensive analysis of the failure cases of the proposed method. While the results demonstrate significant improvements, it is important to understand the limitations of the approach. The paper should include a qualitative analysis of the generated images, highlighting scenarios where the method fails to produce high-quality or realistic images. This analysis should go beyond simple metrics and provide insights into the types of object layouts or scene complexities that pose challenges to the model. For example, it would be beneficial to see examples where the generated objects have incorrect aspect ratios, textures, or spatial relationships, and to understand why these failures occur.

### Suggestions

To address the lack of computational analysis, the authors should include a detailed comparison of the proposed method's computational cost with existing state-of-the-art layout-to-image generation models. This comparison should include metrics such as the number of parameters, FLOPs, memory usage, and inference time. The analysis should also break down the computational cost of each component of the proposed method, such as the Enhanced Shape Generation Module (ESGM), online distillation, and DDPO fine-tuning. This would provide a clear understanding of the computational overhead introduced by each component and help identify potential bottlenecks. Furthermore, the authors should discuss the trade-offs between computational cost and generation quality, providing insights into how the method can be optimized for different resource constraints. For example, they could explore the impact of reducing the number of diffusion steps or using more efficient network architectures.

To improve the analysis of failure cases, the authors should include a qualitative analysis of the generated images, highlighting scenarios where the method fails to produce high-quality or realistic images. This analysis should go beyond simple metrics and provide insights into the types of object layouts or scene complexities that pose challenges to the model. For example, the authors could show examples where the generated objects have incorrect aspect ratios, textures, or spatial relationships, and discuss the reasons for these failures. This could involve analyzing the limitations of the shape priors extracted by the ESGM, the effectiveness of the online distillation strategy, or the impact of the DDPO fine-tuning. Furthermore, the authors should explore potential solutions to address these failure cases, such as incorporating more robust shape priors, improving the distillation process, or using more advanced fine-tuning techniques. This would provide a more complete understanding of the method's limitations and guide future research directions.

Finally, the authors should consider including a more detailed ablation study that explores the impact of different design choices on the performance of the proposed method. For example, they could analyze the effect of varying the number of distillation steps, the strength of the DDPO fine-tuning, or the architecture of the ESGM. This would provide a more comprehensive understanding of the method's sensitivity to different hyperparameters and help identify the optimal configuration for different datasets and applications. Additionally, the authors could explore the impact of different loss functions or training strategies on the generation quality and diversity. This would provide a more thorough evaluation of the proposed method and help identify areas for further improvement.

### Questions

1. Can the authors provide more details on the computational complexity and efficiency of the proposed method compared to existing methods? This would help understand the practical applicability of the approach.

2. What are the limitations of the proposed method, and in what scenarios might it fail to generate high-quality images? A discussion of potential failure cases would provide a more complete understanding of the method's capabilities and limitations.

### Rating

8

### Confidence

4

**********