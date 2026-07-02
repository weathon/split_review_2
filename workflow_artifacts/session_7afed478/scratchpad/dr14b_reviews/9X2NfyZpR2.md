### Summary

This paper introduces a weakly supervised approach for Long-Term Anticipation (LTA) in videos, which relies solely on video transcripts during training, rather than dense frame-level annotations. The proposed model, TBLTA, uses a temporal alignment module to generate pseudo-labels for supervision and leverages transcripts for cross-modal attention, enriching video features and providing global supervision. Experiments on the Breakfast, 50Salads, and EGTEA Gaze+ benchmarks demonstrate that transcript-based supervision is a robust, cost-effective alternative for LTA.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper is well-written and easy to follow.
2. The proposed method is novel and interesting, as it is the first to address Long-Term Anticipation (LTA) under weak supervision.
3. The experiments are comprehensive, and the results demonstrate the effectiveness of the proposed method.

### Weaknesses

#### Some Related Works


#### comment

1. The proposed method is complex and includes many hyperparameters. Could you provide a sensitivity analysis of these hyperparameters?
2. The paper lacks a detailed analysis of the proposed method. For example, how does the method perform under different levels of transcript noise or with varying lengths of video sequences? How does the performance vary with different types of actions or in scenarios with overlapping actions? These analyses would provide a more comprehensive understanding of the method's strengths and limitations.
3. The paper lacks a comparison with other weakly supervised methods for LTA. It would be beneficial to compare the proposed method with other weakly supervised approaches for LTA, such as those using only video-level labels or those employing self-supervision techniques. This comparison would help to better understand the advantages and disadvantages of the proposed method in the context of existing weakly supervised approaches.

### Suggestions

The paper introduces a novel approach to long-term anticipation (LTA) using weak supervision from video transcripts, which is a promising direction. However, the complexity of the proposed model, TBLTA, raises concerns about its practical applicability and robustness. Specifically, the model's reliance on numerous hyperparameters necessitates a thorough sensitivity analysis. This analysis should not only explore the impact of individual hyperparameters but also investigate their interactions. For example, how does the learning rate affect the optimal values for the temporal alignment module's parameters? Furthermore, the paper should provide guidance on how to select appropriate hyperparameter values for new datasets or tasks. Without this analysis, it is difficult to assess the generalizability of the proposed method and its ease of use for other researchers.

In addition to hyperparameter sensitivity, the paper needs a more detailed analysis of the method's performance under various conditions. The current evaluation lacks a systematic exploration of how the method behaves with different levels of transcript noise. For instance, how does the performance degrade when the transcripts contain errors or omissions? Similarly, the paper should investigate the method's performance on videos of varying lengths. Does the method perform equally well on short and long videos, or does it struggle with longer sequences due to the accumulation of errors? Furthermore, it is important to analyze the method's performance on different types of actions. Does it perform better on actions that are easily distinguishable or does it struggle with actions that are similar or overlapping? A detailed analysis of these factors is crucial for understanding the method's limitations and potential areas for improvement.

Finally, the paper should include a more comprehensive comparison with other weakly supervised methods for LTA. While the paper mentions that it is the first to address LTA under weak supervision, it does not provide a detailed comparison with other weakly supervised approaches for action anticipation. For example, how does the proposed method compare to methods that use only video-level labels or those that employ self-supervision techniques? This comparison is essential for understanding the advantages and disadvantages of the proposed method in the context of existing weakly supervised approaches. Furthermore, the paper should discuss the potential limitations of the proposed method and suggest directions for future research. This would help to place the proposed method in the broader context of weakly supervised learning for action anticipation.

### Questions

Please refer to the weaknesses.

### Rating

6

### Confidence

4

**********