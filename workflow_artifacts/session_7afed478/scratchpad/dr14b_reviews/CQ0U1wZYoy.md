### Summary

This paper proposes a prompted conditional diffusion framework, PRISM, which combines compound-aware supervision over mixed degradations with a weighted contrastive disentanglement objective. The framework is for single-image restoration targeting scientific applications where multiple degradations occur simultaneously.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The proposed framework is novel and well designed, leveraging the power of conditional diffusion model and contrastive learning.
2. The paper is overall well-written, with clear motivation, reasonable implementation, and extensive experiments that effectively demonstrate the superiority of the proposed method over previous approaches.

### Weaknesses

#### Some Related Works


#### comment

1. The proposed method is limited to single-image restoration, whereas real-world applications often involve sequences or bursts of images. The framework should be extended to leverage additional information from neighboring frames.

2. The paper lacks a detailed analysis of the computational complexity and runtime performance of the proposed method, which is crucial for practical applications.

3. The evaluation of the proposed method appears to rely primarily on synthetic data, raising concerns about its applicability to real-world scenarios. The paper should include more experiments on real-world data to better demonstrate the method's effectiveness.

### Suggestions

The paper's focus on single-image restoration is a significant limitation, given that many scientific applications, such as video analysis or time-lapse microscopy, inherently involve sequences of images. While the authors argue that their method addresses compound degradations within a single image, they overlook the potential benefits of leveraging inter-frame correlations present in image sequences. For instance, in video restoration, techniques like block-matching and motion compensation are often used to improve the accuracy of restoration by considering temporal redundancy. The authors should explore how their framework could be extended to incorporate such information, potentially through a recurrent diffusion model or by conditioning the restoration process on features extracted from neighboring frames. This would not only broaden the applicability of the method but also potentially improve its performance in scenarios where temporal coherence is present. The current approach, while effective for single images, risks becoming obsolete as multi-frame restoration techniques become more prevalent.

Furthermore, the lack of a detailed computational analysis is a critical oversight. The paper should provide a breakdown of the computational cost associated with each stage of the proposed framework, including the CLIP fine-tuning, diffusion model, and contrastive learning components. This analysis should not only include FLOPs but also memory usage and runtime on different hardware configurations. For example, the authors could report the inference time per image on a specific GPU, as well as the memory footprint of the model. This information is essential for practitioners to assess the feasibility of deploying the method in real-world scenarios, especially in resource-constrained environments. Without this analysis, it is difficult to determine whether the proposed method is practical for large-scale applications or if it is limited to research settings with access to high-performance computing resources. The authors should also consider comparing the computational cost of their method with existing single-image restoration techniques to provide a clear understanding of the trade-offs involved.

Finally, the reliance on synthetic data for evaluation is a major weakness that needs to be addressed. While synthetic data can be useful for initial validation, it often fails to capture the complexities of real-world degradations. The authors should include more experiments on real-world datasets, demonstrating the method's ability to handle diverse and complex degradations. For example, they could evaluate their method on datasets of satellite imagery, underwater images, or remote sensing data, which often exhibit complex and unknown degradations. The evaluation should also include a comparison with state-of-the-art methods on these real-world datasets. Furthermore, the authors should consider using perceptual metrics, in addition to PSNR and SSIM, to better assess the visual quality of the restored images. This would provide a more comprehensive evaluation of the method's effectiveness and its applicability to real-world scenarios. The current evaluation, based primarily on synthetic data, does not provide sufficient evidence to support the claim that the proposed method is suitable for practical applications.

### Questions

1. How does the proposed method extend to sequences or bursts of images, and how can it leverage additional information from neighboring frames?

2. What is the runtime and computational complexity of the proposed method?

3. Are there any experiments on real-world data to demonstrate the applicability of the proposed method?

### Rating

6

### Confidence

4

**********