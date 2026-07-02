### Summary

This paper introduces a novel approach to address the copy-paste artifact in identity-preserving image generation. The authors first construct a large-scale paired dataset, MultiID-2M, tailored for multi-person scenarios, providing diverse references for each identity. They then introduce a benchmark that quantifies both copy-paste artifacts and the trade-off between identity fidelity and variation. Finally, they propose a novel training paradigm with a contrastive identity loss that leverages paired data to balance fidelity with diversity. These contributions culminate in WithAnyone, a diffusion-based model that effectively mitigates copy-paste while preserving high identity similarity. Extensive experiments demonstrate that WithAnyone substantially reduces copy-paste artifacts, improves controllability over pose and expression, and maintains strong perceptual quality.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper is well-written and easy to follow. The authors clearly articulate the problem of copy-paste artifacts in identity-preserving generation and provide a comprehensive solution that includes data construction, benchmarking, and model development.

2. The construction of the MultiID-2M dataset is a significant contribution. The dataset provides a valuable resource for the research community, enabling more robust evaluation and development of multi-identity generation models. The authors' careful curation of the dataset, including filtering for quality and aesthetic score, ensures that the data is suitable for training high-quality models.

3. The introduction of the MultiID-Bench benchmark is another valuable contribution. The benchmark provides a standardized evaluation protocol for multi-identity generation, enabling systematic and intrinsic assessment of methods. The authors' careful definition of metrics, including the copy-paste metric, allows for a more nuanced understanding of model performance.

4. The proposed WithAnyone model achieves state-of-the-art performance on the MultiID-Bench benchmark. The model effectively mitigates copy-paste artifacts while preserving high identity similarity. The authors' use of a contrastive identity loss with extended negatives is a key innovation that enables the model to learn more robust identity representations.

### Weaknesses

#### Some Related Works


#### comment

1. The paper could benefit from more detailed ablation studies to understand the contribution of each component of the proposed method. For example, it would be helpful to see how the performance of the model changes when different components of the training pipeline are removed or modified. Specifically, the impact of the contrastive loss, the specific architecture choices within the diffusion model, and the effect of different data augmentation strategies are not thoroughly explored. A more granular analysis, such as varying the temperature parameter in the contrastive loss or the number of negative samples, would provide a deeper understanding of the model's behavior.

2. While the paper demonstrates strong quantitative results, more qualitative comparisons with existing methods would be beneficial to better understand the visual differences in the generated images. The current qualitative results are limited and do not fully showcase the strengths and weaknesses of the proposed method compared to other state-of-the-art approaches. It would be valuable to see side-by-side comparisons on a wider range of challenging examples, including those with significant pose and expression variations, to better assess the visual quality and identity preservation capabilities of the model.

3. The paper could discuss the limitations of the proposed method in more detail. For example, how does the model perform on out-of-distribution data or in scenarios with more than a few identities? The current discussion of limitations is somewhat brief and does not fully address potential failure cases. A more thorough analysis of the model's robustness to variations in lighting, occlusion, and image quality would be beneficial. Furthermore, the paper should discuss the computational cost of the proposed method, especially in comparison to other approaches.

### Suggestions

To strengthen the paper, the authors should conduct more comprehensive ablation studies to isolate the impact of each component of their proposed method. Specifically, they should systematically evaluate the effect of the contrastive identity loss by varying the temperature parameter and the number of negative samples. Furthermore, they should analyze the contribution of different architectural choices within the diffusion model, such as the number of layers or the type of attention mechanisms used. The impact of different data augmentation techniques, such as random cropping, rotation, and color jittering, should also be explored. These ablation studies should be presented with clear quantitative metrics to demonstrate the importance of each component and provide a deeper understanding of the model's behavior. This would allow the reader to better understand the design choices and the trade-offs involved in the proposed approach.

In addition to more detailed ablation studies, the authors should provide more extensive qualitative comparisons with existing methods. This should include side-by-side comparisons on a wider range of challenging examples, including those with significant pose and expression variations, as well as examples with different lighting conditions and occlusions. The qualitative comparisons should focus on both the visual quality of the generated images and the preservation of identity. It would be beneficial to include examples where the proposed method performs well and examples where it fails, to better understand the limitations of the approach. The authors should also consider using a perceptual metric, such as LPIPS, to quantify the visual similarity between the generated and ground truth images, which would complement the existing quantitative metrics.

Finally, the authors should provide a more thorough discussion of the limitations of their proposed method. This should include an analysis of the model's performance on out-of-distribution data, such as images with different styles or resolutions. The paper should also discuss the computational cost of the proposed method, including the training time and inference time, and compare it to other state-of-the-art approaches. Furthermore, the authors should explore the model's scalability to scenarios with a larger number of identities and discuss potential failure cases. A more detailed analysis of these limitations would provide a more balanced view of the proposed method and guide future research in this area.

### Questions

1. Could the authors provide more details on the data collection process for the MultiID-2M dataset? How did they ensure the quality and diversity of the data?

2. How does the proposed method handle scenarios with more than a few identities? Are there any limitations in terms of scalability?

3. Could the authors provide more details on the computational cost of the proposed method? How does it compare to existing approaches?

### Rating

6

### Confidence

3

**********