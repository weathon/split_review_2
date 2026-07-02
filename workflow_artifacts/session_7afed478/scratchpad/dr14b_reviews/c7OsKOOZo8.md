### Summary

This paper introduces a novel end-to-end framework for multi-view diabetic retinopathy (DR) grading that integrates lesion-aware cues without requiring external annotations. The proposed GALP module strengthens stage-wise feature discriminability through auxiliary classification and transforms grade-conditioned evidence maps into lesion proposals. The LGRF module enables context-aware cross-view fusion by dynamically routing experts and applying Top-K weighted cross-view attention, ensuring precise and selective integration of lesion proposals across views. Extensive experiments on two multi-view fundus datasets, MFIDDR and DRTiD, demonstrate that the proposed method achieves state-of-the-art performance.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper is well-written and easy to follow.
2. The proposed method is novel and effective.
3. The experiments are comprehensive.

### Weaknesses

#### Some Related Works


#### comment

1. The proposed method is complex and may require more computational resources.
2. The proposed method is tailored for multi-view DR grading and may not be easily applicable to other tasks or datasets.
3. The paper does not provide a detailed analysis of the computational complexity of the proposed method compared to existing approaches.

### Suggestions

The paper introduces a novel end-to-end framework for multi-view diabetic retinopathy grading, which is a valuable contribution. However, the complexity of the proposed method raises concerns about its practical applicability, especially in resource-constrained environments. The authors should provide a more thorough analysis of the computational cost, including FLOPs, memory usage, and inference time, and compare these metrics with existing state-of-the-art methods. This analysis should be performed on the same hardware and software configurations to ensure a fair comparison. Furthermore, the authors should explore potential optimizations to reduce the computational burden, such as model pruning or quantization techniques, without significantly sacrificing performance. This would make the method more accessible for real-world deployment.

While the paper demonstrates strong performance on multi-view DR grading, the generalizability of the proposed method to other tasks or datasets remains unclear. The authors should investigate the performance of their method on other medical imaging datasets, such as those for age-related macular degeneration or glaucoma, to assess its robustness and adaptability. This would involve adapting the input data and potentially modifying the network architecture to accommodate different image characteristics and grading criteria. Additionally, the authors should discuss the limitations of their method and identify potential challenges in applying it to other tasks. This discussion should include an analysis of the specific features of the proposed method that may not be suitable for other medical imaging tasks. Addressing these concerns would significantly enhance the impact and practical value of the proposed method.

Finally, the paper lacks a detailed analysis of the impact of different hyperparameters on the performance of the proposed method. The authors should conduct a sensitivity analysis to determine the optimal values for key hyperparameters, such as the number of experts in the LGRF module and the Top-K value in the cross-view attention mechanism. This analysis should include a discussion of the trade-offs between performance and computational cost associated with different hyperparameter settings. Furthermore, the authors should provide guidelines for selecting appropriate hyperparameter values for different datasets and tasks. This would enable other researchers to reproduce the results and apply the proposed method to their own problems more effectively.

### Questions

1. Could the authors provide a comparison of the computational complexity of the proposed method with other state-of-the-art approaches?
2. Have the authors considered evaluating the proposed method on other retinal diseases or datasets to assess its generalizability?

### Rating

6

### Confidence

3

**********