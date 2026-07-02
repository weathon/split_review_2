### Summary

This paper proposes a new framework called AutoRegressive Transformer for LF-STVG (ART-STVG) to tackle the challenge of Long-Form Spatio-Temporal Video Grounding (LF-STVG). The ART-STSVG framework processes video frames sequentially, unlike existing methods that process all frames simultaneously, making it more suitable for handling long-duration videos. The framework incorporates spatial and temporal memory banks to capture contextual information and employs selective memory strategies to improve performance. Experimental results on extended datasets demonstrate that ART-STVG outperforms existing methods in LF-STVG tasks.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper is well-written and easy to follow.
2. The proposed ART-STVG framework addresses the challenge of LF-STVG by treating videos as streaming inputs and processing frames sequentially, which is a novel approach compared to existing methods that process all frames simultaneously.
3. The introduction of spatial and temporal memory banks, along with selective memory strategies, enhances the model's ability to capture relevant contextual information, improving performance in LF-STVG tasks.
4. The cascaded spatio-temporal decoder design effectively utilizes fine-grained target information from spatial grounding to assist temporal localization in complex long videos, further boosting performance.
5. Extensive experiments on both long-term and short-term benchmarks demonstrate the effectiveness of the proposed ART-STVG framework.

### Weaknesses

#### Some Related Works


#### comment

1. The proposed ART-STVG framework seems computationally expensive, especially when dealing with very long videos. How does the computational complexity of ART-STVG compare to existing methods?
2. While the paper mentions that the source code and models will be released, it would be beneficial to provide more details about the implementation, such as the specific hardware and software requirements, as well as the training procedures.
3. The paper primarily focuses on quantitative results. Including qualitative examples of the grounding results, especially for long videos, would help readers better understand the strengths and limitations of the proposed method.
4. The paper lacks a discussion on the failure cases of the proposed method. Understanding when and why the method fails is crucial for identifying areas for improvement and for gaining deeper insights into the challenges of LF-STVG.

### Suggestions

The paper should provide a more detailed analysis of the computational complexity of the ART-STVG framework, particularly in relation to the sequential processing of frames. While the authors mention that the model avoids processing all frames simultaneously, a rigorous comparison of the computational cost, perhaps in terms of FLOPs or wall-clock time, against existing methods would be beneficial. This analysis should also consider the impact of video length on computational resources, such as memory usage and processing time. Furthermore, it would be helpful to discuss the scalability of the approach to extremely long videos, potentially by analyzing the trade-offs between performance and computational cost as video duration increases. This would give a clearer picture of the practical applicability of the proposed method in resource-constrained environments.

To enhance the reproducibility of the work, the authors should provide a more detailed account of the implementation specifics. This should include a breakdown of the hardware requirements, such as the specific GPUs used, the amount of RAM needed, and the operating system. Additionally, the software environment should be specified, including the versions of libraries and frameworks used, such as PyTorch, CUDA, and any other relevant packages. The training procedure should be described in detail, including the optimization algorithm, learning rate schedule, batch size, and any data augmentation techniques employed. Providing these details will enable other researchers to replicate the results and build upon the proposed method. Furthermore, the authors should consider releasing the code and pre-trained models alongside the paper publication to facilitate immediate adoption and further research.

Finally, the paper would greatly benefit from a more comprehensive qualitative analysis of the grounding results. While quantitative metrics provide an overall assessment of performance, they do not offer insights into the specific types of errors made by the model. Including visualizations of the grounding results, especially for challenging long videos, would help readers understand the strengths and limitations of the proposed method. These visualizations should include examples of both successful and failed grounding attempts, highlighting the scenarios where the model performs well and where it struggles. A discussion of the failure cases, including the reasons for these failures, would be invaluable for identifying areas for improvement and for gaining a deeper understanding of the challenges associated with long-form spatio-temporal video grounding. This could involve analyzing the types of queries that are difficult to ground, the impact of occlusions or fast-moving objects, and the limitations of the memory mechanism in capturing long-range dependencies.

### Questions

Please refer to the weakness.

### Rating

6

### Confidence

4

**********