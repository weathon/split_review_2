### Summary

This paper proposes a shape-adaptive guidance signal for interactive cortical sulcal labeling using spherical convolutional neural networks. The proposed method preserves structural information without sacrificing anatomical details. The experimental results show that the proposed method outperforms fully automatic methods and equidistance schemes in terms of both efficiency and accuracy.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The proposed method is novel and addresses an important problem in neuroimaging data analysis.
2. The experimental results show that the proposed method outperforms existing methods in terms of both efficiency and accuracy.
3. The paper is well-written and easy to understand.

### Weaknesses

#### Some Related Works


#### comment

1. The proposed method is only evaluated on a single dataset, which may limit its generalizability to other datasets or populations.
2. The proposed method requires a large number of user clicks to achieve good performance, which may limit its practicality in real-world applications.
3. The proposed method may be sensitive to the choice of hyperparameters, which may require careful tuning to achieve optimal performance.

### Suggestions

The authors should consider expanding their evaluation to include multiple datasets with varying characteristics, such as different scanner types, resolutions, and subject populations. This would provide a more robust assessment of the method's generalizability. Specifically, the inclusion of datasets with known pathologies or developmental variations could reveal potential limitations of the proposed approach. Furthermore, a quantitative analysis of the performance across these datasets, including metrics such as Dice score and Hausdorff distance, would be beneficial. This would allow for a more comprehensive understanding of the method's strengths and weaknesses in different contexts. The authors should also consider comparing their method against other state-of-the-art interactive segmentation techniques, not just fully automatic methods, to better contextualize their performance gains.

To address the concern about the number of user clicks, the authors should investigate methods to reduce the required interactions. This could involve exploring more efficient guidance signal encoding strategies or incorporating user feedback mechanisms that allow for more targeted corrections. For example, the authors could explore the use of adaptive click placement, where the system suggests optimal click locations based on the current segmentation state. Additionally, the authors should provide a more detailed analysis of the relationship between the number of clicks and the resulting segmentation accuracy. This would help to determine the practical trade-off between user effort and segmentation quality. The authors should also consider the potential for automating some of the click-based refinement process, perhaps by incorporating a confidence map that highlights areas where user input is most needed.

Finally, the authors should provide a more thorough analysis of the hyperparameter sensitivity of their method. This should include a systematic exploration of the parameter space and a discussion of the optimal parameter settings for different datasets or populations. The authors should also consider using automated hyperparameter optimization techniques to reduce the need for manual tuning. Furthermore, the authors should investigate the robustness of their method to variations in the input data, such as noise or artifacts. This would help to determine the practical limitations of the proposed approach and identify potential areas for improvement. The authors should also consider providing a sensitivity analysis of the method's performance with respect to different hyperparameter settings, which would help users to understand the impact of parameter choices on the final segmentation results.

### Questions

1. How does the proposed method perform on other datasets or populations?
2. How does the proposed method compare to other interactive segmentation methods in terms of efficiency and accuracy?
3. How sensitive is the proposed method to the choice of hyperparameters?

### Rating

6

### Confidence

3

**********