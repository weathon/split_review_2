### Summary

This paper explores the theoretical limits of image watermarking capacity and compares them to current practical implementations. The authors derive theoretical bounds on the number of bits that can be embedded in an image while maintaining imperceptibility and robustness to various distortions. Their analysis shows that current watermarking methods operate far below these theoretical limits, suggesting significant room for improvement. The paper also introduces a new watermarking model, Chunky Seal, which increases capacity while preserving image quality and robustness, further demonstrating that current methods are not yet optimized for maximum capacity.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper provides a comprehensive theoretical analysis of watermarking capacity, considering factors like PSNR and robustness to transformations.
2. The empirical results clearly demonstrate the gap between theoretical and practical capacities, highlighting the potential for future advancements.
3. The introduction of Chunky Seal, a model that pushes the boundaries of current watermarking capacity, is a valuable contribution.
4. The paper is well-structured and clearly explains complex concepts, making it accessible to a broad audience.

### Weaknesses

#### Some Related Works


#### comment

1. The theoretical bounds are derived under simplified assumptions, which may not fully capture the complexities of real-world image distributions and distortions. Specifically, the assumption of i.i.d. pixel values and the use of simple linear transformations as distortion models do not accurately reflect the statistical properties of natural images or the complex, non-linear distortions often encountered in practice. This simplification limits the applicability of the theoretical results to real-world scenarios.
2. The analysis primarily focuses on PSNR as a measure of imperceptibility, which may not fully align with human visual perception. PSNR is a simple pixel-wise error metric and does not capture the structural and textural changes that are more perceptually relevant. Metrics like SSIM or LPIPS, which are designed to better align with human perception, should be considered to provide a more accurate assessment of imperceptibility.
3. The Chunky Seal model is shown to improve capacity, but its performance is not compared against a wider range of state-of-the-art watermarking methods. The paper lacks a comprehensive comparison with other recent methods, particularly those that focus on robustness to various distortions. This makes it difficult to assess the true novelty and effectiveness of Chunky Seal in the context of the current state of the art.

### Suggestions

To strengthen the theoretical analysis, the authors should consider incorporating more realistic models for image distributions and distortions. Instead of assuming i.i.d. pixel values, they could explore using models based on natural image statistics, such as Markov Random Fields or deep generative models. For distortion models, they should consider non-linear transformations and complex processing pipelines that are more representative of real-world scenarios. This would involve developing new analytical tools or adapting existing ones to handle these more complex models. Furthermore, the authors should investigate the impact of these more realistic models on the derived capacity bounds, which would provide a more accurate assessment of the theoretical limits of watermarking.

To address the limitations of using PSNR as the sole measure of imperceptibility, the authors should incorporate perceptual metrics such as SSIM or LPIPS into their analysis. This would involve re-evaluating the theoretical bounds and the performance of Chunky Seal using these metrics. Additionally, the authors could explore the use of perceptual loss functions during the training of Chunky Seal to ensure that the embedded watermarks are truly imperceptible to human observers. This would require a more nuanced approach to the trade-off between capacity, imperceptibility, and robustness, and would provide a more comprehensive evaluation of the proposed method.

Finally, the authors should conduct a more thorough comparison of Chunky Seal with a wider range of state-of-the-art watermarking methods. This comparison should include methods that focus on robustness to various distortions, such as geometric transformations, compression, and noise. The evaluation should also consider different types of watermarks, such as fragile and robust watermarks, and should use a variety of metrics to assess performance. This would provide a more comprehensive understanding of the strengths and weaknesses of Chunky Seal and would help to identify areas for further improvement. The comparison should also include a discussion of the computational complexity and practical applicability of each method.

### Questions

1. How do the theoretical bounds change when considering more realistic image distributions and distortion models?
2. Can the authors provide a more detailed analysis of the trade-offs between capacity, imperceptibility (using perceptual metrics), and robustness?
3. What are the limitations of the Chunky Seal model, and how can these be addressed in future work?

### Rating

6

### Confidence

4

**********